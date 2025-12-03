# API Examples and Testing

## Python API Endpoints

All endpoints are available at `http://localhost:8000`

## 1. Streaming Agent API

### 1.1 Stream Answer (SSE)

**Endpoint:** `POST /api/agents/answer-stream`

**Request:**
```bash
curl -X POST http://localhost:8000/api/agents/answer-stream \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How would you design a URL shortening service like bit.ly?",
    "context": "Senior Software Engineer with 5 years experience",
    "conversation_history": []
  }'
```

**Response (Server-Sent Events):**
```
data: {"event_type":"start","timestamp":"2024-12-02T10:00:00.123Z","data":{"message":"Processing question...","question":"How would you design a URL shortening service like bit.ly?"}}

data: {"event_type":"routing","timestamp":"2024-12-02T10:00:00.456Z","data":{"selected_agent":"system_design","reasoning":"Question involves designing a large-scale distributed system with URL shortening functionality","confidence":0.95}}

data: {"event_type":"processing","timestamp":"2024-12-02T10:00:00.789Z","data":{"message":"Processing with system_design agent...","agent":"system_design"}}

data: {"event_type":"content","timestamp":"2024-12-02T10:00:01.012Z","data":{"chunk":"To design a URL shortening service like bit.ly","is_final":false}}

data: {"event_type":"content","timestamp":"2024-12-02T10:00:01.067Z","data":{"chunk":", we need to consider several key componen","is_final":false}}

data: {"event_type":"content","timestamp":"2024-12-02T10:00:01.122Z","data":{"chunk":"ts:\n\n1. **URL Generation**\n- Use base62 ","is_final":false}}

...more content chunks...

data: {"event_type":"answer_complete","timestamp":"2024-12-02T10:00:05.123Z","data":{"full_answer":"To design a URL shortening service like bit.ly, we need to consider...[full answer]","word_count":347,"character_count":2145,"metadata":{}}}

data: {"event_type":"follow_ups","timestamp":"2024-12-02T10:00:05.456Z","data":{"questions":["How would you handle collision in hash generation?","What database would you choose and why?","How would you scale the read operations?"]}}

data: {"event_type":"complete","timestamp":"2024-12-02T10:00:05.789Z","data":{"message":"Processing complete","agent_used":"system_design","success":true}}
```

### 1.2 Get Complete Answer (Non-Streaming)

**Endpoint:** `POST /api/agents/answer`

**Request:**
```bash
curl -X POST http://localhost:8000/api/agents/answer \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain the difference between REST and GraphQL"
  }'
```

**Response:**
```json
{
  "success": true,
  "timestamp": "2024-12-02T10:00:00.123Z",
  "question": "Explain the difference between REST and GraphQL",
  "routing": {
    "selected_agent": "technical",
    "reasoning": "Question about technical concepts and architectural patterns",
    "confidence": 0.92
  },
  "answer": "REST and GraphQL are two different approaches to API design:\n\n**REST (Representational State Transfer)**\n- Resource-based architecture\n- Multiple endpoints for different resources\n- Uses HTTP methods (GET, POST, PUT, DELETE)\n- Fixed data structure in responses\n- Can lead to over-fetching or under-fetching\n\n**GraphQL**\n- Query language for APIs\n- Single endpoint\n- Clients specify exactly what data they need\n- Strongly typed schema\n- Efficient data fetching\n\n**Key Differences:**\n1. Data Fetching: REST fetches fixed structures; GraphQL lets clients request specific fields\n2. Versioning: REST often needs versioning (v1, v2); GraphQL evolves without versions\n3. Learning Curve: REST is simpler; GraphQL has steeper learning curve\n4. Performance: GraphQL can be more efficient; REST may require multiple requests",
  "metadata": {},
  "follow_up_questions": [
    "When would you choose REST over GraphQL?",
    "What are the caching challenges with GraphQL?",
    "How does GraphQL handle authentication?"
  ],
  "statistics": {
    "word_count": 127,
    "character_count": 873
  }
}
```

### 1.3 List Available Agents

**Endpoint:** `GET /api/agents/available`

**Request:**
```bash
curl http://localhost:8000/api/agents/available
```

