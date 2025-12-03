"""
Product Management Case Study Analyzer - LangGraph API
FastAPI + LangGraph implementation

Usage:
    uvicorn pm_api:app --reload --port 8000
"""

from typing import TypedDict, Annotated, List, Dict, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import json
import os
from dotenv import load_dotenv
from framework import get_frameworks_sync

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="PM Case Study Analyzer API",
    description="AI-powered Product Management case study analysis using LangGraph",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Load frameworks from database
print("🔄 Loading frameworks from database...")
try:
    frameworks_list = get_frameworks_sync()
    FRAMEWORKS = {}
    
    for fw in frameworks_list:
        category = fw.get('category', 'Other')
        if category not in FRAMEWORKS:
            FRAMEWORKS[category] = {
                "primary": fw['name'],
                "alternatives": [],
                "description": fw.get('description', ''),
                "frameworks": [fw]
            }
        else:
            FRAMEWORKS[category]["alternatives"].append(fw['name'])
            FRAMEWORKS[category]["frameworks"].append(fw)
    
    print(f"✅ Loaded {len(FRAMEWORKS)} framework categories\n")
except Exception as e:
    print(f"⚠️  Error loading frameworks: {e}")
    FRAMEWORKS = {
        "Product Improvement": {
            "primary": "CIRCLES Method",
            "alternatives": ["SWOT Analysis", "Jobs-to-be-Done"],
            "description": "Comprehend, Identify, Report, Cut, List, Evaluate, Summarize",
            "frameworks": []
        }
    }


# ============================================================================
# PYDANTIC MODELS FOR API
# ============================================================================

class CaseStudyRequest(BaseModel):
    case_study: str = Field(..., description="The case study problem statement", min_length=5)
    additional_context: Optional[str] = Field(None, description="Additional context or constraints")
    include_clarifying_questions: bool = Field(True, description="Whether to generate clarifying questions")
    include_complete_solution: bool = Field(True, description="Whether to generate complete solution")


class QuestionItem(BaseModel):
    question: str
    why_important: str
    category: str


class ClassificationResult(BaseModel):
    problem_type: str
    confidence: float
    reasoning: str
    key_indicators: List[str]


class FrameworkRecommendation(BaseModel):
    framework: str
    rationale: str
    application_steps: List[str]
    key_tips: List[str]
    common_pitfalls: List[str]
    alternatives: List[str]


class UserSegment(BaseModel):
    segment: str
    needs: str
    pain_points: str


class ProposedSolution(BaseModel):
    solution_name: str
    description: str
    user_impact: str
    business_impact: str
    priority: str
    implementation_complexity: str


class PrioritizedRecommendation(BaseModel):
    top_solution: str
    rationale: str
    success_metrics: List[str]
    implementation_timeline: str
    resource_requirements: str


class TradeOff(BaseModel):
    tradeoff: str
    decision: str


class RiskMitigation(BaseModel):
    risk: str
    mitigation: str


class CompleteSolution(BaseModel):
    executive_summary: str
    situation_analysis: Dict
    user_analysis: Dict
    proposed_solutions: List[ProposedSolution]
    prioritized_recommendation: PrioritizedRecommendation
    tradeoffs_considered: List[TradeOff]
    risks_and_mitigations: List[RiskMitigation]
    next_steps: List[str]


class AnalysisResponse(BaseModel):
    case_study: str
    classification: ClassificationResult
    clarifying_questions: Optional[List[QuestionItem]] = None
    framework_recommendation: FrameworkRecommendation
    complete_solution: Optional[CompleteSolution] = None


# ============================================================================
# LANGGRAPH STATE DEFINITION
# ============================================================================

class PMCaseState(TypedDict):
    """State for PM case study analysis workflow"""
    # Input
    case_study: str
    additional_context: Optional[str]
    include_clarifying_questions: bool
    include_complete_solution: bool
    
    # Intermediate states
    classification: Optional[Dict]
    clarifying_questions: Optional[Dict]
    framework_recommendation: Optional[Dict]
    complete_solution: Optional[Dict]
    
    # Output
    result: Optional[Dict]
    error: Optional[str]


# ============================================================================
# LANGGRAPH NODE FUNCTIONS
# ============================================================================

