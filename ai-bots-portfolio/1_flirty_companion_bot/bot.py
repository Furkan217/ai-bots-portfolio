#!/usr/bin/env python3
"""
Flirty Companion Bot (Console)
- Mock-friendly: works without API keys.
- If xai-sdk is installed and XAI_API_KEY is set, it will try to use Grok; otherwise uses MockLLM.

Run:
  pip install -r requirements.txt
  python bot.py
Env:
  XAI_API_KEY=...  (optional)
"""
import os
import json
from dataclasses import dataclass, field
from typing import List

try:
    # Optional dependency; if missing, we use mock
    from xai import AsyncClient as XAIAsyncClient  # type: ignore
except Exception:
    XAIAsyncClient = None

from dotenv import load_dotenv
load_dotenv()

@dataclass
class Message:
    role: str
    content: str

@dataclass
class AffectionSystem:
    level: int = 2  # 1..5
    pos_keywords: List[str] = field(default_factory=list)
    neg_keywords: List[str] = field(default_factory=list)

    def update(self, user_text: str) -> None:
        text = user_text.lower()
        delta = 0
        for kw in self.pos_keywords:
            if kw in text:
                delta += 1
        for kw in self.neg_keywords:
            if kw in text:
                delta -= 1
        if "sorry" in text or "apologize" in text:
            delta += 1
        # clamp level
        self.level = max(1, min(5, self.level + (1 if delta > 0 else (-1 if delta < 0 else 0))))

    def tag(self) -> str:
        return f"[affection:{self.level}]"

class MockLLM:
    def __init__(self, persona_name: str, style: str):
        self.persona_name = persona_name
        self.style = style

    def chat(self, sys_prompt: str, messages: List[Message], affection_level: int) -> str:
        # Simple mock reply using last user message
        user_last = ""
        for m in reversed(messages):
            if m.role == "user":
                user_last = m.content
                break
        base = "Hehe~" if affection_level >= 4 else "Hmm,"
        tail = " 💫" if affection_level >= 3 else ""
        return f"{base} I'm {self.persona_name}, your {self.style} companion. You said: '{user_last}'. Ask me more?{tail}"

class GrokClient:
    def __init__(self):
        self.key = os.getenv("XAI_API_KEY")
        self.enabled = bool(self.key and XAIAsyncClient is not None)
        self.client = None

    async def _ensure(self):
        if not self.enabled:
            return False
        if self.client is None:
            self.client = XAIAsyncClient(api_key=self.key)  # type: ignore
        return True

    async def chat(self, sys_prompt: str, messages: List[Message]) -> str:
        # If not enabled, raise to let caller fallback
        if not await self._ensure():
            raise RuntimeError("Grok not available")
        # Pseudo-call; adjust to actual xAI SDK signature if needed.
        # Here we just echo for safety in mock environment.
        text = ""
        for m in messages:
            text += f"{m.role.upper()}: {m.content}\n"
        return f"[Grok mock] Based on prompt: {sys_prompt[:80]}... | Msgs: {len(messages)}\n{text[-120:]}"
        # In real code: await self.client.chat.completions.create(...)

def build_system_prompt(p):
    rules = "\n".join(f"- {r}" for r in p["rules"])
    return f"""You are {p['name']}, a {p['style']} companion.
Follow these rules:
{rules}
Respond in 1-3 sentences.
"""

def main():
    # Load personality
    here = os.path.dirname(__file__)
    with open(os.path.join(here, "personality.json"), "r", encoding="utf-8") as f:
        persona = json.load(f)

    affection = AffectionSystem(
        level=2,
        pos_keywords=persona.get("keywords_positive", []),
        neg_keywords=persona.get("keywords_negative", []),
    )
    sys_prompt = build_system_prompt(persona)
    messages: List[Message] = [Message(role="system", content=sys_prompt)]
    mock = MockLLM(persona_name=persona["name"], style=persona["style"])
    grok = GrokClient()

    print("=== Flirty Companion Console (Mock-friendly) ===")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            user = input("You: ").strip()
        except EOFError:
            break
        if user.lower() in ("exit", "quit"):
            break

        affection.update(user)
        messages.append(Message(role="user", content=user))

        # Try Grok, fallback to mock
        reply = None
        if grok.enabled:
            try:
                # In this offline demo, GrokClient returns a mock string.
                # Replace with actual SDK call when running with real xAI credentials.
                import asyncio
                reply = asyncio.run(grok.chat(sys_prompt, messages[-8:]))
            except Exception:
                reply = None

        if reply is None:
            reply = mock.chat(sys_prompt, messages[-8:], affection.level)

        # Append assistant message
        messages.append(Message(role="assistant", content=reply))
        print(f"Raven {affection.tag()}: {reply}\n")

if __name__ == "__main__":
    main()
