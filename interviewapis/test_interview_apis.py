"""
Test script for Interview Tracking APIs
Tests the interviews and questions endpoints
"""

import requests
import json
from datetime import date

BASE_URL = "http://127.0.0.1:8000"


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*80}\n")


def test_health_check():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/api/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print_response("Root Endpoint", response)
    return response.status_code == 200


def test_create_company():
    """Test creating a company"""
    company_data = {
        "company_name": "TechCorp Inc",
        "industry": "Technology",
        "company_size": "1000-5000",
        "headquarters": "San Francisco, CA",
        "website": "https://techcorp.example.com",
        "company_description": "Leading technology company"
    }
    response = requests.post(f"{BASE_URL}/api/companies/", json=company_data)
    print_response("Create Company", response)
    if response.status_code == 201:
        return response.json()["company_id"]
    return None


def test_list_companies():
    """Test listing companies"""
    response = requests.get(f"{BASE_URL}/api/companies/")
    print_response("List Companies", response)
    return response.status_code == 200


def test_create_role():
    """Test creating a role"""
    role_data = {
        "role_name": "Senior Software Engineer",
        "role_category": "Engineering",
        "role_description": "Senior engineer position",
        "typical_skills": ["Python", "JavaScript", "AWS", "Docker"]
    }
    response = requests.post(f"{BASE_URL}/api/roles/", json=role_data)
    print_response("Create Role", response)
    if response.status_code == 201:
        return response.json()["role_id"]
    return None


def test_list_roles():
    """Test listing roles"""
    response = requests.get(f"{BASE_URL}/api/roles/")
    print_response("List Roles", response)
    return response.status_code == 200


def test_create_interview(company_id, role_id):
    """Test creating an interview"""
    interview_data = {
        "company_id": company_id,
        "role_id": role_id,
        "custom_role_title": "Senior Full Stack Engineer",
        "interview_type": "actual",
        "seniority_level": "senior",
        "interview_status": "scheduled",
        "interview_result": "pending",
        "job_description": "Looking for a senior engineer with 5+ years experience in full stack development",
        "main_skills_required": ["Python", "React", "AWS", "PostgreSQL"],
        "required_experience_years": 5,
        "job_location": "San Francisco, CA",
        "is_remote": True,
        "salary_range": "$150,000 - $200,000",
        "application_date": "2024-12-01",
        "preparation_notes": "Review system design patterns and AWS architecture",
        "created_by": "test_user"
    }
    response = requests.post(f"{BASE_URL}/api/interviews/", json=interview_data)
    print_response("Create Interview", response)
    if response.status_code == 201:
        return response.json()["interview_id"]
    return None


def test_list_interviews():
    """Test listing interviews"""
    response = requests.get(f"{BASE_URL}/api/interviews/")
    print_response("List Interviews", response)
    return response.status_code == 200


def test_get_interview(interview_id):
    """Test getting a specific interview"""
    response = requests.get(f"{BASE_URL}/api/interviews/{interview_id}")
    print_response(f"Get Interview {interview_id}", response)
    return response.status_code == 200


def test_update_interview(interview_id):
    """Test updating an interview"""
    update_data = {
        "interview_status": "completed",
        "interview_result": "passed",
        "overall_feedback": "Great interview! Demonstrated strong technical skills.",
        "strengths": "Strong system design knowledge, good communication",
        "areas_for_improvement": "Could improve algorithm optimization"
    }
    response = requests.put(f"{BASE_URL}/api/interviews/{interview_id}", json=update_data)
    print_response(f"Update Interview {interview_id}", response)
    return response.status_code == 200


def test_create_question():
    """Test creating a question"""
    question_data = {
        "question_text": "How would you design a URL shortening service like bit.ly?",
        "question_category": "system_design",
        "question_difficulty": "medium",
        "question_context": "Common system design interview question",
        "answer_summary": "Design should include URL generation, storage, redirection, and analytics. Key components: hash generation, database, caching layer, and API gateway.",
        "key_concepts": ["Hashing", "Database Design", "Caching", "Load Balancing", "API Design"],
        "common_mistakes": [
            "Not considering collision handling",
            "Ignoring scalability requirements",
            "Forgetting about analytics tracking"
        ],
        "tips_and_tricks": [
            "Use base62 encoding for short URLs",
            "Consider Redis for caching frequently accessed URLs",
            "Think about rate limiting and security"
        ],
        "time_to_answer_minutes": 45,
        "suggested_frameworks": ["RADIO (Requirements, Architecture, Data Model, Interface, Optimization)"],
        "approach_steps": [
            "Clarify requirements and constraints",
            "Design high-level architecture",
            "Define data model",
            "Design API endpoints",
            "Discuss scalability and optimization"
        ],
        "tags": ["system_design", "scalability", "distributed_systems", "url_shortener"],
        "source": "System Design Interview Course",
        "is_active": True,
        "created_by": "test_user"
    }
    response = requests.post(f"{BASE_URL}/api/questions/", json=question_data)
    print_response("Create Question", response)
    if response.status_code == 201:
        return response.json()["question_id"]
    return None


