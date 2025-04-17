import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import spacy
from spacy.matcher import PhraseMatcher
import re
from typing import Dict, List, Tuple, Union
import joblib

class MixedDataProcessor:
    def __init__(self):
        # Initialize components
        self.nlp = spacy.load('en_core_web_sm')
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000)
        
    def process_structured_data(self, data: Dict) -> Dict:
        """Process structured data (tables with defined columns)"""
        features = {
            'years_experience': float(data.get('years_experience', 0)),
            'education_level': self._encode_education(data.get('education_level', '')),
            'location_match': 1.0 if data.get('location') == data.get('preferred_location') else 0.0,
        }
        return features
        
    def process_unstructured_data(self, text: str) -> Tuple[Dict, np.ndarray]:
        """Process unstructured data (resumes, job descriptions)"""
        # Extract structured information
        extracted_info = {
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text)
        }
        
        # Get semantic embedding
        embedding = self.sentence_transformer.encode(text)
        
        return extracted_info, embedding
        
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using NLP"""
        doc = self.nlp(text.lower())
        skills = []
        
        # Common skill indicators
        skill_indicators = ['proficient in', 'experience with', 'knowledge of', 'skilled in']
        
        for indicator in skill_indicators:
            if indicator in text.lower():
                # Extract the skill after the indicator
                start_idx = text.lower().find(indicator) + len(indicator)
                end_idx = text.find('.', start_idx) if '.' in text[start_idx:] else len(text)
                skill_text = text[start_idx:end_idx].strip()
                skills.extend([token.text for token in self.nlp(skill_text) if token.pos_ in ['NOUN', 'PROPN']])
        
        return list(set(skills))
        
    def _extract_experience(self, text: str) -> float:
        """Extract years of experience from text"""
        experience_pattern = r'(\d+)\s*(?:year|yr)s?\s+experience'
        matches = re.findall(experience_pattern, text.lower())
        return float(matches[0]) if matches else 0.0
        
    def _extract_education(self, text: str) -> str:
        """Extract education level from text"""
        education_levels = ['PhD', 'Master', 'Bachelor', 'High School']
        for level in education_levels:
            if level.lower() in text.lower():
                return level
        return 'Unknown'
        
    def _encode_education(self, education: str) -> float:
        """Convert education level to numerical value"""
        education_map = {
            'PhD': 4.0,
            'Master': 3.0,
            'Bachelor': 2.0,
            'High School': 1.0,
            'Unknown': 0.0
        }
        return education_map.get(education, 0.0)

class HybridMatcher:
    def __init__(self):
        self.processor = MixedDataProcessor()
        self.random_forest = RandomForestRegressor()
        self.is_trained = False
        
    def _calculate_structured_similarity(self, candidate: Dict, job: Dict) -> float:
        """Calculate similarity between structured features"""
        similarities = []
        
        # Experience similarity
        exp_similarity = min(candidate['years_experience'] / max(job['years_experience'], 1), 1.0)
        similarities.append(exp_similarity)
        
        # Education similarity
        edu_similarity = 1.0 if candidate['education_level'] >= job['education_level'] else 0.5
        similarities.append(edu_similarity)
        
        # Location match
        similarities.append(candidate['location_match'])
        
        # Calculate base structured similarity
        return np.mean(similarities)
        
    def prepare_features(self, candidate_data: Dict, job_data: Dict) -> pd.DataFrame:
        """Prepare features from mixed data sources"""
        # Process structured data
        candidate_structured = self.processor.process_structured_data(
            candidate_data.get('structured', {})
        )
        job_structured = self.processor.process_structured_data(
            job_data.get('structured', {})
        )
        
        # Process unstructured data
        candidate_unstructured = self.processor.process_unstructured_data(
            candidate_data.get('unstructured', '')
        )
        job_unstructured = self.processor.process_unstructured_data(
            job_data.get('unstructured', '')
        )
        
        # Calculate structured similarity
        structured_similarity = self._calculate_structured_similarity(
            candidate_structured,
            job_structured
        )
        
        # Calculate semantic similarity
        semantic_similarity = cosine_similarity(
            candidate_unstructured[1].reshape(1, -1),
            job_unstructured[1].reshape(1, -1)
        )[0][0]
        
        # Calculate TF-IDF similarity for specific fields
        tfidf_similarity = self._calculate_tfidf_similarity(
            candidate_unstructured[0],
            job_unstructured[0]
        )
        
        # Combine all features
        features = {
            'structured_similarity': structured_similarity,
            'semantic_similarity': semantic_similarity,
            'tfidf_similarity': tfidf_similarity,
            'years_experience': candidate_structured['years_experience'],
            'education_level': candidate_structured['education_level'],
            'location_match': candidate_structured['location_match']
        }
        
        return pd.DataFrame([features])
        
    def _calculate_tfidf_similarity(self, candidate_info: Dict, job_info: Dict) -> float:
        """Calculate TF-IDF similarity for specific fields"""
        similarities = []
        
        # Compare skills
        if 'skills' in candidate_info and 'skills' in job_info:
            candidate_skills = ' '.join(candidate_info['skills'])
            job_skills = ' '.join(job_info['skills'])
            
            if candidate_skills and job_skills:
                tfidf_matrix = self.processor.tfidf_vectorizer.fit_transform([candidate_skills, job_skills])
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                similarities.append(similarity)
        
        return np.mean(similarities) if similarities else 0.0
        
    def train(self, training_data: List[Dict]) -> None:
        """Train the model on labeled data"""
        X = []
        y = []
        
        for sample in training_data:
            features = self.prepare_features(
                sample['candidate'],
                sample['job']
            )
            X.append(features.iloc[0].to_dict())
            y.append(sample['match_score'])
            
        X_df = pd.DataFrame(X)
        self.random_forest.fit(X_df, y)
        self.is_trained = True
        
    def predict_score(self, candidate_data: Dict, job_data: Dict) -> Tuple[float, Dict]:
        """Predict matching score and provide explanation"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        features = self.prepare_features(candidate_data, job_data)
        score = self.random_forest.predict(features)[0]
        
        # Get feature importances
        importances = dict(zip(features.columns, self.random_forest.feature_importances_))
        
        # Get feature contributions using SHAP (if available)
        try:
            import shap
            explainer = shap.TreeExplainer(self.random_forest)
            shap_values = explainer.shap_values(features)
            contributions = dict(zip(features.columns, shap_values[0]))
        except ImportError:
            contributions = None
            
        explanation = {
            'score': float(score),
            'feature_importance': importances,
            'feature_contribution': contributions
        }
        
        return score, explanation
        
    def save(self, path: str) -> None:
        """Save the model to disk"""
        model_data = {
            'random_forest': self.random_forest,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, path)
        
    @classmethod
    def load(cls, path: str) -> 'HybridMatcher':
        """Load the model from disk"""
        matcher = cls()
        model_data = joblib.load(path)
        matcher.random_forest = model_data['random_forest']
        matcher.is_trained = model_data['is_trained']
        return matcher 