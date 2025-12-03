"""
API Routes for Interview Tracking System
Endpoints for interviews, questions, companies, roles, and skills
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional
from datetime import datetime

from framework import get_db
from models import (
    Interview, Question, Company, Role, Skill,
    InterviewRound, InterviewQuestion, InterviewSkill,
    QuestionSkill
)
from schemas import (
    InterviewCreate, InterviewUpdate, InterviewResponse, InterviewListResponse,
    QuestionCreate, QuestionUpdate, QuestionResponse, QuestionListResponse,
    CompanyCreate, CompanyResponse,
    RoleCreate, RoleResponse,
    SkillCreate, SkillResponse,
    InterviewRoundCreate, InterviewRoundResponse,
    InterviewQuestionCreate, InterviewQuestionResponse
)


# ============================================================================
# ROUTER INITIALIZATION
# ============================================================================

router = APIRouter(prefix="/api", tags=["Interview Tracking"])

companies_router = APIRouter(prefix="/api/companies", tags=["Companies"])
roles_router = APIRouter(prefix="/api/roles", tags=["Roles"])
skills_router = APIRouter(prefix="/api/skills", tags=["Skills"])
interviews_router = APIRouter(prefix="/api/interviews", tags=["Interviews"])
questions_router = APIRouter(prefix="/api/questions", tags=["Questions"])


# ============================================================================
# COMPANY ENDPOINTS
# ============================================================================

@companies_router.get("/", response_model=List[CompanyResponse])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all companies with optional search
    """
    query = db.query(Company)

    if search:
        search_filter = or_(
            Company.company_name.ilike(f"%{search}%"),
            Company.industry.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    companies = query.order_by(Company.company_name).offset(skip).limit(limit).all()
    return [company.as_dict() for company in companies]


@companies_router.post("/", response_model=CompanyResponse, status_code=201)
async def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new company
    """
    # Check if company already exists
    existing = db.query(Company).filter(Company.company_name == company.company_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company with this name already exists")

    db_company = Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company.as_dict()


@companies_router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific company by ID
    """
    company = db.query(Company).filter(Company.company_id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company.as_dict()


# ============================================================================
# ROLE ENDPOINTS
# ============================================================================

@roles_router.get("/", response_model=List[RoleResponse])
async def list_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all roles with optional filtering
    """
    query = db.query(Role)

    if search:
        search_filter = or_(
            Role.role_name.ilike(f"%{search}%"),
            Role.role_description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    if category:
        query = query.filter(Role.role_category == category)

    roles = query.order_by(Role.role_name).offset(skip).limit(limit).all()
    return [role.as_dict() for role in roles]


@roles_router.post("/", response_model=RoleResponse, status_code=201)
async def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new role
    """
    # Check if role already exists
    existing = db.query(Role).filter(Role.role_name == role.role_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role with this name already exists")

    db_role = Role(**role.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)

    return db_role.as_dict()


@roles_router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific role by ID
    """
    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    return role.as_dict()


# ============================================================================
# SKILL ENDPOINTS
# ============================================================================

@skills_router.get("/", response_model=List[SkillResponse])
async def list_skills(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    is_trending: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    List all skills with optional filtering
    """
    query = db.query(Skill).filter(Skill.is_active == True)

    if search:
        search_filter = or_(
            Skill.skill_name.ilike(f"%{search}%"),
            Skill.skill_description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    if category:
        query = query.filter(Skill.skill_category == category)

    if is_trending is not None:
        query = query.filter(Skill.is_trending == is_trending)

    skills = query.order_by(Skill.skill_name).offset(skip).limit(limit).all()
    return [skill.as_dict() for skill in skills]


@skills_router.post("/", response_model=SkillResponse, status_code=201)
async def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new skill
    """
    # Check if skill already exists
    existing = db.query(Skill).filter(Skill.skill_name == skill.skill_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill with this name already exists")

    db_skill = Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)

    return db_skill.as_dict()


@skills_router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(
    skill_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific skill by ID
    """
    skill = db.query(Skill).filter(Skill.skill_id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    return skill.as_dict()


# ============================================================================
# INTERVIEW ENDPOINTS
# ============================================================================

@interviews_router.get("/", response_model=InterviewListResponse)
async def list_interviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    company_id: Optional[int] = None,
    role_id: Optional[int] = None,
    interview_type: Optional[str] = None,
    interview_status: Optional[str] = None,
    interview_result: Optional[str] = None,
    seniority_level: Optional[str] = None,
    is_remote: Optional[bool] = None,
    sort_by: str = Query("created_at", regex="^(created_at|application_date|first_interview_date|company_name|interview_status)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    List all interviews with filtering, sorting, and pagination

    Filters:
    - company_id: Filter by company
    - role_id: Filter by role
    - interview_type: Filter by type (actual, mock, practice)
    - interview_status: Filter by status (scheduled, in_progress, completed, etc.)
    - interview_result: Filter by result (pending, passed, failed, etc.)
    - seniority_level: Filter by seniority
    - is_remote: Filter by remote/onsite

    Sorting:
    - sort_by: Field to sort by (created_at, application_date, first_interview_date, company_name, interview_status)
    - order: Sort order (asc, desc)
    """
    query = db.query(Interview).options(
        joinedload(Interview.company),
        joinedload(Interview.role)
    )

    # Apply filters
    if company_id:
        query = query.filter(Interview.company_id == company_id)
    if role_id:
        query = query.filter(Interview.role_id == role_id)
    if interview_type:
        query = query.filter(Interview.interview_type == interview_type)
    if interview_status:
        query = query.filter(Interview.interview_status == interview_status)
    if interview_result:
        query = query.filter(Interview.interview_result == interview_result)
    if seniority_level:
        query = query.filter(Interview.seniority_level == seniority_level)
    if is_remote is not None:
        query = query.filter(Interview.is_remote == is_remote)

    # Apply sorting
    if sort_by == "company_name":
        sort_column = Company.company_name
        query = query.join(Company, Interview.company_id == Company.company_id, isouter=True)
    else:
        sort_column = getattr(Interview, sort_by)

    if order == "desc":
        sort_column = desc(sort_column)

    query = query.order_by(sort_column)

    # Get total count
    total = query.count()

    # Apply pagination
    interviews = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [interview.as_dict() for interview in interviews]
    }


@interviews_router.post("/", response_model=InterviewResponse, status_code=201)
async def create_interview(
    interview: InterviewCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new interview

    Required fields:
    - seniority_level: intern, junior, mid, senior, staff, principal, lead, manager, director

    Optional fields:
    - company_id: Link to existing company
    - role_id: Link to existing role
    - custom_role_title: Custom role title if not using role_id
    - interview_type: actual (default), mock, practice
    - interview_status: scheduled (default), in_progress, completed, cancelled, rescheduled
    - Many other fields for detailed tracking
    """
    # Validate company exists if provided
    if interview.company_id:
        company = db.query(Company).filter(Company.company_id == interview.company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail=f"Company with ID {interview.company_id} not found")

    # Validate role exists if provided
    if interview.role_id:
        role = db.query(Role).filter(Role.role_id == interview.role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail=f"Role with ID {interview.role_id} not found")

    # Create interview
    db_interview = Interview(**interview.model_dump())
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)

    # Load relationships
    db.refresh(db_interview)
    db_interview = db.query(Interview).options(
        joinedload(Interview.company),
        joinedload(Interview.role)
    ).filter(Interview.interview_id == db_interview.interview_id).first()

    return db_interview.as_dict()


@interviews_router.get("/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific interview by ID with all related data
    """
    interview = db.query(Interview).options(
        joinedload(Interview.company),
        joinedload(Interview.role),
        joinedload(Interview.rounds),
        joinedload(Interview.interview_skills),
        joinedload(Interview.interview_questions)
    ).filter(Interview.interview_id == interview_id).first()

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    return interview.as_dict()


@interviews_router.put("/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: int,
    interview: InterviewUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing interview
    """
    db_interview = db.query(Interview).filter(Interview.interview_id == interview_id).first()
    if not db_interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Validate company exists if provided
    if interview.company_id:
        company = db.query(Company).filter(Company.company_id == interview.company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail=f"Company with ID {interview.company_id} not found")

    # Validate role exists if provided
    if interview.role_id:
        role = db.query(Role).filter(Role.role_id == interview.role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail=f"Role with ID {interview.role_id} not found")

    # Update fields
    update_data = interview.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_interview, field, value)

    db_interview.updated_at = datetime.now()
    db.commit()
    db.refresh(db_interview)

    # Load relationships
    db_interview = db.query(Interview).options(
        joinedload(Interview.company),
        joinedload(Interview.role)
    ).filter(Interview.interview_id == interview_id).first()

    return db_interview.as_dict()


@interviews_router.delete("/{interview_id}", status_code=204)
async def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an interview (soft delete by setting status to cancelled)
    """
    db_interview = db.query(Interview).filter(Interview.interview_id == interview_id).first()
    if not db_interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Soft delete - set status to cancelled
    db_interview.interview_status = 'cancelled'
    db.commit()

    return None


@interviews_router.get("/{interview_id}/rounds", response_model=List[InterviewRoundResponse])
async def get_interview_rounds(
    interview_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all rounds for a specific interview
    """
    interview = db.query(Interview).filter(Interview.interview_id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    rounds = db.query(InterviewRound).filter(
        InterviewRound.interview_id == interview_id
    ).order_by(InterviewRound.round_number).all()

    return [round.as_dict() for round in rounds]


@interviews_router.post("/{interview_id}/rounds", response_model=InterviewRoundResponse, status_code=201)
async def create_interview_round(
    interview_id: int,
    round: InterviewRoundCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new round for an interview
    """
    # Verify interview exists
    interview = db.query(Interview).filter(Interview.interview_id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Override interview_id from path
    round_data = round.model_dump()
    round_data['interview_id'] = interview_id

    db_round = InterviewRound(**round_data)
    db.add(db_round)
    db.commit()
    db.refresh(db_round)

    return db_round.as_dict()


# ============================================================================
# QUESTION ENDPOINTS
# ============================================================================

@questions_router.get("/", response_model=QuestionListResponse)
async def list_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    is_active: bool = True,
    sort_by: str = Query("created_at", regex="^(created_at|times_asked|times_practiced|average_rating|question_difficulty)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    List all questions with filtering, sorting, and pagination

    Filters:
    - category: technical, behavioral, product, system_design, coding, etc.
    - difficulty: easy, medium, hard, expert
    - search: Search in question text and context
    - tags: Filter by tags (can specify multiple)
    - is_active: Show only active questions (default: true)

    Sorting:
    - sort_by: Field to sort by (created_at, times_asked, times_practiced, average_rating, question_difficulty)
    - order: Sort order (asc, desc)
    """
    query = db.query(Question)

    # Apply filters
    query = query.filter(Question.is_active == is_active)

    if category:
        query = query.filter(Question.question_category == category)

    if difficulty:
        query = query.filter(Question.question_difficulty == difficulty)

    if search:
        search_filter = or_(
            Question.question_text.ilike(f"%{search}%"),
            Question.question_context.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    if tags:
        # Filter questions that contain any of the specified tags
        for tag in tags:
            query = query.filter(Question.tags.any(tag))

    # Apply sorting
    sort_column = getattr(Question, sort_by)
    if order == "desc":
        sort_column = desc(sort_column)

    query = query.order_by(sort_column)

    # Get total count
    total = query.count()

    # Apply pagination
    questions = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [question.as_dict() for question in questions]
    }


@questions_router.post("/", response_model=QuestionResponse, status_code=201)
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new question

    Required fields:
    - question_text: The question text (minimum 10 characters)
    - question_category: technical, behavioral, product, system_design, coding, case_study, brainteaser, cultural_fit, leadership, other

    Optional fields:
    - question_difficulty: easy, medium (default), hard, expert
    - answer_summary: Brief summary of the answer
    - answer_markdown_content: Full answer in markdown
    - key_concepts: List of key concepts tested
    - common_mistakes: List of common mistakes
    - tips_and_tricks: List of tips for answering
    - suggested_frameworks: Frameworks to use for answering
    - approach_steps: Step-by-step approach
    - tags: Tags for categorization
    - And many more fields for comprehensive tracking
    """
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    return db_question.as_dict()


@questions_router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific question by ID with all details
    """
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question.as_dict()


@questions_router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question: QuestionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing question
    """
    db_question = db.query(Question).filter(Question.question_id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Update fields
    update_data = question.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_question, field, value)

    db_question.updated_at = datetime.now()
    db.commit()
    db.refresh(db_question)

    return db_question.as_dict()


@questions_router.delete("/{question_id}", status_code=204)
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a question (soft delete by setting is_active to false)
    """
    db_question = db.query(Question).filter(Question.question_id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Soft delete - set is_active to False
    db_question.is_active = False
    db.commit()

    return None


@questions_router.get("/category/{category}", response_model=QuestionListResponse)
async def get_questions_by_category(
    category: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all questions in a specific category
    """
    query = db.query(Question).filter(
        and_(
            Question.question_category == category,
            Question.is_active == True
        )
    )

    if difficulty:
        query = query.filter(Question.question_difficulty == difficulty)

    total = query.count()
    questions = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [question.as_dict() for question in questions]
    }


# ============================================================================
# INTERVIEW-QUESTION LINKING ENDPOINTS
# ============================================================================

@interviews_router.post("/{interview_id}/questions", response_model=InterviewQuestionResponse, status_code=201)
async def link_question_to_interview(
    interview_id: int,
    interview_question: InterviewQuestionCreate,
    db: Session = Depends(get_db)
):
    """
    Link a question to an interview (record that a question was asked in an interview)
    """
    # Verify interview exists
    interview = db.query(Interview).filter(Interview.interview_id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Verify question exists
    question = db.query(Question).filter(Question.question_id == interview_question.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Verify round exists if provided
    if interview_question.round_id:
        round = db.query(InterviewRound).filter(InterviewRound.round_id == interview_question.round_id).first()
        if not round:
            raise HTTPException(status_code=404, detail="Round not found")

    # Override interview_id from path
    question_data = interview_question.model_dump()
    question_data['interview_id'] = interview_id

    db_interview_question = InterviewQuestion(**question_data)
    db.add(db_interview_question)

    # Increment times_asked counter
    question.times_asked = (question.times_asked or 0) + 1

    db.commit()
    db.refresh(db_interview_question)

    return db_interview_question.as_dict()


@interviews_router.get("/{interview_id}/questions", response_model=List[InterviewQuestionResponse])
async def get_interview_questions(
    interview_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all questions asked in a specific interview
    """
    interview = db.query(Interview).filter(Interview.interview_id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    interview_questions = db.query(InterviewQuestion).filter(
        InterviewQuestion.interview_id == interview_id
    ).order_by(InterviewQuestion.order_asked).all()

    return [iq.as_dict() for iq in interview_questions]


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@router.get("/stats/overview")
async def get_overview_statistics(db: Session = Depends(get_db)):
    """
    Get overall statistics for the interview tracking system
    """
    total_interviews = db.query(func.count(Interview.interview_id)).scalar()
    total_questions = db.query(func.count(Question.question_id)).filter(Question.is_active == True).scalar()
    total_companies = db.query(func.count(Company.company_id)).scalar()

    interviews_by_status = db.query(
        Interview.interview_status,
        func.count(Interview.interview_id)
    ).group_by(Interview.interview_status).all()

    interviews_by_result = db.query(
        Interview.interview_result,
        func.count(Interview.interview_id)
    ).group_by(Interview.interview_result).all()

    questions_by_category = db.query(
        Question.question_category,
        func.count(Question.question_id)
    ).filter(Question.is_active == True).group_by(Question.question_category).all()

    questions_by_difficulty = db.query(
        Question.question_difficulty,
        func.count(Question.question_id)
    ).filter(Question.is_active == True).group_by(Question.question_difficulty).all()

    return {
        "total_interviews": total_interviews,
        "total_questions": total_questions,
        "total_companies": total_companies,
        "interviews_by_status": {status: count for status, count in interviews_by_status},
        "interviews_by_result": {result: count for result, count in interviews_by_result},
        "questions_by_category": {category: count for category, count in questions_by_category},
        "questions_by_difficulty": {difficulty: count for difficulty, count in questions_by_difficulty}
    }
