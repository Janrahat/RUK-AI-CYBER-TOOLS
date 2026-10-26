"""Optional AI helper; offline fallback is available without an API key."""
import requests, config
def ask(question):
    question=question.strip()
    if not question: return "Enter a question first."
    if not config.AI_API_KEY: return ("Offline assistant: I can help interpret URL checks, DNS results, SSL details, and HTTP headers. Configure AI_API_KEY in your .env file to enable remote AI explanations. Never paste passwords, tokens, or private keys here.")
    try:
        response=requests.post(config.AI_API_URL,headers={"Authorization":f"Bearer {config.AI_API_KEY}","Content-Type":"application/json"},json={"model":config.AI_MODEL,"messages":[{"role":"system","content":"You are a defensive cybersecurity assistant. Help only with authorized security work. Never request secrets."},{"role":"user","content":question}],"temperature":0.2},timeout=25)
        response.raise_for_status(); data=response.json(); return data["choices"][0]["message"]["content"]
    except Exception as exc: return f"AI request failed safely: {exc}. Check the provider URL, model, API key, and network."
