import type { TrackingData } from '../types';

/**
 * Generate a unique session ID
 */
export function generateSessionId(): string {
  const timestamp = Date.now().toString(36);
  const randomStr = Math.random().toString(36).substring(2, 8);
  return `session_${timestamp}_${randomStr}`;
}

/**
 * Extract UTM parameters from URL
 */
export function extractUTMParams(): Partial<TrackingData> {
  const urlParams = new URLSearchParams(window.location.search);
  
  return {
    utmSource: urlParams.get('utm_source') || undefined,
    utmMedium: urlParams.get('utm_medium') || undefined,
    utmCampaign: urlParams.get('utm_campaign') || undefined,
    utmTerm: urlParams.get('utm_term') || undefined,
    utmContent: urlParams.get('utm_content') || undefined,
    referrer: document.referrer || undefined,
  };
}

/**
 * Get or create tracking data for session
 */
export function getTrackingData(sessionId?: string): TrackingData {
  const utmParams = extractUTMParams();
  
  return {
    sessionId: sessionId || generateSessionId(),
    ...utmParams,
    userAgent: navigator.userAgent,
    timestamp: new Date(),
  };
}

/**
 * Store session recovery data
 */
export function storeSessionRecovery(sessionId: string, formId: string, clientId: string, step: number): void {
  const recoveryData = {
    sessionId,
    formId,
    clientId,
    step,
    timestamp: new Date().toISOString(),
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString() // 7 days
  };
  
  localStorage.setItem(`recovery_${sessionId}`, JSON.stringify(recoveryData));
}

/**
 * Get session recovery data
 */
export function getSessionRecovery(sessionId: string): {
  sessionId: string;
  formId: string;
  clientId: string;
  step: number;
  timestamp: string;
  expiresAt: string;
} | null {
  try {
    const data = localStorage.getItem(`recovery_${sessionId}`);
    if (!data) return null;
    
    const recoveryData = JSON.parse(data);
    
    // Check if recovery data has expired
    if (new Date(recoveryData.expiresAt) < new Date()) {
      localStorage.removeItem(`recovery_${sessionId}`);
      return null;
    }
    
    return recoveryData;
  } catch (error) {
    console.error('Failed to parse session recovery data:', error);
    return null;
  }
}

/**
 * Clear session recovery data
 */
export function clearSessionRecovery(sessionId: string): void {
  localStorage.removeItem(`recovery_${sessionId}`);
}

/**
 * Clear expired session recovery data
 */
export function cleanupExpiredSessions(): void {
  const keys = Object.keys(localStorage);
  const recoveryKeys = keys.filter(key => key.startsWith('recovery_'));
  
  recoveryKeys.forEach(key => {
    try {
      const data = localStorage.getItem(key);
      if (data) {
        const recoveryData = JSON.parse(data);
        if (new Date(recoveryData.expiresAt) < new Date()) {
          localStorage.removeItem(key);
        }
      }
    } catch (error) {
      // Remove corrupted data
      localStorage.removeItem(key);
    }
  });
}

/**
 * Generate resume URL for incomplete form
 */
export function generateResumeURL(clientId: string, formId: string, sessionId: string): string {
  const baseUrl = window.location.origin;
  return `${baseUrl}/form/${clientId}/${formId}?session=${sessionId}&resume=true`;
}

/**
 * Parse form URL parameters
 */
export function parseFormURL(pathname: string, search: string): {
  clientId?: string;
  formId?: string;
  sessionId?: string;
  resume?: boolean;
} {
  // Expected format: /form/:clientId/:formId
  const pathParts = pathname.split('/').filter(Boolean);
  
  if (pathParts.length < 3 || pathParts[0] !== 'form') {
    return {};
  }
  
  const urlParams = new URLSearchParams(search);
  
  return {
    clientId: pathParts[1],
    formId: pathParts[2],
    sessionId: urlParams.get('session') || undefined,
    resume: urlParams.get('resume') === 'true'
  };
}

/**
 * Check if form session is recoverable
 */
export function isSessionRecoverable(sessionId: string): boolean {
  const recoveryData = getSessionRecovery(sessionId);
  return recoveryData !== null;
}