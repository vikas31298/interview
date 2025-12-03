# AI Interview System with Streaming Support

This project implements a **multi-agent AI interview system** with **real-time streaming responses** using Server-Sent Events (SSE). The Angular frontend displays answers as they are generated, providing a ChatGPT-like experience.

## Architecture Overview

### Backend (Python FastAPI)
- **Framework**: FastAPI with LangGraph for agent orchestration
- **AI Agents**: 6 specialized agents (Product Manager, Technical, Architect, Coding, Behavioral, System Design)
- **Streaming**: Server-Sent Events (SSE) for real-time response streaming
- **Database**: PostgreSQL for interview tracking

### Frontend (Angular)
- **Framework**: Angular 19
- **Streaming Client**: HttpClient with SSE event parsing
- **UI**: Real-time chat interface with streaming visualization

## Features

### ✨ Real-time Streaming
- **Server-Sent Events (SSE)** for continuous data flow
- **Chunk-by-chunk rendering** of AI responses
- **Visual indicators** for routing, processing, and completion
- **Live status updates** during answer generation

### 🤖 Multi-Agent System
- **Supervisor Agent**: Routes questions to the appropriate specialized agent
- **6 Specialized Agents**:
  - Product Manager: Product strategy, metrics, frameworks
  - Technical: Algorithms, data structures, technical concepts
  - Architect: System architecture, scalability
  - Coding: Code implementation, best practices
  - Behavioral: Leadership, soft skills, STAR method
  - System Design: Distributed systems, large-scale design

### 💬 Chat Interface
- **Conversation history** with context awareness
- **Follow-up questions** automatically suggested
- **Agent identification** with color-coded badges
- **Markdown-like formatting** support

## API Endpoints

### Streaming API

#### POST `/api/agents/answer-stream`
Stream interview question answer in real-time using SSE.

**Request:**
```json
{
  "question": "How would you design Instagram?",
  "context": "Senior engineer with 5 years experience",
  "conversation_history": []
}
```

**Response:** Server-Sent Events stream

**Event Types:**
- `start`: Processing started
- `routing`: Agent selection information
- `processing`: Processing status
- `content`: Answer content chunks (streamed)
- `answer_complete`: Full answer with metadata
- `follow_ups`: Suggested follow-up questions
- `complete`: Processing complete
- `error`: Error information

**Example SSE Event:**
```
data: {"event_type":"routing","timestamp":"2024-12-02T10:30:00","data":{"selected_agent":"system_design","reasoning":"Question involves designing a large-scale system","confidence":0.95}}

data: {"event_type":"content","timestamp":"2024-12-02T10:30:01","data":{"chunk":"To design Instagram, we need to consider...","is_final":false}}
```

#### POST `/api/agents/answer`
Get complete answer without streaming (fallback).

#### GET `/api/agents/available`
List all available agents with their capabilities.

### Interview Tracking API

#### Companies
- `GET /api/companies` - List all companies
- `POST /api/companies` - Create a company
- `GET /api/companies/{id}` - Get company details

#### Roles
- `GET /api/roles` - List all roles
- `POST /api/roles` - Create a role
- `GET /api/roles/{id}` - Get role details

#### Skills
- `GET /api/skills` - List all skills
- `POST /api/skills` - Create a skill
- `GET /api/skills/{id}` - Get skill details

#### Interviews
- `GET /api/interviews` - List interviews with filters
- `POST /api/interviews` - Create an interview
- `GET /api/interviews/{id}` - Get interview details
- `PUT /api/interviews/{id}` - Update interview
- `DELETE /api/interviews/{id}` - Delete interview
- `GET /api/interviews/{id}/rounds` - Get interview rounds
- `POST /api/interviews/{id}/rounds` - Create round
- `GET /api/interviews/{id}/questions` - Get questions
- `POST /api/interviews/{id}/questions` - Link question

#### Questions
- `GET /api/questions` - List questions with filters
- `POST /api/questions` - Create a question
- `GET /api/questions/{id}` - Get question details
- `PUT /api/questions/{id}` - Update question
- `DELETE /api/questions/{id}` - Delete question

## Setup Instructions

### Backend Setup (Python)

1. **Navigate to the API directory:**
   ```bash
   cd interviewapis
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/interview_db
   ```

5. **Run the server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Frontend Setup (Angular)

1. **Navigate to the web directory:**
   ```bash
   cd interviewweb
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   ng serve
   ```

4. **Access the application:**
   - URL: http://localhost:4200
   - Navigate to Interview Room: http://localhost:4200/interview/room

## How to Use

### Starting an Interview Session

1. **Open the Interview Room** at http://localhost:4200/interview/room

