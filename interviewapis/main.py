

from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Import modular agents
from agents import (
    SupervisorAgent,
    ProductManagerAgent,
    TechnicalAgent,
    ArchitectAgent,
    CodingAgent,
    BehavioralAgent,
    SystemDesignAgent,
)

# Import interview tracking routes
from database.routes import (
    router as stats_router,
    companies_router,
    roles_router,
    skills_router,
    interviews_router,
    questions_router
)

# Import agents streaming router
from agents.router import router as agents_stream_router

# Load environment variables
load_dotenv()


app = FastAPI(
    title="Multi-Agent Mock Interview System",
    description="AI-powered interview preparation with 6 specialized agents",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# LLM AND AGENTS INITIALIZATION
# ============================================================================

print("🔧 Initializing Multi-Agent Interview System...")

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Initialize all agents
print("   → Creating Supervisor Agent...")
supervisor_agent = SupervisorAgent(llm=llm)

print("   → Creating Product Manager Agent...")
product_manager_agent = ProductManagerAgent(llm=llm)

print("   → Creating Technical Expert Agent...")
technical_agent = TechnicalAgent(llm=llm)

print("   → Creating System Architect Agent...")
architect_agent = ArchitectAgent(llm=llm)

print("   → Creating Coding Expert Agent...")
coding_agent = CodingAgent(llm=llm)

print("   → Creating Behavioral Coach Agent...")
behavioral_agent = BehavioralAgent(llm=llm)

print("   → Creating System Design Agent...")
system_design_agent = SystemDesignAgent(llm=llm)

# Agent registry for routing
AGENT_REGISTRY = {
    'product_manager': product_manager_agent,
    'technical': technical_agent,
    'architect': architect_agent,
    'coding': coding_agent,
    'behavioral': behavioral_agent,
    'system_design': system_design_agent,
}

print("✅ All agents initialized successfully\n")

# ============================================================================
# REGISTER INTERVIEW TRACKING ROUTERS
# ============================================================================

print("Registering Interview Tracking API routes...")
app.include_router(stats_router)
app.include_router(companies_router)
app.include_router(roles_router)
app.include_router(skills_router)
app.include_router(interviews_router)
app.include_router(questions_router)
print("Interview Tracking API routes registered\n")

print("Registering Agents Streaming API routes...")
app.include_router(agents_stream_router)
print("Agents Streaming API routes registered\n")

# ============================================================================
# STATE DEFINITIONS
# ============================================================================

class InterviewState(TypedDict):
    """State for the interview workflow"""
    # Input
    question: str
    interview_type: Optional[str]
    user_context: Optional[str]
    conversation_history: List[Dict]
    
    # Routing
    selected_agent: Optional[str]
    routing_reasoning: Optional[str]
    routing_confidence: Optional[float]
    
    # Processing
    answer: Optional[str]
    agent_metadata: Optional[Dict]
    
    # Output
    suggested_follow_ups: List[str]
    timestamp: str
    
    # Error handling
    error: Optional[str]


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class InterviewRequest(BaseModel):
    """Request model for interview endpoint"""
    question: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="The interview question to answer"
    )
    interview_type: Optional[str] = Field(
        None,
        description="Optional hint about interview type (auto-detected if not provided)"
    )
    user_context: Optional[str] = Field(
        None,
        max_length=500,
        description="Additional context about the candidate (experience, role, etc.)"
    )
    conversation_history: List[Dict] = Field(
        default_factory=list,
        description="Previous Q&A exchanges for context-aware responses"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "question": "How would you design Instagram?",
                "interview_type": "system_design",
                "user_context": "5 years as software engineer at tech startup",
                "conversation_history": []
            }
        }


class InterviewResponse(BaseModel):
    """Response model for interview endpoint"""
    question: str
    answer: str
    agent_used: str
    routing_reasoning: str
    confidence_score: float
    suggested_follow_ups: List[str]
    timestamp: str
    
    class Config:
        schema_extra = {
            "example": {
                "question": "How would you design Instagram?",
                "answer": "Detailed system design answer...",
                "agent_used": "system_design",
                "routing_reasoning": "Question involves designing a large-scale system",
                "confidence_score": 0.95,
                "suggested_follow_ups": [
                    "How would you handle image storage?",
                    "What database would you choose?",
                    "How would you scale the feed?"
                ],
                "timestamp": "2024-12-02T10:30:00"
            }
        }


