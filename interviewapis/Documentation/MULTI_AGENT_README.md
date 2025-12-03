# Multi-Agent Mock Interview System

AI-powered interview preparation with 6 specialized agents using LangGraph orchestration.

## 🎯 Overview

This system features a **supervisor pattern** where questions are automatically routed to the most appropriate specialized agent:

```
User Question → Supervisor Agent → Specialized Agent → Answer + Follow-ups
```

## 🤖 Available Agents

### 1. Product Manager Agent
**Best for**: Product strategy, frameworks, metrics, user research

**Expertise**:
- Product strategy and vision
- Prioritization frameworks (RICE, ICE, Kano)
- Metrics (AARRR, HEART)
- User research and insights
- Roadmap planning
- Stakeholder management

**Example Questions**:
- "How would you prioritize features for a new product?"
- "What metrics would you track for a social media app?"
- "Explain the CIRCLES method"

---

### 2. Technical Expert Agent
**Best for**: Algorithms, data structures, technical concepts

**Expertise**:
- Algorithms and complexity analysis
- Data structures
- Design patterns
- Debugging and optimization
- Software engineering principles
- Testing strategies

**Example Questions**:
- "Explain binary search trees"
- "What's the time complexity of quicksort?"
- "How do hash tables work?"

---

### 3. System Architect Agent
**Best for**: Architecture, scalability, infrastructure

**Expertise**:
- System architecture and design patterns
- Scalability and performance
- Microservices vs monoliths
- Database design
- Cloud architecture (AWS, GCP, Azure)
- Load balancing and high availability

**Example Questions**:
- "Design a microservices architecture for e-commerce"
- "How would you scale a database?"
- "Explain CAP theorem"

---

### 4. Coding Expert Agent
**Best for**: Writing code, implementation

**Expertise**:
- Production-quality code
- Multiple programming languages
- Code review and best practices
- Testing and TDD
- Error handling
- Performance optimization

**Example Questions**:
- "Write a function to reverse a linked list"
- "Implement binary search in Python"
- "How would you handle errors in this code?"

---

### 5. Behavioral Coach Agent
**Best for**: Soft skills, past experiences

**Expertise**:
- STAR method
- Leadership and team management
- Conflict resolution
- Communication skills
- Decision-making
- Stakeholder management

**Example Questions**:
- "Tell me about a time you dealt with conflict"
- "Describe a project that failed"
- "How do you handle difficult stakeholders?"

---

### 6. System Design Expert Agent
**Best for**: Distributed systems, scalability

**Expertise**:
- Distributed systems design
- Trade-offs (CAP theorem)
- Database selection (SQL vs NoSQL)
- Caching strategies
- Message queues
- Data partitioning

**Example Questions**:
- "Design Twitter"
- "Design a URL shortener"
- "How would you design Netflix?"

---

## 🚀 Quick Start

### Installation

```bash
# 1. Install dependencies
pip install fastapi uvicorn langchain langchain-openai langgraph python-dotenv pydantic

# 2. Set environment variables
export OPENAI_API_KEY="sk-your-key-here"

# 3. Start the API
uvicorn main:app --reload --port 8000

# 4. In another terminal, run client
python interview_client.py
```

---

## 💻 API Usage

### Start API
```bash
uvicorn main:app --reload --port 8000
```

### Python Client
```python
from interview_client import InterviewClient

# Initialize
client = InterviewClient("http://localhost:8000")

# Ask a question
result = client.ask_question(
    question="How would you design Instagram?",
    user_context="5 years as software engineer"
)

print(result['answer'])
print(result['agent_used'])
print(result['suggested_follow_ups'])
```

### cURL
```bash
curl -X POST http://localhost:8000/api/interview \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain the STAR method",
    "user_context": "Preparing for PM interviews"
  }'
```

---

## 📡 API Endpoints

### Health Check
```bash
GET /api/health
```

### List Agents
```bash
GET /api/agents
```

### Ask Question
```bash
POST /api/interview

Body:
{
  "question": "Your interview question",
  "interview_type": "optional - auto-detected",
  "user_context": "optional - about yourself",
  "conversation_history": []
}

Response:
{
  "question": "...",
  "answer": "...",
  "agent_used": "product_manager",
  "reasoning": "...",
  "confidence_score": 0.85,
  "suggested_follow_ups": ["...", "...", "..."],
  "timestamp": "..."
}
```

---

## 🎓 Interactive Client Features

### Mode 1: Interactive Session
- Continuous Q&A
- Context-aware (remembers conversation)
- Suggested follow-up questions
- Command support: `quit`, `clear`, `history`

### Mode 2: Quick Test
- Pre-loaded example questions
- Different categories
- Quick testing

### Mode 3: Single Question
- Ask one question
- Get answer and exit

---

## 🏗️ Architecture

