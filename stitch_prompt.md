# Stitch MCP Prompt for Groww Mutual Fund Assistant

Please copy and paste the following prompt directly into the Google Stitch UI to generate the React frontend for this project:

---

**PROMPT:**

Design and generate a premium React web application for a Mutual Fund FAQ assistant. 

**1. Design Language & Aesthetics**
- Fully replicate the "Groww" brand identity. Use their signature teal/cyan accent colors, clean rounded borders, and a minimalist, distraction-free chat layout.
- Use a modern font (e.g., Inter or Roboto).

**2. Strict Compliance Requirements**
- A highly visible disclaimer banner must be permanently pinned to the top of the chat interface reading: **"⚠️ Disclaimer: Facts-only. No investment advice."** The banner should be styled with a yellow/warning background.

**3. API Integration**
- The chat input must send user messages via `POST` requests to `http://localhost:8000/api/chat`.
- Implement loading states (e.g., a flashing dot micro-animation) while waiting for the response.

**4. Markdown & Citation Parsing**
- The backend will return responses in Markdown format containing hyperlinks and italicized source footers. You must integrate a markdown parser (like `react-markdown` or `marked`) so the citations render as beautiful, clickable HTML links within the chat bubbles.

**5. Empty State**
- Before the user types anything, display 3 clickable example question pills (e.g., "What is the exit load for HDFC Small Cap?"). Clicking a pill should instantly send that query to the backend.

---
