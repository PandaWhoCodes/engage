# Message Generator Standalone App - Design Document

**Date**: 2025-11-12
**Status**: Approved for implementation

## Overview

Convert the Discord personality check message generator into a standalone web app deployable to Fly.io. The app will provide a simple, mobile-friendly UI for generating engagement messages using Claude AI.

## Architecture

**Single Docker Image Structure** (following assistomatic pattern):
- **Frontend**: Next.js 14+ with shadcn/ui, static export to `/out`
- **Backend**: FastAPI (Python 3.11) serving both API and static files
- **Build**: Multi-stage Docker - Node.js builds frontend, Python runtime serves everything
- **Port**: 8080 (FastAPI listens, serves `/api/*` routes + static frontend)

**Key characteristics**:
- Simple: Only one API endpoint (`POST /api/generate`)
- No authentication needed
- No database or external services (just Claude API)
- Claude-only (no xAI/Grok fallback)

## Project Structure

```
engage/
├── backend/
│   ├── main.py (FastAPI app)
│   ├── services/
│   │   └── message_generator.py (adapted from discord_personality_check)
│   └── requirements.txt
├── frontend/
│   ├── app/ (Next.js pages)
│   ├── components/ (shadcn/ui components)
│   └── package.json
├── Dockerfile (multi-stage)
├── fly.toml
├── .env (gitignored)
├── .env.example
└── docs/
    └── plans/
        └── 2025-11-12-message-generator-design.md
```

## Frontend Design

**Technology**:
- Next.js 14+ with App Router
- shadcn/ui component library
- Tailwind CSS
- Mobile-first responsive design
- Dark/light mode support

**UI Components**:

1. **Header**: Simple title "Engagement Message Generator"

2. **Theme Selector**:
   - shadcn `<Select>` component
   - Options: "Random" (default), plus 8 specific themes:
     - meme/internet culture
     - sports/competition
     - music/arts
     - gaming/tech
     - real talk/deep thoughts
     - goals/ambitions
     - funny/lighthearted
     - challenges/support
   - Full-width on mobile

3. **Generate Button**:
   - Large, prominent button
   - Loading state with spinner during API call
   - Disabled while generating

4. **Output Display**:
   - Shows only `mentee_template` (the actual engagement prompt)
   - shadcn `<Card>` with readonly `<Textarea>`
   - Copy button with icon
   - Smooth fade-in animation
   - Shows which theme was used

5. **Error Handling**:
   - Toast notifications (sonner library)
   - Graceful degradation with fallback messages

**Component Structure**:
- `app/page.tsx`: Main page with state management
- `components/theme-selector.tsx`: Theme dropdown
- `components/generate-button.tsx`: Button with loading state
- `components/output-display.tsx`: Result card with copy

## Backend Design

**FastAPI Application** (`backend/main.py`):
- Health check: `GET /health` (for Fly.io)
- Generation endpoint: `POST /api/generate`
- CORS middleware for local development
- Static file serving for production frontend

**API Endpoint**:
```
POST /api/generate
Request: {
  "theme": "random" | "meme/internet culture" | ...
}
Response: {
  "content": "...",  # The mentee_template
  "theme_used": "gaming/tech"
}
Error: {
  "error": "Error message"
}
```

**Message Generator Service** (`backend/services/message_generator.py`):
- Adapted from discord_personality_check
- Claude-only (remove xAI fallback)
- Methods:
  - `generate_with_theme(theme: str)` - main generation method
  - `_get_fallback_message()` - backup if API fails
- Uses Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
- Temperature: 1.0 for creativity
- Returns only mentee_template + theme used

**Dependencies** (`backend/requirements.txt`):
```
fastapi
uvicorn
anthropic
python-dotenv
```

## Docker Configuration

**Multi-stage Dockerfile**:
```dockerfile
# Stage 1: Build Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Runtime
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/ ./backend/
COPY --from=frontend-builder /app/frontend/out ./frontend/out
EXPOSE 8080
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Fly.io Deployment

**Configuration** (`fly.toml`):
```toml
app = "engage"
primary_region = "sin"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0  # Cost optimization

[[http_service.checks]]
  interval = "15s"
  timeout = "5s"
  grace_period = "10s"
  method = "GET"
  path = "/health"

[env]
  PORT = "8080"
```

**Secrets Management**:
- Local dev: `.env` file (gitignored) with `CLAUDE_API_KEY`
- `.env.example` committed with placeholder
- Production: `fly secrets set CLAUDE_API_KEY=sk-...`

**Cost Optimization**:
- `min_machines_running = 0` - machines stop when idle
- Shared CPU (smallest machine type)
- Static frontend (no separate CDN/hosting)
- Fast cold starts (~1-2 seconds acceptable for generate button)

## Implementation Steps

1. **Backend Setup**:
   - Create FastAPI app structure
   - Copy and adapt message_generator.py
   - Add requirements.txt
   - Create .env structure

2. **Frontend Setup**:
   - Initialize Next.js with shadcn/ui
   - Build theme selector component
   - Build generate button with loading state
   - Build output display with copy functionality
   - Configure static export

3. **Docker & Deployment**:
   - Create multi-stage Dockerfile
   - Create fly.toml
   - Test local Docker build
   - Deploy to Fly.io
   - Set secrets

4. **Testing**:
   - Test theme selection
   - Test generation with different themes
   - Test error handling
   - Test mobile responsiveness
   - Test cold start behavior

## Success Criteria

- ✅ Single button generates creative engagement messages
- ✅ Theme selection works (including random)
- ✅ Mobile-friendly UI
- ✅ Deploys to Fly.io successfully
- ✅ Costs minimal when idle (auto-stop working)
- ✅ Copy functionality works
- ✅ Error handling graceful
- ✅ Cold start acceptable (~1-2 seconds)
