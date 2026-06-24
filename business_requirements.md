# Business Requirements — Multi-Deployment Demo App

## Project Goal

Build a small demo web application and deploy the same product through multiple
technology stacks and hosting providers, so we can compare the developer
experience, cost, and operational complexity of each option.

## Deployment Targets

| Priority | Platform | Stack |
|----------|----------|-------|
| Required | **Streamlit Cloud** | Pure Python (Streamlit) |
| Required | **Vercel** | React (Vite) frontend + Python (FastAPI) serverless backend |
| Optional | **VPS** | React + FastAPI behind Nginx (reverse proxy) |

## Features

### 1 — Weather
- Text input: user types a city name.
- Action: pressing Enter or clicking "Get temperature" fetches live weather data.
- Display: current temperature (°C and °F), city name, weather description.
- API: `wttr.in` — free, no account, no API key required.
  - Example call: `https://wttr.in/London?format=j1`

### 2 — Dice Roller
- Button: "Roll Dice" triggers a roll of two independent dice (1–6 each).
- Animation: show rolling dice visually for ~1 second before revealing results.
- Display after roll:
  - Die 1 result
  - Die 2 result
  - Total sum
- "Roll Again" button resets and repeats.

## Technology Decisions

| Layer | Technology | Reason |
|-------|-----------|--------|
| Frontend | React + Vite | Fast, Vercel-native, component-friendly |
| Backend API | FastAPI (Python) | Lightweight, async, Vercel serverless-compatible |
| Streamlit version | Streamlit (Python) | Self-contained, zero frontend build step |
| Styling | Plain CSS + emoji dice | No extra dependencies |
| Weather API | wttr.in | Free, no auth required |

## File Layout

```
Bussines requirements/
├── business_requirements.md   ← this file
├── README.md
├── .gitignore
├── .env.example
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── App.css
│       └── components/
│           ├── Weather.jsx
│           └── Dice.jsx
├── streamlit_app/
│   ├── app.py
│   └── requirements.txt
└── deployment/
    ├── vercel.json
    └── nginx.conf.example
```

## Constraints

- All files must live inside this directory.
- Do NOT publish to GitHub or create remote repositories without explicit user approval.
- No paid APIs. No API keys required for core functionality.
- If an API key ever becomes needed, store it in `.env` (never committed) and
  document the setup in README.md.

## Self-Instructions for Claude

1. Inspect directory first — never overwrite existing work silently.
2. Write `business_requirements.md` before any other file.
3. Summarise planned structure and get implicit or explicit approval before scaffolding.
4. Keep each file focused and minimal — no over-engineering.
5. Test commands must be reproducible on Windows (PowerShell) and Linux/macOS.
6. Git: initialise locally only. Never `git push` without user instruction.