def classify_problem_node(state: PMCaseState) -> PMCaseState:
    """Node 1: Classify the PM problem type"""
    print("📊 Node 1: Classifying problem type...")
    
    case_study = state['case_study']
    if state.get('additional_context'):
        case_study += f". Additional context: {state['additional_context']}"
    
    categories = list(FRAMEWORKS.keys())
    categories_str = "\n- ".join(categories)
    
    system_prompt = "You are a Product Management expert. Analyze case studies and classify them into PM problem categories."
    
    user_prompt = f"""Analyze this case study and classify it.

Case Study: "{case_study}"

Classify into ONE of these categories:
- {categories_str}

Respond in JSON format:
{{
  "problem_type": "category name",
  "confidence": 0.95,
  "reasoning": "brief explanation",
  "key_indicators": ["keyword1", "keyword2"]
}}"""

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        response_text = response.content
        
        # Extract JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        classification = json.loads(response_text)
        
        # Validate problem_type
        if classification['problem_type'] not in FRAMEWORKS:
            for category in FRAMEWORKS.keys():
                if category.lower() in classification['problem_type'].lower():
                    classification['problem_type'] = category
                    break
            else:
                classification['problem_type'] = list(FRAMEWORKS.keys())[0]
        
        state['classification'] = classification
        print(f"   ✅ Classified as: {classification['problem_type']}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        state['classification'] = {
            "problem_type": list(FRAMEWORKS.keys())[0],
            "confidence": 0.7,
            "reasoning": "Default classification due to error",
            "key_indicators": []
        }
    
    return state


def generate_questions_node(state: PMCaseState) -> PMCaseState:
    """Node 2: Generate clarifying questions"""
    if not state.get('include_clarifying_questions'):
        print("⏭️  Node 2: Skipping clarifying questions")
        state['clarifying_questions'] = None
        return state
    
    print("❓ Node 2: Generating clarifying questions...")
    
    case_study = state['case_study']
    problem_type = state['classification']['problem_type']
    
    system_prompt = """You are a senior Product Manager conducting a case study interview. 
    Generate insightful clarifying questions that help understand the problem better."""
    
    user_prompt = f"""Given this case study, generate 5-7 clarifying questions that a PM should ask.

Case Study: "{case_study}"
Problem Type: {problem_type}

Generate questions that cover:
- Understanding constraints (time, budget, resources)
- Target users and stakeholders
- Success criteria and metrics
- Current state and context
- Business goals
- Technical constraints

Respond in JSON format:
{{
  "questions": [
    {{
      "question": "What is the primary goal: user satisfaction or business metrics?",
      "why_important": "Helps prioritize solutions between user experience and revenue",
      "category": "Goals"
    }}
  ]
}}

Provide 5-7 questions that are specific to this case and problem type."""

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        response_text = response.content
        
        # Extract JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        state['clarifying_questions'] = json.loads(response_text)
        print(f"   ✅ Generated {len(state['clarifying_questions']['questions'])} questions")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        state['clarifying_questions'] = {
            "questions": [
                {
                    "question": "What are the main constraints?",
                    "why_important": "Helps scope the solution",
                    "category": "Constraints"
                }
            ]
        }
    
    return state


