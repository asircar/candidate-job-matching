# Candidate-Job Matching System

A hybrid matching system that combines structured and unstructured data analysis to provide explainable candidate-job matching scores. The system uses a combination of machine learning models and rule-based approaches to generate comprehensive matching scores.

## Features

- **Hybrid Matching Algorithm**: Combines structured data (experience, education, location) with unstructured data (resume text, job descriptions)
- **Explainable Scores**: Provides detailed feature importance and contributions for each match
- **Comprehensive Matching Factors**:
  - Experience match (years of experience)
  - Education match (level)
  - Location match (preferences vs. requirements)
  - Skills match (extracted from text)
  - Text similarity (semantic and TF-IDF based)
- **REST API**: FastAPI-based endpoint for easy integration
- **Test Suite**: Comprehensive test cases covering various matching scenarios

## Algorithm Details

### 1. Data Processing Pipeline

The system uses a `MixedDataProcessor` class that handles both structured and unstructured data:

1. **Structured Data Processing**:
   - Experience level normalization
   - Education level encoding (High School → PhD)
   - Location preference matching
   - Work arrangement compatibility

2. **Unstructured Data Processing**:
   - Text preprocessing using spaCy
   - TF-IDF vectorization for skill matching
   - Semantic similarity using pre-trained SentenceTransformer (all-MiniLM-L6-v2)
   - Skill extraction from text descriptions

### 2. Feature Engineering

The system generates multiple similarity scores:

1. **Structured Similarity**:
   - Experience match (years ratio)
   - Education level match (hierarchical)
   - Location compatibility (exact match)
   - Work arrangement compatibility

2. **Unstructured Similarity**:
   - TF-IDF based skill similarity
   - Semantic similarity using embeddings
   - Technical skill overlap ratio

### 3. Model Architecture

The hybrid matcher uses a stacked approach:

1. **Base Components**:
   - Random Forest for final score prediction
   - Pre-trained SentenceTransformer for text embeddings (using 'all-MiniLM-L6-v2')
   - TF-IDF vectorizer for skill matching

2. **Training Process**:
   - 80/20 train/validation split
   - Mean Squared Error optimization
   - Feature importance tracking
   - R² score validation

### 4. Explainability

The system provides two levels of explanation:

1. **Feature Importance**:
   - Global importance from Random Forest
   - Contribution of each feature type:
     - Semantic similarity (41.5%)
     - Years experience (33.7%)
     - TF-IDF similarity (10.9%)
     - Education level (10.7%)
     - Location match (2.8%)
     - Structured similarity (0.5%)

2. **Feature Contributions**:
   - Per-prediction feature contributions
   - Positive/negative impact analysis
   - Local explanation for each match

## Installation

1. Clone the repository:
```bash
git clone https://github.com/asircar/candidate-job-matching.git
cd candidate-job-matching
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Training the Model

First, generate training data:
```bash
python src/data/data_generator.py
```
This will create:
- `sample_candidates.csv`: 100 diverse candidate profiles
- `sample_jobs.csv`: 50 job listings

Then train the model:
```python
from src.train_hybrid_model import train_hybrid_model

# Train the model with automatic train/validation split
model = train_hybrid_model(training_data)
```

The training process includes:
- 80/20 train/validation split
- Model evaluation metrics (MSE and R² score)
- Feature importance analysis
- Model saved as `hybrid_model.joblib`

### 2. Using the API

Start the API server:
```bash
uvicorn src.api.main:app --reload --port 8001
```

Make a matching request:
```bash
curl -X POST "http://localhost:8001/match" \
     -H "Content-Type: application/json" \
     -d '{
           "candidate": {
             "years_experience": 5.0,
             "education_level": "Master",
             "preferred_location": "New York",
             "resume_text": "Experienced software engineer..."
           },
           "job": {
             "required_experience": 5.0,
             "education_requirement": "Bachelor",
             "location": "New York",
             "job_description": "Looking for a senior engineer..."
           }
         }'
```

### 3. Running Tests

```bash
python src/test_api.py
```

## Project Structure

```
.
├── src/
│   ├── api/
│   │   └── main.py              # FastAPI application
│   ├── models/
│   │   └── hybrid_matcher.py    # Core matching algorithm
│   ├── data/
│   │   └── test_cases.py        # Test scenarios
│   └── test_api.py              # Test suite
├── requirements.txt             # Project dependencies
├── hybrid_model.joblib          # Trained model
└── README.md                    # This file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 