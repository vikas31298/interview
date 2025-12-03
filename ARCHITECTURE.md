# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                         │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Angular Application                          │  │
│  │                                                           │  │
│  │  ┌─────────────────┐    ┌──────────────────────────┐   │  │
│  │  │ Interview Room  │───▶│  AgentStreamService     │   │  │
│  │  │   Component     │    │                          │   │  │
│  │  │                 │    │  - streamAnswer()        │   │  │
│  │  │  - Chat UI      │    │  - getAnswer()           │   │  │
│  │  │  - Streaming    │    │  - HttpClient + SSE      │   │  │
│  │  │  - Messages     │    │                          │   │  │
│  │  └─────────────────┘    └──────────────────────────┘   │  │
│  │           │                        │                     │  │
│  └───────────┼────────────────────────┼─────────────────────┘  │
│              │                        │                         │
└──────────────┼────────────────────────┼─────────────────────────┘
               │                        │
               │  HTTP POST (SSE)       │
               │  /api/agents/answer-stream
               │                        │
               ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Streaming Router (agents/router.py)          │  │
│  │                                                           │  │
│  │  POST /api/agents/answer-stream  ──▶  SSE Streaming     │  │
│  │  POST /api/agents/answer          ──▶  JSON Response    │  │
│  │  GET  /api/agents/available       ──▶  List Agents      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           Multi-Agent System (LangGraph)                  │  │
│  │                                                           │  │
│  │  ┌────────────┐       ┌──────────────────────────────┐  │  │
│  │  │ Supervisor │──────▶│   Specialized Agents         │  │  │
│  │  │   Agent    │       │                              │  │  │
│  │  │            │       │  • Product Manager Agent     │  │  │
│  │  │  Routing   │       │  • Technical Agent           │  │  │
│  │  │  Decision  │       │  • Architect Agent           │  │  │
│  │  └────────────┘       │  • Coding Agent              │  │  │
│  │                       │  • Behavioral Agent          │  │  │
│  │                       │  • System Design Agent       │  │  │
│  │                       └──────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  OpenAI GPT-4o API                        │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │         Interview Tracking Database (PostgreSQL)          │  │
│  │                                                           │  │
│  │  • Companies  • Roles      • Skills                      │  │
│  │  • Interviews • Questions  • Rounds                      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Streaming Flow Diagram

```
User                Angular              FastAPI              AI Agent
 │                    │                     │                    │
 │  1. Ask Question   │                     │                    │
 ├───────────────────▶│                     │                    │
 │                    │  2. POST /answer-   │                    │
 │                    │     stream (SSE)    │                    │
 │                    ├────────────────────▶│                    │
 │                    │                     │  3. Route Question │
 │                    │                     ├───────────────────▶│
 │                    │                     │                    │
 │                    │  4. Event: routing  │  Supervisor        │
 │                    │◀────────────────────┤    analyzes        │
 │  Show routing      │                     │                    │
 │◀───────────────────┤                     │                    │
 │  card with agent   │                     │                    │
 │                    │                     │  5. Process        │
 │                    │                     │     Question       │
 │                    │                     ├───────────────────▶│
 │                    │  6. Event:          │                    │
 │                    │     processing      │  Agent generates   │
 │                    │◀────────────────────┤    answer          │
 │  Show spinner      │                     │                    │
 │◀───────────────────┤                     │                    │
 │                    │                     │                    │
 │                    │  7. Event: content  │                    │
 │                    │     (chunk 1)       │                    │
 │                    │◀────────────────────┤                    │
 │  Append text       │                     │                    │
 │◀───────────────────┤                     │                    │
 │                    │                     │                    │
 │                    │  8. Event: content  │                    │
 │                    │     (chunk 2)       │                    │
 │                    │◀────────────────────┤                    │
 │  Append text       │                     │                    │
 │◀───────────────────┤                     │                    │
 │                    │                     │                    │
 │                    │  ... more chunks    │                    │
 │                    │◀────────────────────┤                    │
 │                    │                     │                    │
 │                    │  9. Event:          │                    │
 │                    │     answer_complete │                    │
 │                    │◀────────────────────┤                    │
 │  Finalize answer   │                     │                    │
 │◀───────────────────┤                     │                    │
 │                    │                     │                    │
 │                    │ 10. Event:          │                    │
 │                    │     follow_ups      │                    │
 │                    │◀────────────────────┤                    │
 │  Show follow-up    │                     │                    │
 │  questions         │                     │                    │
 │◀───────────────────┤                     │                    │
 │                    │                     │                    │
 │                    │ 11. Event: complete │                    │
 │                    │◀────────────────────┤                    │
 │  Hide indicators   │                     │                    │
 │◀───────────────────┤                     │                    │
```

## Component Architecture

### Frontend Components

```
InterviewModule
│
├── InterviewRoomComponent
│   ├── Properties
│   │   ├── question: string
│   │   ├── context: string
│   │   ├── messages: Message[]
│   │   ├── currentAnswer: string
│   │   ├── isStreaming: boolean
│   │   ├── currentAgent: string
│   │   ├── routingReasoning: string
│   │   ├── confidence: number
│   │   ├── followUpQuestions: string[]
│   │   └── conversationHistory: any[]
│   │
│   ├── Methods
│   │   ├── sendQuestion()
│   │   ├── handleStreamEvent(event: StreamEvent)
│   │   ├── askFollowUp(question: string)
│   │   ├── clearConversation()
│   │   ├── addUserMessage(content: string)
│   │   ├── addAgentMessage(content: string, agentType: string)
│   │   ├── addSystemMessage(content: string)
│   │   ├── formatAgentName(agentType: string)
│   │   └── getAgentColor(agentType: string)
│   │
│   └── Dependencies
│       └── AgentStreamService
│
├── AgentStreamService
│   ├── Methods
│   │   ├── streamAnswer(request: QuestionRequest): Observable<StreamEvent>
│   │   ├── getAnswer(request: QuestionRequest): Observable<any>
│   │   └── getAvailableAgents(): Observable<any>
│   │
│   └── Dependencies
│       └── HttpClient
│
└── SanitizeHtmlPipe
    └── transform(value: string): SafeHtml
```

