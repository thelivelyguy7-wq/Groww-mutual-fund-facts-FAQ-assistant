---
title: Mutual Fund FAQ
emoji: 📈
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---

# Mutual Fund FAQ Assistant (Facts-Only RAG)

A highly constrained, strictly compliant Retrieval-Augmented Generation (RAG) system built to answer factual queries about HDFC Mutual Funds using live data from Groww.

## Project Scope
- **Asset Management Company**: HDFC AMC
- **Data Source**: Official public HTML pages from [Groww.in](https://groww.in)
- **Schemes Indexed**: 15 distinct HDFC Mutual Fund schemes (e.g., Small Cap, Large Cap, Balanced Advantage, Liquid, etc.). See `sources.md` for the full list of indexed URLs.

## Known Limits & Guardrails
- **No Performance Computation**: The system will NOT compute, predict, or compare future returns.
- **Strictly Factual**: The system cannot offer investment advice. Advisory queries trigger a hard refusal.
- **Sentence Limit**: Every response is artificially constrained to a maximum of 3 sentences.
- **No PII**: The architecture is 100% stateless. It does not collect, log, or accept personal identifiable information (PAN, Aadhaar, OTPs, etc.).

## Setup Steps

### Prerequisites
- Python 3.12+
- Node.js (Optional, our frontend currently uses CDNs)
- Groq API Key

### Installation
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv` and activate it.
3. Install dependencies: `pip install -r requirements.txt`.
4. Install Playwright browsers: `playwright install chromium`.
5. Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

### Running the System
The system is decoupled into a FastAPI backend and a React (CDN) frontend.

1. **Start the Backend API:**
   ```bash
   python src/api.py
   ```
   *The server will start on `http://localhost:8000`.*

2. **Start the Frontend UI:**
   In a new terminal window, run:
   ```bash
   python -m http.server 8001 --directory frontend
   ```
   *Navigate to `http://localhost:8001` in your browser.*

### Data Ingestion Pipeline (Optional)
If you want to manually refresh the vector database with the latest NAVs and exit loads:
```bash
python src/scraper.py
python src/cleaner.py
python src/indexer.py
```
*(Note: This pipeline is also automated via a GitHub Actions cron job that runs daily at 9:15 AM IST).*

## Compliance UI Disclaimer
The frontend features a hardcoded, highly visible disclaimer banner to ensure complete transparency with the retail user. 
**Snippet used in UI (`frontend/index.html`):**
```html
<div className="bg-yellow-50 border-b border-yellow-200 px-4 py-2 text-center text-sm text-yellow-800 font-medium z-10 w-full flex items-center justify-center gap-2 shadow-sm">
    ⚠️ Disclaimer: Facts-only. No investment advice.
</div>
```