2. **Add Context (Optional)**:
   - Click "➕ Add Context" to provide your background
   - E.g., "Senior Software Engineer with 5 years experience"

3. **Ask a Question**:
   - Type your interview question
   - Press Enter or click "Send 📤"

4. **Watch the Streaming Response**:
   - See real-time agent routing information
   - Watch the answer appear word-by-word
   - View suggested follow-up questions

### Example Questions

**System Design:**
```
How would you design Instagram?
How would you design a URL shortening service?
```

**Technical:**
```
Explain the difference between REST and GraphQL
What is the CAP theorem?
```

**Behavioral:**
```
Tell me about a time you led a team
Describe a conflict you resolved
```

**Coding:**
```
Implement a function to reverse a linked list
Write code to find the longest substring without repeating characters
```

## Streaming Implementation Details

### Backend (Python)

The streaming is implemented using FastAPI's `StreamingResponse` with async generators:

```python
async def generate_stream_events(question: str, context: str, history: List[Dict]):
    # Event 1: Routing
    yield format_sse_event({
        "event_type": "routing",
        "data": {"selected_agent": agent, "reasoning": reason}
    })

    # Event 2: Content streaming
    for chunk in answer_chunks:
        yield format_sse_event({
            "event_type": "content",
            "data": {"chunk": chunk}
        })

    # Event 3: Complete
    yield format_sse_event({
        "event_type": "complete",
        "data": {"success": True}
    })
```

### Frontend (Angular)

The Angular client uses HttpClient with `observe: 'events'` and `reportProgress: true`:

```typescript
this.http.post(url, body, {
  observe: 'events',
  responseType: 'text',
  reportProgress: true
}).subscribe(event => {
  if (event.type === HttpEventType.DownloadProgress) {
    const lines = event.partialText.split('\n\n');
    lines.forEach(line => {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.substring(6));
        this.handleStreamEvent(data);
      }
    });
  }
});
```

## File Structure

```
interview/
├── interviewapis/           # Python FastAPI Backend
│   ├── main.py             # Main application entry
│   ├── agents/             # AI agent implementations
│   │   ├── router.py       # Streaming API router
│   │   ├── supervisor.py   # Supervisor agent
│   │   └── ...             # Specialized agents
│   ├── database/           # Database models and routes
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   └── requirements.txt    # Python dependencies
│
└── interviewweb/           # Angular Frontend
    ├── src/
    │   └── app/
    │       └── interview/
    │           ├── interview-room/          # Main interview component
    │           │   ├── interview-room.component.ts
    │           │   ├── interview-room.component.html
    │           │   └── interview-room.component.scss
    │           ├── services/
    │           │   └── agent-stream.service.ts  # Streaming service
    │           └── pipes/
    │               └── sanitize-html.pipe.ts    # HTML sanitization
    └── package.json
```

## Troubleshooting

### Backend Issues

**Issue**: Module not found errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: OpenAI API key not found
```bash
# Solution: Add OPENAI_API_KEY to .env file
echo "OPENAI_API_KEY=sk-..." > .env
```

**Issue**: CORS errors
```bash
# Solution: Check CORS configuration in main.py (already set to allow all origins)
```

### Frontend Issues

**Issue**: HttpClient not found
```bash
# Solution: HttpClientModule is already added to InterviewModule
```

**Issue**: Streaming not working
```bash
# Solution: Ensure backend is running on http://localhost:8000
# Check browser console for errors
# Verify API URL in agent-stream.service.ts
```

**Issue**: Content not displaying
```bash
# Solution: Check that SanitizeHtmlPipe is declared in InterviewModule
```

## Performance Optimization

### Backend
- Chunk size: 50 characters per chunk (configurable)
- Async processing for non-blocking I/O
- Connection pooling for database queries

### Frontend
- RxJS takeUntil for subscription cleanup
- OnPush change detection (can be enabled)
- Virtual scrolling for large message lists (can be added)

## Security Considerations

1. **API Key Protection**: Never commit `.env` file
2. **CORS Configuration**: Restrict origins in production
3. **Input Validation**: Pydantic models validate all inputs
4. **XSS Prevention**: DomSanitizer used for HTML content
5. **Rate Limiting**: Can be added using slowapi

## Future Enhancements

- [ ] Voice input for questions
- [ ] Code syntax highlighting
- [ ] Export conversation as PDF
- [ ] Real-time collaboration features
- [ ] Interview performance analytics
- [ ] Custom agent creation
- [ ] WebSocket support as alternative to SSE

## License

MIT License

## Support

For issues and questions:
- Check the API documentation at http://localhost:8000/docs
- Review browser console for frontend errors
- Check Python logs for backend errors
