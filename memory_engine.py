#!/usr/bin/env python3
"""
Memory Engine Demo (Short/Mid/Long) - No external services.
Simulates layered memory with different retention policies.
"""
from dataclasses import dataclass, field
from typing import Deque, List, Tuple
from collections import deque
import time

@dataclass
class MemoryItem:
    role: str
    text: str
    ts: float

class ShortMemory:
    def __init__(self, max_items: int = 20, min_keep: int = 3, ttl_seconds: int = 36*3600):
        self.max_items = max_items
        self.min_keep = min_keep
        self.ttl = ttl_seconds
        self.data: Deque[MemoryItem] = deque()

    def add(self, role: str, text: str):
        self.data.append(MemoryItem(role, text, time.time()))
        self._trim()

    def _trim(self):
        # Keep last min_keep
        while len(self.data) > self.max_items:
            self.data.popleft()
        # TTL drop (except last min_keep)
        while len(self.data) > self.min_keep and self.data and (time.time() - self.data[0].ts) > self.ttl:
            self.data.popleft()

    def recent(self, k: int = 8) -> List[Tuple[str, str]]:
        return [(m.role, m.text) for m in list(self.data)[-k:]]

class MidMemory:
    def __init__(self):
        self.topics: List[str] = []  # pseudo-topic store

    def consider(self, text: str):
        # naive topic extraction
        words = [w.lower() for w in text.split() if len(w) > 4]
        for w in words:
            if w not in self.topics:
                self.topics.append(w)

    def snapshot(self) -> List[str]:
        return self.topics[-10:]

class LongMemory:
    def __init__(self):
        self.facts: List[str] = []

    def consider(self, text: str):
        # store simple facts using heuristic
        if "i am" in text.lower() or "my name is" in text.lower():
            self.facts.append(text.strip())

    def summary(self) -> str:
        if not self.facts:
            return "No long-term facts yet."
        return "Long-term facts:\n- " + "\n- ".join(self.facts[-10:])

class MemoryEngine:
    def __init__(self):
        self.short = ShortMemory()
        self.mid = MidMemory()
        self.long = LongMemory()

    def ingest(self, role: str, text: str):
        self.short.add(role, text)
        if role == "user":
            self.mid.consider(text)
            self.long.consider(text)

    def context_window(self) -> str:
        lines = [f"{r.upper()}: {t}" for (r, t) in self.short.recent(8)]
        return "\n".join(lines)

def demo():
    eng = MemoryEngine()
    print("=== Memory Engine Demo ===")
    samples = [
        ("user", "Hi, my name is Alex."),
        ("assistant", "Nice to meet you, Alex."),
        ("user", "I am working on an AI project."),
        ("assistant", "That sounds exciting."),
        ("user", "By the way, I love flirty anime chatbots."),
        ("assistant", "Good to know 😄"),
    ]
    for r, t in samples:
        eng.ingest(r, t)
    print("\n[Context Window]\n", eng.context_window())
    print("\n[Mid Topics]\n", eng.mid.snapshot())
    print("\n[Long Summary]\n", eng.long.summary())

if __name__ == "__main__":
    demo()
