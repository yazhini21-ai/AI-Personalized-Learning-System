"""A simple Flask dashboard for the AI-Based Personalized Learning System."""

from __future__ import annotations

from flask import Flask, redirect, render_template_string, request, url_for
from markupsafe import Markup

from data_input import create_student_record, load_students, save_students, students_to_dataframe
from notes_generator import extract_key_points, summarize_notes
from performance_model import annotate_student_performance, get_overall_category
from syllabus_manager import SyllabusManager


STUDENTS_JSON_PATH = "data/students.json"
SYLLABUS_JSON_PATH = "data/syllabus.json"


app = Flask(__name__)

# In-memory caches (loaded on app start)
students = load_students(STUDENTS_JSON_PATH)
syllabus = SyllabusManager.load(SYLLABUS_JSON_PATH)

# Notes structure: { student_name: { subject: { topic: notes_text }}}
notes_store: dict = {}


def _get_student_by_name(name: str) -> dict | None:
    for s in students:
        if s.get("name") == name:
            return s
    return None


def _build_student_context(student: dict) -> dict:
    optimizer = annotate_student_performance([student])[0]
    overall = get_overall_category(student)

    subject_breakdown = []
    for subject, mark, category in zip(
        student.get("subjects", []), student.get("marks", []), optimizer.get("performance", [])
    ):
        subject_breakdown.append({"subject": subject, "mark": mark, "category": category})

    weak_subjects = [x for x in subject_breakdown if x["category"] == "Weak"]

    student_notes = notes_store.get(student.get("name"), {})

    return {
        "student": student,
        "overall": overall,
        "breakdown": subject_breakdown,
        "weak_subjects": weak_subjects,
        "syllabus": syllabus.get_all(),
        "notes": student_notes,
    }


@app.route("/")
def index():
    student_summaries = []
    for student in students:
        avg_marks = 0.0
        if student.get("marks"):
            avg_marks = sum(student.get("marks")) / len(student.get("marks"))
        student_summaries.append(
            {
                "name": student.get("name"),
                "average": round(avg_marks, 1),
                "category": get_overall_category(student),
            }
        )

    return render_template_string(
        """<!doctype html>
<html lang='en'>
  <head>
    <meta charset='utf-8'>
    <title>AI-Based Personalized Learning System</title>
    <style>
      body { font-family: system-ui, sans-serif; margin: 1.5rem; }
      table { border-collapse: collapse; width: 100%; margin-bottom: 1rem; }
      th, td { border: 1px solid #ddd; padding: 0.5rem; }
      th { background: #f4f4f4; }
      a { color: #0b6efd; text-decoration: none; }
      a:hover { text-decoration: underline; }
      form { margin-top: 1rem; }
      textarea { width: 100%; height: 100px; }
      .card { border: 1px solid #ddd; padding: 1rem; border-radius: 4px; margin-bottom: 1rem; }
    </style>
  </head>
  <body>
    <h1>AI-Based Personalized Learning System</h1>

    <section class="card">
      <h2>Students</h2>
      <table>
        <thead>
          <tr><th>Name</th><th>Average Mark</th><th>Category</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {% for s in students %}
          <tr>
            <td>{{ s.name }}</td>
            <td>{{ s.average }}</td>
            <td>{{ s.category }}</td>
            <td><a href="{{ url_for('student_detail', name=s.name) }}">View</a></td>
          </tr>
          {% endfor %}
        </tbody>
      </table>

      <h3>Add a student</h3>
      <form method="post" action="{{ url_for('add_student') }}">
        <label>Name: <input name="name" required></label><br>
        <label>Subjects (comma separated): <input name="subjects" required></label><br>
        <label>Marks (comma separated): <input name="marks" required></label><br>
        <label>Attendance (%) : <input name="attendance" type="number" step="0.1" value="90"></label><br>
        <label>Study hours per week: <input name="study_hours" type="number" step="0.1" value="5"></label><br>
        <button type="submit">Add Student</button>
      </form>
    </section>

    <section class="card">
      <h2>Syllabus</h2>
      <form method="post" action="{{ url_for('add_topic') }}">
        <label>Subject: <input name="subject" required></label><br>
        <label>Topic: <input name="topic" required></label><br>
        <button type="submit">Add Topic</button>
      </form>

      <h3>Current syllabus</h3>
      {% for subject, topics in syllabus.items() %}
      <div class="card">
        <strong>{{ subject }}:</strong>
        <ul>
        {% for topic in topics %}
          <li>{{ topic }}</li>
        {% endfor %}
        </ul>
      </div>
      {% endfor %}
    </section>

    <section class="card">
      <h2>Notes & Recommendations</h2>
      <p>Click on any student to see their personalized notes, weak subjects, and study recommendations.</p>
    </section>
  </body>
</html>
""",
        students=student_summaries,
        syllabus=syllabus.get_all(),
    )


