# Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 18+
- OpenAI API Key

## Quick Setup (5 minutes)

### 1. Backend Setup
```bash
# Navigate to backend
cd interviewapis

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Start server
uvicorn main:app --reload
```

Backend will run at: **http://localhost:8000**

### 2. Frontend Setup
```bash
# Open new terminal
cd interviewweb

# Install dependencies
npm install

# Start Angular app
ng serve
```

Frontend will run at: **http://localhost:4200**

### 3. Test Streaming

1. Open browser: http://localhost:4200/interview/room
2. Type question: "How would you design Instagram?"
3. Click "Send" and watch the streaming response!

## API Endpoints Summary

### Streaming (for Angular app)
- **POST** `/api/agents/answer-stream` - Stream AI responses (SSE)
- **POST** `/api/agents/answer` - Get complete response (non-streaming)
- **GET** `/api/agents/available` - List available agents

### Interview Tracking
- **GET** `/api/companies` - List companies
- **POST** `/api/companies` - Create company
- **GET** `/api/interviews` - List interviews
- **POST** `/api/interviews` - Create interview
- **GET** `/api/questions` - List questions
- **POST** `/api/questions` - Create question

### Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

**Backend not starting?**
- Check if Python 3.8+ is installed: `python --version`
- Verify OpenAI API key in `.env` file

**Frontend not starting?**
- Check if Node.js is installed: `node --version`
- Run `npm install` again if modules are missing

**Streaming not working?**
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify CORS is enabled (already configured)

## Next Steps

1. Read full documentation: `STREAMING_SETUP.md`
2. Explore API docs: http://localhost:8000/docs
3. Try different question types:
   - System Design: "Design a URL shortener"
   - Technical: "Explain REST vs GraphQL"
   - Behavioral: "Tell me about a conflict you resolved"
   - Coding: "Reverse a linked list"
