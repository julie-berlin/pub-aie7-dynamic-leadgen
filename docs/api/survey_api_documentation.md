# Survey API Documentation

## Overview

The Survey API provides endpoints for managing dynamic lead generation surveys with AI-powered question selection, real-time scoring, and abandonment tracking.

**Base URL**: `/api/survey`
**Authentication**: Not required (public-facing)
**Content-Type**: `application/json`

## API Endpoints

### 1. Start Survey Session

**Endpoint**: `POST /api/survey/start`

Initializes a new survey session with UTM tracking and returns the first set of questions.

#### Request Schema

```typescript
interface StartSessionRequest {
  form_id: string;                    // Required: Form configuration ID
  client_id?: string;                 // Optional: Client identifier
  
  // UTM Parameters (for marketing attribution)
  utm_source?: string;                // e.g., "facebook", "google"
  utm_medium?: string;                // e.g., "social", "cpc", "email"
  utm_campaign?: string;              // e.g., "summer_dog_walking_2025"
  utm_content?: string;               // Ad content identifier
  utm_term?: string;                  // Search term
  
  // Additional tracking
  landing_page?: string;              // Landing page URL
  metadata?: Record<string, any>;     // Additional metadata
}
```

#### Response Schema

```typescript
interface StartSessionResponse {
  session_id: string;                 // Unique session identifier
  questions: QuestionData[];          // Initial questions to display
  headline: string;                   // Engaging step headline
  motivation: string;                 // Motivational text
  step: number;                       // Current step (always 1)
  progress?: Record<string, any>;     // Progress indicators
}

interface QuestionData {
  id: number;                         // Question ID within form
  question: string;                   // Original question text
  phrased_question: string;           // AI-adapted question text
  data_type: string;                  // "text", "email", "multiple_choice", etc.
  is_required: boolean;               // Whether question is required
  options?: string[];                 // Multiple choice options (if applicable)
  scoring_rubric?: string;            // Scoring criteria (for reference)
}
```

#### Example Request

```json
{
  "form_id": "550e8400-e29b-41d4-a716-446655440000",
  "utm_source": "facebook",
  "utm_medium": "social",
  "utm_campaign": "summer_dog_walking_2025",
  "utm_content": "carousel_ad_golden_retriever",
  "landing_page": "https://pawsomedogwalking.com/get-started?ref=fb"
}
```

#### Example Response

```json
{
  "session_id": "session_20250809_143022_abc123",
  "questions": [
    {
      "id": 1,
      "question": "What is your name?",
      "phrased_question": "What should we call you?",
      "data_type": "text",
      "is_required": true,
      "scoring_rubric": "Contact information required"
    },
    {
      "id": 2,
      "question": "What is your dog's name?",
      "phrased_question": "What's your furry friend's name?",
      "data_type": "text",
      "is_required": false,
      "scoring_rubric": "+5 points for engagement"
    }
  ],
  "headline": "Welcome! Let's find the perfect dog walking service for you.",
  "motivation": "This will only take 2-3 minutes and help us personalize our service to your needs.",
  "step": 1,
  "progress": {
    "total_steps": 4,
    "completion_percentage": 0
  }
}
```

#### Error Responses

```json
// 400 Bad Request - Invalid form_id
{
  "error": "validation_error",
  "message": "form_id cannot be empty",
  "details": {
    "field": "form_id",
    "value": ""
  },
  "timestamp": "2025-08-09T14:30:22.123Z"
}

// 404 Not Found - Form not found
{
  "error": "form_not_found",
  "message": "Form configuration not found",
  "details": {
    "form_id": "invalid-form-id"
  },
  "timestamp": "2025-08-09T14:30:22.123Z"
}

// 500 Internal Server Error
{
  "error": "initialization_failed",
  "message": "Failed to initialize survey session",
  "timestamp": "2025-08-09T14:30:22.123Z"
}
```

---

### 2. Submit Responses and Continue

**Endpoint**: `POST /api/survey/step`

Submits user responses and returns the next step or completion message.

#### Request Schema

