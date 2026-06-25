# Replyze

AI-powered reply generator for customer messages across all platforms.

## Features
- Paste a review/message → get an AI reply in seconds
- Works on Google Maps, WhatsApp, Instagram, Facebook, Twitter, Email
- Tone control (formal to casual)
- Language support (11 languages)
- Reply history & editable replies
- PWA (installable on phone)

## Tech Stack
- **Backend:** Flask + Python
- **AI:** Anthropic Claude API (claude-haiku-4-5)
- **Database:** SQLite
- **Frontend:** Vanilla HTML/CSS/JS
- **Auth:** Google OAuth + email/password
- **Deployment:** Render
- **Pricing:** PPP (Pay-Per-Person) — ₹299 India, $19 USA, etc.

## Getting Started
```bash
git clone https://github.com/titanium10/replyze
cd replyze
pip install -r requirements.txt
export SECRET_KEY=your-secret
export GOOGLE_CLIENT_ID=your-client-id
export GOOGLE_CLIENT_SECRET=your-secret
export ANTHROPIC_API_KEY=your-api-key
python app.py
```

Visit `http://localhost:5001`

## Live Demo
https://replyze.onrender.com

## Built by
14-year-old developer [@samratbuilds](https://x.com/samratbuilds)