class AgentInfo(BaseModel):
    """Information about an agent"""
    id: str
    name: str
    specializations: List[str]
    best_for: List[str]


class AgentsListResponse(BaseModel):
    """Response for agents list endpoint"""
    total_agents: int
    agents: List[AgentInfo]


# ============================================================================
# WORKFLOW NODE FUNCTIONS
# ============================================================================

def supervisor_node(state: InterviewState) -> InterviewState:
    """
    Supervisor node: Analyzes question and routes to appropriate agent
    """
    print("🎯 Supervisor: Analyzing question and routing...")
    
    try:
        # Use supervisor agent to determine routing
        routing_result = supervisor_agent.route_question(
            question=state['question'],
            user_context=state.get('user_context'),
            interview_type=state.get('interview_type')
        )
        
        state['selected_agent'] = routing_result['selected_agent']
        state['routing_reasoning'] = routing_result['reasoning']
        state['routing_confidence'] = routing_result.get('confidence', 0.85)
        
        print(f"   ✅ Routed to: {state['selected_agent']}")
        print(f"   💡 Reasoning: {state['routing_reasoning'][:80]}...")
        print(f"   📊 Confidence: {state['routing_confidence']:.2f}")
        
    except Exception as e:
        print(f"   ❌ Routing error: {e}")
        # Fallback to technical agent
        state['selected_agent'] = 'technical'
        state['routing_reasoning'] = f"Fallback routing due to error: {str(e)}"
        state['routing_confidence'] = 0.6
    
    return state


def process_agent_node(state: InterviewState) -> InterviewState:
    """
    Agent processing node: Executes selected specialized agent
    """
    agent_type = state['selected_agent']
    agent = AGENT_REGISTRY.get(agent_type, technical_agent)  # Fallback to technical
    
    print(f"🤖 {agent_type.replace('_', ' ').title()}: Processing question...")
    
    try:
        # Process question with selected agent
        result = agent.process(
            question=state['question'],
            user_context=state.get('user_context'),
            conversation_history=state.get('conversation_history', [])
        )
        
        state['answer'] = result['answer']
        state['agent_metadata'] = result.get('metadata', {})
        
        word_count = len(result['answer'].split())
        print(f"   ✅ Answer generated: {word_count} words, {len(result['answer'])} chars")
        
    except Exception as e:
        print(f"   ❌ Processing error: {e}")
        state['answer'] = f"I apologize, but I encountered an error processing your question. Please try rephrasing or ask a different question."
        state['error'] = str(e)
    
    return state