```typescript
interface SubmitResponsesRequest {
  session_id: string;                 // Required: Session identifier
  responses: ResponseSubmission[];    // User's answers
}

interface ResponseSubmission {
  question_id: number;                // Question being answered
  answer: string;                     // User's answer
  question_text?: string;             // Original question (for logging)
  response_time_seconds?: number;     // Time taken to answer
}
```

#### Response Schema

```typescript
interface StepResponse {
  session_id: string;                 // Session identifier
  step: number;                       // Current step number
  questions: QuestionData[];          // Next questions (empty if complete)
  headline: string;                   // Step headline
  motivation: string;                 // Motivational content
  progress: Record<string, any>;      // Progress information
  completed: boolean;                 // Whether survey is complete
  completion_message?: string;        // Final message (if completed)
}
```

#### Example Request

```json
{
  "session_id": "session_20250809_143022_abc123",
  "responses": [
    {
      "question_id": 1,
      "answer": "Emma Thompson",
      "question_text": "What should we call you?",
      "response_time_seconds": 8
    },
    {
      "question_id": 2,
      "answer": "Luna",
      "question_text": "What's your furry friend's name?"
    }
  ]
}
```

#### Example Response (Continuing)

```json
{
  "session_id": "session_20250809_143022_abc123",
  "step": 2,
  "questions": [
    {
      "id": 3,
      "question": "What breed is Luna?",
      "phrased_question": "What breed is your beautiful Luna?",
      "data_type": "text",
      "is_required": false,
      "scoring_rubric": "+10 points, helps with compatibility"
    },
    {
      "id": 4,
      "question": "How often would you need dog walking services?",
      "phrased_question": "How often does Luna need walks?",
      "data_type": "multiple_choice",
      "is_required": true,
      "options": ["Daily", "3-4 times per week", "1-2 times per week", "Occasionally"],
      "scoring_rubric": "+20 for daily, +15 for 3-4x week, +10 for 1-2x week, +5 for occasional"
    }
  ],
  "headline": "Great! Now let's learn about Luna's needs.",
  "motivation": "Understanding Luna's breed and walking needs helps us provide the best care.",
  "progress": {
    "total_steps": 4,
    "current_step": 2,
    "completion_percentage": 50
  },
  "completed": false
}
```

#### Example Response (Completed - Qualified Lead)

```json
{
  "session_id": "session_20250809_143022_abc123",
  "step": 4,
  "questions": [],
  "headline": "Perfect! We'd love to help Luna!",
  "motivation": "",
  "progress": {
    "total_steps": 4,
    "current_step": 4,
    "completion_percentage": 100
  },
  "completed": true,
  "completion_message": "Hi Emma!\n\nI'm thrilled to hear from you about Luna! A Golden Retriever who needs daily walks and loves other dogs - you're exactly the kind of client Pawsome Dog Walking was created for.\n\nYour budget of $60-80/week works perfectly for daily service, and Luna's friendly personality means she'd be great for our pack walks which dogs absolutely love.\n\nI'd love to meet you and Luna this week to get started. I'm Darlene, and I'm passionate about giving dogs the exercise they deserve.\n\nCan I call you tomorrow to set up our first meeting?\n\nBest,\nDarlene Demo\nPawsome Dog Walking\n(617) 555-0123"
}
```

#### Example Response (Completed - Unqualified Lead)

```json
{
  "session_id": "session_20250809_143022_abc123",
  "step": 3,
  "questions": [],
  "headline": "Thank you for your interest!",
  "motivation": "",
  "progress": {
    "total_steps": 4,
    "current_step": 3,
    "completion_percentage": 100
  },
  "completed": true,
  "completion_message": "Thank you for taking the time to learn about our services. We appreciate your interest."
}
```

---

### 3. Abandon Session

**Endpoint**: `POST /api/survey/abandon`

Marks a session as abandoned (user leaves without completing).

#### Request Schema

```typescript
interface AbandonSessionRequest {
  session_id: string;                 // Required: Session identifier
  reason?: string;                    // Optional: Abandonment reason
}
```

#### Response Schema

