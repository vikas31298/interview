# Interview Tracking System - API Documentation

## Overview

This system provides comprehensive APIs for:
1. **Interview Tracking**: Manage interviews, companies, roles, skills, and questions
2. **AI-Powered Question Answering**: Streaming and non-streaming endpoints for interview question assistance
3. **Agent-Based Processing**: Specialized AI agents for different interview types

Base URL: `http://localhost:8000`

---

## Table of Contents

1. [Agents Streaming API](#agents-streaming-api)
2. [Interview Tracking API](#interview-tracking-api)
3. [Companies API](#companies-api)
4. [Roles API](#roles-api)
5. [Skills API](#skills-api)
6. [Questions API](#questions-api)
7. [Statistics API](#statistics-api)

---

## Agents Streaming API

### POST `/api/agents/answer-stream`
**Stream interview question answer in real-time using Server-Sent Events (SSE)**

#### Request Body:
```json
{
  "question": "How would you design a URL shortening service?",
  "context": "Senior engineer with 5 years experience",
  "conversation_history": []
}
```

#### Response: Server-Sent Events Stream

The endpoint returns a stream of events:

**Event Types:**
- `start`: Processing started
- `routing`: Agent selection information
- `processing`: Processing status
- `content`: Answer content chunks (streamed)
- `answer_complete`: Full answer with metadata
- `follow_ups`: Suggested follow-up questions
- `complete`: Processing complete
- `error`: Error information

**Example Events:**

```text
data: {"event_type":"start","timestamp":"2024-12-02T10:00:00","data":{"message":"Processing question...","question":"How would you design a URL shortening service?"}}

data: {"event_type":"routing","timestamp":"2024-12-02T10:00:01","data":{"selected_agent":"system_design","reasoning":"Question involves designing a large-scale system","confidence":0.95}}

data: {"event_type":"processing","timestamp":"2024-12-02T10:00:02","data":{"message":"Processing with system_design agent...","agent":"system_design"}}

data: {"event_type":"content","timestamp":"2024-12-02T10:00:03","data":{"chunk":"To design a URL shortening service, we need to consider...","is_final":false}}

data: {"event_type":"answer_complete","timestamp":"2024-12-02T10:00:10","data":{"full_answer":"Complete answer...","word_count":250,"character_count":1500}}

data: {"event_type":"follow_ups","timestamp":"2024-12-02T10:00:11","data":{"questions":["How would you handle collision?","What database would you choose?","How would you implement rate limiting?"]}}

data: {"event_type":"complete","timestamp":"2024-12-02T10:00:12","data":{"message":"Processing complete","agent_used":"system_design","success":true}}
```

#### Angular Consumption Example:

See `angular_example.ts` for complete implementation.

```typescript
this.interviewService.streamAnswer(request).subscribe({
  next: (event: StreamEvent) => {
    if (event.event_type === 'content') {
      this.answer += event.data.chunk;
    } else if (event.event_type === 'follow_ups') {
      this.followUpQuestions = event.data.questions;
    }
  }
});
```

---

### POST `/api/agents/answer`
**Get complete interview question answer (non-streaming)**

#### Request Body:
```json
{
  "question": "How would you design a URL shortening service?",
  "context": "Senior engineer with 5 years experience",
  "conversation_history": []
}
```

#### Response:
```json
{
  "success": true,
  "timestamp": "2024-12-02T10:00:00",
  "question": "How would you design a URL shortening service?",
  "routing": {
    "selected_agent": "system_design",
    "reasoning": "Question involves designing a large-scale system",
    "confidence": 0.95
  },
  "answer": "To design a URL shortening service...",
  "metadata": {},
  "follow_up_questions": [
    "How would you handle collision?",
    "What database would you choose?",
    "How would you implement rate limiting?"
  ],
  "statistics": {
    "word_count": 250,
    "character_count": 1500
  }
}
```

---

### GET `/api/agents/available`
**List all available AI agents with their capabilities**

#### Response:
```json
{
  "total_agents": 6,
  "agents": [
    {
      "id": "product_manager",
      "name": "Product Manager",
      "specializations": ["Product Strategy", "Prioritization", "Frameworks"],
      "best_for": ["Product design questions", "Feature prioritization"]
    },
    {
      "id": "system_design",
      "name": "System Design",
      "specializations": ["Distributed Systems", "Scalability", "Architecture"],
      "best_for": ["System design interviews", "Architecture questions"]
    }
  ]
}
```

---

## Interview Tracking API

### GET `/api/interviews`
**List all interviews with filtering and pagination**

#### Query Parameters:
- `skip` (default: 0): Number of records to skip
- `limit` (default: 20, max: 100): Number of records to return
- `company_id`: Filter by company ID
- `role_id`: Filter by role ID
- `interview_type`: Filter by type (actual, mock, practice)
- `interview_status`: Filter by status (scheduled, in_progress, completed, cancelled, rescheduled)
- `interview_result`: Filter by result (pending, passed, failed, offer_received, offer_accepted, offer_declined)
- `seniority_level`: Filter by seniority (intern, junior, mid, senior, staff, principal, lead, manager, director)
- `is_remote`: Filter by remote/onsite (true/false)
- `sort_by`: Sort field (created_at, application_date, first_interview_date, company_name, interview_status)
- `order`: Sort order (asc, desc)

#### Response:
```json
{
  "total": 50,
  "skip": 0,
  "limit": 20,
  "data": [
    {
      "interview_id": 1,
      "company_id": 1,
      "company_name": "TechCorp Inc",
      "role_id": 1,
      "role_name": "Senior Software Engineer",
      "interview_type": "actual",
      "seniority_level": "senior",
      "interview_status": "completed",
      "interview_result": "passed",
      "job_location": "San Francisco, CA",
      "is_remote": true,
      "salary_range": "$150,000 - $200,000",
      "application_date": "2024-12-01",
      "created_at": "2024-12-01T10:00:00",
      "updated_at": "2024-12-02T15:00:00"
    }
  ]
}
```

---

### POST `/api/interviews`
**Create a new interview**

#### Request Body:
```json
{
  "company_id": 1,
  "role_id": 1,
  "custom_role_title": "Senior Full Stack Engineer",
  "interview_type": "actual",
  "seniority_level": "senior",
  "interview_status": "scheduled",
  "interview_result": "pending",
  "job_description": "Looking for a senior engineer with 5+ years experience",
  "main_skills_required": ["Python", "React", "AWS", "PostgreSQL"],
  "required_experience_years": 5,
  "job_location": "San Francisco, CA",
  "is_remote": true,
  "salary_range": "$150,000 - $200,000",
  "application_date": "2024-12-01",
  "preparation_notes": "Review system design patterns and AWS architecture",
  "created_by": "user@example.com"
}
```

#### Response:
Returns the created interview object with all fields populated.

---

### GET `/api/interviews/{interview_id}`
**Get a specific interview by ID**

#### Response:
Returns complete interview details including company, role, rounds, and questions.

---

### PUT `/api/interviews/{interview_id}`
**Update an existing interview**

#### Request Body:
Partial update - only include fields you want to update:
```json
{
  "interview_status": "completed",
  "interview_result": "passed",
  "overall_feedback": "Great interview! Demonstrated strong technical skills.",
  "strengths": "Strong system design knowledge, good communication",
  "areas_for_improvement": "Could improve algorithm optimization"
}
```

---

### DELETE `/api/interviews/{interview_id}`
**Delete an interview (soft delete)**

Sets interview status to "cancelled". Returns 204 No Content.

---

### GET `/api/interviews/{interview_id}/rounds`
**Get all rounds for a specific interview**

#### Response:
```json
[
  {
    "round_id": 1,
    "interview_id": 1,
    "round_number": 1,
    "round_name": "Technical Phone Screen",
    "round_type": "phone_screen",
    "scheduled_date": "2024-12-05",
    "duration_minutes": 60,
    "is_virtual": true,
    "interviewer_name": "John Doe",
    "round_status": "completed",
    "round_result": "passed",
    "rating": 8
  }
]
```

---

### POST `/api/interviews/{interview_id}/rounds`
**Create a new round for an interview**

#### Request Body:
```json
{
  "interview_id": 1,
  "round_number": 1,
  "round_name": "Technical Phone Screen",
  "round_type": "phone_screen",
  "scheduled_date": "2024-12-05",
  "scheduled_time": "14:00:00",
  "duration_minutes": 60,
  "is_virtual": true,
  "meeting_platform": "Zoom",
  "interviewer_name": "John Doe",
  "interviewer_title": "Senior Engineering Manager"
}
```

---

### POST `/api/interviews/{interview_id}/questions`
**Link a question to an interview**

#### Request Body:
```json
{
  "interview_id": 1,
  "question_id": 10,
  "round_id": 1,
  "was_asked": true,
  "order_asked": 1,
  "candidate_answer": "I would start by clarifying requirements...",
  "answer_quality_rating": 8,
  "time_taken_minutes": 40,
  "was_prepared": true,
  "confidence_level": 7,
  "what_went_well": "Good structure and covered all key points",
  "what_could_improve": "Could have discussed more about analytics"
}
```

---

### GET `/api/interviews/{interview_id}/questions`
**Get all questions asked in a specific interview**

---

## Companies API

### GET `/api/companies`
**List all companies**

Query parameters: `skip`, `limit`, `search`

### POST `/api/companies`
**Create a new company**

```json
{
  "company_name": "TechCorp Inc",
  "industry": "Technology",
  "company_size": "1000-5000",
  "headquarters": "San Francisco, CA",
  "website": "https://techcorp.com",
  "company_description": "Leading technology company"
}
```

### GET `/api/companies/{company_id}`
**Get a specific company by ID**

---

## Roles API

### GET `/api/roles`
**List all roles**

Query parameters: `skip`, `limit`, `search`, `category`

### POST `/api/roles`
**Create a new role**

```json
{
  "role_name": "Senior Software Engineer",
  "role_category": "Engineering",
  "role_description": "Senior engineer position",
  "typical_skills": ["Python", "JavaScript", "AWS", "Docker"]
}
```

### GET `/api/roles/{role_id}`
**Get a specific role by ID**

---

## Skills API

### GET `/api/skills`
**List all skills**

Query parameters: `skip`, `limit`, `search`, `category`, `is_trending`

### POST `/api/skills`
**Create a new skill**

```json
{
  "skill_name": "Python",
  "skill_category": "Programming Language",
  "skill_type": "Technical",
  "skill_description": "High-level programming language",
  "is_trending": true,
  "market_demand": "high"
}
```

### GET `/api/skills/{skill_id}`
**Get a specific skill by ID**

---

## Questions API

### GET `/api/questions`
**List all questions with filtering and pagination**

#### Query Parameters:
- `skip`, `limit`: Pagination
- `category`: technical, behavioral, product, system_design, coding, case_study, etc.
- `difficulty`: easy, medium, hard, expert
- `search`: Search in question text
- `tags`: Filter by tags (can specify multiple)
- `is_active`: Show only active questions (default: true)
- `sort_by`: created_at, times_asked, times_practiced, average_rating, question_difficulty
- `order`: asc, desc

#### Response:
```json
{
  "total": 100,
  "skip": 0,
  "limit": 20,
  "data": [
    {
      "question_id": 1,
      "question_text": "How would you design a URL shortening service?",
      "question_category": "system_design",
      "question_difficulty": "medium",
      "answer_summary": "Design should include URL generation, storage, redirection",
      "key_concepts": ["Hashing", "Database Design", "Caching"],
      "common_mistakes": ["Not considering collision handling"],
      "tips_and_tricks": ["Use base62 encoding", "Consider Redis for caching"],
      "time_to_answer_minutes": 45,
      "tags": ["system_design", "scalability"],
      "times_asked": 5,
      "times_practiced": 12,
      "is_active": true
    }
  ]
}
```

---

### POST `/api/questions`
**Create a new question**

```json
{
  "question_text": "How would you design a URL shortening service?",
  "question_category": "system_design",
  "question_difficulty": "medium",
  "answer_summary": "Design should include URL generation, storage, redirection",
  "key_concepts": ["Hashing", "Database Design", "Caching"],
  "common_mistakes": ["Not considering collision handling"],
  "tips_and_tricks": ["Use base62 encoding"],
  "time_to_answer_minutes": 45,
  "tags": ["system_design", "scalability"],
  "created_by": "admin"
}
```

---

### GET `/api/questions/{question_id}`
**Get a specific question by ID**

---

### PUT `/api/questions/{question_id}`
**Update an existing question**

---

### DELETE `/api/questions/{question_id}`
**Delete a question (soft delete)**

---

### GET `/api/questions/category/{category}`
**Get all questions in a specific category**

---

## Statistics API

### GET `/api/stats/overview`
**Get overall statistics**

```json
{
  "total_interviews": 50,
  "total_questions": 200,
  "total_companies": 25,
  "interviews_by_status": {
    "scheduled": 10,
    "completed": 35,
    "cancelled": 5
  },
  "interviews_by_result": {
    "pending": 10,
    "passed": 30,
    "failed": 10
  },
  "questions_by_category": {
    "system_design": 50,
    "coding": 70,
    "behavioral": 40
  },
  "questions_by_difficulty": {
    "easy": 60,
    "medium": 90,
    "hard": 50
  }
}
```

---

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK`: Success
- `201 Created`: Resource created successfully
- `204 No Content`: Resource deleted successfully
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Interactive API Documentation

Visit `/docs` for interactive Swagger UI documentation where you can test all endpoints.

Visit `/redoc` for ReDoc documentation with detailed schemas.

---

## Running the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 8000
```

Server will be available at: `http://localhost:8000`

---

## CORS Configuration

The API has CORS enabled for all origins in development. Update CORS settings in `main.py` for production use.

---

## Database

The system uses PostgreSQL with the `interview_schema` schema. Connection string is configured in `.env`:

```
DATABASE_URL=postgresql://user:password@host:port/database
```

---

## Authentication

Currently, the API does not require authentication. Add authentication middleware as needed for production use.