def generate_followups_node(state: InterviewState) -> InterviewState:
    """
    Follow-up generation node: Creates relevant follow-up questions
    """
    print("💭 Generating follow-up questions...")
    
    # Skip if error occurred
    if state.get('error'):
        state['suggested_follow_ups'] = []
        state['timestamp'] = datetime.utcnow().isoformat()
        return state
    
    try:
        # Build prompt for follow-up generation
        prompt = f"""Based on this interview question and answer, suggest 3 highly relevant follow-up questions an interviewer might ask.

Original Question: {state['question']}

Answer Summary: {state['answer'][:400]}...

Agent Type: {state['selected_agent']}

Generate 3 follow-up questions that:
1. Dive deeper into the answer
2. Explore edge cases or alternatives
3. Test understanding of trade-offs

Respond with ONLY a JSON array: ["question 1", "question 2", "question 3"]"""

        # Call LLM for follow-ups
        response = llm.invoke([{"role": "user", "content": prompt}])
        response_text = response.content
        
        # Extract JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        follow_ups = json.loads(response_text)
        
        # Validate we got a list
        if not isinstance(follow_ups, list):
            raise ValueError("Follow-ups must be a list")
        
        state['suggested_follow_ups'] = follow_ups[:3]  # Ensure max 3
        print(f"   ✅ Generated {len(state['suggested_follow_ups'])} follow-up questions")
        
    except Exception as e:
        print(f"   ⚠️  Follow-up generation failed: {e}")
        # Provide generic follow-ups based on agent type
        agent_type = state['selected_agent']
        
        generic_followups = {
            'product_manager': [
                "How would you measure the success of this approach?",
                "What trade-offs would you consider?",
                "How would you prioritize if resources were limited?"
            ],
            'technical': [
                "Can you explain the time complexity?",
                "How would you handle edge cases?",
                "What are alternative approaches?"
            ],
            'architect': [
                "How would you scale this to millions of users?",
                "What failure scenarios should we consider?",
                "What are the cost implications?"
            ],
            'coding': [
                "How would you test this code?",
                "What edge cases need to be handled?",
                "How could this be optimized?"
            ],
            'behavioral': [
                "What did you learn from this experience?",
                "How would you handle it differently now?",
                "What was the biggest challenge?"
            ],
            'system_design': [
                "How would you handle data consistency?",
                "What caching strategy would you use?",
                "How would you monitor this system?"
            ]
        }
        
        state['suggested_follow_ups'] = generic_followups.get(
            agent_type,
            [
                "Can you elaborate on that approach?",
                "What alternatives did you consider?",
                "How would you validate this solution?"
            ]
        )
    
    # Add timestamp
    state['timestamp'] = datetime.utcnow().isoformat()
    
    return state


# ============================================================================
# WORKFLOW CONSTRUCTION
# ============================================================================

def build_interview_workflow() -> StateGraph:
    """
    Build the LangGraph workflow for interview processing
    """
    workflow = StateGraph(InterviewState)
    
    # Add nodes
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("process", process_agent_node)
    workflow.add_node("followups", generate_followups_node)
    
    # Define edges (workflow flow)
    workflow.set_entry_point("supervisor")
    workflow.add_edge("supervisor", "process")
    workflow.add_edge("process", "followups")
    workflow.add_edge("followups", END)
    
    return workflow.compile()


# Compile the workflow
print("🔧 Compiling LangGraph workflow...")
interview_workflow = build_interview_workflow()
print("✅ Workflow compiled and ready\n")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", tags=["General"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Multi-Agent Mock Interview System",
        "version": "3.0.0",
        "description": "AI-powered interview preparation with specialized agents",
        "architecture": "Modular agents with LangGraph orchestration",
        "agents": {
            "total": len(AGENT_REGISTRY),
            "types": list(AGENT_REGISTRY.keys())
        },
        "endpoints": {
            "documentation": "/docs",
            "health": "/api/health",
            "agents": "/api/agents",
            "agents_streaming": "/api/agents/answer-stream",
            "agents_non_streaming": "/api/agents/answer",
            "agents_available": "/api/agents/available",
            "interview": "/api/interview",
            "workflow": "/api/workflow",
            "stats": "/api/stats/overview",
            "companies": "/api/companies",
            "roles": "/api/roles",
            "skills": "/api/skills",
            "interviews": "/api/interviews",
            "questions": "/api/questions"
        },
        "quick_start": "POST /api/interview with your question",
        "interview_tracking": {
            "companies": "Manage companies",
            "roles": "Manage job roles",
            "skills": "Manage skills",
            "interviews": "Track interviews (list, add, update, delete)",
            "questions": "Manage interview questions (list, add, update, delete)"
        }
    }


@app.get("/api/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents_loaded": len(AGENT_REGISTRY),
        "llm_configured": bool(os.environ.get("OPENAI_API_KEY")),
        "workflow_ready": interview_workflow is not None,
        "version": "3.0.0"
    }


@app.get("/api/agents", response_model=AgentsListResponse, tags=["Agents"])
async def list_agents():
    """
    List all available agents with their capabilities
    """
    agents_info = []
    
    for agent_id, agent in AGENT_REGISTRY.items():
        capabilities = agent.get_capabilities()
        
        agents_info.append(AgentInfo(
            id=agent_id,
            name=agent_id.replace('_', ' ').title(),
            specializations=capabilities.get('specializations', []),
            best_for=capabilities.get('best_for', [])
        ))
    
    return AgentsListResponse(
        total_agents=len(agents_info),
        agents=agents_info
    )


