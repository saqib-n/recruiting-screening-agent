# Resume Screening Agent

## Portfolio entry

Screens a batch of resumes against a job description and returns a ranked shortlist where every score carries specific, evidence-based strengths and gaps rather than a bare number. The scoring prompt explicitly excludes school name, employer prestige, graduation year and other common proxies for bias, and the sample data includes a career-changer resume built specifically to test that the instruction holds.

**Stack:** Python, LangChain, Pydantic, OpenAI / Anthropic / Gemini

---

## Why recruiters want this

A single job posting pulls hundreds of applications. Most get about ten seconds of attention, which means good candidates get missed for reasons that have nothing to do with their ability, mostly where they happened to land in the pile.

A first pass that reads every resume properly and explains its reasoning is genuinely useful. It's also repeat work rather than a one-off build, which makes it a better fit for a retainer than a fixed-price project.

## The part that needed the most thought

A naive version of this automates existing bias and makes it faster.

The model never needs to be told someone's age. Graduation year implies it. A bootcamp certificate instead of a CS degree, an employer nobody's heard of, a two-year gap, all of these correlate with things that don't predict job performance, and a model left to its own judgment will quietly weight them.

So the prompt names them:

> Do not factor in age, gender, name, what school someone attended, how prestigious a past employer sounds, or graduation year, none of those are job-relevant signals and using them introduces bias, not accuracy.

## Testing it rather than asserting it

Writing that instruction is easy. Knowing whether it works is the harder question, and it's why the sample data is built the way it is.

Five resumes: a strong match, a partial match, a clear mismatch, someone overqualified, and Omar Siddiqui, a former teacher six months into a career change with a FastAPI project he built himself and no degree in the field.

That fifth resume is the test. If the screening is working, he's scored on the code he's written, not marked down for the route he took. A demo where every candidate is a conventional software engineer proves nothing about the fairness instruction.

## Score plus reasoning, not score alone

Everything returns through a typed model: name, score, strengths, gaps, summary. All tied to evidence in the resume.

"72" tells a recruiter nothing. "72, four years of relevant Python but no cloud experience against a posting that lists AWS" is something they can act on, and disagree with, which matters as much.

## Worth saying to a client directly

Automated hiring tools are regulated in a growing number of jurisdictions, with specific rules emerging around AI in recruitment. For a client deploying this, the bias approach and an audit trail aren't extras, they're part of what makes it safe to use.

I'd rather raise that in the pitch than have it surface after deployment.

## Not built

PDF and Word parsing, it reads plain text only. Screening against multiple open roles in one run. Audit logging of every score and its reasoning, which is the thing a client would want if a decision were ever challenged. And batch questions across the shortlist.

## My part

The scoring approach, the bias instruction, the structured output pipeline, and a sample set designed to exercise the fairness claim rather than just demonstrate that scoring runs.