**Response:**
```json
{
  "total_agents": 6,
  "agents": [
    {
      "id": "product_manager",
      "name": "Product Manager",
      "specializations": [
        "Product Strategy",
        "Metrics & KPIs",
        "User Research",
        "Prioritization Frameworks"
      ],
      "best_for": [
        "Product strategy questions",
        "Metrics and measurement",
        "Feature prioritization",
        "User-centric thinking"
      ]
    },
    {
      "id": "technical",
      "name": "Technical",
      "specializations": [
        "Algorithms",
        "Data Structures",
        "System Concepts",
        "Performance Optimization"
      ],
      "best_for": [
        "Algorithm analysis",
        "Data structure selection",
        "Time complexity",
        "Technical concepts"
      ]
    },
    {
      "id": "system_design",
      "name": "System Design",
      "specializations": [
        "Distributed Systems",
        "Scalability",
        "System Architecture",
        "Trade-offs Analysis"
      ],
      "best_for": [
        "Large-scale system design",
        "Distributed systems",
        "Scalability problems",
        "Architecture decisions"
      ]
    }
    // ... more agents
  ]
}
```

## 2. Interview Tracking API

### 2.1 Companies

#### List Companies
```bash
curl "http://localhost:8000/api/companies?skip=0&limit=10"
```

#### Create Company
```bash
curl -X POST http://localhost:8000/api/companies \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Tech Corp",
    "industry": "Technology",
    "company_size": "1000-5000",
    "headquarters": "San Francisco, CA",
    "website": "https://techcorp.com"
  }'
```

**Response:**
```json
{
  "company_id": 1,
  "company_name": "Tech Corp",
  "industry": "Technology",
  "company_size": "1000-5000",
  "headquarters": "San Francisco, CA",
  "website": "https://techcorp.com",
  "company_description": null,
  "created_at": "2024-12-02T10:00:00.000Z",
  "updated_at": "2024-12-02T10:00:00.000Z"
}
```

### 2.2 Interviews

#### List Interviews
```bash
curl "http://localhost:8000/api/interviews?skip=0&limit=10&interview_status=scheduled"
```

#### Create Interview
```bash
curl -X POST http://localhost:8000/api/interviews \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": 1,
    "seniority_level": "senior",
    "interview_type": "actual",
    "interview_status": "scheduled",
    "custom_role_title": "Senior Software Engineer",
    "job_description": "Looking for senior engineer with 5+ years experience",
    "main_skills_required": ["Python", "JavaScript", "AWS"],
    "required_experience_years": 5,
    "job_location": "San Francisco, CA",
    "is_remote": true,
    "salary_range": "$150k - $200k",
    "application_date": "2024-12-01"
  }'
```

**Response:**
```json
{
  "interview_id": 1,
  "company_id": 1,
  "company_name": "Tech Corp",
  "role_id": null,
  "role_name": null,
  "custom_role_title": "Senior Software Engineer",
  "interview_type": "actual",
  "seniority_level": "senior",
  "interview_status": "scheduled",
  "interview_result": "pending",
  "job_description": "Looking for senior engineer with 5+ years experience",
  "main_skills_required": ["Python", "JavaScript", "AWS"],
  "required_experience_years": 5,
  "job_location": "San Francisco, CA",
  "is_remote": true,
  "salary_range": "$150k - $200k",
  "application_date": "2024-12-01",
  "created_at": "2024-12-02T10:00:00.000Z",
  "updated_at": "2024-12-02T10:00:00.000Z"
}
```

#### Update Interview
```bash
curl -X PUT http://localhost:8000/api/interviews/1 \
  -H "Content-Type: application/json" \
  -d '{
    "interview_status": "completed",
    "interview_result": "passed",
    "overall_feedback": "Strong technical skills, good communication"
  }'
```

### 2.3 Questions

#### List Questions
```bash
curl "http://localhost:8000/api/questions?category=system_design&difficulty=medium&skip=0&limit=10"
```

#### Create Question
```bash
curl -X POST http://localhost:8000/api/questions \
  -H "Content-Type: application/json" \
  -d '{
    "question_text": "How would you design a URL shortening service?",
    "question_category": "system_design",
    "question_difficulty": "medium",
    "question_context": "Common system design interview question",
    "key_concepts": ["Hashing", "Database Design", "Caching", "Load Balancing"],
    "common_mistakes": ["Not considering collision handling", "Ignoring scalability"],
    "tips_and_tricks": ["Use base62 encoding", "Consider Redis for caching"],
    "time_to_answer_minutes": 45,
    "tags": ["system_design", "scalability", "distributed_systems"]
  }'
```