### Backend Components

```
FastAPI Application
│
├── Main Application (main.py)
│   ├── CORS Middleware
│   ├── Agent Registry
│   │   ├── product_manager
│   │   ├── technical
│   │   ├── architect
│   │   ├── coding
│   │   ├── behavioral
│   │   └── system_design
│   │
│   └── Routers
│       ├── agents_stream_router (agents/router.py)
│       ├── stats_router
│       ├── companies_router
│       ├── roles_router
│       ├── skills_router
│       ├── interviews_router
│       └── questions_router
│
├── Streaming Router (agents/router.py)
│   ├── POST /api/agents/answer-stream
│   │   └── generate_stream_events()
│   │       ├── Event: start
│   │       ├── Event: routing
│   │       ├── Event: processing
│   │       ├── Event: content (multiple)
│   │       ├── Event: answer_complete
│   │       ├── Event: follow_ups
│   │       └── Event: complete
│   │
│   ├── POST /api/agents/answer
│   └── GET /api/agents/available
│
└── Database Routes (database/routes.py)
    ├── Companies CRUD
    ├── Roles CRUD
    ├── Skills CRUD
    ├── Interviews CRUD
    └── Questions CRUD
```

## Data Flow

### Request Flow (Streaming)

```
1. User Input
   └─▶ InterviewRoomComponent.sendQuestion()
       └─▶ AgentStreamService.streamAnswer(request)
           └─▶ HttpClient.post('/api/agents/answer-stream', {
                 observe: 'events',
                 responseType: 'text',
                 reportProgress: true
               })

2. Backend Processing
   └─▶ FastAPI receives POST /api/agents/answer-stream
       └─▶ generate_stream_events(question, context, history)
           ├─▶ supervisor_agent.route_question()
           │   └─▶ Emit: routing event
           │
           ├─▶ selected_agent.process()
           │   └─▶ Emit: content events (chunks)
           │
           ├─▶ generate_follow_up_questions()
           │   └─▶ Emit: follow_ups event
           │
           └─▶ Emit: complete event

3. Frontend Handling
   └─▶ HttpClient captures DownloadProgress
       └─▶ Parse SSE from partialText
           └─▶ Emit StreamEvent to component
               └─▶ handleStreamEvent(event)
                   ├─▶ routing → Show agent card
                   ├─▶ content → Append to currentAnswer
                   ├─▶ answer_complete → Add to messages
                   └─▶ follow_ups → Display suggestions
```

### Event Types

```typescript
interface StreamEvent {
  event_type: 'start' | 'routing' | 'processing' | 'content' |
              'answer_complete' | 'follow_ups' | 'complete' | 'error';
  timestamp: string;
  data: {
    // Event-specific data
  };
}
```

### SSE Message Format

```
data: {"event_type":"routing","timestamp":"2024-12-02T10:00:00","data":{"selected_agent":"technical","reasoning":"Question about algorithms","confidence":0.95}}

data: {"event_type":"content","timestamp":"2024-12-02T10:00:01","data":{"chunk":"The time complexity of...","is_final":false}}

data: {"event_type":"complete","timestamp":"2024-12-02T10:00:05","data":{"message":"Processing complete","success":true}}

```

## Technology Stack

### Frontend
```
├── Angular 19
├── TypeScript 5.7
├── RxJS 7.8 (Reactive programming)
├── SCSS (Styling)
└── HttpClient (SSE communication)
```

### Backend
```
├── Python 3.8+
├── FastAPI (Web framework)
├── LangGraph (Agent orchestration)
├── LangChain (AI chains)
├── OpenAI GPT-4o (LLM)
├── PostgreSQL (Database)
├── SQLAlchemy (ORM)
├── Pydantic (Validation)
└── Uvicorn (ASGI server)
```

## Deployment Architecture (Production)

```
┌──────────────────────────────────────────────────────────────┐
│                      Load Balancer (Nginx)                   │
└──────────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌─────────────────┐            ┌─────────────────┐
│  Angular App    │            │  FastAPI Server │
│  (Static Files) │            │  (Multiple      │
│  CDN / S3       │            │   instances)    │
└─────────────────┘            └─────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │   PostgreSQL    │
                               │   (RDS/managed) │
                               └─────────────────┘
```

## Security Layers

```
1. Frontend
   ├── XSS Protection (DomSanitizer)
   ├── HTTPS enforcement
   └── Environment-based config

2. Backend
   ├── CORS configuration
   ├── Input validation (Pydantic)
   ├── Rate limiting (slowapi)
   ├── Authentication (JWT)
   └── API key protection (.env)

3. Database
   ├── Connection pooling
   ├── Parameterized queries (SQLAlchemy)
   └── Encrypted connections
```

This architecture provides a scalable, maintainable, and user-friendly interview preparation system with real-time AI-powered responses.
