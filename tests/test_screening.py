from agent import screening
from tests.fakes import FakeStructuredLLM


def test_loads_job_and_resumes():
    assert "Backend Software Engineer" in screening.load_job_description()
    assert len(screening.load_resumes()) == 5


def test_bias_instruction_is_in_the_prompt():
    for phrase in ("age, gender, name", "graduation year", "career-changer"):
        assert phrase in screening.SYSTEM_PROMPT


def test_score_is_clamped_and_prompt_sent():
    raw = screening.CandidateScore(candidate_name="Omar", score=140, strengths=["s"], gaps=["g"], reasoning="r")
    llm = FakeStructuredLLM(raw)
    result = screening.score_resume("resume", "job", llm=llm)
    assert result.score == 100
    assert llm.calls[0][0].content == screening.SYSTEM_PROMPT
