from app import app, QUESTIONS


def answers(correct=True):
    return {f"q{i}": str(q["answer"] if correct else (q["answer"] + 1) % 4)
            for i, q in enumerate(QUESTIONS)}


def test_full_marks():
    r = app.test_client().post("/submit", data=answers(True))
    assert b"5 / 5" in r.data


def test_zero_marks():
    r = app.test_client().post("/submit", data=answers(False))
    assert b"0 / 5" in r.data


def test_health():
    assert app.test_client().get("/health").get_json()["version"] == "v2"
