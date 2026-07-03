# Implementation Plan: Mutual Fund FAQ Assistant

This document outlines the phase-wise execution plan used to build the live-web RAG chatbot based on our finalized architecture.

## Execution Status

### [x] Phase 1: Environment Setup & Project Scaffolding
- **Goal**: Initialize the Python environment and install dependencies.
- **Actions**:
  - `[x]` Created `requirements.txt` containing: `langchain`, `langchain-groq`, `langchain-huggingface`, `chromadb`, `playwright`, `beautifulsoup4`, `streamlit`, `python-dotenv`, `sentence-transformers`.
  - `[x]` Set up basic project directory structure (`/data/raw`, `/data/processed`, `/data/chroma_db`, `/src`).
  - `[x]` Configured the `.env` file with necessary API keys (Groq).

### [x] Phase 2: Data Ingestion Pipeline (Offline)
- **Goal**: Scrape and parse the 15 target Groww Mutual Fund URLs (representing the HDFC schemes).
- **Actions**:
  - `[x]` **`urls.json`**: Defined the 15 exact Groww URLs for HDFC mutual funds.
  - `[x]` **`src/scraper.py`**: Rewrote the scraper to use **headless Playwright**. This was a critical pivot necessary to bypass Cloudflare bot protections and wait for the React/Next.js frontend to fully render the dynamic financial tables before extracting the raw HTML.
  - `[x]` **`src/cleaner.py`**: Developed a **BeautifulSoup** script to ingest the raw HTML. It actively strips out non-content tags (`<script>`, `<style>`, `<nav>`, `<footer>`) and specifically iterates over `<table>` elements to format rows/cells cleanly into text, ensuring facts like Expense Ratio and Exit Load are preserved.

### [x] Phase 3: Chunking & Vector Database Setup
- **Goal**: Process the extracted text into semantic chunks and store them in ChromaDB.
- **Actions**:
  - `[x]` **`src/indexer.py`**: Rebuilt to wipe the old PDF ChromaDB and instantiate a fresh one. It uses the `RecursiveCharacterTextSplitter` (chunk size = 1000, overlap = 200). 
  - `[x]` **Metadata Injection**: Each chunk is prepended with the "Fund Name:" to guarantee semantic isolation. The `metadata` payload attaches the exact `source_url`.
  - `[x]` **Embedding Strategy**: Used `BAAI/bge-small-en-v1.5`. Because our chunks are heavily constrained (<250 tokens), this 384-dimensional small model provides flawless, fast semantic matching.

### [x] Phase 4: Query Pipeline & LLM Integration (Online)
- **Goal**: Build the RAG retrieval logic, guardrails, and LLM prompt.
- **Actions**:
  - `[x]` **`src/rag_pipeline.py`**: 
    - **Query Classifier**: Rejects advisory queries immediately with a refusal template using a heuristic keyword matcher.
    - **Retriever**: Performs an initial broad semantic search over ChromaDB (top 15 chunks).
    - **Cross-Encoder Reranker**: Passes the 15 chunks to `cross-encoder/ms-marco-MiniLM-L-6-v2` to rigorously score and filter down to the absolute top 3 most relevant chunks.
    - **Generator**: Connects to Groq (`llama-3.1-8b-instant`). Uses a strict System Prompt limiting answers to a max of 3 sentences and prohibiting advice.
    - **Citation Post-Processing**: Programmatically intercepts the LLM output to append the hyperlinked Groww `source_url` and the `"Last updated from sources: <date>"` footer.

### [x] Phase 5: Frontend Interface Development
- **Goal**: Build the user-facing React application.
- **Actions**:
  - `[x]` **Stitch MCP UI**: Pivoted to a beautiful, React-based Single Page Application (SPA) generated via Google Stitch. Added the required disclaimer: **"Facts-only. No investment advice."** Provided 3 clickable example questions and connected the frontend via POST requests to the FastAPI backend.

### [x] Phase 6: Automated Evaluation (Enterprise)
- **Goal**: Systematically evaluate the RAG pipeline to prevent regressions.
- **Actions**:
  - `[x]` **`src/eval.py`**: Developed a custom automated evaluator using Groq as an LLM-as-a-judge. It runs a set of golden queries through the pipeline and scores the final output on **Faithfulness** (ensuring no hallucinations occur relative to the retrieved context).

### [ ] Phase 7: Automated Ingestion Scheduler
- **Goal**: Ensure the RAG database stays synchronized with the live Groww platform on a daily basis.
- **Actions**:
  - `[ ]` **`.github/workflows/ingestion.yml`**: Create a GitHub Actions workflow with a cron trigger (`schedule: - cron: '45 3 * * *'`) that automatically provisions an Ubuntu runner, installs Playwright dependencies, and executes the offline ingestion pipeline (`scraper.py` -> `cleaner.py` -> `indexer.py`) at 9:15 AM IST every day.
  - `[ ]` **Incremental Updates**: Ensure the vector database gracefully updates rather than drops existing data, or implement a safe database swap to prevent downtime during the nightly update.

---

## Verification Plan

### Automated / Scripted Tests
- `[x]` Run `scraper.py` and verify that the HTML outputs exist, bypassing Cloudflare.
- `[x]` Verify `cleaner.py` successfully extracts textual representations of HTML tables.
- `[x]` Verify `indexer.py` correctly embeds chunks and attaches the live Groww URLs as metadata.
- `[x]` Run `eval.py` to confirm the pipeline achieves high faithfulness scores.

### Manual Verification
- **Test Factual Query**: Ask "What is the exit load for HDFC Small Cap?" -> System fetches context, returns <3 sentences, and links directly to the live Groww page.
- `[ ]` **Test Advisory Guardrail**: Ask "Should I invest in HDFC Large Cap?" -> Verify the system gracefully refuses and provides an educational link.
