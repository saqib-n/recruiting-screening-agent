"""Scores a resume against a job description.

The scoring instruction is deliberately explicit about what to ignore, not
just what to look for. Bias isn't something that goes away by not
mentioning it, a system that scores resumes needs to be told directly to
score only job-relevant criteria, or proxies for age, gender, and
background creep in through things like university name or graduation
year.
"""

from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from agent.llm import get_llm

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

SYSTEM_PROMPT = """You screen resumes against a job description for a recruiter.

Score strictly on job-relevant criteria: does their experience match what the
role actually requires, do they show the specific skills listed, is their
level of seniority a reasonable match. Explain your reasoning with specific
evidence from the resume, not vague impressions.

Do not factor in age, gender, name, what school someone attended, how
prestigious a past employer sounds, or graduation year, none of those are
job-relevant signals and using them introduces bias, not accuracy. A
career-changer with strong relevant personal projects should be judged on
that work, not treated as less credible for having a non-traditional path.

Be honest about both strengths and real gaps, don't inflate a score to be
encouraging, and don't be harsh about gaps that don't actually matter for
this specific role.
"""


class CandidateScore(BaseModel):
    candidate_name: str
    score: int = Field(description="0 to 100, fit for this specific role")
    strengths: list[str] = Field(description="2-4 specific, evidence-based strengths")
    gaps: list[str] = Field(description="1-3 specific, evidence-based gaps or open questions")
    reasoning: str = Field(description="2-3 sentence summary of the overall fit assessment")


def load_job_description() -> str:
    return (DATA_DIR / "job_description.txt").read_text(encoding="utf-8")


def load_resumes() -> list[dict]:
    resumes = []
    for path in sorted((DATA_DIR / "resumes").glob("*.txt")):
        resumes.append({"filename": path.name, "text": path.read_text(encoding="utf-8")})
    return resumes


def score_resume(resume_text: str, job_description: str, model: str | None = None, llm=None) -> CandidateScore:
    human = HumanMessage(content=f"Job description:\n{job_description}\n\nResume:\n{resume_text}")
    llm = llm or get_llm(model)
    result = llm.with_structured_output(CandidateScore).invoke([SystemMessage(content=SYSTEM_PROMPT), human])
    # Keep the ranking sane even if the model drifts outside 0-100.
    return result.model_copy(update={"score": max(0, min(100, result.score))})
