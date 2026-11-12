<div align="center">

<h1>Resume Screening Agent</h1>

<p><b>Reads a stack of resumes against a job description and returns a ranked shortlist, with the evidence behind every score.</b></p>

<p>
  <a href="https://github.com/saqib-n/recruiting-screening-agent/actions/workflows/tests.yml"><img src="https://github.com/saqib-n/recruiting-screening-agent/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white" alt="Python: 3.12+">
  <img src="https://img.shields.io/badge/LangChain-1.x-1C3C3C" alt="LangChain: 1.x">
  <img src="https://img.shields.io/badge/models-OpenAI%20%7C%20Claude%20%7C%20Gemini-444444" alt="models: OpenAI | Claude | Gemini">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2E7D32" alt="license: MIT"></a>
</p>

<p>
  <a href="#what-it-does">What it does</a> &nbsp;|&nbsp;
  <a href="#how-it-works">How it works</a> &nbsp;|&nbsp;
  <a href="#sample-run">Sample run</a> &nbsp;|&nbsp;
  <a href="#quick-start">Quick start</a> &nbsp;|&nbsp;
  <a href="#configuration">Configuration</a> &nbsp;|&nbsp;
  <a href="#roadmap">Roadmap</a>
</p>

</div>

<br>

<h2>See it in action</h2>

<p align="center"><img src="demo/demo.gif" alt="Terminal recording of Resume Screening Agent running on Google Gemini" width="100%"></p>

<p align="center"><sub>Recorded from a real run on Google Gemini (<code>gemini-3.5-flash-lite</code>) on 12 November 2026. Nothing is edited or scripted. Only the waiting time while the model thinks is shortened. <a href="demo/demo.mp4">Download the MP4</a>.</sub></p>

<h2>The problem</h2>

<p>A single job post can bring in hundreds of resumes. Recruiters skim each one for seconds, good candidates get missed, and the reasons behind a rejection are rarely written down.</p>

<p>A score on its own doesn't help. "72" tells a recruiter nothing. "72, four years of relevant Python but no cloud experience" lets them make a decision.</p>

<h2>What it does</h2>

<table>
  <tr><th align="left">Capability</th><th align="left">What that means in practice</th></tr>
  <tr><td><b>Ranked shortlist</b></td><td>Every resume is scored against the job description and the list comes back in order.</td></tr>
  <tr><td><b>Evidence, not just numbers</b></td><td>Each candidate gets specific strengths, specific gaps and a short summary, all tied to what the resume actually says.</td></tr>
  <tr><td><b>Bias safeguards</b></td><td>The prompt rules out age, gender, name, school, employer prestige and graduation year as signals.</td></tr>
  <tr><td><b>Fair to career changers</b></td><td>Relevant personal projects count as real experience. The sample data includes a career changer to test this.</td></tr>
  <tr><td><b>Spreadsheet export</b></td><td>The full results go to <code>output/ranked_candidates.csv</code>.</td></tr>
</table>

<h2>How it works</h2>

