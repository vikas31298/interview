"""
Streaming API Router for Interview Question Answering
Provides Server-Sent Events (SSE) streaming for real-time responses
Compatible with Angular HttpClient and EventSource
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, AsyncGenerator
import json
import asyncio
from datetime import datetime

from langchain_openai import ChatOpenAI
from agents.supervisor import SupervisorAgent
from agents.product_manager import ProductManagerAgent
from agents.technical import TechnicalAgent
from agents.architect import ArchitectAgent
from agents.coding import CodingAgent
from agents.behavioral import BehavioralAgent
from agents.system_design import SystemDesignAgent
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize router
router = APIRouter(prefix="/api/agents", tags=["Agents Streaming"])

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Initialize agents
supervisor_agent = SupervisorAgent(llm=llm)
product_manager_agent = ProductManagerAgent(llm=llm)
technical_agent = TechnicalAgent(llm=llm)
architect_agent = ArchitectAgent(llm=llm)
coding_agent = CodingAgent(llm=llm)
behavioral_agent = BehavioralAgent(llm=llm)
system_design_agent = SystemDesignAgent(llm=llm)

# Agent registry
AGENT_REGISTRY = {
    'product_manager': product_manager_agent,
    'technical': technical_agent,
    'architect': architect_agent,
    'coding': coding_agent,
    'behavioral': behavioral_agent,
    'system_design': system_design_agent,
}


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class QuestionRequest(BaseModel):
    """Request model for question answering"""
    question: str = Field(..., min_length=5, max_length=2000, description="The interview question")
    context: Optional[str] = Field(None, max_length=1000, description="Additional context about the candidate")
    conversation_history: Optional[List[Dict]] = Field(default_factory=list, description="Previous conversation")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "How would you design a URL shortening service?",
                "context": "Senior engineer with 5 years experience",
                "conversation_history": []
            }
        }


class StreamEvent(BaseModel):
    """Structured event model for streaming"""
    event_type: str  # routing, processing, content, follow_ups, complete, error
    timestamp: str
    data: Dict


# ============================================================================
# STREAMING FUNCTIONS
# ============================================================================

async def generate_stream_events(question: str, context: Optional[str], conversation_history: List[Dict]) -> AsyncGenerator[str, None]:
    """
    Generate Server-Sent Events (SSE) for streaming responses

    Event Types:
    - routing: Agent selection and routing information
    - processing: Processing status updates
    - content: Answer content (streamed in chunks)
    - follow_ups: Suggested follow-up questions
    - complete: Final completion event
    - error: Error information
    """

    try:
        # Event 1: Start
        yield format_sse_event({
            "event_type": "start",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "message": "Processing question...",
                "question": question
            }
        })

        await asyncio.sleep(0.1)  # Small delay for client to process

        # Event 2: Routing
        try:
            routing_result = supervisor_agent.route_question(
                question=question,
                user_context=context,
                interview_type=None
            )

            selected_agent = routing_result['selected_agent']
            routing_reasoning = routing_result['reasoning']
            confidence = routing_result.get('confidence', 0.85)

            yield format_sse_event({
                "event_type": "routing",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "selected_agent": selected_agent,
                    "reasoning": routing_reasoning,
                    "confidence": confidence
                }
            })

            await asyncio.sleep(0.1)

        except Exception as e:
            # Fallback to technical agent
            selected_agent = 'technical'
            routing_reasoning = f"Fallback routing: {str(e)}"
            confidence = 0.6

            yield format_sse_event({
                "event_type": "routing",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "selected_agent": selected_agent,
                    "reasoning": routing_reasoning,
                    "confidence": confidence,
                    "fallback": True
                }
            })

        # Event 3: Processing
        yield format_sse_event({
            "event_type": "processing",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "message": f"Processing with {selected_agent} agent...",
                "agent": selected_agent
            }
        })

        await asyncio.sleep(0.1)

        # Event 4: Generate Answer (streamed)
        agent = AGENT_REGISTRY.get(selected_agent, technical_agent)

        try:
            result = agent.process(
                question=question,
                user_context=context,
                conversation_history=conversation_history
            )

            answer = result.get('answer', '')
            metadata = result.get('metadata', {})

            # Stream answer in chunks (simulate streaming for better UX)
            chunk_size = 50  # Characters per chunk
            for i in range(0, len(answer), chunk_size):
                chunk = answer[i:i + chunk_size]

                yield format_sse_event({
                    "event_type": "content",
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": {
                        "chunk": chunk,
                        "is_final": i + chunk_size >= len(answer)
                    }
                })

                await asyncio.sleep(0.05)  # Small delay between chunks

            # Event 5: Complete Answer
            yield format_sse_event({
                "event_type": "answer_complete",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "full_answer": answer,
                    "word_count": len(answer.split()),
                    "character_count": len(answer),
                    "metadata": metadata
                }
            })

            await asyncio.sleep(0.1)

        except Exception as e:
            yield format_sse_event({
                "event_type": "error",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "error": str(e),
                    "message": "Failed to generate answer"
                }
            })
            return

        # Event 6: Generate Follow-ups
        try:
            follow_ups = await generate_follow_up_questions(question, answer, selected_agent)

            yield format_sse_event({
                "event_type": "follow_ups",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "questions": follow_ups
                }
            })

        except Exception as e:
            # Provide generic follow-ups on error
            generic_followups = get_generic_followups(selected_agent)

            yield format_sse_event({
                "event_type": "follow_ups",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "questions": generic_followups,
                    "generic": True
                }
            })

        # Event 7: Complete
        yield format_sse_event({
            "event_type": "complete",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "message": "Processing complete",
                "agent_used": selected_agent,
                "success": True
            }
        })

    except Exception as e:
        # Final error event
        yield format_sse_event({
            "event_type": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "data": {
                "error": str(e),
                "message": "An unexpected error occurred"
            }
        })


def format_sse_event(data: Dict) -> str:
    """
    Format data as Server-Sent Event

    SSE Format:
    data: <json>\n\n
    """
    json_data = json.dumps(data)
    return f"data: {json_data}\n\n"


async def generate_follow_up_questions(question: str, answer: str, agent_type: str) -> List[str]:
    """Generate follow-up questions based on the answer"""

    prompt = f"""Based on this interview question and answer, suggest 3 highly relevant follow-up questions.

