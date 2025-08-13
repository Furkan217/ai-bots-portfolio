# AI Bots Portfolio (Mock-friendly)

This portfolio contains **three small, self-contained AI bot demos** you can run locally **without any API keys** (mock mode). 
They showcase prior work patterns: personality + affection systems, layered memory, and document Q&A.

> Created: 2025-08-13

## Contents
1. **Flirty Companion Bot** (`1_flirty_companion_bot/`) — console chatbot with *personality* and *affection (1–5)* tracking. Mock by default, optionally works with `xai-sdk` if configured.
2. **Memory AI Demo** (`2_memory_ai_demo/`) — layered memory (short/mid/long) with context window rendering.
3. **PDF Q&A Bot** (`3_pdf_qa_bot/`) — loads .txt or PDFs (if PyPDF2 installed) and answers questions using simple retrieval.

---

## 1) Flirty Companion Bot
**Folder:** `1_flirty_companion_bot/`

**Run (mock mode, no keys):**
```bash
cd 1_flirty_companion_bot
pip install -r requirements.txt
python bot.py
```

**Optional (try Grok later):**
```bash
# pip install xai-sdk  # uncomment if you have access
export XAI_API_KEY=your_key_here
python bot.py
```

**What it shows**
- Personality via `personality.json`
- Affection tracking (1–5) based on keywords/sentiment heuristics
- Conversation loop with fallback to mock LLM

---

## 2) Memory AI Demo
**Folder:** `2_memory_ai_demo/`

**Run:**
```bash
cd 2_memory_ai_demo
pip install -r requirements.txt
python demo.py
```

**What it shows**
- Short memory with TTL & FIFO
- Mid memory topic snapshot
- Long memory fact capture
- Context window rendering

---

## 3) PDF Q&A Bot (Mock)
**Folder:** `3_pdf_qa_bot/`

**Run:**
```bash
cd 3_pdf_qa_bot
pip install -r requirements.txt  # optional
python pdf_bot.py --docs ./
```
Put some `.txt` or `.pdf` files in the folder. If `PyPDF2` is installed, PDFs will be parsed; otherwise `.txt` files will be used.

**What it shows**
- Document loading
- Simple keyword-overlap retrieval
- Mock answer generation using top-ranked passages

---

## Notes
- These demos are **safe to share** publicly: no API keys, no proprietary data.
- Each module is easy to extend with real LLM calls (OpenAI/Anthropic/xAI) where commented.
- Ideal for showcasing **previous bot work** in proposals.
