## Overview
🚀 **Gen-AI Powered Cold Email Generator** – AI-powered outreach for business development

This project generates **highly personalized cold emails** by scraping job descriptions from company career pages, extracting structured job data with an LLM, matching skills to your **personal portfolio**, and then composing a tailored email.

Leveraging **Llama 3.3 (via Groq Cloud)**, **LangChain**, and **ChromaDB**, the app turns a single job URL into a convincing, context-aware outreach email that highlights the most relevant parts of your portfolio.

Whether you're in **business development, freelancing, or recruitment**, this tool helps you:

- Understand what a company is hiring for
- Match their needs with your skills/portfolio
- Generate a ready-to-send cold email

---

## Workflow Overview

### High-Level Flow

1. **User Input**  
   - You provide a **job URL** in the Streamlit UI.

2. **Web Scraping & Cleaning**  
   - The app uses `WebBaseLoader` to scrape the page content.  
   - `clean_text()` (in `utils.py`) removes HTML, URLs, and noise.

3. **LLM: Job Extraction (JSON)**  
   - The cleaned text is passed to `Chain.extract_jobs()`.  
   - Llama 3.3 (via Groq) extracts job postings into **JSON** with:
     - `role`
     - `experience`
     - `skills`
     - `description`

4. **Mini-RAG: Portfolio Matching with ChromaDB**  
   - Only the **`skills`** field from the JSON is used for retrieval.  
   - `Portfolio.load_portfolio()` loads `my_portfolio.csv` into ChromaDB as a vector collection (`portfolio`).  
   - `Portfolio.query_links(skills)` queries ChromaDB with those skills and returns the **most relevant portfolio links**.

5. **LLM: Cold Email Generation**  
   - For each extracted job:
     - The full job JSON (`role`, `experience`, `skills`, `description`)
     - plus the retrieved portfolio `links`
   - are passed to `Chain.write_mail()`.
   - The LLM writes a **personalized cold email** introducing AtliQ, referencing the job and including relevant portfolio links.

6. **UI Output**  
   - Streamlit displays each generated email in a code-style block for easy copy/paste.


## Cover Image
![Cover Image](<output_cold_email.png>)

## Tech Stack
- 🧠 **Llama-3.3-70B** (via Groq Cloud) – LLM used for job extraction & email generation  
- 🔗 **LangChain** – Prompt orchestration and LLM pipeline  
- 📊 **Comet Opik** – LLM observability, tracing, prompt versioning & online evaluation  
- 🗃️ **ChromaDB** – Vector database for portfolio management  
- 🐍 **Python** – Backend scripting  
- 🔒 **python-dotenv** – Secure API key management


## Monitoring & Evaluation (Opik)

This project is instrumented with **Comet Opik** for LLM observability:

- Each run logs two traces:
  - `extract_jobs` – JSON extraction from the careers page
  - `write_mail` – final cold-email generation
- Traces are tagged with prompt versions, e.g.:
  - `prompt_kind:extract`, `extract_v1_basic`
  - `prompt_kind:email`, `email_v1_personal_bullets`

Online evaluation:

- A rule `email_quality` scores each generated email (0–1) using an LLM-as-judge.
- You can analyze scores per prompt version in the **Traces** and **Metrics** tabs in Opik.

To enable Opik:

1. Install Opik: `pip install opik`
2. Run `opik configure` and choose your workspace.
3. Set the `OPIK_API_KEY` in your environment (or use the config file created by the CLI).


## Project Structure
```
generate_email_with_llm/
│── app/
│ ├── pycache/ # Python cache files (ignored in git)
│ ├── resource/
│ │ └── my_portfolio.csv # Portfolio CSV used to build the vector store
│ ├── vectorstore/ # ChromaDB persistent storage (auto-created)
│ ├── .env # Local environment variables (NOT committed)
│ ├── .env.example # Example env file for users to copy & fill
│ ├── chains.py # LLM chains (job extraction + email generation)
│ ├── main.py # Streamlit entrypoint for the UI
│ ├── portfolio.py # Portfolio loading + ChromaDB retrieval
│ └── utils.py # Helper functions (e.g., text cleaning)
│
├── .gitignore # Ignore .env, cache, etc.
├── Dockerfile # Docker configuration for containerized runs
├── output_cold_email.png # Cover image for README
├── README.md # Project documentation
└── requirements.txt # Python dependencies
```

## Installation & Setup

You can run this project in two ways:

1. Using a **local Python environment** (simpler if you’re comfortable with Python)
2. Using **Docker** (no local Python needed, fully reproducible)

---

### 🔹 Option 1 — Local Python Environment



```bash
git clone https://github.com/uddipan77/generate_email_with_llm.git
cd generate_email_with_llm
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
cp app/.env.example app/.env
GROQ_API_KEY=your_groq_api_key_here
OPIK_API_KEY=your_opik_api_key_here   # optional, for Opik monitoring
streamlit run app/main.py
```

### 🔹 Option 2 — Run with Docker

```bash
git clone https://github.com/uddipan77/generate_email_with_llm.git
cd generate_email_with_llm
cp app/.env.example app/.env
GROQ_API_KEY=your_groq_api_key_here
OPIK_API_KEY=your_opik_api_key_here   # optional, for Opik monitoring
docker build -t cold-email-generator .
docker run --env-file app/.env -p 8501:8501 cold-email-generator
```

## Notes
- 🔑 **API Key**: Make sure to update the `.env` file with your API key according to your model.








