"""
Database models for Interview Tracking System
Aligned with the interview_schema PostgreSQL database
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, Time, Numeric, ForeignKey, ARRAY
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime, timezone

Base = declarative_base()

def get_utc_now():
    """Helper function to get current UTC datetime"""
    return datetime.now(timezone.utc)


# Enum types
interview_type_enum = ENUM(
    'actual', 'mock', 'practice',
    name='interview_type_enum',
    schema='interview_schema'
)

seniority_level_enum = ENUM(
    'intern', 'junior', 'mid', 'senior', 'staff', 'principal', 'lead', 'manager', 'director',
    name='seniority_level_enum',
    schema='interview_schema'
)

interview_status_enum = ENUM(
    'scheduled', 'in_progress', 'completed', 'cancelled', 'rescheduled',
    name='interview_status_enum',
    schema='interview_schema'
)

interview_result_enum = ENUM(
    'pending', 'passed', 'failed', 'offer_received', 'offer_accepted', 'offer_declined',
    name='interview_result_enum',
    schema='interview_schema'
)

interview_round_type_enum = ENUM(
    'phone_screen', 'technical', 'coding', 'system_design', 'behavioral',
    'cultural_fit', 'hiring_manager', 'final', 'assessment', 'other',
    name='interview_round_type_enum',
    schema='interview_schema'
)

question_category_enum = ENUM(
    'technical', 'behavioral', 'product', 'system_design', 'coding',
    'case_study', 'brainteaser', 'cultural_fit', 'leadership', 'other',
    name='question_category_enum',
    schema='interview_schema'
)

question_difficulty_enum = ENUM(
    'easy', 'medium', 'hard', 'expert',
    name='question_difficulty_enum',
    schema='interview_schema'
)


class Company(Base):
    """Companies where interviews are conducted"""
    __tablename__ = 'companies'
    __table_args__ = {'schema': 'interview_schema'}

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(200), nullable=False, unique=True)
    industry = Column(String(100))
    company_size = Column(String(50))
    headquarters = Column(String(200))
    website = Column(String(500))
    company_description = Column(Text)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    # Relationships
    interviews = relationship("Interview", back_populates="company")

    def as_dict(self):
        return {
            'company_id': self.company_id,
            'company_name': self.company_name,
            'industry': self.industry,
            'company_size': self.company_size,
            'headquarters': self.headquarters,
            'website': self.website,
            'company_description': self.company_description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Role(Base):
    """Reference table for job roles"""
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'interview_schema'}

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(200), nullable=False, unique=True)
    role_category = Column(String(100))
    role_description = Column(Text)
    typical_skills = Column(ARRAY(Text))
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    # Relationships
    interviews = relationship("Interview", back_populates="role")

    def as_dict(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'role_category': self.role_category,
            'role_description': self.role_description,
            'typical_skills': self.typical_skills,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Skill(Base):
    """Master table of all skills tracked in the system"""
    __tablename__ = 'skills'
    __table_args__ = {'schema': 'interview_schema'}

    skill_id = Column(Integer, primary_key=True, autoincrement=True)
    skill_name = Column(String(200), nullable=False, unique=True)
    skill_category = Column(String(100))
    skill_type = Column(String(100))
    skill_description = Column(Text)
    proficiency_levels = Column(ARRAY(Text))
    related_skills = Column(ARRAY(Integer))
    parent_skill_id = Column(Integer, ForeignKey('interview_schema.skills.skill_id'))
    is_trending = Column(Boolean, default=False)
    market_demand = Column(String(20))
    average_salary_impact_percentage = Column(Numeric(5, 2))
    learning_resources = Column(ARRAY(Text))
    official_documentation_url = Column(String(500))
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    is_active = Column(Boolean, default=True)

    def as_dict(self):
        return {
            'skill_id': self.skill_id,
            'skill_name': self.skill_name,
            'skill_category': self.skill_category,
            'skill_type': self.skill_type,
            'skill_description': self.skill_description,
            'proficiency_levels': self.proficiency_levels,
            'is_trending': self.is_trending,
            'market_demand': self.market_demand,
            'is_active': self.is_active
        }


class Interview(Base):
    """Main interviews tracking table"""
    __tablename__ = 'interviews'
    __table_args__ = {'schema': 'interview_schema'}

    interview_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('interview_schema.companies.company_id'))
    role_id = Column(Integer, ForeignKey('interview_schema.roles.role_id'))
    custom_role_title = Column(String(200))
    interview_type = Column(interview_type_enum, nullable=False, default='actual')
    seniority_level = Column(seniority_level_enum, nullable=False)
    interview_status = Column(interview_status_enum, default='scheduled')
    interview_result = Column(interview_result_enum, default='pending')
    job_description = Column(Text)
    main_skills_required = Column(ARRAY(Text))
    required_experience_years = Column(Integer)
    job_location = Column(String(200))
    is_remote = Column(Boolean, default=False)
    salary_range = Column(String(100))
    application_date = Column(Date)
    job_posting_url = Column(String(500))
    referral_source = Column(String(200))
    first_interview_date = Column(Date)
    final_interview_date = Column(Date)
    offer_date = Column(Date)
    offer_deadline = Column(Date)
    overall_feedback = Column(Text)
    strengths = Column(Text)
    areas_for_improvement = Column(Text)
    offer_details = Column(Text)
    preparation_notes = Column(Text)
    resources_used = Column(Text)
    time_spent_preparing_hours = Column(Numeric(5, 2))
    cv_content = Column(Text)
    cv_file_path = Column(String(500))
    cv_file_url = Column(String(500))
    cv_version = Column(String(50))
    cv_tailored_for_role = Column(Boolean, default=False)
    cv_highlights = Column(ARRAY(Text))
    cv_uploaded_at = Column(DateTime)
    cv_last_updated = Column(DateTime)
    cv_version_id = Column(Integer)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    created_by = Column(String(100))

    # Relationships
    company = relationship("Company", back_populates="interviews")
    role = relationship("Role", back_populates="interviews")
    rounds = relationship("InterviewRound", back_populates="interview", cascade="all, delete-orphan")
    interview_skills = relationship("InterviewSkill", back_populates="interview", cascade="all, delete-orphan")
    interview_questions = relationship("InterviewQuestion", back_populates="interview", cascade="all, delete-orphan")

    def as_dict(self):
        return {
            'interview_id': self.interview_id,
            'company_id': self.company_id,
            'company_name': self.company.company_name if self.company else None,
            'role_id': self.role_id,
            'role_name': self.role.role_name if self.role else None,
            'custom_role_title': self.custom_role_title,
            'interview_type': self.interview_type,
            'seniority_level': self.seniority_level,
            'interview_status': self.interview_status,
            'interview_result': self.interview_result,
            'job_description': self.job_description,
            'main_skills_required': self.main_skills_required,
            'required_experience_years': self.required_experience_years,
            'job_location': self.job_location,
            'is_remote': self.is_remote,
            'salary_range': self.salary_range,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'job_posting_url': self.job_posting_url,
            'referral_source': self.referral_source,
            'first_interview_date': self.first_interview_date.isoformat() if self.first_interview_date else None,
            'final_interview_date': self.final_interview_date.isoformat() if self.final_interview_date else None,
            'offer_date': self.offer_date.isoformat() if self.offer_date else None,
            'offer_deadline': self.offer_deadline.isoformat() if self.offer_deadline else None,
            'overall_feedback': self.overall_feedback,
            'strengths': self.strengths,
            'areas_for_improvement': self.areas_for_improvement,
            'offer_details': self.offer_details,
            'preparation_notes': self.preparation_notes,
            'resources_used': self.resources_used,
            'time_spent_preparing_hours': float(self.time_spent_preparing_hours) if self.time_spent_preparing_hours else None,
            'cv_version': self.cv_version,
            'cv_tailored_for_role': self.cv_tailored_for_role,
            'cv_highlights': self.cv_highlights,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }


class InterviewRound(Base):
    """Individual rounds within interviews"""
    __tablename__ = 'interview_rounds'
    __table_args__ = {'schema': 'interview_schema'}

    round_id = Column(Integer, primary_key=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey('interview_schema.interviews.interview_id'), nullable=False)
    round_number = Column(Integer, nullable=False)
    round_name = Column(String(200))
    round_type = Column(interview_round_type_enum, nullable=False)
    scheduled_date = Column(Date)
    scheduled_time = Column(Time)
    duration_minutes = Column(Integer)
    timezone = Column(String(50), default='UTC')
    is_virtual = Column(Boolean, default=True)
    meeting_platform = Column(String(100))
    meeting_link = Column(String(500))
    physical_location = Column(String(500))
    interviewer_name = Column(String(200))
    interviewer_title = Column(String(200))
    interviewer_linkedin_url = Column(String(500))
    interviewer_email = Column(String(200))
    interviewer_notes = Column(Text)
    round_status = Column(interview_status_enum, default='scheduled')
    round_result = Column(interview_result_enum, default='pending')
    feedback = Column(Text)
    rating = Column(Integer)
    preparation_notes = Column(Text)
    questions_asked_summary = Column(Text)
    key_topics_covered = Column(ARRAY(Text))
    follow_up_actions = Column(Text)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    # Relationships
    interview = relationship("Interview", back_populates="rounds")
    interview_questions = relationship("InterviewQuestion", back_populates="round", cascade="all, delete-orphan")

    def as_dict(self):
        return {
            'round_id': self.round_id,
            'interview_id': self.interview_id,
            'round_number': self.round_number,
            'round_name': self.round_name,
            'round_type': self.round_type,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'duration_minutes': self.duration_minutes,
            'is_virtual': self.is_virtual,
            'meeting_platform': self.meeting_platform,
            'interviewer_name': self.interviewer_name,
            'interviewer_title': self.interviewer_title,
            'round_status': self.round_status,
            'round_result': self.round_result,
            'feedback': self.feedback,
            'rating': self.rating,
            'key_topics_covered': self.key_topics_covered
        }


class Question(Base):
    """Master table of interview questions"""
    __tablename__ = 'questions'
    __table_args__ = {'schema': 'interview_schema'}

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(Text, nullable=False)
    question_category = Column(question_category_enum, nullable=False)
    question_difficulty = Column(question_difficulty_enum, default='medium')
    question_context = Column(Text)
    assumptions = Column(Text)
    answer_markdown_link = Column(String(500))
    answer_summary = Column(Text)
    answer_markdown_content = Column(Text)
    reference_image_urls = Column(ARRAY(Text))
    diagram_url = Column(String(500))
    video_explanation_url = Column(String(500))
    follow_up_questions = Column(ARRAY(Text))
    related_questions = Column(ARRAY(Integer))
    prerequisites = Column(ARRAY(Text))
    additional_information = Column(Text)
    key_concepts = Column(ARRAY(Text))
    common_mistakes = Column(ARRAY(Text))
    tips_and_tricks = Column(ARRAY(Text))
    time_to_answer_minutes = Column(Integer)
    suggested_frameworks = Column(ARRAY(Text))
    approach_steps = Column(ARRAY(Text))
    source = Column(String(200))
    source_url = Column(String(500))
    author = Column(String(200))
    times_asked = Column(Integer, default=0)
    times_practiced = Column(Integer, default=0)
    average_rating = Column(Numeric(3, 2))
    tags = Column(ARRAY(Text))
    question_embedding = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    created_by = Column(String(100))

    # Relationships
    interview_questions = relationship("InterviewQuestion", back_populates="question", cascade="all, delete-orphan")
    question_skills = relationship("QuestionSkill", back_populates="question", cascade="all, delete-orphan")

    def as_dict(self):
        return {
            'question_id': self.question_id,
            'question_text': self.question_text,
            'question_category': self.question_category,
            'question_difficulty': self.question_difficulty,
            'question_context': self.question_context,
            'assumptions': self.assumptions,
            'answer_summary': self.answer_summary,
            'answer_markdown_content': self.answer_markdown_content,
            'reference_image_urls': self.reference_image_urls,
            'diagram_url': self.diagram_url,
            'video_explanation_url': self.video_explanation_url,
            'follow_up_questions': self.follow_up_questions,
            'related_questions': self.related_questions,
            'prerequisites': self.prerequisites,
            'key_concepts': self.key_concepts,
            'common_mistakes': self.common_mistakes,
            'tips_and_tricks': self.tips_and_tricks,
            'time_to_answer_minutes': self.time_to_answer_minutes,
            'suggested_frameworks': self.suggested_frameworks,
            'approach_steps': self.approach_steps,
            'source': self.source,
            'source_url': self.source_url,
            'author': self.author,
            'times_asked': self.times_asked,
            'times_practiced': self.times_practiced,
            'average_rating': float(self.average_rating) if self.average_rating else None,
            'tags': self.tags,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }


class InterviewQuestion(Base):
    """Questions asked in specific interview rounds"""
    __tablename__ = 'interview_questions'
    __table_args__ = {'schema': 'interview_schema'}

    interview_question_id = Column(Integer, primary_key=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey('interview_schema.interviews.interview_id'))
    round_id = Column(Integer, ForeignKey('interview_schema.interview_rounds.round_id'))
    question_id = Column(Integer, ForeignKey('interview_schema.questions.question_id'))
    was_asked = Column(Boolean, default=True)
    order_asked = Column(Integer)
    candidate_answer = Column(Text)
    answer_quality_rating = Column(Integer)
    time_taken_minutes = Column(Integer)
    interviewer_feedback = Column(Text)
    what_went_well = Column(Text)
    what_could_improve = Column(Text)
    was_prepared = Column(Boolean, default=False)
    preparation_notes = Column(Text)
    confidence_level = Column(Integer)
    follow_up_questions_asked = Column(ARRAY(Text))
    follow_up_answers = Column(ARRAY(Text))
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    # Relationships
    interview = relationship("Interview", back_populates="interview_questions")
    round = relationship("InterviewRound", back_populates="interview_questions")
    question = relationship("Question", back_populates="interview_questions")

    def as_dict(self):
        return {
            'interview_question_id': self.interview_question_id,
            'interview_id': self.interview_id,
            'round_id': self.round_id,
            'question_id': self.question_id,
            'was_asked': self.was_asked,
            'order_asked': self.order_asked,
            'candidate_answer': self.candidate_answer,
            'answer_quality_rating': self.answer_quality_rating,
            'time_taken_minutes': self.time_taken_minutes,
            'interviewer_feedback': self.interviewer_feedback,
            'what_went_well': self.what_went_well,
            'what_could_improve': self.what_could_improve,
            'was_prepared': self.was_prepared,
            'confidence_level': self.confidence_level
        }


class InterviewSkill(Base):
    """Skills required and assessed in interviews"""
    __tablename__ = 'interview_skills'
    __table_args__ = {'schema': 'interview_schema'}

    interview_skill_id = Column(Integer, primary_key=True, autoincrement=True)
    interview_id = Column(Integer, ForeignKey('interview_schema.interviews.interview_id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('interview_schema.skills.skill_id'), nullable=False)
    is_required = Column(Boolean, default=True)
    is_nice_to_have = Column(Boolean, default=False)
    required_proficiency = Column(String(50))
    priority_level = Column(String(20))
    was_assessed = Column(Boolean, default=False)
    assessed_proficiency = Column(String(50))
    assessment_notes = Column(Text)
    passed_assessment = Column(Boolean)
    created_at = Column(DateTime, default=get_utc_now)

    # Relationships
    interview = relationship("Interview", back_populates="interview_skills")
    skill = relationship("Skill")

    def as_dict(self):
        return {
            'interview_skill_id': self.interview_skill_id,
            'interview_id': self.interview_id,
            'skill_id': self.skill_id,
            'is_required': self.is_required,
            'is_nice_to_have': self.is_nice_to_have,
            'required_proficiency': self.required_proficiency,
            'priority_level': self.priority_level,
            'was_assessed': self.was_assessed,
            'assessed_proficiency': self.assessed_proficiency,
            'passed_assessment': self.passed_assessment
        }


class QuestionSkill(Base):
    """Skills tested by specific interview questions"""
    __tablename__ = 'question_skills'
    __table_args__ = {'schema': 'interview_schema'}

    question_skill_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('interview_schema.questions.question_id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('interview_schema.skills.skill_id'), nullable=False)
    is_primary_skill = Column(Boolean, default=False)
    skill_importance = Column(String(20))
    required_proficiency = Column(String(50))
    created_at = Column(DateTime, default=get_utc_now)

    # Relationships
    question = relationship("Question", back_populates="question_skills")
    skill = relationship("Skill")

    def as_dict(self):
        return {
            'question_skill_id': self.question_skill_id,
            'question_id': self.question_id,
            'skill_id': self.skill_id,
            'is_primary_skill': self.is_primary_skill,
            'skill_importance': self.skill_importance,
            'required_proficiency': self.required_proficiency
        }
