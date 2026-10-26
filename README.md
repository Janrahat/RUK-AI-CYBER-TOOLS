# RUK AI CYBER TOOLS

A Python cybersecurity helper for **Termux and Kali Linux**, with a Rich terminal menu and a Flask web dashboard. Includes URL heuristics, DNS lookup, TLS certificate inspection, HTTP security-header checks, IP address classification, an optional AI API, and privacy-notice-based link analytics.

## Safety and limits
- Only assess websites and systems you own or are authorized to test.
- URL checks are heuristics, not a definitive malware verdict.
- The dashboard binds to `127.0.0.1` by default. Do not expose it publicly without authentication, HTTPS, and production hardening.
- Visitors see a privacy notice before continuing. Optional referral-domain analytics require explicit opt-in.
- No precise location, device fingerprint, passwords, or private messages are collected.

## Install on Termux
```bash
pkg update && pkg upgrade -y
pkg install python git -y
cd ruk-ai-cyber-tools
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
python -m unittest discover -s tests -v
python main.py
```

## Install on Kali Linux
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
cd ruk-ai-cyber-tools
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
python -m unittest discover -s tests -v
python main.py
```

## Web dashboard
Run `python app.py`, then open `http://127.0.0.1:8080` on the same device.

## Optional AI
Edit `.env` and set `AI_API_KEY`, `AI_API_URL`, and `AI_MODEL` for a compatible chat-completions API. Keep `.env` private; it is ignored by Git. Never commit API keys. Without a key, an offline fallback is used.

## Configuration
`RUK_HOST` defaults to `127.0.0.1`; `RUK_PORT` defaults to `8080`; `RUK_DATABASE` selects the SQLite file; `RUK_SECRET_KEY` should be replaced with a long random secret; `RUK_PUBLIC_BASE_URL` is optional.

## Before public deployment
The dashboard has no administrator login. Add authentication, CSRF protection, HTTPS, secret management, abuse prevention, and a production WSGI server before public deployment.

## Tests
```bash
python -m unittest discover -s tests -v
```
