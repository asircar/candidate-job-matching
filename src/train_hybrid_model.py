from models.hybrid_matcher import HybridMatcher
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Constants
EDUCATION_LEVELS = ['High School', 'Bachelor', 'Master', 'PhD']

def generate_training_data():
    """Generate training data from CSV files with calculated match scores."""
    print("Loading generated data...")
    candidates_df = pd.read_csv('src/data/sample_candidates.csv')
    jobs_df = pd.read_csv('src/data/sample_jobs.csv')
    
    training_data = []
    
    # For each job, find matching candidates
    for _, job in jobs_df.iterrows():
        job_dict = {
            'structured': {
                'years_experience': job['required_experience'],
                'education_level': job['education_requirement'],
                'location': job['location'],
                'work_arrangement': job['work_arrangement']
            },
            'unstructured': f"""
            {job['title']}
            Required Skills: {', '.join(eval(job['required_tech_skills']))}
            Soft Skills: {', '.join(eval(job['required_soft_skills']))}
            Education: {job['education_requirement']}
            Location: {job['location']}
            Work Arrangement: {job['work_arrangement']}
            Industry: {job['industry']}
            """
        }
        
        # Sample 5 random candidates for each job
        for _, candidate in candidates_df.sample(n=min(5, len(candidates_df))).iterrows():
            candidate_dict = {
                'structured': {
                    'years_experience': candidate['years_experience'],
                    'education_level': candidate['education_level'],
                    'preferred_location': candidate['preferred_locations'],
                    'work_preference': candidate['work_preference']
                },
                'unstructured': f"""
                {candidate['name']}
                Technical Skills: {', '.join(eval(candidate['tech_skills']))}
                Soft Skills: {', '.join(eval(candidate['soft_skills']))}
                Education: {candidate['education_level']}
                Preferred Locations: {candidate['preferred_locations']}
                Work Preference: {candidate['work_preference']}
                Industry Experience: {', '.join(eval(candidate['industry_experience']))}
                """
            }
            
            # Calculate match score based on various factors
            exp_match = min(1.0, candidate['years_experience'] / max(job['required_experience'], 1))
            edu_match = 1.0 if EDUCATION_LEVELS.index(candidate['education_level']) >= EDUCATION_LEVELS.index(job['education_requirement']) else 0.5
            loc_match = 1.0 if job['location'] in eval(candidate['preferred_locations']) else 0.0
            work_match = 1.0 if candidate['work_preference'] == job['work_arrangement'] else 0.5
            
            # Calculate skill overlap
            candidate_skills = set(eval(candidate['tech_skills']))
            required_skills = set(eval(job['required_tech_skills']))
            skill_match = len(candidate_skills.intersection(required_skills)) / len(required_skills) if required_skills else 0.0
            
            # Combine all factors for final score
            match_score = np.mean([exp_match, edu_match, loc_match, work_match, skill_match])
            
            training_data.append({
                'candidate': candidate_dict,
                'job': job_dict,
                'match_score': match_score
            })
    
    return training_data

def evaluate_model(matcher, validation_data):
    """Evaluate model performance on validation data."""
    true_scores = []
    pred_scores = []
    
    for sample in validation_data:
        true_score = sample['match_score']
        pred_score, _ = matcher.predict_score(sample['candidate'], sample['job'])
        
        true_scores.append(true_score)
        pred_scores.append(pred_score)
    
    mse = mean_squared_error(true_scores, pred_scores)
    r2 = r2_score(true_scores, pred_scores)
    
    print("\nValidation Metrics:")
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R² Score: {r2:.4f}")
    
    return mse, r2

def main():
    print("Initializing Hybrid Matcher...")
    matcher = HybridMatcher()
    
    print("Generating training data...")
    all_data = generate_training_data()
    
    # Split data into training and validation sets
    train_data, val_data = train_test_split(
        all_data, 
        test_size=0.2,
        random_state=42
    )
    
    print(f"\nDataset sizes:")
    print(f"Training samples: {len(train_data)}")
    print(f"Validation samples: {len(val_data)}")
    
    print("\nTraining model...")
    matcher.train(train_data)
    
    print("\nEvaluating model...")
    evaluate_model(matcher, val_data)
    
    print("\nSaving model...")
    matcher.save('hybrid_model.joblib')
    
    print("Training complete!")

if __name__ == "__main__":
    main() 