from models.hybrid_matcher import HybridMatcher
from data.test_cases import test_cases
import numpy as np

def generate_training_data():
    """Generate training data with known match scores."""
    training_data = []
    
    # Add our test cases with manually assigned scores
    scores = {
        "Perfect match case - all attributes align perfectly": 0.95,
        "Technical skills mismatch but other factors align": 0.65,
        "Candidate overqualified in experience and education": 0.75,
        "Skills match but location and work arrangement mismatch": 0.60,
        "Skills and location match but salary and industry mismatch": 0.70
    }
    
    # Add test cases to training data
    for case in test_cases:
        training_data.append({
            'candidate': case['candidate'],
            'job': case['job'],
            'match_score': scores.get(case['description'], 0.5)  # Default score of 0.5 for unknown cases
        })
    
    # Generate additional synthetic data
    for _ in range(20):
        # Create variations of existing cases
        base_case = np.random.choice(test_cases)
        score_noise = np.random.normal(0, 0.1)  # Add some random variation to scores
        
        training_data.append({
            'candidate': base_case['candidate'],
            'job': base_case['job'],
            'match_score': min(1.0, max(0.0, scores.get(base_case['description'], 0.5) + score_noise))
        })
    
    return training_data

def main():
    print("Initializing Hybrid Matcher...")
    matcher = HybridMatcher()
    
    print("Generating training data...")
    training_data = generate_training_data()
    
    print("Training model...")
    matcher.train(training_data)
    
    print("Saving model...")
    matcher.save('hybrid_model.joblib')
    
    print("Training complete!")

if __name__ == "__main__":
    main() 