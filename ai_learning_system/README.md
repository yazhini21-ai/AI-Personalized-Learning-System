# AI-Based Personalized Learning System

A comprehensive Python project that implements an AI-powered personalized learning system designed to enhance student learning experiences.

## Features

- Captures and processes student performance data, including marks, attendance, and study hours.
- Manages syllabus topics for each subject, allowing for easy addition, removal, and listing of topics.
- Classifies student performance into three categories:
  - Weak student (marks < 50)
  - Average student (marks between 50 and 75)
  - Top student (marks > 75)
- Generates tailored learning material recommendations based on student performance.
- Enables students to upload and manage notes for each subject topic.
- Utilizes Natural Language Processing (NLP) techniques to summarize notes and extract key points.
- Provides a user-friendly Flask dashboard to visualize student performance, identify weak subjects, manage syllabus, view notes, and access recommendations.

## Project Structure

- `src/data_input.py` - Utilities for capturing and loading student data.
- `src/syllabus_manager.py` - Manages syllabus topics per subject.
- `src/performance_model.py` - Implements classification logic and model pipeline.
- `src/notes_generator.py` - Processes notes for summarization and key point extraction.
- `src/dashboard_app.py` - Sets up the Flask web application.
- `src/templates/index.html` - Main HTML template for the dashboard.
- `src/static/css/styles.css` - CSS styles for the dashboard.
- `src/static/js/scripts.js` - JavaScript for client-side interactivity.

## Getting Started

1. Create a virtual environment:

   python -m venv venv  
   source venv/bin/activate   # macOS/Linux  
   venv\Scripts\activate    # Windows  

2. Install dependencies:

   pip install -r requirements.txt  

3. Run the dashboard:

   python src/dashboard_app.py  

4. Open your browser at `http://127.0.0.1:5000/`.

## Notes

- The project includes a rule-based performance classifier and a scikit-learn compatible pipeline for demonstration purposes.
- For NLP functionalities, ensure that the necessary NLTK resources are downloaded. If you encounter "Resource not found" errors, run:

   import nltk  
   nltk.download('punkt')  
   nltk.download('stopwords')  

This project aims to provide an interactive and personalized learning experience for students, leveraging AI and web technologies.