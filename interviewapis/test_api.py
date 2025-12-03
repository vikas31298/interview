"""
Quick API Test Script
Tests all API endpoints

Usage:
    python test_api.py
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n1️⃣  Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_frameworks():
    """Test frameworks endpoint"""
    print("\n2️⃣  Testing Frameworks Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/frameworks")
        data = response.json()
        print(f"   Status Code: {response.status_code}")
        print(f"   Total Categories: {data['total_categories']}")
        print(f"   Categories: {', '.join(data['categories'][:5])}...")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_workflow_graph():
    """Test workflow graph endpoint"""
    print("\n3️⃣  Testing Workflow Graph Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/workflow/graph")
        data = response.json()
        print(f"   Status Code: {response.status_code}")
        print(f"   Nodes: {len(data['nodes'])}")
        print(f"   Edges: {len(data['edges'])}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_analyze_simple():
    """Test analyze endpoint with simple case"""
    print("\n4️⃣  Testing Analyze Endpoint (Simple)...")
    try:
        payload = {
            "case_study": "How would you improve Gmail?",
            "include_clarifying_questions": False,
            "include_complete_solution": False
        }
        
        print("   Sending request...")
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json=payload,
            timeout=60
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Classification: {data['classification']['problem_type']}")
            print(f"   Framework: {data['framework_recommendation']['framework']}")
            return True
        else:
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_analyze_complete():
    """Test analyze endpoint with complete solution"""
    print("\n5️⃣  Testing Analyze Endpoint (Complete)...")
    try:
        payload = {
            "case_study": "Design a budget tracking app for college students",
            "additional_context": "Students have limited income and need simple interface",
            "include_clarifying_questions": True,
            "include_complete_solution": True
        }
        
        print("   Sending request (this may take 30-60 seconds)...")
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json=payload,
            timeout=120
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Classification: {data['classification']['problem_type']}")
            print(f"   Confidence: {data['classification']['confidence']}")
            print(f"   Framework: {data['framework_recommendation']['framework']}")
            
            if data.get('clarifying_questions'):
                print(f"   Questions Generated: {len(data['clarifying_questions'])}")
            
            if data.get('complete_solution'):
                print(f"   Complete Solution: ✅ Generated")
                solution = data['complete_solution']
                print(f"   Proposed Solutions: {len(solution.get('proposed_solutions', []))}")
            
            # Save full result
            with open('test_result.json', 'w') as f:
                json.dump(data, f, indent=2)
            print(f"   📄 Full result saved to: test_result.json")
            
            return True
        else:
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  🧪 PM CASE ANALYZER API - TEST SUITE")
    print("="*70)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    sleep(1)
    
    results.append(("Frameworks", test_frameworks()))
    sleep(1)
    
    results.append(("Workflow Graph", test_workflow_graph()))
    sleep(1)
    
    results.append(("Analyze (Simple)", test_analyze_simple()))
    sleep(2)
    
    results.append(("Analyze (Complete)", test_analyze_complete()))
    
    # Summary
    print("\n" + "="*70)
    print("  📊 TEST RESULTS SUMMARY")
    print("="*70)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {test_name:<25} {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\n   Total: {total_passed}/{total_tests} tests passed")
    print("="*70 + "\n")
    
    if total_passed == total_tests:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Tests interrupted!")