**Response:**
```json
{
  "question_id": 1,
  "question_text": "How would you design a URL shortening service?",
  "question_category": "system_design",
  "question_difficulty": "medium",
  "question_context": "Common system design interview question",
  "key_concepts": ["Hashing", "Database Design", "Caching", "Load Balancing"],
  "common_mistakes": ["Not considering collision handling", "Ignoring scalability"],
  "tips_and_tricks": ["Use base62 encoding", "Consider Redis for caching"],
  "time_to_answer_minutes": 45,
  "tags": ["system_design", "scalability", "distributed_systems"],
  "times_asked": 0,
  "times_practiced": 0,
  "is_active": true,
  "created_at": "2024-12-02T10:00:00.000Z",
  "updated_at": "2024-12-02T10:00:00.000Z"
}
```

## 3. Angular Service Usage

### Using AgentStreamService in Component

```typescript
import { Component, OnInit } from '@angular/core';
import { AgentStreamService, StreamEvent } from './services/agent-stream.service';

@Component({
  selector: 'app-example',
  template: `
    <div>
      <textarea [(ngModel)]="question"></textarea>
      <button (click)="askQuestion()">Ask</button>
      <div *ngIf="isStreaming">Streaming: {{ currentAnswer }}</div>
      <div *ngIf="!isStreaming && answer">Answer: {{ answer }}</div>
    </div>
  `
})
export class ExampleComponent implements OnInit {
  question = '';
  currentAnswer = '';
  answer = '';
  isStreaming = false;

  constructor(private agentService: AgentStreamService) {}

  ngOnInit() {}

  askQuestion() {
    this.isStreaming = true;
    this.currentAnswer = '';
    this.answer = '';

    this.agentService.streamAnswer({
      question: this.question,
      context: 'Senior Developer'
    }).subscribe({
      next: (event: StreamEvent) => {
        console.log('Event:', event.event_type, event.data);

        switch (event.event_type) {
          case 'content':
            this.currentAnswer += event.data.chunk;
            break;

          case 'answer_complete':
            this.answer = event.data.full_answer;
            this.currentAnswer = '';
            break;

          case 'complete':
            this.isStreaming = false;
            break;

          case 'error':
            console.error('Error:', event.data);
            this.isStreaming = false;
            break;
        }
      },
      error: (error) => {
        console.error('Stream error:', error);
        this.isStreaming = false;
      }
    });
  }
}
```

## 4. Testing with Postman

### Import Collection

Create a Postman collection with these requests:

1. **Streaming Answer**
   - Method: POST
   - URL: `http://localhost:8000/api/agents/answer-stream`
   - Body (JSON):
   ```json
   {
     "question": "How would you design Instagram?",
     "context": "Senior Engineer"
   }
   ```
   - Note: Postman will show the SSE stream in the response

2. **Non-Streaming Answer**
   - Method: POST
   - URL: `http://localhost:8000/api/agents/answer`
   - Body (JSON):
   ```json
   {
     "question": "What is REST API?"
   }
   ```

3. **List Agents**
   - Method: GET
   - URL: `http://localhost:8000/api/agents/available`

## 5. Common Question Examples

### System Design Questions
```json
{
  "question": "How would you design Instagram?",
  "context": "Focus on scalability and real-time features"
}

{
  "question": "Design a distributed cache system",
  "context": "High availability and consistency"
}
```

### Technical Questions
```json
{
  "question": "Explain the difference between SQL and NoSQL databases",
  "context": "Include use cases"
}

{
  "question": "What is the CAP theorem?",
  "context": "With practical examples"
}
```

### Behavioral Questions
```json
{
  "question": "Tell me about a time you disagreed with your manager",
  "context": "Use STAR method"
}

{
  "question": "Describe a project you're most proud of",
  "context": "Senior engineering role"
}
```

### Coding Questions
```json
{
  "question": "Write a function to reverse a linked list",
  "context": "Include time and space complexity"
}

{
  "question": "Implement LRU cache",
  "context": "Optimize for O(1) operations"
}
```

## 6. API Documentation

Access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 7. Error Responses

### 400 Bad Request
```json
{
  "detail": "Question must be at least 5 characters long"
}
```

### 404 Not Found
```json
{
  "detail": "Interview not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing question: Connection timeout"
}
```

## 8. Rate Limiting (Future)

When rate limiting is implemented:

```
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

This comprehensive guide covers all major API endpoints and usage patterns for both the streaming AI system and interview tracking functionality.
