#!/usr/bin/env python3
"""
PDF Q&A Bot (Mock-friendly)
- Loads plain .txt files by default (no external deps).
- If PyPDF2 is installed, it can also read PDFs.
- Uses a naive keyword-overlap ranking for retrieval (no embeddings required).

Run:
  python pdf_bot.py --docs docs_folder
Then ask questions.
"""
import os
import argparse

def read_text_from_file(path: str) -> str:
    if path.lower().endswith(".pdf"):
        try:
            import PyPDF2  # type: ignore
            text = ""
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"[warn] Could not read PDF '{path}': {e}. Skipping.")
            return ""
    else:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"[warn] Could not read file '{path}': {e}. Skipping.")
            return ""

def tokenize(text: str):
    return [w.lower() for w in text.split()]

def jaccard(a, b):
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)

def build_corpus(folder: str):
    corpus = []
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if os.path.isfile(path) and (name.lower().endswith(".txt") or name.lower().endswith(".pdf")):
            text = read_text_from_file(path)
            if text.strip():
                corpus.append((name, text, tokenize(text)))
    print(f"[info] Loaded {len(corpus)} docs from {folder}")
    return corpus

def answer_question(corpus, question: str, top_k: int = 2) -> str:
    q_tokens = tokenize(question)
    ranked = sorted(corpus, key=lambda x: jaccard(x[2], q_tokens), reverse=True)[:top_k]
    context = "\n---\n".join([f"[{name}]\n{text[:800]}" for (name, text, _) in ranked])
    # Mock "LLM": concatenate top contexts + a heuristic answer
    return f"Top matches:\n{context}\n\nAnswer (mock): Based on the most relevant passages above."

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", required=False, default=".", help="Folder with .txt or .pdf files")
    args = parser.parse_args()

    corpus = build_corpus(args.docs)
    if not corpus:
        print("No documents found. Put some .txt or .pdf files in the folder and try again.")
        return

    print("=== PDF Q&A (Mock) ===")
    print("Ask a question (type 'exit' to quit).")
    while True:
        q = input("Q: ").strip()
        if q.lower() in ("exit", "quit"):
            break
        print(answer_question(corpus, q), "\n")

if __name__ == "__main__":
    main()
