from flask import Flask, render_template, request, redirect, url_for
from data_input import load_student_data
from syllabus_manager import SyllabusManager
from performance_model import classify_student
from notes_generator import summarize_notes

app = Flask(__name__)

syllabus_manager = SyllabusManager()

@app.route('/')
def index():
    student_data = load_student_data()
    performance = classify_student(student_data['marks'])
    weak_subjects = [subject for subject, mark in student_data['subjects'].items() if mark < 50]
    return render_template('index.html', performance=performance, weak_subjects=weak_subjects, syllabus=syllabus_manager.get_topics())

@app.route('/add_topic', methods=['POST'])
def add_topic():
    subject = request.form['subject']
    topic = request.form['topic']
    syllabus_manager.add_topic(subject, topic)
    return redirect(url_for('index'))

@app.route('/upload_notes', methods=['POST'])
def upload_notes():
    subject = request.form['subject']
    notes = request.form['notes']
    summary = summarize_notes(notes)
    # Save summary and notes logic here
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)