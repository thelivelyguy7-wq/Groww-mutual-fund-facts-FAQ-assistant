# Comprehensive Problem Statement: Mutual Fund FAQ Assistant (Facts-Only Q&A)

## 1. Executive Summary
The objective of this project is to design, develop, and deploy a facts-only, RAG-based (Retrieval-Augmented Generation) FAQ assistant for mutual fund schemes. Using **Groww** as the single real-time source distributor, the assistant will retrieve information exclusively from official public HTML pages for select HDFC Mutual Funds. 

The most critical constraint of this system is compliance: it must strictly avoid providing investment advice, opinions, predictions, or recommendations. The goal is to prioritize absolute factual accuracy and transparency over generative intelligence, ensuring every answer is source-backed.

---

## 2. Background and Motivation
In the fintech domain, retail investors frequently search for objective data points regarding mutual fund schemes (e.g., exit loads, expense ratios, lock-in periods). Customer support teams also spend significant time answering these repetitive queries. 
While LLMs are powerful, their tendency to hallucinate or offer unsolicited financial advice poses a massive regulatory and reputational risk. Therefore, there is a clear business need for a heavily constrained, "facts-only" RAG system that acts as a secure, reliable lookup tool rather than a financial advisor.

---

## 3. Core Objectives
1. **Factual Accuracy**: Answer verifiable queries about mutual fund schemes using exclusively approved, official documents.
2. **Strict Compliance**: Implement rigid guardrails to detect and refuse advisory, comparative, or speculative questions.
3. **Transparent Citations**: Provide exactly one clear source link and a "last updated" timestamp for every response to establish trust.
4. **Conciseness**: Restrict the generative output to a maximum of three sentences to prevent rambling and reduce hallucination surface area.

---

## 4. Target Audience & User Stories
### Retail Investors
- *Goal*: Quickly compare objective facts across different mutual funds without digging through lengthy PDF documents.
- *Example*: "What is the exit load if I redeem my HDFC Small Cap Fund within 6 months?"

### Customer Support & Content Teams
- *Goal*: Rapidly retrieve standardized, approved answers to resolve customer tickets faster.
- *Example*: "How do I download my capital gains statement for tax filing?"

---

## 5. Detailed Scope of Work

### 5.1 Corpus Definition
The system's knowledge base is restricted to a specific set of mutual fund schemes managed by **HDFC Asset Management Company**, using **Groww** as the single real-time product source. The system must scrape, chunk, and index **only** the official public HTML pages for the following schemes:

- **Selected Mutual Fund Schemes:**
  15 distinct HDFC Mutual Fund schemes (e.g., Small Cap, Large Cap, Balanced Advantage, Liquid, etc.)

*Note: The corpus contains 15 live HTML web pages representing these 15 schemes.*

### 5.2 Functional Requirements (FAQ Assistant)
- **Supported Query Types**: The system must accurately answer queries regarding:
  - Expense ratios, exit loads, and NAVs (from the scraped context).
  - Minimum SIP and Lumpsum investment amounts.
  - ELSS lock-in periods and tax implications.
  - Riskometer classifications and benchmark indices.
  - Administrative processes (e.g., downloading statements).
- **Response Formatting Enforcements**:
  - Maximum length of 3 sentences.
  - Inclusion of exactly one source hyperlink.
  - Mandatory footer: `"Last updated from sources: <date>"`

### 5.3 Non-Functional Requirements
- **Minimal User Interface**: The UI should be clean, distraction-free, and feature a welcome message, 3 example questions, and a highly visible disclaimer: *"Facts-only. No investment advice."*
- **Statelessness**: The system does not need to remember long conversational histories. Each query is treated as an independent lookup to prevent context-bleeding and hallucination.

---

## 6. Key Constraints and Guardrails

To ensure strict compliance and data security, the system must adhere to the following key constraints:

1. **Public sources only.** No screenshots of the app back-end; no third-party blogs as sources. The system relies entirely on official, live public HTML pages from Groww.
2. **No PII.** Do not accept/store PAN, Aadhaar, account numbers, OTPs, emails, or phone numbers. The system architecture is completely stateless and performs zero PII logging.
3. **No performance claims.** Don’t compute/compare returns; link to the official factsheet (or public Groww source page) if asked. 
4. **Clarity & transparency.** Keep answers ≤3 sentences; add “Last updated from sources: <date>” footer to every response along with the direct source hyperlink.

---

## 7. Refusal Handling Strategy
Handling queries that violate constraints is as important as answering valid queries. 
- **Trigger**: When a user asks an advisory question (e.g., "Should I invest in HDFC Large Cap?").
- **Action**: The system must politely refuse.
- **Required Format**:
  - Clear, non-combative refusal.
  - Reiteration of the system's "facts-only" limitation.
  - Provision of an educational link (e.g., SEBI or AMFI investor education page).

---

## 8. Expected Deliverables
1. **Knowledge Base (Vector DB)**: Processed and chunked data from the 15 real-time Groww HTML pages.
2. **RAG Backend System**: The logic encompassing retrieval, guardrails, prompt enforcement, and generation.
3. **User Interface**: A beautifully designed React frontend using the Stitch MCP prototype.
4. **Documentation**:
   - `Architecture.md` (System design and pipeline)
   - `README.md` (Setup instructions, known limitations, and RAG approach summary).

---

## 9. Success Criteria
The project will be considered successful if it achieves:
1. **0% Advice Rate**: Passes adversarial testing where the system refuses 100% of queries asking for recommendations.
2. **High Retrieval Accuracy**: Correctly fetches facts like expense ratios for the specified funds without mixing up data between similar funds.
3. **Format Adherence**: Consistently provides the single citation link and the mandatory footer in every factual response.
4. **User Experience**: Delivers a clean, fast, and highly transparent lookup experience.
