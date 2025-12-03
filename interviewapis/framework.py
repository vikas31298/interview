# productmanagement/models/framework.py
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ARRAY, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime


from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# OYRDB password - Postgres@1

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


Base = declarative_base()

def get_utc_now():
    """Helper function to get current UTC datetime"""
    return datetime.now(timezone.utc)


class ProductFramework(Base):
    __tablename__ = 'product_frameworks'
    __table_args__ = {'schema': 'productschema'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    category = Column(String(100), nullable=False)
    description = Column(Text)
    when_to_use = Column(Text)
    how_to_apply = Column(Text)
    example_application = Column(Text)
    visual_diagram_url = Column(String(500))
    difficulty_level = Column(String(20), default='medium')
    typical_interview_types = Column(ARRAY(Text))
    related_framework_ids = Column(ARRAY(Integer), default=list)
    view_count = Column(Integer, default=0)
    usefulness_rating = Column(Numeric(3, 2), default=0)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    
    # New fields from your schema
    prerequisites = Column(Text)
    time_to_complete_minutes = Column(Integer)
    key_benefits = Column(ARRAY(Text))
    common_pitfalls = Column(ARRAY(Text))
    resources = Column(JSON, default=list)
    is_featured = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    
    # Relationships
    steps = relationship("FrameworkStep", back_populates="framework", cascade="all, delete-orphan")
    applications = relationship("FrameworkApplication", back_populates="framework", cascade="all, delete-orphan")
    templates = relationship("FrameworkTemplate", back_populates="framework", cascade="all, delete-orphan")
    
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'when_to_use': self.when_to_use,
            'how_to_apply': self.how_to_apply,
            'example_application': self.example_application,
            'visual_diagram_url': self.visual_diagram_url,
            'difficulty_level': self.difficulty_level,
            'typical_interview_types': self.typical_interview_types,
            'related_framework_ids': self.related_framework_ids,
            'view_count': self.view_count,
            'usefulness_rating': float(self.usefulness_rating) if self.usefulness_rating else 0,
            'prerequisites': self.prerequisites,
            'time_to_complete_minutes': self.time_to_complete_minutes,
            'key_benefits': self.key_benefits,
            'common_pitfalls': self.common_pitfalls,
            'resources': self.resources,
            'is_featured': self.is_featured,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class FrameworkStep(Base):
    __tablename__ = 'framework_steps'
    __table_args__ = {'schema': 'productschema'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    framework_id = Column(Integer, ForeignKey('productschema.product_frameworks.id'), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    tips = Column(Text)
    common_mistakes = Column(Text)
    examples = Column(JSON)
    tools_required = Column(ARRAY(Text))
    estimated_time_minutes = Column(Integer)
    is_optional = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    
    framework = relationship("ProductFramework", back_populates="steps")
    
    def as_dict(self):
        return {
            'id': self.id,
            'framework_id': self.framework_id,
            'step_number': self.step_number,
            'title': self.title,
            'description': self.description,
            'tips': self.tips,
            'common_mistakes': self.common_mistakes,
            'examples': self.examples,
            'tools_required': self.tools_required,
            'estimated_time_minutes': self.estimated_time_minutes,
            'is_optional': self.is_optional
        }


class FrameworkApplication(Base):
    __tablename__ = 'framework_applications'
    __table_args__ = {'schema': 'productschema'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    framework_id = Column(Integer, ForeignKey('productschema.product_frameworks.id'), nullable=False)
    title = Column(String(300), nullable=False)
    industry = Column(String(100))
    company_size = Column(String(50))
    context = Column(Text, nullable=False)
    implementation = Column(Text, nullable=False)
    outcomes = Column(Text)
    lessons_learned = Column(Text)
    application_type = Column(String(50))
    difficulty_level = Column(String(20), default='medium')
    is_verified = Column(Boolean, default=False)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    
    framework = relationship("ProductFramework", back_populates="applications")
    
    def as_dict(self):
        return {
            'id': self.id,
            'framework_id': self.framework_id,
            'title': self.title,
            'industry': self.industry,
            'company_size': self.company_size,
            'context': self.context,
            'implementation': self.implementation,
            'outcomes': self.outcomes,
            'lessons_learned': self.lessons_learned,
            'application_type': self.application_type,
            'difficulty_level': self.difficulty_level,
            'is_verified': self.is_verified
        }


class FrameworkTemplate(Base):
    __tablename__ = 'framework_templates'
    __table_args__ = {'schema': 'productschema'}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    framework_id = Column(Integer, ForeignKey('productschema.product_frameworks.id'), nullable=False)
    template_name = Column(String(200), nullable=False)
    template_type = Column(String(50))
    template_content = Column(JSON, nullable=False)
    description = Column(Text)
    file_url = Column(String(500))
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)
    
    framework = relationship("ProductFramework", back_populates="templates")
    
    def as_dict(self):
        return {
            'id': self.id,
            'framework_id': self.framework_id,
            'template_name': self.template_name,
            'template_type': self.template_type,
            'template_content': self.template_content,
            'description': self.description,
            'file_url': self.file_url,
            'download_count': self.download_count
        }


def get_frameworks_sync(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    featured: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: str = "sort_order",
    order: str = "asc"
):
    """Get all frameworks - Direct database access for scripts (no pagination)"""
    db = SessionLocal()
    try:
        query = db.query(ProductFramework)
        
        # Apply filters
        if category:
            query = query.filter(ProductFramework.category == category)
        if difficulty:
            query = query.filter(ProductFramework.difficulty_level == difficulty)
        if featured is not None:
            query = query.filter(ProductFramework.is_featured == featured)
        if search:
            search_filter = or_(
                ProductFramework.name.ilike(f"%{search}%"),
                ProductFramework.description.ilike(f"%{search}%"),
                ProductFramework.category.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Apply sorting
        sort_column = getattr(ProductFramework, sort_by)
        if order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
        
        # Get all frameworks (no pagination)
        frameworks = query.all()
        
        return [f.as_dict() for f in frameworks]
    finally:
        db.close()


async def get_frameworks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    featured: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: str = Query("sort_order", regex="^(name|view_count|usefulness_rating|created_at|sort_order)$"),
    order: str = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """Get all frameworks with optional filtering and pagination - FastAPI endpoint"""
    query = db.query(ProductFramework)
    
    # Apply filters
    if category:
        query = query.filter(ProductFramework.category == category)
    if difficulty:
        query = query.filter(ProductFramework.difficulty_level == difficulty)
    if featured is not None:
        query = query.filter(ProductFramework.is_featured == featured)
    if search:
        search_filter = or_(
            ProductFramework.name.ilike(f"%{search}%"),
            ProductFramework.description.ilike(f"%{search}%"),
            ProductFramework.category.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Apply sorting
    sort_column = getattr(ProductFramework, sort_by)
    if order == "desc":
        sort_column = sort_column.desc()
    query = query.order_by(sort_column)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    frameworks = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [f.as_dict() for f in frameworks]
    }