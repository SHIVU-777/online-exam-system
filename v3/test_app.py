from app import app, QUESTIONS, grade_for


def answers(correct=True):
    return {f"q{i}": str(q["answer"] if correct else (q["answer"] + 1) % 4)
            for i, q in enumerate(QUESTIONS)}


def test_result_pass():
    r = app.test_client().post("/result", data=answers(True))
    assert b"5 / 5" in r.data and b"PASS" in r.data and b"100.0%" in r.data


def test_result_fail():
    r = app.test_client().post("/result", data=answers(False))
    assert b"0 / 5" in r.data and b"FAIL" in r.data


def test_grades():
    assert grade_for(95) == "A+" and grade_for(45) == "D" and grade_for(10) == "F"


def test_health():
    assert app.test_client().get("/health").get_json()["version"] == "v3"
