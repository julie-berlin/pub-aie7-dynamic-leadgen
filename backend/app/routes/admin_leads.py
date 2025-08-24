"""
Admin Leads API - Lead Management and Analytics

This module provides API endpoints for:
1. Lead listing and filtering
2. Lead detail views and management
3. Lead conversion tracking
4. Lead analytics and summary statistics
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional, Literal
import logging
from datetime import datetime

from app.database import db
from app.utils.response_helpers import success_response, error_response
from app.routes.admin_auth import AdminUserResponse, get_current_admin_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin/leads", tags=["admin-leads"])

# === PYDANTIC MODELS ===

class LeadSummary(BaseModel):
    """Summary model for lead listing."""
    session_id: str
    form_id: str
    form_title: str
    status: str
    score: Optional[int] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    utm_source: Optional[str] = None
    utm_campaign: Optional[str] = None

class LeadDetail(BaseModel):
    """Detailed model for individual lead."""
    session_id: str
    form_id: str
    form_title: str
    status: str
    score: Optional[int] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    responses: List[dict] = []
    tracking_data: dict = {}

class LeadStats(BaseModel):
    """Lead statistics summary."""
    total_leads: int
    completed_leads: int
    qualified_leads: int
    conversion_rate: float
    average_score: float
    leads_today: int
    leads_this_week: int
    leads_this_month: int

class ConversionUpdate(BaseModel):
    """Model for updating lead conversion status."""
    converted: bool
    conversion_value: Optional[float] = None
    notes: Optional[str] = None

# === LEADS MANAGEMENT ENDPOINTS ===

@router.get("/")
async def get_leads(
    form_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    converted: Optional[str] = Query(None),
    utm_source: Optional[str] = Query(None),
    limit: int = Query(50, le=1000),
    offset: int = Query(0, ge=0),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get leads with filtering and pagination."""
    try:
        # Base query for lead sessions with all needed fields
        query = db.client.table('lead_sessions').select(
            'id, session_id, form_id, lead_status, final_score, started_at, completed_at'
        ).eq('client_id', current_user.client_id)
        
        # Apply filters
        if form_id:
            query = query.eq('form_id', form_id)
        if status:
            query = query.eq('lead_status', status)
            
        # Execute query with pagination
        lead_sessions = query.order('started_at', desc=True).range(offset, offset + limit - 1).execute()
        
        if not lead_sessions.data:
            return success_response({"leads": []}, "No leads found")
        
        session_ids = [session['session_id'] for session in lead_sessions.data]
        
        # Get form titles for each unique form_id
        form_ids = list(set(session['form_id'] for session in lead_sessions.data))
        forms_result = db.client.table('forms').select('id, title').in_('id', form_ids).execute()
        form_titles = {form['id']: form['title'] for form in forms_result.data}
        
        # Get tracking data
        tracking_result = db.client.table('tracking_data').select(
            'session_id, utm_source, utm_campaign, utm_medium'
        ).in_('session_id', session_ids).execute()
        tracking_data = {track['session_id']: track for track in tracking_result.data}
        
        # Get conversion data from lead_outcomes
        outcomes_result = db.client.table('lead_outcomes').select(
            'session_id, converted, conversion_value, conversion_date, conversion_type'
        ).in_('session_id', session_ids).execute()
        outcomes_data = {outcome['session_id']: outcome for outcome in outcomes_result.data}
        
        # Get contact information from responses
        contact_data = {}
        # Look for name, email, phone in responses
        responses_result = db.client.table('responses').select(
            'session_id, question_id, answer, form_questions!inner(question_text)'
        ).in_('session_id', session_ids).execute()
        
        for response in responses_result.data:
            session_id = response['session_id']
            if session_id not in contact_data:
                contact_data[session_id] = {}
            
            question_text = response['form_questions']['question_text'].lower()
            answer = response['answer']
            
            if 'name' in question_text and not contact_data[session_id].get('name'):
                contact_data[session_id]['name'] = answer
            elif 'email' in question_text and not contact_data[session_id].get('email'):
                contact_data[session_id]['email'] = answer
            elif 'phone' in question_text and not contact_data[session_id].get('phone'):
                contact_data[session_id]['phone'] = answer
        
        # Build response and apply filters
        leads = []
        for session in lead_sessions.data:
            session_tracking = tracking_data.get(session['session_id'], {})
            session_outcome = outcomes_data.get(session['session_id'], {})
            session_contact = contact_data.get(session['session_id'], {})
            
            # Apply utm_source filter if specified
            if utm_source and session_tracking.get('utm_source') != utm_source:
                continue
            
            # Apply converted filter if specified
            if converted:
                is_converted = session_outcome.get('converted', False)
                if converted == 'true' and not is_converted:
                    continue
                elif converted == 'false' and is_converted:
                    continue
            
            lead_data = {
                "lead_id": session['id'],  # Proper lead UUID from database
                "form_id": session['form_id'],  # Add form_id for filtering
                "form_title": form_titles.get(session['form_id'], 'Unknown Form'),
                "lead_status": session['lead_status'],
                "final_score": session.get('final_score'),
                "started_at": session['started_at'],
                "completed_at": session.get('completed_at'),
                "utm_source": session_tracking.get('utm_source'),
                "utm_campaign": session_tracking.get('utm_campaign'),
                "utm_medium": session_tracking.get('utm_medium'),
                "contact_name": session_contact.get('name'),
                "contact_email": session_contact.get('email'),
                "contact_phone": session_contact.get('phone'),
                "actual_conversion": session_outcome.get('converted'),
                "conversion_date": session_outcome.get('conversion_date'),
                "conversion_value": session_outcome.get('conversion_value'),
                "conversion_type": session_outcome.get('conversion_type')
            }
            leads.append(lead_data)
        
        return success_response({"leads": leads}, f"Retrieved {len(leads)} leads")
        
    except Exception as e:
        logger.error(f"Failed to get leads: {e}")
        return error_response("Failed to retrieve leads", 500)