<pre>
job_description.txt + resumes/*.txt --&gt; model scores each resume (structured output)
                                                   |
                         ranked shortlist + strengths, gaps and summary --&gt; CSV
</pre>

<p>Each resume is scored separately against the job description. The result comes back as a Pydantic object with the name, score, strengths, gaps and summary, and the score is clamped to 0 to 100.</p>

<p>To screen for a different role, replace <code>data/job_description.txt</code> and the files in <code>data/resumes/</code>.</p>

<h2>Decisions I made on purpose</h2>

<h3>The bias instruction</h3>

<p>A model doesn't need to be told someone's age to be biased against them. Graduation year, a career gap, a bootcamp instead of a degree, or an unfamiliar employer all correlate with things unrelated to the job. Left alone, a model will quietly use them, so the prompt rules them out directly.</p>

<p>Stating it isn't proof, so the sample data tests it. One of the five resumes belongs to a former teacher six months into a career change, with a FastAPI project he built himself and no degree in the field. He should be judged on that work, not on the path he took.</p>

<h3>Built for compliance conversations</h3>

<p>Automated hiring tools are regulated in a growing number of places. The bias approach and the written reasoning are part of the deliverable, not an extra, and I raise them with a client before deployment, not after.</p>

<h2>Sample run</h2>

<pre>
$ python screen_candidates.py
Ranked shortlist:

1. Wei Chen (wei_chen.txt) - 91/100
   Strengths: 6 years leading backend teams on Python/Django and GCP; deep
   Postgres and API design; mentoring experience matches the nice-to-have
   Gaps: Seniority sits well above the mid-level target, likely a level
   or compensation mismatch

2. Maria Lopez (maria_lopez.txt) - 85/100
   Strengths: 4 years production Python and FastAPI; direct Postgres and
   AWS experience; has reviewed code for other engineers
   Gaps: No large-scale system design experience mentioned
</pre>

<h2>Quick start</h2>

<p>You need Python 3.12 or newer and an API key from OpenAI, Anthropic or Google Gemini.</p>

<pre>
pip install -r requirements.txt
cp .env.example .env        # on Windows: copy .env.example .env
# open .env and paste your API key
python screen_candidates.py
</pre>

<h2>Configuration</h2>

<p>Everything is set in <code>.env</code>. Copy <code>.env.example</code> to start.</p>

<table>
  <tr><th align="left">Variable</th><th align="left">Required</th><th align="left">Purpose</th></tr>
  <tr><td><code>LLM_MODEL</code></td><td>Yes</td><td>Which model to use, as <code>provider:model</code>. Default <code>openai:gpt-5.5</code>. Also works with <code>anthropic:claude-opus-5-5</code> or <code>google_genai:gemini-3.5-flash</code>.</td></tr>
  <tr><td><code>OPENAI_API_KEY / ANTHROPIC_API_KEY / GOOGLE_API_KEY</code></td><td>One of them</td><td>The key for whichever provider you picked.</td></tr>
</table>

<h2>Project structure</h2>

<pre>
recruiting-screening-agent/
  .env.example                                           # copy to .env and add your key
  case_study.md                                          # longer write-up of the design
  README.md
  requirements.txt                                       # dependencies
  screen_candidates.py                                   # screens every resume and prints the shortlist
  .git/
    COMMIT_EDITMSG
    config
    description
    HEAD
    hooks/applypatch-msg.sample
    hooks/commit-msg.sample
    hooks/fsmonitor-watchman.sample
    hooks/post-update.sample
    hooks/pre-applypatch.sample
    hooks/pre-commit.sample
    hooks/pre-merge-commit.sample
    hooks/pre-push.sample
    hooks/pre-rebase.sample
    hooks/pre-receive.sample
    hooks/prepare-commit-msg.sample
    hooks/push-to-checkout.sample
    hooks/sendemail-validate.sample
    hooks/update.sample
    index
    info/exclude
    logs/HEAD
    logs/refs/heads/main
    logs/refs/remotes/origin/main
    objects/08/6b6100f7918763f67a5ffd44f815202ec5cd1e
    objects/0a/a3e919369540be96480bc2730bf75c4f9f9492
    objects/0d/19a37d674a332b9dba9f34ec54f3144a81a21f
    objects/13/df72d287e6b11db618a976c14cb8ac433cc7eb
    objects/2a/eaa4af67a297cdb164a1f4dd061ab85154d5e7
    objects/48/f562655acea78d009f619bbd29769385880946
    objects/4b/8e0366d16c28c64a9c00f9058c36f6064c2e87
    objects/5f/03cc7fc374a543e01cee41ba306937fd05940c
    objects/6f/9f46f10d45edafeb3701b3bbddf77e1922e912
    objects/71/efd8b031d1f9bc244e96ef48c4310f55079258
    objects/78/613bb912fd5177040bc593fd1f8932de151010
    objects/78/998da0758f803a8b7d9b492206632524003f81
    objects/7a/3a4f0ab20b8170a7b714479283340f5fe09e10
    objects/7f/d1df9761c3294fcb5b79b84e2c1581211b58fe
    objects/80/b83ba80f29149a8662f8b7cef0d0516c6f1a8c
    objects/8a/48dd072be3bf8c820ee6384db3167eafb4fb1b
    objects/8e/8b702ac01cf23fd7fcd9ca64e2a10ac89ebc6b
    objects/a2/2992dd5a497d81f2c4d52d29bebebfab28c81d
    objects/a2/667477f906e25e4d46862b73a0cf1d10163a78
    objects/a4/93b49fd5a6f847273ae7d9c847f4f07ae67f4b
    objects/ae/5e34ffc1c5558f645ff8af4f9194400bcc81dd
    objects/ae/af811bb6f234c59581c34ea74add0b0a69691b
    objects/bb/1d0d20270c6b562a687dd6c5e21f3c4d7ba090
    objects/c5/4aeb32cf364cf433dfb7c8ce58583bc231b3a2
    objects/c5/97c23fa30e7a1e2dfac8278bb520f879e325c9
    objects/cb/c138741f76c8142b81d1884b0ff9e85cf76ce6
    objects/de/746f20e8d94bc4bca3a762ef31b38beac8dfce
    objects/e5/6d0464232e3f00c54b6317bcda0a87126ef783
    objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
    objects/fe/bef78fa2bbf9ca7578a856fb0958dce1d19148
    refs/heads/main
    refs/remotes/origin/main
  agent/
    llm.py                                               # picks the model from LLM_MODEL
    screening.py                                         # the scoring prompt and bias rules
  data/
    job_description.txt                                  # the role being hired for
    resumes/                                             # five sample resumes
  demo/
    demo.gif
    demo.mp4
  tests/                                                 # pytest suite, runs without any API key
</pre>

<h2>Built with</h2>

<p>Python &nbsp;&middot;&nbsp; LangChain &nbsp;&middot;&nbsp; Pydantic &nbsp;&middot;&nbsp; OpenAI / Anthropic / Gemini</p>

<h2>Tests</h2>

<pre>
pip install -r requirements-dev.txt
pytest
</pre>

<p>Three tests cover loading the job description and resumes, the bias instruction staying in the prompt, and score clamping. None of the tests call a model or need an API key, so they run on GitHub Actions on every push. The badge at the top shows the latest result.</p>

<h2>Roadmap</h2>

<p>What I would build next if a client took this into production:</p>
<ul>
  <li>PDF and Word resume parsing</li>
  <li>Pulling candidates straight from an ATS such as Greenhouse, Lever or Workable</li>
  <li>An audit log of every score and its reasoning, in case a decision is ever challenged</li>
  <li>Screening against several open roles at once</li>
</ul>

<h2>More from this series</h2>

<p>Nine production-minded AI agents, each solving one business problem properly.</p>

<table>
  <tr><td><a href="https://github.com/saqib-n/ai-research-report-agent"><b>Research Report Agent</b></a></td><td>Researches a topic, notices its own gaps, and writes a report with a source for every claim.</td></tr>
  <tr><td><a href="https://github.com/saqib-n/ai-sales-outreach-agent"><b>AI Sales Outreach Agent</b></a></td><td>Personalised cold emails and follow-ups, with a human approving every send.</td></tr>
  <tr><td><a href="https://github.com/saqib-n/ecommerce-automation-agent"><b>E-commerce Order and Inventory Agent</b></a></td><td>Shopify order, stock and returns assistant, plus a monitor that warns you before stock runs out.</td></tr>
  <tr><td><a href="https://github.com/saqib-n/email-triage-agent"><b>Email Triage Agent</b></a></td><td>Sorts an inbox into four buckets and gives each one a different level of autonomy.</td></tr>
  <tr><td><a href="https://github.com/saqib-n/lead-qualification-crm-agent"><b>Lead Qualification Agent</b></a></td><td>Scores inbound leads against your own rubric and pushes the good ones to HubSpot.</td></tr>
  <tr><td><a href="https://github.com/saqib-n/multi-agent-customer-support"><b>Multi-Agent Customer Support</b></a></td><td>A router plus specialist agents for orders, refunds, FAQs and human handoff.</td></tr>
  <tr><td><a href="https://github.com/saqib-n/rag-knowledge-base-agent"><b>RAG Knowledge Base Agent</b></a></td><td>Answers questions from your own documents and names the source for every answer.</td></tr>
  <tr><td><a href="https://github.com/saqib-n/whatsapp-support-agent"><b>WhatsApp Support Agent</b></a></td><td>A WhatsApp Cloud API agent that checks orders, answers FAQs and escalates to a person.</td></tr>
</table>

<h2>Work with me</h2>

<p>I'm Saqib Nawaz, founder of WolfXense AI. I build AI agents and automations for businesses, with Python, LangChain, LangGraph and n8n, and connect them to the tools teams already use, like CRMs, Shopify, Slack, email and WhatsApp.</p>

<p>If your hiring team spends days on first-pass screening, I can adapt this to your roles and your ATS, with the fairness and audit pieces built in from the start.</p>

<p><a href="https://www.upwork.com/freelancers/~01de008504a38baf28"><b>Hire me on Upwork</b></a> &nbsp;|&nbsp; <a href="https://github.com/saqib-n"><b>More of my work on GitHub</b></a></p>

<hr>

<p><sub>Released under the <a href="LICENSE">MIT License</a>. A longer write-up of the design is in <a href="case_study.md">case_study.md</a>.</sub></p>
