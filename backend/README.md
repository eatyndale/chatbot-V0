# EFT Chatbot Backend

This is the backend service for the EFT (Emotional Freedom Techniques) Chatbot application. It provides secure user authentication, personalized anxiety assessment, conversational AI, EFT tapping session management, progress tracking, and crisis support resources.

## Features

- **User Authentication**: Secure signup, login, and JWT-based session management.
- **PHQ-9 Anxiety Assessment**: Personalized mental health screening and next-step guidance.
- **Conversational Chatbot**: Context-aware chat with OpenAI LLM integration.
- **EFT Tapping Sessions**: Guided setup, feedback, and multi-round session tracking.
- **Progress Tracking**: Log and retrieve EFT session history with analytics-ready endpoints.
- **Crisis Support**: Public access to global/regional mental health hotlines and proactive crisis detection.

## Tech Stack
- **FastAPI** (Python 3.9+)
- **SQLAlchemy** (PostgreSQL)
- **Pydantic**
- **OpenAI API** (for LLM chat)

## Setup

1. **Clone the repository**

```bash
git clone https://github.com/eatyndale/chatbot-V0.git
cd chatbotV0/backend
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the `backend/` directory with your secrets (see `.env.example`).

5. **Run database migrations**

Tables are auto-created on startup, but for production use Alembic or similar.

6. **Start the server**

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000/api/`.

## API Overview

- **Auth**: `/api/auth/signup`, `/api/auth/login`, `/api/auth/refresh`
- **Assessment**: `/api/assessment/phq9`
- **Chat**: `/api/chat/message`
- **EFT**: `/api/eft/session`, `/api/eft/feedback`
- **Progress**: `/api/progress/` (GET session logs)
- **Crisis Support**:
  - `GET /api/crisis/resources` — List of global/regional hotlines
  - `GET /api/crisis/sos` — Quick access to hotlines (no auth required)
  - `POST /api/crisis/check` — Detect crisis signals in user input

## Crisis Support

- All users (even unauthenticated) can access mental health hotlines and resources.
- The backend detects high-risk crisis phrases in chat or assessment and can trigger safety messages.
- No sensitive user input is stored unless the user is authenticated and opts in.
- Data is served from `app/data/crisis_hotlines.json` and can be expanded for more regions.

## Development

- Code is organized by feature: `router/`, `services/`, `models/`, `data/`.
- All endpoints return JSON and use modern, secure practices.
- Contributions and improvements are welcome!

## License

eatyndale
