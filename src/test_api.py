import requests
import json
from data.test_cases import test_cases

# API endpoint
url = "http://localhost:8001/match"

def test_match(test_case):
    print("\n" + "="*80)
    print(f"Testing: {test_case['description']}")
    print("="*80)
    
    # Extract candidate and job info from unstructured text
    candidate_info = test_case['candidate']['unstructured'].split('\n')[1].strip()  # First non-empty line
    job_info = test_case['job']['unstructured'].split('\n')[1].strip()  # First non-empty line
    
    # Make the request
    response = requests.post(url, json={
        "candidate": test_case["candidate"],
        "job": test_case["job"]
    })
    
    # Print the response
    print(f"Candidate: {candidate_info}")
    print(f"Job: {job_info}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\nMatch Score:", result["score"])
        print("\nFeature Importance:")
        for feature, importance in result["feature_importance"].items():
            print(f"  {feature}: {importance:.3f}")
        print("\nFeature Contributions:")
        for feature, contribution in result["feature_contribution"].items():
            print(f"  {feature}: {contribution:.3f}")
    else:
        print("Error:", response.text)
    
    print("\n")

def main():
    print(f"Running {len(test_cases)} test cases...\n")
    
    for test_case in test_cases:
        test_match(test_case)
        
    print("All test cases completed.")

if __name__ == "__main__":
    main() 