@app.route("/student/<name>")
def student_detail(name: str):
    student = _get_student_by_name(name)
    if not student:
        return redirect(url_for("index"))

    context = _build_student_context(student)

    return render_template_string(
        """<!doctype html>
<html lang='en'>
  <head>
    <meta charset='utf-8'>
    <title>{{ student.name }} - Dashboard</title>
    <style>
      body { font-family: system-ui, sans-serif; margin: 1.5rem; }
      .card { border: 1px solid #ddd; padding: 1rem; border-radius: 4px; margin-bottom: 1rem; }
      table { border-collapse: collapse; width: 100%; margin-bottom: 1rem; }
      th, td { border: 1px solid #ddd; padding: 0.5rem; }
      th { background: #f4f4f4; }
    </style>
  </head>
  <body>
    <a href="{{ url_for('index') }}">← Back to home</a>
    <h1>{{ student.name }}’s Dashboard</h1>

    <section class="card">
      <h2>Performance</h2>
      <p><strong>Overall category:</strong> {{ overall }}</p>
      <table>
        <thead><tr><th>Subject</th><th>Mark</th><th>Category</th></tr></thead>
        <tbody>
          {% for item in breakdown %}
          <tr>
            <td>{{ item.subject }}</td>
            <td>{{ item.mark }}</td>
            <td>{{ item.category }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>

      <h3>Weak subjects</h3>
      {% if weak_subjects %}
      <ul>
        {% for w in weak_subjects %}
        <li>{{ w.subject }} ({{ w.mark }})</li>
        {% endfor %}
      </ul>
      {% else %}
      <p>None at the moment. Great job!</p>
      {% endif %}

      <h3>Study recommendations</h3>
      {% if overall == 'Weak' %}
        <p>Focus on core concepts and review foundational topics. Consider spending more time on weak subjects.</p>
      {% elif overall == 'Average' %}
        <p>Practice regularly and revisit key syllabus topics. Mix short notes with practice questions.</p>
      {% else %}
        <p>Challenge yourself with advanced analytical questions and explore deeper topics.</p>
      {% endif %}
    </section>

    <section class="card">
      <h2>Syllabus</h2>
      {% for subject, topics in syllabus.items() %}
        <div class="card">
          <strong>{{ subject }}:</strong>
          <ul>
            {% for topic in topics %}
            <li>{{ topic }}</li>
            {% endfor %}
          </ul>
        </div>
      {% endfor %}
    </section>

    <section class="card">
      <h2>Notes</h2>
      <form method="post" action="{{ url_for('add_notes', name=student.name) }}">
        <label>Subject: <input name="subject" required></label><br>
        <label>Topic: <input name="topic" required></label><br>
        <label>Notes (plain text):</label><br>
        <textarea name="notes" required></textarea><br>
        <button type="submit">Save Notes</button>
      </form>

      {% if notes %}
        <h3>Notes by Subject</h3>
        {% for subject, topic_map in notes.items() %}
          <div class="card">
            <strong>{{ subject }}</strong>
            <ul>
              {% for topic, content in topic_map.items() %}
                <li>
                  <strong>{{ topic }}</strong>
                  <p>{{ content }}</p>
                  <p><em>Summary:</em> {{ summarize_notes(content) }}</p>
                  <p><em>Key points:</em> {{ extract_key_points(content) | join(', ') }}</p>
                </li>
              {% endfor %}
            </ul>
          </div>
        {% endfor %}
      {% else %}
        <p>No notes have been added yet.</p>
      {% endif %}
    </section>
  </body>
</html>
""",
        **context,
        summarize_notes=summarize_notes,
        extract_key_points=extract_key_points,
    )


@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    subjects_raw = request.form.get("subjects", "")
    marks_raw = request.form.get("marks", "")
    attendance = request.form.get("attendance", 0)
    study_hours = request.form.get("study_hours", 0)

    subjects = [s.strip() for s in subjects_raw.split(",") if s.strip()]
    marks = [float(m.strip()) for m in marks_raw.split(",") if m.strip()]

    record = create_student_record(name, subjects, marks, attendance, study_hours)
    students.append(record)

    save_students(STUDENTS_JSON_PATH, students)
    return redirect(url_for("index"))


@app.route("/add_topic", methods=["POST"])
def add_topic():
    subject = request.form.get("subject", "")
    topic = request.form.get("topic", "")
    syllabus.add_topic(subject, topic)
    syllabus.to_json(SYLLABUS_JSON_PATH)
    return redirect(url_for("index"))


@app.route("/student/<name>/add_notes", methods=["POST"])
def add_notes(name: str):
    student = _get_student_by_name(name)
    if not student:
        return redirect(url_for("index"))

    subject = request.form.get("subject", "").strip()
    topic = request.form.get("topic", "").strip()
    notes_text = request.form.get("notes", "").strip()

    if not subject or not topic or not notes_text:
        return redirect(url_for("student_detail", name=name))

    student_notes = notes_store.setdefault(name, {})
    subject_notes = student_notes.setdefault(subject, {})
    subject_notes[topic] = notes_text

    return redirect(url_for("student_detail", name=name))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