def test_list_questions():
    """Test listing questions"""
    response = requests.get(f"{BASE_URL}/api/questions/")
    print_response("List Questions", response)
    return response.status_code == 200


def test_get_question(question_id):
    """Test getting a specific question"""
    response = requests.get(f"{BASE_URL}/api/questions/{question_id}")
    print_response(f"Get Question {question_id}", response)
    return response.status_code == 200


def test_filter_questions():
    """Test filtering questions by category and difficulty"""
    response = requests.get(f"{BASE_URL}/api/questions/?category=system_design&difficulty=medium")
    print_response("Filter Questions (system_design, medium)", response)
    return response.status_code == 200


def test_link_question_to_interview(interview_id, question_id):
    """Test linking a question to an interview"""
    link_data = {
        "interview_id": interview_id,
        "question_id": question_id,
        "was_asked": True,
        "order_asked": 1,
        "candidate_answer": "I would start by clarifying requirements...",
        "answer_quality_rating": 8,
        "time_taken_minutes": 40,
        "was_prepared": True,
        "confidence_level": 7,
        "what_went_well": "Good structure and covered all key points",
        "what_could_improve": "Could have discussed more about analytics implementation"
    }
    response = requests.post(f"{BASE_URL}/api/interviews/{interview_id}/questions", json=link_data)
    print_response(f"Link Question {question_id} to Interview {interview_id}", response)
    return response.status_code == 201


def test_get_interview_questions(interview_id):
    """Test getting questions for an interview"""
    response = requests.get(f"{BASE_URL}/api/interviews/{interview_id}/questions")
    print_response(f"Get Questions for Interview {interview_id}", response)
    return response.status_code == 200


def test_statistics():
    """Test statistics endpoint"""
    response = requests.get(f"{BASE_URL}/api/stats/overview")
    print_response("Statistics Overview", response)
    return response.status_code == 200


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("INTERVIEW TRACKING API TEST SUITE")
    print("="*80 + "\n")

    results = {
        "passed": 0,
        "failed": 0
    }

    # Test basic endpoints
    print("\n--- Testing Basic Endpoints ---")
    if test_health_check():
        results["passed"] += 1
    else:
        results["failed"] += 1

    if test_root():
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Test company endpoints
    print("\n--- Testing Company Endpoints ---")
    company_id = test_create_company()
    if company_id:
        results["passed"] += 1
    else:
        results["failed"] += 1

    if test_list_companies():
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Test role endpoints
    print("\n--- Testing Role Endpoints ---")
    role_id = test_create_role()
    if role_id:
        results["passed"] += 1
    else:
        results["failed"] += 1

    if test_list_roles():
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Test interview endpoints
    print("\n--- Testing Interview Endpoints ---")
    interview_id = None
    if company_id and role_id:
        interview_id = test_create_interview(company_id, role_id)
        if interview_id:
            results["passed"] += 1
        else:
            results["failed"] += 1

    if test_list_interviews():
        results["passed"] += 1
    else:
        results["failed"] += 1

    if interview_id:
        if test_get_interview(interview_id):
            results["passed"] += 1
        else:
            results["failed"] += 1

        if test_update_interview(interview_id):
            results["passed"] += 1
        else:
            results["failed"] += 1

    # Test question endpoints
    print("\n--- Testing Question Endpoints ---")
    question_id = test_create_question()
    if question_id:
        results["passed"] += 1
    else:
        results["failed"] += 1

    if test_list_questions():
        results["passed"] += 1
    else:
        results["failed"] += 1

    if question_id:
        if test_get_question(question_id):
            results["passed"] += 1
        else:
            results["failed"] += 1

    if test_filter_questions():
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Test linking questions to interviews
    print("\n--- Testing Interview-Question Linking ---")
    if interview_id and question_id:
        if test_link_question_to_interview(interview_id, question_id):
            results["passed"] += 1
        else:
            results["failed"] += 1

        if test_get_interview_questions(interview_id):
            results["passed"] += 1
        else:
            results["failed"] += 1

    # Test statistics
    print("\n--- Testing Statistics ---")
    if test_statistics():
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Total: {results['passed'] + results['failed']}")
    print(f"Success Rate: {results['passed'] / (results['passed'] + results['failed']) * 100:.1f}%")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
