#!/usr/bin/env python3
from memory_engine import MemoryEngine

def main():
    eng = MemoryEngine()
    print("Type 'exit' to quit.")
    while True:
        msg = input("You: ").strip()
        if msg.lower() in ("exit", "quit"):
            break
        eng.ingest("user", msg)
        # Trivial assistant reply (mock). Replace with LLM if desired.
        reply = "I hear you. (mock reply)"
        eng.ingest("assistant", reply)
        print("Bot:", reply)
        print("--- Context ---")
        print(eng.context_window())
        print("----------------\n")

if __name__ == "__main__":
    main()
