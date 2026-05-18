import ollama
from config import OLLAMA_MODEL, OLLAMA_HOST

class Brain:
    def __init__(self, system_prompt=None):
        self.model = OLLAMA_MODEL
        ollama_client = ollama.Client(host=OLLAMA_HOST)
        self.client = ollama_client
        self.system_prompt = system_prompt or "You are Vikram, a helpful AI assistant. Be concise and direct."
        self.history = []

    def think(self, user_input, context=None):
        messages = [{"role": "system", "content": self.system_prompt}]
        for h in self.history[-10:]:
            messages.append(h)
        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})
        messages.append({"role": "user", "content": user_input})

        response = self.client.chat(model=self.model, messages=messages)
        reply = response["message"]["content"]

        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": reply})

        return reply.strip()

    def classify_intent(self, user_input):
        prompt = f"""Classify this request into EXACTLY ONE category:
- system: open/close apps, control volume/brightness, system info
- web: search, weather, news
- remind: set reminder, timer
- memory: remember, recall, store
- chat: general conversation, questions

Request: {user_input}
Category:"""
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"].strip().lower()

    def clear_history(self):
        self.history = []
