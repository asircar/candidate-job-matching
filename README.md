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
   - Normalizes experience levels
   - Processes location preferences
   - Handles education level encoding

2. **Unstructured Data Processing**:
   - Text preprocessing using spaCy
   - TF-IDF vectorization
   - Semantic similarity using pre-trained SentenceTransformer
   - Skill extraction from text

### 2. Feature Engineering

The system generates multiple similarity scores:

1. **Structured Similarity**:
   - Experience match score
   - Education level match
   - Location compatibility

2. **Unstructured Similarity**:
   - TF-IDF based text similarity
   - Semantic similarity using embeddings
   - Skill overlap analysis

### 3. Model Architecture

The hybrid matcher uses a stacked approach:

1. **Base Models**:
   - Random Forest for structured features
   - Pre-trained SentenceTransformer for text embeddings (using 'all-MiniLM-L6-v2')
   - Linear model for TF-IDF features

2. **Meta Model**:
   - Combines predictions from base models
   - Weighted ensemble approach
   - Calibrated probability outputs

### 4. Explainability

The system provides two levels of explanation:

1. **Feature Importance**:
   - Shows which factors had the most impact
   - Ranks features by their contribution
   - Provides global feature importance

2. **Feature Contributions**:
   - Shows how each factor affected the score
   - Positive and negative contributions
   - Local explanation for each prediction

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

```python
from src.train_hybrid_model import train_hybrid_model

# Train the model with your data
model = train_hybrid_model(training_data)
```

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