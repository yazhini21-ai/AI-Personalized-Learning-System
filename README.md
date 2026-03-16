# AI-Based Personalized Learning System

A simple Python project demonstrating an AI-powered personalized learning system.

## Features

- Accepts student performance data (marks, attendance, study hours).
- Allows entering syllabus topics per subject.
- Classifies student performance into:
  - Weak student (marks < 50)
  - Average student (marks between 50 and 75)
  - Top student (marks > 75)
- Generates different learning material recommendations based on performance.
- Allows students to add/upload notes for each subject topic.
- Uses basic NLP (NLTK) to summarize notes and extract key points.
- Provides a simple Flask dashboard to view student performance, weak subjects, syllabus, notes, and recommendations.

## Project Structure

- `data_input.py` - utilities for capturing and loading student data.
- `syllabus_manager.py` - manage syllabus topics per subject.
- `performance_model.py` - classification logic and model pipeline.
- `notes_generator.py` - simple NLP-based summarization and key point extraction.
- `dashboard_app.py` - Flask web UI.

## Getting Started

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate    # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the dashboard:

```bash
python dashboard_app.py
```

4. Open your browser at `http://127.0.0.1:5000/`.

## Notes

- The project uses a rule-based performance classifier but includes a scikit-learn compatible pipeline for demonstration.
- The notes summarization uses NLTK's `punkt` tokenizer and `stopwords`. If you see "Resource not found" errors, run:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```