```typescript
interface AbandonResponse {
  status: string;                     // "success"
  message: string;                    // Confirmation message
}
```

#### Example Request

```json
{
  "session_id": "session_20250809_143022_abc123",
  "reason": "user_navigated_away"
}
```

#### Example Response

```json
{
  "status": "success",
  "message": "Session marked as abandoned"
}
```

---

### 4. Get Session Status

**Endpoint**: `GET /api/survey/status/{session_id}`

Retrieves current session status and state information.

#### Response Schema

```typescript
interface SessionStatusResponse {
  session_id: string;                 // Session identifier
  form_id: string;                    // Form configuration ID
  step: number;                       // Current step number
  completed: boolean;                 // Whether session is completed
  lead_status: "unknown" | "yes" | "maybe" | "no";  // Lead qualification
  current_score: number;              // Current lead score (0-100)
  responses_count: number;            // Number of responses collected
  started_at: string;                 // ISO timestamp
  last_updated: string;               // ISO timestamp
  abandonment_status: "active" | "at_risk" | "high_risk" | "abandoned";
}
```

#### Example Response

```json
{
  "session_id": "session_20250809_143022_abc123",
  "form_id": "550e8400-e29b-41d4-a716-446655440000",
  "step": 2,
  "completed": false,
  "lead_status": "maybe",
  "current_score": 45,
  "responses_count": 4,
  "started_at": "2025-08-09T14:30:22.123Z",
  "last_updated": "2025-08-09T14:32:15.456Z",
  "abandonment_status": "active"
}
```

---

## Error Handling

### Standard Error Response Format

```typescript
interface ErrorResponse {
  error: string;                      // Error type/code
  message: string;                    // Human-readable message
  details?: Record<string, any>;      // Additional error details
  timestamp: string;                  // ISO timestamp
}
```

### Common Error Types

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `validation_error` | 400 | Request validation failed |
| `session_not_found` | 404 | Session ID not found |
| `form_not_found` | 404 | Form configuration not found |
| `session_expired` | 410 | Session has expired |
| `session_completed` | 409 | Session already completed |
| `rate_limit_exceeded` | 429 | Too many requests |
| `database_error` | 500 | Database operation failed |
| `ai_service_error` | 503 | AI/LLM service unavailable |

## Frontend Integration Guidelines

### 1. Session Management

- **Store session_id** in browser storage (sessionStorage recommended)
- **Handle session recovery** by checking status endpoint on page refresh
- **Clear session data** after completion or abandonment

### 2. Progress Tracking

- **Use progress data** to show completion percentage
- **Display step indicators** based on total_steps
- **Show abandonment prevention** messages for at-risk users

### 3. Form Rendering

- **Render questions dynamically** based on data_type
- **Handle multiple choice options** when provided
- **Respect is_required flags** for validation
- **Use phrased_question** for display (more engaging than original)

### 4. Error Handling

- **Validate responses** client-side before submission
- **Handle network errors** gracefully with retry logic  
- **Show user-friendly messages** for validation errors
- **Implement fallbacks** for service unavailability

### 5. Analytics Integration

- **Track UTM parameters** from URL and pass to start endpoint
- **Monitor abandonment rates** per step
- **Measure completion times** for optimization
- **A/B test question phrasing** and engagement strategies

## Rate Limiting

- **Start session**: 10 requests per minute per IP
- **Submit responses**: 30 requests per minute per session
- **Status check**: 60 requests per minute per IP
- **Abandon session**: 5 requests per minute per IP

## CORS Configuration

```javascript
// Allowed origins (will be configured in Phase 9)
const allowedOrigins = [
  'http://localhost:3000',        // Local development
  'https://yourdomain.com',       // Production frontend
  'https://staging.yourdomain.com' // Staging environment
];
```

## TypeScript Types

Complete TypeScript type definitions will be auto-generated from the Pydantic models and provided as a separate package or file for frontend integration.

---

**Last Updated**: August 9, 2025
**API Version**: 1.0
**OpenAPI Spec**: Available at `/docs` endpoint when server is running