### Supervisor Pattern
```
┌─────────────┐
│   User Q    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   Supervisor    │  ← Analyzes question
│     Agent       │  ← Routes to best agent
└─────────┬───────┘
          │
    ┌─────┴─────┬──────┬────────┬─────────┬──────────┐
    ▼           ▼      ▼        ▼         ▼          ▼
┌────────┐  ┌────┐ ┌──────┐ ┌──────┐ ┌────────┐ ┌──────┐
│Product │  │Tech│ │Arch  │ │Coding│ │Behavior│ │System│
│Manager │  │    │ │      │ │      │ │        │ │Design│
└────┬───┘  └─┬──┘ └───┬──┘ └──┬───┘ └───┬────┘ └──┬───┘
     │        │        │       │         │         │
     └────────┴────────┴───────┴─────────┴─────────┘
                       │
                       ▼
              ┌────────────────┐
              │  Synthesize    │  ← Generate follow-ups
              │  Final Answer  │  ← Calculate confidence
              └───────┬────────┘
                      │
                      ▼
                ┌──────────┐
                │ Response │
                └──────────┘
```

### State Management
Each question goes through:
1. **Routing** - Supervisor determines best agent
2. **Processing** - Specialized agent generates answer
3. **Synthesis** - Final answer + follow-ups
4. **History** - Context maintained across conversation

---

## 🎯 Use Cases

### 1. Interview Preparation
```python
# Practice product management interviews
result = client.ask_question(
    "How would you improve Spotify?",
    user_context="3 years PM at music streaming startup"
)
```

### 2. Technical Practice
```python
# Practice coding interviews
result = client.ask_question(
    "Write a function to find the longest palindrome",
    user_context="Preparing for FAANG interviews"
)
```

### 3. System Design Practice
```python
# Practice system design
result = client.ask_question(
    "Design WhatsApp",
    user_context="Senior engineer, 7 years experience"
)
```

### 4. Behavioral Prep
```python
# Practice behavioral questions
result = client.ask_question(
    "Tell me about a time you disagreed with your manager",
    user_context="5 years as team lead"
)
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Required
export OPENAI_API_KEY="sk-..."

# Optional
export API_HOST="0.0.0.0"
export API_PORT="8000"
```

### Customize Agents
Edit `AGENT_PROMPTS` in `main.py`:
```python
AGENT_PROMPTS = {
    AgentType.PRODUCT_MANAGER: """Your custom prompt...""",
    # Add more customizations
}
```

### Add New Agents
1. Add to `AgentType` class
2. Create prompt in `AGENT_PROMPTS`
3. Create node function
4. Add to workflow graph
5. Update routing logic

---

## 📊 Response Format

```python
{
    "question": "Original question",
    "answer": "Comprehensive answer from agent",
    "agent_used": "product_manager",
    "reasoning": "Why this agent was selected",
    "confidence_score": 0.85,
    "suggested_follow_ups": [
        "Can you elaborate on...?",
        "How would you handle...?",
        "What trade-offs did you consider?"
    ],
    "timestamp": "2024-12-02T10:30:00"
}
```

---

## 🧪 Testing

### Quick Test
```bash
# Start API
uvicorn main:app --reload

# Run client with test mode
python interview_client.py
# Select option 2 (Quick Test)
```

### API Tests
```bash
# Health check
curl http://localhost:8000/api/health

# List agents
curl http://localhost:8000/api/agents

# Test question
curl -X POST http://localhost:8000/api/interview \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain microservices"}'
```

---

## 💡 Tips for Best Results

### 1. Provide Context
```python
# Better results with context
result = client.ask_question(
    "How would you scale this system?",
    user_context="10 years as architect, worked at Netflix"
)
```

### 2. Use Conversation History
The system remembers previous Q&A in a session, making follow-ups more relevant.

### 3. Leverage Follow-ups
The system generates contextual follow-up questions - use them to practice deeper!

### 4. Be Specific
```python
# Too vague
"Tell me about databases"

# Better
"How would you choose between PostgreSQL and MongoDB for a social media app?"
```

---

## 🔐 Security Notes

- API key stored in environment variables
- No authentication by default (add for production)
- Consider rate limiting for public deployment
- Add CORS configuration for web clients

---

## 📈 Performance

- **Routing**: ~2-3 seconds
- **Answer Generation**: ~10-30 seconds
- **Total per Question**: ~15-35 seconds

Factors:
- LLM response time
- Question complexity
- Conversation history length

---

## 🚢 Deployment

### Docker (Recommended)
```bash
# Create Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Build and run
docker build -t interview-api .
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY interview-api
```

### Cloud Deployment
- **AWS**: ECS/Fargate
- **GCP**: Cloud Run
- **Azure**: Container Apps
- **Heroku**: Container deployment

---

## 🛠️ Troubleshooting

### API Won't Start
```bash
# Check Python version
python --version  # Need 3.10+

# Check dependencies
pip install -r requirements.txt

# Check OpenAI key
echo $OPENAI_API_KEY
```

### Slow Responses
- Normal for first request (cold start)
- LLM calls take 10-30 seconds
- Check internet connection
- Verify OpenAI API status

### Routing Issues
- Supervisor has fallback to technical agent
- Check logs for routing reasoning
- Adjust agent prompts if needed

---

## 📚 Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API](https://platform.openai.com/docs)

---

## 🎉 Next Steps

1. **Start practicing**: Run the interactive client
2. **Try all agents**: Test different question types
3. **Customize agents**: Adjust prompts for your needs
4. **Add features**: Extend with your own agents
5. **Deploy**: Make it available for your team

---

**Built with LangGraph, FastAPI, and OpenAI GPT-4**

**Status**: ✅ Production-Ready

**Version**: 2.0.0
