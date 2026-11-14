from fastapi.testclient import TestClient

import app as web
from agent import screening
from tests.fakes import FakeStructuredLLM


def test_board_and_screen_api(monkeypatch):
    raw = screening.CandidateScore(candidate_name="Maria Lopez", score=88, strengths=["Python"], gaps=["None"], reasoning="Good fit.")
    real = screening.score_resume
    monkeypatch.setattr(web, "score_resume", lambda text, job: real(text, job, llm=FakeStructuredLLM(raw)))
    client = TestClient(web.app)

    assert "Screen candidates" in client.get("/").text
    assert "Backend Software Engineer" in client.get("/api/job").json()["text"]
    resumes = client.get("/api/resumes").json()
    assert len(resumes) == 5

    result = client.post("/api/screen", json={"filename": resumes[0]["filename"], "text": resumes[0]["text"]}).json()
    assert result["candidate_name"] == "Maria Lopez" and result["score"] == 88
    assert result["filename"] == resumes[0]["filename"]
    assert client.post("/api/screen", json={"text": "too short"}).status_code == 422
