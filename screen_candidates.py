"""Score every resume in data/resumes/ against data/job_description.txt
and print a ranked shortlist.

Run:
    python screen_candidates.py
"""

import csv
from pathlib import Path

from dotenv import load_dotenv

from agent.screening import load_job_description, load_resumes, score_resume

load_dotenv()

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_FILE = OUTPUT_DIR / "ranked_candidates.csv"


def main():
    job_description = load_job_description()
    resumes = load_resumes()
    if not resumes:
        print("No resumes found in data/resumes/. Add some .txt files and try again.")
        return
    print(f"Screening {len(resumes)} resumes\n")

    scored = []
    for resume in resumes:
        result = score_resume(resume["text"], job_description)
        scored.append((resume["filename"], result))

    scored.sort(key=lambda pair: pair[1].score, reverse=True)

    print("Ranked shortlist:\n")
    for rank, (filename, result) in enumerate(scored, start=1):
        print(f"{rank}. {result.candidate_name} ({filename}) - {result.score}/100")
        print(f"   Strengths: {'; '.join(result.strengths)}")
        print(f"   Gaps: {'; '.join(result.gaps)}")
        print(f"   {result.reasoning}\n")

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "candidate_name", "filename", "score", "strengths", "gaps", "reasoning"])
        for rank, (filename, result) in enumerate(scored, start=1):
            writer.writerow([
                rank, result.candidate_name, filename, result.score,
                "; ".join(result.strengths), "; ".join(result.gaps), result.reasoning,
            ])

    print(f"Saved ranked shortlist to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