@router.get("/{session_id}", response_model=LeadDetail)
async def get_lead_detail(
    session_id: str,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get detailed information for a specific lead."""
    try:
        # Get lead session
        session_result = db.client.table('lead_sessions').select('*').eq(
            'session_id', session_id
        ).eq('client_id', current_user.client_id).execute()
        
        if not session_result.data:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        session = session_result.data[0]
        
        # Get form title
        form_result = db.client.table('forms').select('title').eq('id', session['form_id']).execute()
        form_title = form_result.data[0]['title'] if form_result.data else 'Unknown Form'
        
        # Get responses
        responses_result = db.client.table('responses').select(
            '*, form_questions!inner(question_text, input_type)'
        ).eq('session_id', session_id).order('created_at').execute()
        
        responses = []
        for response in responses_result.data:
            responses.append({
                'question_id': response['question_id'],
                'question_text': response['form_questions']['question_text'],
                'input_type': response['form_questions']['input_type'],
                'answer': response['answer'],
                'created_at': response['created_at']
            })
        
        # Get tracking data
        tracking_result = db.client.table('tracking_data').select('*').eq('session_id', session_id).execute()
        tracking_data = tracking_result.data[0] if tracking_result.data else {}
        
        return LeadDetail(
            session_id=session['session_id'],
            form_id=session['form_id'],
            form_title=form_title,
            status=session['status'],
            score=session.get('score'),
            started_at=datetime.fromisoformat(session['started_at'].replace('Z', '+00:00')),
            completed_at=datetime.fromisoformat(session['completed_at'].replace('Z', '+00:00')) if session.get('completed_at') else None,
            responses=responses,
            tracking_data=tracking_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get lead detail: {e}")
        return error_response("Failed to retrieve lead details", 500)

@router.put("/{session_id}/conversion")
async def update_lead_conversion(
    session_id: str,
    conversion_data: ConversionUpdate,
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Update lead conversion status."""
    try:
        # Verify lead exists and belongs to user's client
        session_result = db.client.table('lead_sessions').select('session_id, client_id').eq(
            'session_id', session_id
        ).eq('client_id', current_user.client_id).execute()
        
        if not session_result.data:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Update or insert lead outcome
        outcome_data = {
            'session_id': session_id,
            'converted': conversion_data.converted,
            'conversion_value': conversion_data.conversion_value,
            'notes': conversion_data.notes,
            'updated_at': datetime.utcnow().isoformat(),
            'updated_by_user_id': current_user.id
        }
        
        # Check if outcome already exists
        existing_outcome = db.client.table('lead_outcomes').select('session_id').eq('session_id', session_id).execute()
        
        if existing_outcome.data:
            # Update existing
            update_result = db.client.table('lead_outcomes').update(outcome_data).eq('session_id', session_id).execute()
        else:
            # Insert new
            outcome_data['created_at'] = datetime.utcnow().isoformat()
            update_result = db.client.table('lead_outcomes').insert(outcome_data).execute()
        
        if not update_result.data:
            raise HTTPException(status_code=500, detail="Failed to update conversion status")
        
        return success_response({
            "session_id": session_id,
            "converted": conversion_data.converted
        }, "Lead conversion status updated successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update lead conversion: {e}")
        return error_response("Failed to update lead conversion", 500)

@router.get("/stats/summary")
async def get_leads_summary(
    form_id: Optional[str] = Query(None),
    days: int = Query(30, ge=1, le=365),
    current_user: AdminUserResponse = Depends(get_current_admin_user)
):
    """Get lead statistics summary."""
    try:
        # Base query
        base_query = db.client.table('lead_sessions').select('*').eq('client_id', current_user.client_id)
        
        if form_id:
            base_query = base_query.eq('form_id', form_id)
        
        # Get recent leads based on days parameter
        from datetime import timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        recent_leads = base_query.gte('started_at', cutoff_date).execute()
        
        total_leads = len(recent_leads.data)
        completed_leads = len([l for l in recent_leads.data if l.get('completed_at')])
        
        # Calculate qualified leads (lead_status = 'yes' or final_score >= threshold)
        qualified_leads = len([
            l for l in recent_leads.data 
            if l.get('lead_status') == 'yes' or (l.get('final_score') and l['final_score'] >= 70)
        ])
        
        # Calculate conversion rate
        conversion_rate = (qualified_leads / total_leads * 100) if total_leads > 0 else 0
        
        # Calculate average score
        scored_leads = [l for l in recent_leads.data if l.get('final_score') is not None]
        average_score = sum(l['final_score'] for l in scored_leads) / len(scored_leads) if scored_leads else 0
        
        # Time-based counts
        now = datetime.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)
        
        leads_today = len([
            l for l in recent_leads.data 
            if datetime.fromisoformat(l['started_at'].replace('Z', '+00:00')).date() == today.date()
        ])
        
        leads_this_week = len([
            l for l in recent_leads.data 
            if datetime.fromisoformat(l['started_at'].replace('Z', '+00:00')) >= week_start.replace(tzinfo=datetime.now().astimezone().tzinfo)
        ])
        
        leads_this_month = len([
            l for l in recent_leads.data 
            if datetime.fromisoformat(l['started_at'].replace('Z', '+00:00')) >= month_start.replace(tzinfo=datetime.now().astimezone().tzinfo)
        ])
        
        # Status breakdown
        status_breakdown = {}
        for status in ['yes', 'maybe', 'no', 'unknown']:
            status_leads = [l for l in recent_leads.data if l.get('lead_status') == status]
            status_scores = [l.get('final_score', 0) for l in status_leads if l.get('final_score') is not None]
            status_breakdown[status] = {
                "count": len(status_leads),
                "avg_score": round(sum(status_scores) / len(status_scores), 2) if status_scores else 0
            }
        
        # UTM sources breakdown  
        utm_sources = []
        utm_data = {}
        for lead in recent_leads.data:
            # We'd need to join with tracking_data table for this, simplified for now
            pass
        
        stats_data = {
            "status_breakdown": status_breakdown,
            "conversion_stats": {
                "total_leads": total_leads,
                "tracked_conversions": 0,  # Placeholder - would need lead_outcomes data
                "conversions": qualified_leads,
                "conversion_rate": round(conversion_rate, 2),
                "total_value": 0,  # Placeholder - could calculate from lead outcomes
                "avg_value": 0     # Placeholder
            },
            "utm_sources": utm_sources,  # Placeholder - empty for now
            "period_days": days
        }
        
        return success_response(stats_data, f"Retrieved summary for {total_leads} leads over {days} days")
        
    except Exception as e:
        logger.error(f"Failed to get leads summary: {e}")
        return error_response("Failed to retrieve leads summary", 500)