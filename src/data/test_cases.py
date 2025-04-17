"""
Test cases for candidate-job matching API.
Each case is designed to test different aspects of the matching algorithm.
"""

test_cases = [
    # Case 1: Perfect Match
    {
        "candidate": {
            "structured": {
                "years_experience": 5.0,
                "education_level": "Master",
                "preferred_location": "New York",
                "work_preference": "Hybrid"
            },
            "unstructured": """
            Senior Software Engineer with 5 years of experience in Python, SQL, AWS, and Docker.
            Strong communication and teamwork skills with a proven track record in technology and finance sectors.
            Master's degree holder seeking opportunities in New York or Remote locations.
            Technical Skills: Python, SQL, AWS, Docker
            Soft Skills: Communication, Teamwork, Problem Solving
            """
        },
        "job": {
            "structured": {
                "years_experience": 5.0,
                "education_level": "Master",
                "location": "New York",
                "work_arrangement": "Hybrid"
            },
            "unstructured": """
            Senior Software Engineer position requiring 5 years of experience.
            Required Skills: Python, SQL, AWS, Docker
            Must have strong communication and teamwork abilities.
            Master's degree required. Position based in New York with hybrid work arrangement.
            Competitive salary range: $110,000 - $130,000
            """
        },
        "description": "Perfect match case - all attributes align perfectly"
    },
    
    # Case 2: Skills Mismatch
    {
        "candidate": {
            "structured": {
                "years_experience": 3.0,
                "education_level": "Bachelor",
                "preferred_location": "San Francisco",
                "work_preference": "Remote"
            },
            "unstructured": """
            Software Developer with 3 years of experience in Java development.
            Proficient in Java, Spring Framework, and MySQL database.
            Bachelor's degree in Computer Science.
            Technical Skills: Java, Spring, MySQL
            Soft Skills: Leadership, Communication
            """
        },
        "job": {
            "structured": {
                "years_experience": 4.0,
                "education_level": "Bachelor",
                "location": "San Francisco",
                "work_arrangement": "Remote"
            },
            "unstructured": """
            Full Stack Developer position requiring 4 years of experience.
            Must be proficient in Python, React, and MongoDB.
            Bachelor's degree required. Remote work available.
            Salary range: $90,000 - $120,000
            Strong communication and teamwork skills required.
            """
        },
        "description": "Technical skills mismatch but other factors align"
    },
    
    # Case 3: Experience and Education Overqualified
    {
        "candidate": {
            "structured": {
                "years_experience": 8.0,
                "education_level": "PhD",
                "preferred_location": "Boston",
                "work_preference": "Onsite"
            },
            "unstructured": """
            Senior Software Architect with PhD in Computer Science
            8 years of experience in software development and research
            Expert in Python, Java, Kubernetes, and AWS
            Led multiple research projects and mentored junior developers
            Technical Skills: Python, Java, Kubernetes, AWS
            Soft Skills: Leadership, Communication, Mentoring
            """
        },
        "job": {
            "structured": {
                "years_experience": 3.0,
                "education_level": "Bachelor",
                "location": "Boston",
                "work_arrangement": "Onsite"
            },
            "unstructured": """
            Entry-level Software Developer position
            3 years of experience required
            Must know Python and Java
            Bachelor's degree in Computer Science or related field
            Salary range: $80,000 - $100,000
            """
        },
        "description": "Candidate overqualified in experience and education"
    },
    
    # Case 4: Location and Work Arrangement Mismatch
    {
        "candidate": {
            "structured": {
                "years_experience": 4.0,
                "education_level": "Bachelor",
                "preferred_location": "Remote",
                "work_preference": "Remote"
            },
            "unstructured": """
            Frontend Developer with 4 years of experience
            Expert in JavaScript, React, and Node.js
            Bachelor's degree in Computer Science
            Looking for remote work opportunities
            Technical Skills: JavaScript, React, Node.js
            Soft Skills: Communication, Problem Solving
            """
        },
        "job": {
            "structured": {
                "years_experience": 4.0,
                "education_level": "Bachelor",
                "location": "Chicago",
                "work_arrangement": "Onsite"
            },
            "unstructured": """
            Frontend Developer position in Chicago
            4 years of experience required
            Must be proficient in JavaScript, React, and Node.js
            Onsite position with occasional work from home
            Salary range: $100,000 - $120,000
            """
        },
        "description": "Skills match but location and work arrangement mismatch"
    },
    
    # Case 5: Salary and Industry Mismatch
    {
        "candidate": {
            "structured": {
                "years_experience": 6.0,
                "education_level": "Master",
                "preferred_location": "Seattle",
                "work_preference": "Hybrid"
            },
            "unstructured": """
            Machine Learning Engineer with 6 years of experience
            Master's in Computer Science
            Expert in Python, TensorFlow, and PyTorch
            Published researcher in deep learning
            Technical Skills: Python, TensorFlow, PyTorch
            Soft Skills: Research, Problem Solving, Communication
            Seeking compensation in the $200,000 range
            """
        },
        "job": {
            "structured": {
                "years_experience": 5.0,
                "education_level": "Master",
                "location": "Seattle",
                "work_arrangement": "Hybrid"
            },
            "unstructured": """
            Healthcare ML Engineer position
            5+ years of experience required
            Must be proficient in Python, TensorFlow, and PyTorch
            Experience in healthcare data analysis preferred
            Master's degree required
            Salary range: $130,000 - $160,000
            """
        },
        "description": "Skills and location match but salary and industry mismatch"
    },
    
    # Case 6: Resume Text Match
    {
        "candidate": {
            "structured": {
                "years_experience": 5.0,
                "education_level": "Master",
                "preferred_location": "Seattle",
                "work_preference": "Hybrid"
            },
            "unstructured": """
            EMILY WILSON
            Software Engineer
            Seattle, WA | emily.wilson@email.com

            PROFESSIONAL SUMMARY
            Experienced Machine Learning Engineer with 5 years of expertise in developing and deploying ML models. 
            Proficient in Python, TensorFlow, and PyTorch, with a strong background in computer vision and NLP projects.

            SKILLS
            Technical: Python, TensorFlow, PyTorch, Docker, AWS, Scikit-learn
            Soft Skills: Team Leadership, Communication, Problem-solving

            EXPERIENCE
            Senior Machine Learning Engineer | TechCorp | 2020-Present
            - Led development of computer vision models using PyTorch
            - Implemented and deployed ML pipelines using Docker and AWS
            - Mentored junior engineers and presented at tech conferences

            Machine Learning Engineer | AI Solutions | 2018-2020
            - Developed NLP models using TensorFlow and BERT
            - Optimized model performance resulting in 40% faster inference
            
            EDUCATION
            Master's in Computer Science
            University of Washington, 2018

            CERTIFICATIONS
            - AWS Certified Machine Learning Specialist
            - Deep Learning Specialization, Coursera
            """
        },
        "job": {
            "structured": {
                "years_experience": 5.0,
                "education_level": "Master",
                "location": "Seattle",
                "work_arrangement": "Hybrid"
            },
            "unstructured": """
            Senior Machine Learning Engineer Position

            We are seeking a Senior Machine Learning Engineer to join our AI team in Seattle.

            Required Qualifications:
            - 5+ years of experience in machine learning engineering
            - Strong proficiency in Python, TensorFlow, and PyTorch
            - Experience with computer vision and NLP projects
            - Master's degree in Computer Science or related field
            - Experience with AWS and containerization
            
            Responsibilities:
            - Develop and deploy machine learning models
            - Lead technical projects and mentor junior engineers
            - Optimize model performance and scalability
            - Collaborate with cross-functional teams

            We offer:
            - Competitive salary range: $150,000 - $180,000
            - Hybrid work arrangement
            - Comprehensive benefits package
            """
        },
        "description": "Testing resume text matching with job description"
    },
    
    # Case 7: Unstructured Data Only
    {
        "candidate": {
            "structured": {},
            "unstructured": """
            JOHN DOE
            Data Scientist
            San Francisco, CA | john.doe@email.com

            PROFESSIONAL SUMMARY
            Data Scientist with expertise in machine learning, statistical analysis, and big data processing.
            Experienced in developing predictive models and working with large datasets.

            SKILLS
            Technical: Python, R, SQL, TensorFlow, PyTorch, Spark, Hadoop
            Data Analysis: Statistical Modeling, A/B Testing, Data Visualization
            Tools: Tableau, Jupyter, Git, Docker

            EXPERIENCE
            Data Scientist | Tech Analytics | 2019-Present
            - Developed machine learning models for customer behavior prediction
            - Led A/B testing initiatives resulting in 15% conversion improvement
            - Built data pipelines using Spark and Hadoop
            - Created interactive dashboards using Tableau

            Data Analyst | Data Insights | 2017-2019
            - Performed statistical analysis on large datasets
            - Built predictive models using Python and R
            - Collaborated with cross-functional teams on data-driven decisions
            
            EDUCATION
            Bachelor's in Statistics
            University of California, Berkeley, 2017

            PROJECTS
            - Customer Churn Prediction Model (Python, TensorFlow)
            - Real-time Analytics Dashboard (Tableau, SQL)
            - A/B Testing Framework (Python, R)
            """
        },
        "job": {
            "structured": {},
            "unstructured": """
            Data Scientist Position

            We are looking for a Data Scientist to join our analytics team.

            Required Skills and Experience:
            - Strong background in machine learning and statistical analysis
            - Proficiency in Python, R, and SQL
            - Experience with big data tools (Spark, Hadoop)
            - Knowledge of data visualization tools (Tableau)
            - Experience with A/B testing and predictive modeling
            - Ability to work with large datasets and build data pipelines

            Responsibilities:
            - Develop and implement machine learning models
            - Design and analyze A/B tests
            - Create data visualizations and dashboards
            - Build and maintain data pipelines
            - Collaborate with business teams to drive data-driven decisions

            Nice to Have:
            - Experience with TensorFlow or PyTorch
            - Knowledge of Docker and cloud platforms
            - Strong communication and presentation skills

            Location: San Francisco (Hybrid work arrangement)
            """
        },
        "description": "Testing matching based solely on unstructured data (resume and job description)"
    }
] 