def recommend_framework_node(state: PMCaseState) -> PMCaseState:
    """Node 3: Recommend framework with detailed guidance"""
    print("📚 Node 3: Recommending framework...")
    
    case_study = state['case_study']
    if state.get('additional_context'):
        case_study += f". Additional context: {state['additional_context']}"
    
    problem_type = state['classification']['problem_type']
    framework_info = FRAMEWORKS.get(problem_type, FRAMEWORKS[list(FRAMEWORKS.keys())[0]])
    
    # Get detailed framework info from database
    framework_details = ""
    if framework_info.get('frameworks'):
        primary_fw = framework_info['frameworks'][0]
        framework_details = f"""
Framework Details from Database:
- When to Use: {primary_fw.get('when_to_use', 'N/A')}
- How to Apply: {primary_fw.get('how_to_apply', 'N/A')}
- Key Benefits: {', '.join(primary_fw.get('key_benefits', [])) if primary_fw.get('key_benefits') else 'N/A'}
- Common Pitfalls: {', '.join(primary_fw.get('common_pitfalls', [])) if primary_fw.get('common_pitfalls') else 'N/A'}
"""
    
    system_prompt = "You are a PM framework expert. Provide detailed, actionable guidance for applying product management frameworks."
    
    user_prompt = f"""Provide detailed guidance for this case study.

Case Study: "{case_study}"
Problem Type: {problem_type}
Recommended Framework: {framework_info['primary']}
Framework Description: {framework_info['description']}
{framework_details}

Provide a detailed response in JSON format:
{{
  "framework": "{framework_info['primary']}",
  "rationale": "why this framework is perfect for this specific case",
  "application_steps": [
    "Step 1: Specific actionable guidance for this case",
    "Step 2: Next step with concrete examples",
    "Step 3: Continue with detailed steps (provide 5-7 steps)"
  ],
  "key_tips": ["tip 1", "tip 2", "tip 3"],
  "common_pitfalls": ["pitfall 1", "pitfall 2"]
}}"""

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        response_text = response.content
        
        # Extract JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        recommendation = json.loads(response_text)
        recommendation["alternatives"] = framework_info["alternatives"]
        state['framework_recommendation'] = recommendation
        print(f"   ✅ Recommended: {recommendation['framework']}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        state['framework_recommendation'] = {
            "framework": framework_info['primary'],
            "rationale": f"Standard framework for {problem_type}",
            "application_steps": ["Apply framework systematically"],
            "key_tips": [],
            "common_pitfalls": [],
            "alternatives": framework_info["alternatives"]
        }
    
    return state


def generate_solution_node(state: PMCaseState) -> PMCaseState:
    """Node 4: Generate complete solution"""
    if not state.get('include_complete_solution'):
        print("⏭️  Node 4: Skipping complete solution")
        state['complete_solution'] = None
        return state
    
    print("🎯 Node 4: Generating complete solution...")
    
    case_study = state['case_study']
    if state.get('additional_context'):
        case_study += f". Additional context: {state['additional_context']}"
    
    problem_type = state['classification']['problem_type']
    framework = state['framework_recommendation']['framework']
    
    system_prompt = """You are an expert Product Manager who excels at solving PM case studies. 
    Provide comprehensive, detailed solutions that would impress in a PM interview."""
    
    user_prompt = f"""Provide a COMPLETE SOLUTION for this PM case study.

Case Study: "{case_study}"
Problem Type: {problem_type}
Framework: {framework}

Generate a comprehensive solution in JSON format with these sections:

{{
  "executive_summary": "2-3 sentence overview of your recommended solution",
  "situation_analysis": {{
    "current_state": "Analysis of current situation",
    "key_challenges": ["challenge 1", "challenge 2", "challenge 3"],
    "opportunities": ["opportunity 1", "opportunity 2"]
  }},
  "user_analysis": {{
    "user_segments": [
      {{"segment": "segment name", "needs": "key needs", "pain_points": "main pain points"}}
    ],
    "primary_persona": "Description of primary target user"
  }},
  "proposed_solutions": [
    {{
      "solution_name": "Solution 1 Name",
      "description": "Detailed description",
      "user_impact": "How it helps users",
      "business_impact": "How it helps business",
      "priority": "High/Medium/Low",
      "implementation_complexity": "Low/Medium/High"
    }}
  ],
  "prioritized_recommendation": {{
    "top_solution": "Name of #1 recommended solution",
    "rationale": "Why this is the best choice",
    "success_metrics": ["metric 1", "metric 2", "metric 3"],
    "implementation_timeline": "Estimated timeline",
    "resource_requirements": "Team and resources needed"
  }},
  "tradeoffs_considered": [
    {{"tradeoff": "description", "decision": "how we handle it"}}
  ],
  "risks_and_mitigations": [
    {{"risk": "potential risk", "mitigation": "how to address it"}}
  ],
  "next_steps": ["step 1", "step 2", "step 3"]
}}

Be specific, detailed, and actionable. Use real numbers and concrete examples where possible."""

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        response_text = response.content
        
        # Extract JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        state['complete_solution'] = json.loads(response_text)
        print(f"   ✅ Solution generated")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        state['complete_solution'] = {
            "executive_summary": "Solution generation failed",
            "situation_analysis": {},
            "user_analysis": {},
            "proposed_solutions": [],
            "prioritized_recommendation": {},
            "tradeoffs_considered": [],
            "risks_and_mitigations": [],
            "next_steps": []
        }
    
    return state