Original Question: {question}

Answer Summary: {answer[:400]}...

Agent Type: {agent_type}

Generate 3 follow-up questions that:
1. Dive deeper into the answer
2. Explore edge cases or alternatives
3. Test understanding of trade-offs

Respond with ONLY a JSON array: ["question 1", "question 2", "question 3"]"""

    try:
        response = llm.invoke([{"role": "user", "content": prompt}])
        response_text = response.content

        # Extract JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()

        follow_ups = json.loads(response_text)

        if isinstance(follow_ups, list):
            return follow_ups[:3]
        else:
            return get_generic_followups(agent_type)

    except:
        return get_generic_followups(agent_type)


def get_generic_followups(agent_type: str) -> List[str]:
    """Get generic follow-up questions based on agent type"""

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

    return generic_followups.get(
        agent_type,
        [
            "Can you elaborate on that approach?",
            "What alternatives did you consider?",
            "How would you validate this solution?"
        ]
    )


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.post("/answer-stream")
async def answer_question_stream(request: QuestionRequest):
    """
    Stream interview question answer in real-time using Server-Sent Events (SSE)

    This endpoint returns a stream of events that can be consumed by Angular's HttpClient
    or native EventSource API.

    Event Types:
    - start: Processing started
    - routing: Agent selection information
    - processing: Processing status
    - content: Answer content chunks (streamed)
    - answer_complete: Full answer with metadata
    - follow_ups: Suggested follow-up questions
    - complete: Processing complete
    - error: Error information

    Example Angular consumption:
    ```typescript
    this.http.post('/api/agents/answer-stream', body, {
      observe: 'events',
      responseType: 'text',
      reportProgress: true
    }).subscribe(event => {
      if (event.type === HttpEventType.DownloadProgress) {
        const lines = event.partialText.split('\\n\\n');
        lines.forEach(line => {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.substring(6));
            this.handleEvent(data);
          }
        });
      }
    });
    ```
    """

    return StreamingResponse(
        generate_stream_events(
            question=request.question,
            context=request.context,
            conversation_history=request.conversation_history or []
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.post("/answer")
async def answer_question(request: QuestionRequest):
    """
    Get complete interview question answer (non-streaming)

    Returns a structured JSON response with the complete answer and metadata.
    Use this endpoint if you don't need streaming functionality.
    """

    try:
        # Route question
        routing_result = supervisor_agent.route_question(
            question=request.question,
            user_context=request.context,
            interview_type=None
        )

        selected_agent = routing_result['selected_agent']
        routing_reasoning = routing_result['reasoning']
        confidence = routing_result.get('confidence', 0.85)

        # Process with selected agent
        agent = AGENT_REGISTRY.get(selected_agent, technical_agent)
        result = agent.process(
            question=request.question,
            user_context=request.context,
            conversation_history=request.conversation_history or []
        )

        answer = result.get('answer', '')
        metadata = result.get('metadata', {})

        # Generate follow-ups
        try:
            follow_ups = await generate_follow_up_questions(request.question, answer, selected_agent)
        except:
            follow_ups = get_generic_followups(selected_agent)

        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "question": request.question,
            "routing": {
                "selected_agent": selected_agent,
                "reasoning": routing_reasoning,
                "confidence": confidence
            },
            "answer": answer,
            "metadata": metadata,
            "follow_up_questions": follow_ups,
            "statistics": {
                "word_count": len(answer.split()),
                "character_count": len(answer)
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@router.get("/available")
async def list_available_agents():
    """
    List all available agents with their capabilities
    """

    agents_info = []

    for agent_id, agent in AGENT_REGISTRY.items():
        capabilities = agent.get_capabilities()

        agents_info.append({
            "id": agent_id,
            "name": agent_id.replace('_', ' ').title(),
            "specializations": capabilities.get('specializations', []),
            "best_for": capabilities.get('best_for', [])
        })

    return {
        "total_agents": len(agents_info),
        "agents": agents_info
    }
