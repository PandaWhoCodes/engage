# Engagement Message Generator

A standalone web application for generating creative engagement messages for Gen Z teens using Claude AI.

## Features

- 🎨 Theme selection (8 different themes + random)
- 📱 Mobile-friendly shadcn/ui interface
- 🚀 Fast generation with Claude Sonnet 4.5
- 📋 One-click copy to clipboard
- 💰 Cost-optimized deployment (auto-stop on Fly.io)

## Tech Stack

- **Frontend**: Next.js 16 with App Router, shadcn/ui, Tailwind CSS
- **Backend**: FastAPI (Python 3.11)
- **AI**: Anthropic Claude Sonnet 4.5
- **Deployment**: Docker + Fly.io

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 20+
- npm

### Setup

1. **Clone and navigate to the project**:
   ```bash
   cd engage
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your CLAUDE_API_KEY
   ```

3. **Install backend dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Install frontend dependencies**:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

5. **Run backend** (in one terminal):
   ```bash
   uvicorn backend.main:app --reload --port 8080
   ```

6. **Run frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

7. **Open browser**:
   - Development: http://localhost:3000
   - Backend API docs: http://localhost:8080/docs

## Production Build

### Build frontend static export:
```bash
cd frontend
npm run build
cd ..
```

### Run backend (serves both API and static frontend):
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8080
```

## Docker

### Build:
```bash
docker build -t engage .
```

### Run:
```bash
docker run -p 8080:8080 -e CLAUDE_API_KEY=your_key_here engage
```

## Deployment to Fly.io

### First-time setup:
```bash
fly launch
# Follow prompts (use existing fly.toml)
```

### Set secrets:
```bash
fly secrets set CLAUDE_API_KEY=your_claude_api_key_here
```

### Deploy:
```bash
fly deploy
```

### Check status:
```bash
fly status
fly logs
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /api/generate` - Generate message
  - Request body: `{"theme": "random" | "meme/internet culture" | ...}`
  - Response: `{"content": "...", "theme_used": "..."}`

## Cost Optimization

The app is configured for minimal costs on Fly.io:
- `min_machines_running = 0` - Machines stop when idle
- `auto_start_machines = true` - Start on request (~1-2s cold start)
- Shared CPU instance (smallest size)
- Static frontend served directly from backend

Expected cost: < $5/month with light usage

## Project Structure

```
engage/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── services/
│   │   └── message_generator.py  # Claude integration
│   └── requirements.txt
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   └── package.json
├── Dockerfile               # Multi-stage build
├── fly.toml                 # Fly.io config
└── docs/
    └── plans/
        └── 2025-11-12-message-generator-design.md
```

## License

Private project
