"""Online Exam System - v3: MCQ Quiz + Auto Score + Result (final score, grade, review)."""
from flask import Flask, render_template_string, request

app = Flask(__name__)
VERSION = "v3"
PASS_PERCENT = 40

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
 h1{margin-bottom:4px} .tag{background:#c2255c;color:#fff;border-radius:12px;padding:2px 10px;font-size:13px}
 .card{background:#fff;border-radius:10px;padding:16px 20px;margin:14px 0;box-shadow:0 1px 4px rgba(0,0,0,.08)}
 label{display:block;padding:4px 0;cursor:pointer}
 button{background:#c2255c;color:#fff;border:0;border-radius:8px;padding:10px 22px;font-size:16px;cursor:pointer}
 .score{font-size:44px;font-weight:700}
 .pass{color:#2b8a3e} .fail{color:#c92a2a}
 .ok{color:#2b8a3e} .bad{color:#c92a2a}
 table{width:100%;border-collapse:collapse} td,th{padding:6px 8px;border-bottom:1px solid #eee;text-align:left;font-size:14px}
</style></head><body><div class="wrap">
<h1>Online Exam <span class="tag">{{ version }}</span></h1>
{% block_content %}
</div></body></html>
"""

QUIZ_BODY = """
<p>Answer all questions. Your final result is shown after submission.</p>
<form method="post" action="/result">
{% for i in range(questions|length) %}
 <div class="card"><b>Q{{ i+1 }}. {{ questions[i].q }}</b>
 {% for j in range(questions[i].options|length) %}
  <label><input type="radio" name="q{{ i }}" value="{{ j }}" required> {{ questions[i].options[j] }}</label>
 {% endfor %}</div>
{% endfor %}
<button type="submit">Submit Test</button>
</form>
"""

RESULT_BODY = """
<div class="card"><h2>Final Result</h2>
<div class="score {{ 'pass' if passed else 'fail' }}">{{ score }} / {{ total }}</div>
<p><b>Percentage:</b> {{ percent }}% &nbsp; <b>Grade:</b> {{ grade }} &nbsp;
<b>Status:</b> <span class="{{ 'pass' if passed else 'fail' }}">{{ 'PASS' if passed else 'FAIL' }}</span></p></div>
<div class="card"><h3>Answer review</h3>
<table><tr><th>#</th><th>Your answer</th><th>Correct answer</th><th></th></tr>
{% for r in review %}
<tr><td>{{ loop.index }}</td><td>{{ r.chosen }}</td><td>{{ r.correct }}</td>
<td class="{{ 'ok' if r.is_correct else 'bad' }}">{{ '✔' if r.is_correct else '✘' }}</td></tr>
{% endfor %}</table></div>
<p><a href="/">Retake the test</a></p>
"""


def render(body, **ctx):
    return render_template_string(PAGE.replace("{% block_content %}", body), version=VERSION, **ctx)


def grade_for(percent):
    if percent >= 90: return "A+"
    if percent >= 80: return "A"
    if percent >= 70: return "B"
    if percent >= 60: return "C"
    if percent >= PASS_PERCENT: return "D"
    return "F"


def evaluate(form):
    """Auto Score + Result: returns score, per-question review, percent and grade."""
    score, review = 0, []
    for i, item in enumerate(QUESTIONS):
        chosen = form.get(f"q{i}")
        valid = chosen is not None and chosen.isdigit() and int(chosen) < len(item["options"])
        is_correct = valid and int(chosen) == item["answer"]
        score += 1 if is_correct else 0
        review.append({
            "chosen": item["options"][int(chosen)] if valid else "Not answered",
            "correct": item["options"][item["answer"]],
            "is_correct": is_correct,
        })
    total = len(QUESTIONS)
    percent = round(score * 100 / total, 1)
    return {"score": score, "total": total, "percent": percent,
            "grade": grade_for(percent), "passed": percent >= PASS_PERCENT, "review": review}


@app.route("/")
def index():
    return render(QUIZ_BODY, questions=QUESTIONS)


@app.route("/result", methods=["POST"])
def result():
    return render(RESULT_BODY, **evaluate(request.form))


@app.route("/health")
def health():
    return {"status": "ok", "version": VERSION}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
