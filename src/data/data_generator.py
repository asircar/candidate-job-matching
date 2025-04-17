import numpy as np
import pandas as pd
from typing import List, Dict
import random
from datetime import datetime, timedelta

# Sample data for generation
TECH_SKILLS = [
    'Python', 'Java', 'JavaScript', 'SQL', 'AWS', 'Docker', 'Kubernetes',
    'React', 'Node.js', 'Machine Learning', 'Data Analysis', 'DevOps',
    'CI/CD', 'Git', 'REST API', 'GraphQL', 'MongoDB', 'PostgreSQL'
]

SOFT_SKILLS = [
    'Communication', 'Leadership', 'Teamwork', 'Problem Solving',
    'Time Management', 'Adaptability', 'Critical Thinking', 'Creativity'
]

EDUCATION_LEVELS = ['High School', 'Bachelor', 'Master', 'PhD']
INDUSTRIES = ['Technology', 'Finance', 'Healthcare', 'Education', 'Retail', 'Manufacturing']
LOCATIONS = ['New York', 'San Francisco', 'London', 'Berlin', 'Tokyo', 'Remote']

def generate_candidate_data(num_candidates: int = 100) -> pd.DataFrame:
    """Generate sample candidate data."""
    candidates = []
    
    for i in range(num_candidates):
        # Generate random experience (0-20 years)
        experience = random.uniform(0, 20)
        
        # Generate random number of skills (3-10)
        num_tech_skills = random.randint(3, 10)
        num_soft_skills = random.randint(2, 5)
        
        # Select random skills
        tech_skills = random.sample(TECH_SKILLS, num_tech_skills)
        soft_skills = random.sample(SOFT_SKILLS, num_soft_skills)
        
        # Generate random education level
        education = random.choice(EDUCATION_LEVELS)
        
        # Generate random salary expectation (40k-200k)
        salary_expectation = random.randint(40000, 200000)
        
        # Generate random work preferences
        work_preference = random.choice(['Remote', 'Hybrid', 'Office'])
        
        candidate = {
            'candidate_id': f'C{i+1:03d}',
            'name': f'Candidate {i+1}',
            'years_experience': round(experience, 1),
            'tech_skills': tech_skills,
            'soft_skills': soft_skills,
            'education_level': education,
            'preferred_locations': random.sample(LOCATIONS, random.randint(1, 3)),
            'salary_expectation': salary_expectation,
            'work_preference': work_preference,
            'industry_experience': random.sample(INDUSTRIES, random.randint(1, 3))
        }
        candidates.append(candidate)
    
    return pd.DataFrame(candidates)

def generate_job_data(num_jobs: int = 50) -> pd.DataFrame:
    """Generate sample job data."""
    jobs = []
    
    for i in range(num_jobs):
        # Generate random required experience (0-15 years)
        required_experience = random.uniform(0, 15)
        
        # Generate random number of required skills (3-8)
        num_required_skills = random.randint(3, 8)
        num_required_soft_skills = random.randint(2, 4)
        
        # Select random required skills
        required_tech_skills = random.sample(TECH_SKILLS, num_required_skills)
        required_soft_skills = random.sample(SOFT_SKILLS, num_required_soft_skills)
        
        # Generate random education requirement
        education_requirement = random.choice(EDUCATION_LEVELS)
        
        # Generate random salary range
        min_salary = random.randint(40000, 150000)
        max_salary = min_salary + random.randint(10000, 50000)
        
        # Generate random work arrangement
        work_arrangement = random.choice(['Remote', 'Hybrid', 'Office'])
        
        job = {
            'job_id': f'J{i+1:03d}',
            'title': f'Job Position {i+1}',
            'required_experience': round(required_experience, 1),
            'required_tech_skills': required_tech_skills,
            'required_soft_skills': required_soft_skills,
            'education_requirement': education_requirement,
            'location': random.choice(LOCATIONS),
            'salary_range_min': min_salary,
            'salary_range_max': max_salary,
            'work_arrangement': work_arrangement,
            'industry': random.choice(INDUSTRIES)
        }
        jobs.append(job)
    
    return pd.DataFrame(jobs)

def save_sample_data():
    """Generate and save sample data to CSV files."""
    candidates_df = generate_candidate_data()
    jobs_df = generate_job_data()
    
    candidates_df.to_csv('src/data/sample_candidates.csv', index=False)
    jobs_df.to_csv('src/data/sample_jobs.csv', index=False)
    
    print(f"Generated {len(candidates_df)} candidates and {len(jobs_df)} jobs")
    return candidates_df, jobs_df

if __name__ == "__main__":
    save_sample_data() 