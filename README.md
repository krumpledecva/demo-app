# Demo App — Multi-Deployment Experiment

A small web app with two features — **live weather** and a **dice roller** — deployed
through multiple technology stacks to compare developer experience and hosting options.

## Features

| Feature | Description |
|---------|-------------|
| 🌤 Weather | Enter a city → get current temperature, feels-like, humidity, and description via [wttr.in](https://wttr.in) (no API key needed) |
| 🎲 Dice Roller | Roll two animated dice → see individual results and the total sum |

## Project Structure

```
.
├── backend/          Python FastAPI — /api/weather and /api/dice
├── frontend/         React + Vite — the web UI
├── streamlit_app/    Self-contained Streamlit version (Python only)
├── deployment/       vercel.json and nginx.conf.example
├── .env.example      Environment variable template
├── .gitignore
└── README.md
```

---

## Running Locally

### Option A — React + FastAPI (full stack)

**1. Start the backend**

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**2. Start the frontend** (new terminal)

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173).  
The Vite dev server proxies `/api/*` to `http://localhost:8000`.

---

### Option B — Streamlit only

```bash
cd streamlit_app
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## Deployment

### Vercel (React + FastAPI)

> Requires a GitHub account and the Vercel CLI or the Vercel dashboard.

1. **Install Vercel CLI** (one-time):
   ```bash
   npm install -g vercel
   ```

2. **Initialise a Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Push to GitHub** — create a new *private* repository on github.com, then:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```
   ⚠ Ask before doing this step — do not publish without approval.

4. **Deploy**:
   ```bash
   vercel
   ```
   Follow the prompts. Vercel will detect the config from `deployment/vercel.json`.

5. **Environment variables** — if you add an API key later, set it in the Vercel
   dashboard under *Project → Settings → Environment Variables*.

---

### Streamlit Cloud

1. Push the repository to GitHub (see step 3 above).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select your repository.
4. Set **Main file path** to `streamlit_app/app.py`.
5. Click **Deploy**. Done — Streamlit installs `requirements.txt` automatically.

---

### VPS with Nginx (optional)

1. Build the React frontend:
   ```bash
   cd frontend && npm run build
   ```
2. Copy `frontend/dist/` to `/var/www/demo-app/frontend/dist/` on the server.
3. Run FastAPI with a process manager (e.g. systemd or supervisor):
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```
4. Copy `deployment/nginx.conf.example` to `/etc/nginx/sites-available/demo-app`,
   edit `server_name`, symlink it, and reload Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/demo-app /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   ```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in values.  
`.env` is git-ignored — **never commit it**.

| Variable | Used by | Default | Notes |
|----------|---------|---------|-------|
| `VITE_API_URL` | React (build time) | `http://localhost:8000` | Set to your production backend URL on Vercel |

The weather feature uses `wttr.in` — **no API key required**.

---

## Weather API — wttr.in

- Endpoint: `https://wttr.in/{city}?format=j1`
- Returns JSON with temperature, humidity, weather description, etc.
- Free, open, no account needed.
- Rate limits are generous for personal use.

If you later switch to OpenWeatherMap (more reliable, global coverage):
1. Create a free account at [openweathermap.org](https://openweathermap.org/api).
2. Copy your API key into `.env` as `WEATHER_API_KEY=your_key`.
3. Update `backend/main.py` to call:
   `https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric`
