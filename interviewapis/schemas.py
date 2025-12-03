"""
Pydantic schemas for Interview Tracking System
Request and Response models for API validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime, time
from decimal import Decimal


# ============================================================================
# COMPANY SCHEMAS
# ============================================================================

class CompanyCreate(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=200)
    industry: Optional[str] = Field(None, max_length=100)
    company_size: Optional[str] = Field(None, max_length=50)
    headquarters: Optional[str] = Field(None, max_length=200)
    website: Optional[str] = Field(None, max_length=500)
    company_description: Optional[str] = None


class CompanyResponse(BaseModel):
    company_id: int
    company_name: str
    industry: Optional[str] = None
    company_size: Optional[str] = None
    headquarters: Optional[str] = None
    website: Optional[str] = None
    company_description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# ROLE SCHEMAS
# ============================================================================

class RoleCreate(BaseModel):
    role_name: str = Field(..., min_length=1, max_length=200)
    role_category: Optional[str] = Field(None, max_length=100)
    role_description: Optional[str] = None
    typical_skills: Optional[List[str]] = None


class RoleResponse(BaseModel):
    role_id: int
    role_name: str
    role_category: Optional[str] = None
    role_description: Optional[str] = None
    typical_skills: Optional[List[str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# SKILL SCHEMAS
# ============================================================================

class SkillCreate(BaseModel):
    skill_name: str = Field(..., min_length=1, max_length=200)
    skill_category: Optional[str] = Field(None, max_length=100)
    skill_type: Optional[str] = Field(None, max_length=100)
    skill_description: Optional[str] = None
    proficiency_levels: Optional[List[str]] = None
    is_trending: Optional[bool] = False
    market_demand: Optional[str] = None


class SkillResponse(BaseModel):
    skill_id: int
    skill_name: str
    skill_category: Optional[str] = None
    skill_type: Optional[str] = None
    skill_description: Optional[str] = None
    proficiency_levels: Optional[List[str]] = None
    is_trending: Optional[bool] = False
    market_demand: Optional[str] = None
    is_active: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# INTERVIEW SCHEMAS
# ============================================================================

class InterviewCreate(BaseModel):
    company_id: Optional[int] = None
    role_id: Optional[int] = None
    custom_role_title: Optional[str] = Field(None, max_length=200)
    interview_type: str = Field(default='actual', pattern='^(actual|mock|practice)$')
    seniority_level: str = Field(..., pattern='^(intern|junior|mid|senior|staff|principal|lead|manager|director)$')
    interview_status: Optional[str] = Field(default='scheduled', pattern='^(scheduled|in_progress|completed|cancelled|rescheduled)$')
    interview_result: Optional[str] = Field(default='pending', pattern='^(pending|passed|failed|offer_received|offer_accepted|offer_declined)$')
    job_description: Optional[str] = None
    main_skills_required: Optional[List[str]] = None
    required_experience_years: Optional[int] = Field(None, ge=0, le=50)
    job_location: Optional[str] = Field(None, max_length=200)
    is_remote: Optional[bool] = False
    salary_range: Optional[str] = Field(None, max_length=100)
    application_date: Optional[date] = None
    job_posting_url: Optional[str] = Field(None, max_length=500)
    referral_source: Optional[str] = Field(None, max_length=200)
    first_interview_date: Optional[date] = None
    final_interview_date: Optional[date] = None
    offer_date: Optional[date] = None
    offer_deadline: Optional[date] = None
    overall_feedback: Optional[str] = None
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    offer_details: Optional[str] = None
    preparation_notes: Optional[str] = None
    resources_used: Optional[str] = None
    time_spent_preparing_hours: Optional[float] = Field(None, ge=0)
    cv_content: Optional[str] = None
    cv_file_path: Optional[str] = Field(None, max_length=500)
    cv_file_url: Optional[str] = Field(None, max_length=500)
    cv_version: Optional[str] = Field(None, max_length=50)
    cv_tailored_for_role: Optional[bool] = False
    cv_highlights: Optional[List[str]] = None
    created_by: Optional[str] = Field(None, max_length=100)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "company_id": 1,
                "role_id": 1,
                "custom_role_title": "Senior Software Engineer",
                "interview_type": "actual",
                "seniority_level": "senior",
                "interview_status": "scheduled",
                "job_description": "Looking for a senior engineer with 5+ years experience",
                "main_skills_required": ["Python", "JavaScript", "AWS"],
                "required_experience_years": 5,
                "job_location": "San Francisco, CA",
                "is_remote": True,
                "salary_range": "$150k - $200k",
                "application_date": "2024-12-01"
            }
        }
    )


class InterviewUpdate(BaseModel):
    company_id: Optional[int] = None
    role_id: Optional[int] = None
    custom_role_title: Optional[str] = Field(None, max_length=200)
    interview_type: Optional[str] = Field(None, pattern='^(actual|mock|practice)$')
    seniority_level: Optional[str] = Field(None, pattern='^(intern|junior|mid|senior|staff|principal|lead|manager|director)$')
    interview_status: Optional[str] = Field(None, pattern='^(scheduled|in_progress|completed|cancelled|rescheduled)$')
    interview_result: Optional[str] = Field(None, pattern='^(pending|passed|failed|offer_received|offer_accepted|offer_declined)$')
    job_description: Optional[str] = None
    main_skills_required: Optional[List[str]] = None
    required_experience_years: Optional[int] = Field(None, ge=0, le=50)
    job_location: Optional[str] = Field(None, max_length=200)
    is_remote: Optional[bool] = None
    salary_range: Optional[str] = Field(None, max_length=100)
    application_date: Optional[date] = None
    job_posting_url: Optional[str] = Field(None, max_length=500)
    referral_source: Optional[str] = Field(None, max_length=200)
    first_interview_date: Optional[date] = None
    final_interview_date: Optional[date] = None
    offer_date: Optional[date] = None
    offer_deadline: Optional[date] = None
    overall_feedback: Optional[str] = None
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    offer_details: Optional[str] = None
    preparation_notes: Optional[str] = None
    resources_used: Optional[str] = None
    time_spent_preparing_hours: Optional[float] = Field(None, ge=0)


class InterviewResponse(BaseModel):
    interview_id: int
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    role_id: Optional[int] = None
    role_name: Optional[str] = None
    custom_role_title: Optional[str] = None
    interview_type: str
    seniority_level: str
    interview_status: str
    interview_result: str
    job_description: Optional[str] = None
    main_skills_required: Optional[List[str]] = None
    required_experience_years: Optional[int] = None
    job_location: Optional[str] = None
    is_remote: Optional[bool] = None
    salary_range: Optional[str] = None
    application_date: Optional[str] = None
    job_posting_url: Optional[str] = None
    referral_source: Optional[str] = None
    first_interview_date: Optional[str] = None
    final_interview_date: Optional[str] = None
    offer_date: Optional[str] = None
    offer_deadline: Optional[str] = None
    overall_feedback: Optional[str] = None
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    offer_details: Optional[str] = None
    preparation_notes: Optional[str] = None
    resources_used: Optional[str] = None
    time_spent_preparing_hours: Optional[float] = None
    cv_version: Optional[str] = None
    cv_tailored_for_role: Optional[bool] = None
    cv_highlights: Optional[List[str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    created_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class InterviewListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[InterviewResponse]


# ============================================================================
# INTERVIEW ROUND SCHEMAS
# ============================================================================

class InterviewRoundCreate(BaseModel):
    interview_id: int
    round_number: int = Field(..., ge=1)
    round_name: Optional[str] = Field(None, max_length=200)
    round_type: str = Field(..., pattern='^(phone_screen|technical|coding|system_design|behavioral|cultural_fit|hiring_manager|final|assessment|other)$')
    scheduled_date: Optional[date] = None
    scheduled_time: Optional[time] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    timezone: Optional[str] = Field(default='UTC', max_length=50)
    is_virtual: Optional[bool] = True
    meeting_platform: Optional[str] = Field(None, max_length=100)
    meeting_link: Optional[str] = Field(None, max_length=500)
    physical_location: Optional[str] = Field(None, max_length=500)
    interviewer_name: Optional[str] = Field(None, max_length=200)
    interviewer_title: Optional[str] = Field(None, max_length=200)
    interviewer_linkedin_url: Optional[str] = Field(None, max_length=500)
    interviewer_email: Optional[str] = Field(None, max_length=200)
    interviewer_notes: Optional[str] = None
    round_status: Optional[str] = Field(default='scheduled', pattern='^(scheduled|in_progress|completed|cancelled|rescheduled)$')
    round_result: Optional[str] = Field(default='pending', pattern='^(pending|passed|failed|offer_received|offer_accepted|offer_declined)$')
    feedback: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=10)
    preparation_notes: Optional[str] = None
    questions_asked_summary: Optional[str] = None
    key_topics_covered: Optional[List[str]] = None
    follow_up_actions: Optional[str] = None


class InterviewRoundResponse(BaseModel):
    round_id: int
    interview_id: int
    round_number: int
    round_name: Optional[str] = None
    round_type: str
    scheduled_date: Optional[str] = None
    scheduled_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    is_virtual: Optional[bool] = None
    meeting_platform: Optional[str] = None
    interviewer_name: Optional[str] = None
    interviewer_title: Optional[str] = None
    round_status: str
    round_result: str
    feedback: Optional[str] = None
    rating: Optional[int] = None
    key_topics_covered: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# QUESTION SCHEMAS
# ============================================================================

class QuestionCreate(BaseModel):
    question_text: str = Field(..., min_length=10)
    question_category: str = Field(..., pattern='^(technical|behavioral|product|system_design|coding|case_study|brainteaser|cultural_fit|leadership|other)$')
    question_difficulty: Optional[str] = Field(default='medium', pattern='^(easy|medium|hard|expert)$')
    question_context: Optional[str] = None
    assumptions: Optional[str] = None
    answer_markdown_link: Optional[str] = Field(None, max_length=500)
    answer_summary: Optional[str] = None
    answer_markdown_content: Optional[str] = None
    reference_image_urls: Optional[List[str]] = None
    diagram_url: Optional[str] = Field(None, max_length=500)
    video_explanation_url: Optional[str] = Field(None, max_length=500)
    follow_up_questions: Optional[List[str]] = None
    related_questions: Optional[List[int]] = None
    prerequisites: Optional[List[str]] = None
    additional_information: Optional[str] = None
    key_concepts: Optional[List[str]] = None
    common_mistakes: Optional[List[str]] = None
    tips_and_tricks: Optional[List[str]] = None
    time_to_answer_minutes: Optional[int] = Field(None, ge=0)
    suggested_frameworks: Optional[List[str]] = None
    approach_steps: Optional[List[str]] = None
    source: Optional[str] = Field(None, max_length=200)
    source_url: Optional[str] = Field(None, max_length=500)
    author: Optional[str] = Field(None, max_length=200)
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = True
    created_by: Optional[str] = Field(None, max_length=100)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question_text": "How would you design a URL shortening service like bit.ly?",
                "question_category": "system_design",
                "question_difficulty": "medium",
                "question_context": "System design interview question",
                "answer_summary": "Design should include URL generation, storage, redirection, and analytics",
                "key_concepts": ["Hashing", "Database Design", "Caching", "Load Balancing"],
                "common_mistakes": ["Not considering collision handling", "Ignoring scalability"],
                "tips_and_tricks": ["Use base62 encoding", "Consider Redis for caching"],
                "time_to_answer_minutes": 45,
                "tags": ["system_design", "scalability", "distributed_systems"]
            }
        }
    )


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = Field(None, min_length=10)
    question_category: Optional[str] = Field(None, pattern='^(technical|behavioral|product|system_design|coding|case_study|brainteaser|cultural_fit|leadership|other)$')
    question_difficulty: Optional[str] = Field(None, pattern='^(easy|medium|hard|expert)$')
    question_context: Optional[str] = None
    assumptions: Optional[str] = None
    answer_markdown_link: Optional[str] = Field(None, max_length=500)
    answer_summary: Optional[str] = None
    answer_markdown_content: Optional[str] = None
    reference_image_urls: Optional[List[str]] = None
    diagram_url: Optional[str] = Field(None, max_length=500)
    video_explanation_url: Optional[str] = Field(None, max_length=500)
    follow_up_questions: Optional[List[str]] = None
    related_questions: Optional[List[int]] = None
    prerequisites: Optional[List[str]] = None
    additional_information: Optional[str] = None
    key_concepts: Optional[List[str]] = None
    common_mistakes: Optional[List[str]] = None
    tips_and_tricks: Optional[List[str]] = None
    time_to_answer_minutes: Optional[int] = Field(None, ge=0)
    suggested_frameworks: Optional[List[str]] = None
    approach_steps: Optional[List[str]] = None
    source: Optional[str] = Field(None, max_length=200)
    source_url: Optional[str] = Field(None, max_length=500)
    author: Optional[str] = Field(None, max_length=200)
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class QuestionResponse(BaseModel):
    question_id: int
    question_text: str
    question_category: str
    question_difficulty: str
    question_context: Optional[str] = None
    assumptions: Optional[str] = None
    answer_summary: Optional[str] = None
    answer_markdown_content: Optional[str] = None
    reference_image_urls: Optional[List[str]] = None
    diagram_url: Optional[str] = None
    video_explanation_url: Optional[str] = None
    follow_up_questions: Optional[List[str]] = None
    related_questions: Optional[List[int]] = None
    prerequisites: Optional[List[str]] = None
    key_concepts: Optional[List[str]] = None
    common_mistakes: Optional[List[str]] = None
    tips_and_tricks: Optional[List[str]] = None
    time_to_answer_minutes: Optional[int] = None
    suggested_frameworks: Optional[List[str]] = None
    approach_steps: Optional[List[str]] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    author: Optional[str] = None
    times_asked: Optional[int] = None
    times_practiced: Optional[int] = None
    average_rating: Optional[float] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    created_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class QuestionListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[QuestionResponse]


# ============================================================================
# INTERVIEW QUESTION (JUNCTION) SCHEMAS
# ============================================================================

class InterviewQuestionCreate(BaseModel):
    interview_id: int
    round_id: Optional[int] = None
    question_id: int
    was_asked: Optional[bool] = True
    order_asked: Optional[int] = None
    candidate_answer: Optional[str] = None
    answer_quality_rating: Optional[int] = Field(None, ge=1, le=10)
    time_taken_minutes: Optional[int] = Field(None, ge=0)
    interviewer_feedback: Optional[str] = None
    what_went_well: Optional[str] = None
    what_could_improve: Optional[str] = None
    was_prepared: Optional[bool] = False
    preparation_notes: Optional[str] = None
    confidence_level: Optional[int] = Field(None, ge=1, le=10)
    follow_up_questions_asked: Optional[List[str]] = None
    follow_up_answers: Optional[List[str]] = None


class InterviewQuestionResponse(BaseModel):
    interview_question_id: int
    interview_id: int
    round_id: Optional[int] = None
    question_id: int
    was_asked: bool
    order_asked: Optional[int] = None
    candidate_answer: Optional[str] = None
    answer_quality_rating: Optional[int] = None
    time_taken_minutes: Optional[int] = None
    interviewer_feedback: Optional[str] = None
    what_went_well: Optional[str] = None
    what_could_improve: Optional[str] = None
    was_prepared: bool
    confidence_level: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