def compile_result_node(state: PMCaseState) -> PMCaseState:
    """Node 5: Compile final result"""
    print("📦 Node 5: Compiling final result...")
    
    result = {
        "case_study": state['case_study'],
        "classification": state['classification'],
        "framework_recommendation": state['framework_recommendation']
    }
    
    if state.get('clarifying_questions'):
        result['clarifying_questions'] = state['clarifying_questions']['questions']
    
    if state.get('complete_solution'):
        result['complete_solution'] = state['complete_solution']
    
    state['result'] = result
    print("   ✅ Result compiled successfully")
    
    return state


# ============================================================================
# BUILD LANGGRAPH WORKFLOW
# ============================================================================

def build_pm_case_workflow() -> StateGraph:
    """Build the PM case study analysis workflow"""
    
    workflow = StateGraph(PMCaseState)
    
    # Add nodes
    workflow.add_node("classify_problem", classify_problem_node)
    workflow.add_node("generate_questions", generate_questions_node)
    workflow.add_node("recommend_framework", recommend_framework_node)
    workflow.add_node("generate_solution", generate_solution_node)
    workflow.add_node("compile_result", compile_result_node)
    
    # Define edges
    workflow.set_entry_point("classify_problem")
    workflow.add_edge("classify_problem", "generate_questions")
    workflow.add_edge("generate_questions", "recommend_framework")
    workflow.add_edge("recommend_framework", "generate_solution")
    workflow.add_edge("generate_solution", "compile_result")
    workflow.add_edge("compile_result", END)
    
    return workflow.compile()


# Compile the workflow
pm_workflow = build_pm_case_workflow()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PM Case Study Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "frameworks": "/api/frameworks",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "frameworks_loaded": len(FRAMEWORKS),
        "llm_configured": bool(os.environ.get("OPENAI_API_KEY"))
    }


@app.get("/api/frameworks")
async def get_frameworks():
    """Get all available frameworks"""
    return {
        "total_categories": len(FRAMEWORKS),
        "categories": list(FRAMEWORKS.keys()),
        "frameworks": FRAMEWORKS
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_case_study(request: CaseStudyRequest):
    """
    Analyze a PM case study using LangGraph workflow
    
    This endpoint processes a case study through multiple stages:
    1. Problem classification
    2. Clarifying questions generation (optional)
    3. Framework recommendation
    4. Complete solution generation (optional)
    """
    
    try:
        print(f"\n{'='*70}")
        print(f"🚀 Starting analysis for: {request.case_study[:50]}...")
        print(f"{'='*70}\n")
        
        # Prepare initial state
        initial_state: PMCaseState = {
            "case_study": request.case_study,
            "additional_context": request.additional_context,
            "include_clarifying_questions": request.include_clarifying_questions,
            "include_complete_solution": request.include_complete_solution,
            "classification": None,
            "clarifying_questions": None,
            "framework_recommendation": None,
            "complete_solution": None,
            "result": None,
            "error": None
        }
        
        # Run the workflow
        final_state = pm_workflow.invoke(initial_state)
        
        if final_state.get('error'):
            raise HTTPException(status_code=500, detail=final_state['error'])
        
        result = final_state['result']
        
        print(f"\n{'='*70}")
        print(f"✅ Analysis completed successfully")
        print(f"{'='*70}\n")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workflow/graph")
async def get_workflow_graph():
    """Get the workflow graph structure"""
    return {
        "nodes": [
            "classify_problem",
            "generate_questions",
            "recommend_framework",
            "generate_solution",
            "compile_result"
        ],
        "edges": [
            {"from": "START", "to": "classify_problem"},
            {"from": "classify_problem", "to": "generate_questions"},
            {"from": "generate_questions", "to": "recommend_framework"},
            {"from": "recommend_framework", "to": "generate_solution"},
            {"from": "generate_solution", "to": "compile_result"},
            {"from": "compile_result", "to": "END"}
        ]
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("  🎯 PM CASE STUDY ANALYZER API")
    print("  Powered by LangGraph + FastAPI")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)