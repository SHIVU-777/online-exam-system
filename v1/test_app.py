from app import app


def test_quiz_page_lists_questions():
    r = app.test_client().get("/")
    assert r.status_code == 200
    assert b"Q1." in b"".join([r.data]) and b"Q5." in r.data


def test_submit_records_answers():
    r = app.test_client().post("/submit", data={"q0": "1"})
    assert r.status_code == 200
    assert b"Test submitted" in r.data


def test_health():
    assert app.test_client().get("/health").get_json()["version"] == "v1"
