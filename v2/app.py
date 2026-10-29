"""Online Exam System - v2: MCQ Quiz + Auto Score (marks calculated automatically)."""
from flask import Flask, render_template_string, request

app = Flask(__name__)
VERSION = "v2"

QUESTIONS = [
    {"q": "Which language is used to style web pages?",
     "options": ["HTML", "CSS", "Python", "SQL"], "answer": 1},
    {"q": "Which command builds a Docker image?",
     "options": ["docker run", "docker pull", "docker build", "docker push"], "answer": 2},
    {"q": "What does CI stand for in CI/CD?",
     "options": ["Code Integration", "Continuous Integration", "Container Image", "Central Index"], "answer": 1},
    {"q": "Which tool orchestrates containers at scale?",
     "options": ["Git", "Jenkins", "Kubernetes", "VS Code"], "answer": 2},
    {"q": "Which HTTP method is normally used to submit a form?",
     "options": ["GET", "POST", "HEAD", "TRACE"], "answer": 1},
]

PAGE = """
<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Online Exam {{ version }}</title>
<style>
 body{font-family:Segoe UI,Arial,sans-serif;background:#f4f6fb;margin:0;color:#222}
 .wrap{max-width:720px;margin:30px auto;padding:0 16px}
 h1{margin-bottom:4px} .tag{background:#2b8a3e;color:#fff;border-radius:12px;padding:2px 10px;font-size:13px}
 .card{background:#fff;border-radius:10px;padding:16px 20px;margin:14px 0;box-shadow:0 1px 4px rgba(0,0,0,.08)}
 label{display:block;padding:4px 0;cursor:pointer}
 button{background:#2b8a3e;color:#fff;border:0;border-radius:8px;padding:10px 22px;font-size:16px;cursor:pointer}
 .score{font-size:40px;font-weight:700;color:#2b8a3e}
</style></head><body><div class="wrap">
<h1>Online Exam <span class="tag">{{ version }}</span></h1>
{% block_content %}
</div></body></html>
"""

QUIZ_BODY = """
<p>Answer all questions. Your score is calculated automatically.</p>
<form method="post" action="/submit">
{% for i in range(questions|length) %}
 <div class="card"><b>Q{{ i+1 }}. {{ questions[i].q }}</b>
 {% for j in range(questions[i].options|length) %}
  <label><input type="radio" name="q{{ i }}" value="{{ j }}" required> {{ questions[i].options[j] }}</label>
 {% endfor %}</div>
{% endfor %}
<button type="submit">Submit Test</button>
</form>
"""

SCORE_BODY = """
<div class="card"><h2>Your score (auto-calculated)</h2>
<div class="score">{{ score }} / {{ total }}</div>
<p>You answered {{ score }} of {{ total }} questions correctly.</p>
<p><a href="/">Retake the test</a></p></div>
"""


def render(body, **ctx):
    return render_template_string(PAGE.replace("{% block_content %}", body), version=VERSION, **ctx)


def calculate_score(form):
    """Auto Score: compare each submitted option with the correct answer."""
    score = 0
    for i, item in enumerate(QUESTIONS):
        chosen = form.get(f"q{i}")
        if chosen is not None and chosen.isdigit() and int(chosen) == item["answer"]:
            score += 1
    return score


@app.route("/")
def index():
    return render(QUIZ_BODY, questions=QUESTIONS)


@app.route("/submit", methods=["POST"])
def submit():
    return render(SCORE_BODY, score=calculate_score(request.form), total=len(QUESTIONS))


@app.route("/health")
def health():
    return {"status": "ok", "version": VERSION}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