@app.get("/api/workflow", tags=["Workflow"])
async def get_workflow_info():
    """Get information about the workflow structure"""
    return {
        "workflow_type": "LangGraph StateGraph",
        "nodes": [
            {
                "name": "supervisor",
                "description": "Analyzes question and routes to appropriate agent",
                "input": "question, context, history",
                "output": "selected_agent, routing_reasoning"
            },
            {
                "name": "process",
                "description": "Executes selected specialized agent",
                "input": "question, selected_agent, context",
                "output": "answer, metadata"
            },
            {
                "name": "followups",
                "description": "Generates relevant follow-up questions",
                "input": "question, answer",
                "output": "suggested_follow_ups"
            }
        ],
        "flow": "supervisor → process → followups → END",
        "state_fields": [
            "question",
            "selected_agent",
            "answer",
            "suggested_follow_ups",
            "timestamp"
        ]
    }


@app.post("/api/interview", response_model=InterviewResponse, tags=["Interview"])
async def conduct_interview(request: InterviewRequest):
    """
    Conduct a mock interview with automatic agent routing
    
    The system will:
    1. Analyze your question
    2. Route to the most appropriate specialized agent
    3. Generate a comprehensive answer
    4. Suggest relevant follow-up questions
    
    Supported agent types:
    - product_manager: Product strategy, frameworks, metrics
    - technical: Algorithms, data structures, concepts
    - architect: System architecture, scalability
    - coding: Code implementation, best practices
    - behavioral: Leadership, soft skills, STAR method
    - system_design: Distributed systems, large-scale design
    """
    
    try:
        print(f"\n{'='*80}")
        print(f"🎤 New Interview Question")
        print(f"{'='*80}")
        print(f"Question: {request.question[:100]}{'...' if len(request.question) > 100 else ''}")
        if request.user_context:
            print(f"Context: {request.user_context[:80]}{'...' if len(request.user_context) > 80 else ''}")
        print(f"{'='*80}\n")
        
        # Prepare initial state
        initial_state: InterviewState = {
            "question": request.question,
            "interview_type": request.interview_type,
            "user_context": request.user_context,
            "conversation_history": request.conversation_history,
            "selected_agent": None,
            "routing_reasoning": None,
            "routing_confidence": None,
            "answer": None,
            "agent_metadata": None,
            "suggested_follow_ups": [],
            "timestamp": datetime.utcnow().isoformat(),
            "error": None
        }
        
        # Execute workflow
        final_state = interview_workflow.invoke(initial_state)
        
        print(f"\n{'='*80}")
        print(f"✅ Interview Completed Successfully")
        print(f"{'='*80}\n")
        
        # Check for errors
        if final_state.get('error'):
            raise HTTPException(
                status_code=500,
                detail=f"Error processing question: {final_state['error']}"
            )
        
        # Build response
        return InterviewResponse(
            question=request.question,
            answer=final_state['answer'],
            agent_used=final_state['selected_agent'],
            routing_reasoning=final_state['routing_reasoning'],
            confidence_score=final_state['routing_confidence'],
            suggested_follow_ups=final_state['suggested_follow_ups'],
            timestamp=final_state['timestamp']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n❌ Interview Error: {str(e)}\n")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


# ============================================================================
# STARTUP AND SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("\n" + "="*80)
    print("  🚀 MULTI-AGENT INTERVIEW SYSTEM STARTED")
    print("="*80)
    print(f"  Version: 3.0.0")
    print(f"  Agents: {len(AGENT_REGISTRY)} specialized agents loaded")
    print(f"  Documentation: http://localhost:8000/docs")
    print(f"  Health Check: http://localhost:8000/api/health")
    print("="*80 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("\n" + "="*80)
    print("  👋 MULTI-AGENT INTERVIEW SYSTEM SHUTTING DOWN")
    print("="*80 + "\n")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
