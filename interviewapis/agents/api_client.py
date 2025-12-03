"""
PM Case Analyzer API Client
Simple client to interact with the PM Case Study Analyzer API

Usage:
    python api_client.py
"""

import requests
import json
from typing import Optional


class PMCaseAnalyzerClient:
    """Client for PM Case Study Analyzer API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def health_check(self) -> dict:
        """Check API health"""
        response = requests.get(f"{self.base_url}/api/health")
        return response.json()
    
    def get_frameworks(self) -> dict:
        """Get all available frameworks"""
        response = requests.get(f"{self.base_url}/api/frameworks")
        return response.json()
    
    def analyze_case_study(
        self,
        case_study: str,
        additional_context: Optional[str] = None,
        include_clarifying_questions: bool = True,
        include_complete_solution: bool = True
    ) -> dict:
        """Analyze a case study"""
        
        payload = {
            "case_study": case_study,
            "additional_context": additional_context,
            "include_clarifying_questions": include_clarifying_questions,
            "include_complete_solution": include_complete_solution
        }
        
        response = requests.post(
            f"{self.base_url}/api/analyze",
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
        
        return response.json()
    
    def get_workflow_graph(self) -> dict:
        """Get workflow graph structure"""
        response = requests.get(f"{self.base_url}/api/workflow/graph")
        return response.json()


def print_analysis_results(result: dict):
    """Pretty print analysis results"""
    
    print("\n" + "="*70)
    print("📋 ANALYSIS RESULTS")
    print("="*70)
    
    # Case Study
    print(f"\n📝 Case Study:")
    print(f"   {result['case_study']}")
    
    # Classification
    classification = result['classification']
    print(f"\n🎯 Problem Classification:")
    print(f"   Type: {classification['problem_type']}")
    print(f"   Confidence: {classification['confidence']*100:.0f}%")
    print(f"   Reasoning: {classification['reasoning']}")
    
    if classification.get('key_indicators'):
        print(f"   Key Indicators: {', '.join(classification['key_indicators'])}")
    
    # Clarifying Questions
    if result.get('clarifying_questions'):
        print(f"\n❓ Clarifying Questions:")
        for i, q in enumerate(result['clarifying_questions'], 1):
            print(f"\n   {i}. {q['question']}")
            print(f"      Category: {q['category']}")
            print(f"      Why: {q['why_important']}")
    
    # Framework Recommendation
    recommendation = result['framework_recommendation']
    print(f"\n📚 Recommended Framework:")
    print(f"   {recommendation['framework']}")
    print(f"\n💡 Why This Framework:")
    print(f"   {recommendation['rationale']}")
    
    # Application Steps
    print(f"\n📝 Step-by-Step Application Guide:")
    for i, step in enumerate(recommendation['application_steps'], 1):
        print(f"   {i}. {step}")
    
    # Key Tips
    if recommendation.get('key_tips'):
        print(f"\n✨ Key Tips:")
        for tip in recommendation['key_tips']:
            print(f"   • {tip}")
    
    # Common Pitfalls
    if recommendation.get('common_pitfalls'):
        print(f"\n⚠️  Common Pitfalls to Avoid:")
        for pitfall in recommendation['common_pitfalls']:
            print(f"   • {pitfall}")
    
    # Alternative Frameworks
    if recommendation.get('alternatives'):
        print(f"\n🔄 Alternative Frameworks:")
        print(f"   {', '.join(recommendation['alternatives'])}")
    
    # Complete Solution
    if result.get('complete_solution'):
        solution = result['complete_solution']
        
        print(f"\n{'='*70}")
        print("🎯 COMPLETE SOLUTION")
        print("="*70)
        
        if solution.get('executive_summary'):
            print(f"\n📊 Executive Summary:")
            print(f"   {solution['executive_summary']}")
        
        if solution.get('proposed_solutions'):
            print(f"\n💡 Proposed Solutions:")
            for i, sol in enumerate(solution['proposed_solutions'], 1):
                print(f"\n   Solution {i}: {sol['solution_name']}")
                print(f"   Description: {sol['description']}")
                print(f"   Priority: {sol['priority']} | Complexity: {sol['implementation_complexity']}")
        
        if solution.get('prioritized_recommendation'):
            pr = solution['prioritized_recommendation']
            print(f"\n🏆 TOP RECOMMENDATION:")
            print(f"   Solution: {pr['top_solution']}")
            print(f"   Rationale: {pr['rationale']}")
            if pr.get('success_metrics'):
                print(f"\n   Success Metrics:")
                for metric in pr['success_metrics']:
                    print(f"      • {metric}")
        
        if solution.get('next_steps'):
            print(f"\n🚀 Next Steps:")
            for i, step in enumerate(solution['next_steps'], 1):
                print(f"   {i}. {step}")
    
    print("\n" + "="*70 + "\n")


def main():
    """Main function"""
    
    print("\n" + "="*70)
    print("  🎯 PM CASE STUDY ANALYZER - API CLIENT")
    print("="*70 + "\n")
    
    # Initialize client
    client = PMCaseAnalyzerClient()
    
    # Health check
    print("🔍 Checking API health...")
    try:
        health = client.health_check()
        print(f"   ✅ API Status: {health['status']}")
        print(f"   ✅ Frameworks Loaded: {health['frameworks_loaded']}")
        print(f"   ✅ LLM Configured: {health['llm_configured']}\n")
    except Exception as e:
        print(f"   ❌ Error: API is not reachable. Make sure it's running.")
        print(f"   Start the API with: uvicorn pm_api:app --reload")
        return
    
    # Example case studies
    examples = [
        {
            "title": "Improve Google Maps",
            "case_study": "How would you improve Google Maps for daily commuters?",
            "context": "Focus on reducing commute time and increasing user engagement"
        },
        {
            "title": "Design Fitness App",
            "case_study": "Design a fitness app for seniors",
            "context": "Target users are 60+ years old with limited tech experience"
        },
        {
            "title": "Feature Prioritization",
            "case_study": "You have 5 features but can only ship 2 in this quarter. How do you prioritize?",
            "context": "Limited engineering resources, high user expectations"
        }
    ]
    
    # Let user choose
    print("Select a case study to analyze:")
    for i, ex in enumerate(examples, 1):
        print(f"   {i}. {ex['title']}")
    print(f"   {len(examples) + 1}. Enter custom case study")
    
    try:
        choice = int(input("\nEnter your choice (1-4): ").strip())
        
        if 1 <= choice <= len(examples):
            selected = examples[choice - 1]
            case_study = selected["case_study"]
            additional_context = selected["context"]
            print(f"\n✅ Selected: {selected['title']}")
        else:
            case_study = input("\nEnter your case study: ").strip()
            additional_context = input("Enter additional context (optional): ").strip() or None
        
        print("\n🔍 Analyzing case study...")
        print("   This may take 30-60 seconds...\n")
        
        # Analyze
        result = client.analyze_case_study(
            case_study=case_study,
            additional_context=additional_context,
            include_clarifying_questions=True,
            include_complete_solution=True
        )
        
        # Print results
        print_analysis_results(result)
        
        # Save option
        save = input("💾 Save results to file? (y/n): ").strip().lower()
        if save == 'y':
            filename = "pm_case_analysis_api_result.json"
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"✅ Results saved to: {filename}")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
