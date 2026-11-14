"""Hiring board for the resume screening agent.

Opens a recruiter-style screen in the browser. Press "Screen candidates" and
the agent scores each resume in data/resumes/ against
data/job_description.txt, and the shortlist re-ranks as scores come in.
Same scoring code and fairness prompt as screen_candidates.py.

Run:
    python app.py
"""

import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from agent.llm import DEFAULT_MODEL
from agent.screening import load_job_description, load_resumes, score_resume

load_dotenv()

logger = logging.getLogger("resume-screening")
app = FastAPI(title="Resume Screening Agent")
WEB_DIR = Path(__file__).resolve().parent / "web"


class Resume(BaseModel):
    filename: str = Field(default="pasted resume", max_length=120)
    text: str = Field(min_length=20, max_length=20000)


def screen_one(resume_text: str) -> dict:
    return score_resume(resume_text, load_job_description()).model_dump()


@app.get("/", include_in_schema=False)
def board():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/info")
def info():
    return {"model": os.getenv("LLM_MODEL") or DEFAULT_MODEL}


@app.get("/api/job")
def job():
    return {"text": load_job_description()}


@app.get("/api/resumes")
def resumes():
    return load_resumes()


@app.post("/api/screen")
def screen(resume: Resume):
    started = time.perf_counter()
    try:
        result = screen_one(resume.text)
    except Exception as exc:
        logger.exception("Screening failed for %s", resume.filename)
        detail = str(exc).splitlines()[0][:200] if str(exc) else ""
        return JSONResponse(status_code=502, content={"error": f"The agent could not score this resume ({type(exc).__name__}: {detail})."})
    return {**result, "filename": resume.filename, "seconds": round(time.perf_counter() - started, 1)}


if __name__ == "__main__":
    import threading
    import webbrowser

    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    uvicorn.run(app, host="127.0.0.1", port=port)
