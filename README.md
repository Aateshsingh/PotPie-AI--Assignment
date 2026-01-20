# Code Review Agent

A full-stack AI-powered code review application built with Pydantic AI and React.

## Features

- **Intelligent Code Analysis**: Uses OpenRouter's LLMs to provide comprehensive code reviews
- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust
- **Real-time Feedback**: Instant code analysis with suggestions and severity ratings
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Production-Ready**: Proper error handling, validation, and logging

## Tech Stack

### Backend
- FastAPI (Python web framework)
- Pydantic AI (AI agent orchestration)
- OpenRouter API (LLM provider)
- Python 3.9+

### Frontend
- React 18
- Axios (HTTP client)
- Vite (build tool)
- Modern CSS

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenRouter API key (free)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
# Add your OpenRouter API key
```

5. Run the server:
```bash
python main.py
```

Backend runs on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend runs on `http://localhost:5173`

## API Endpoints

### POST /review
Analyzes code and provides a comprehensive review.

**Request:**
```json
{
  "code": "def hello():\n    print('world')",
  "language": "python"
}
```

**Response:**
```json
{
  "review": "The function works correctly...",
  "suggestions": ["Add docstring", "Add type hints"],
  "severity_level": "low"
}
```

### GET /health
Health check endpoint.

## Deployment

### Backend Deployment (Render, Railway, or Heroku)

1. Create `.env` with OpenRouter API key
2. Push to GitHub
3. Connect repository to hosting platform
4. Set environment variables
5. Deploy

### Frontend Deployment (Vercel)

1. Push to GitHub
2. Import repository in Vercel
3. Set `REACT_APP_API_URL` environment variable to backend URL
4. Deploy

## Code Quality

The project includes:
- Input validation (max 10k characters)
- Error handling and logging
- CORS enabled for cross-origin requests
- Graceful fallbacks
- Clean code structure
- Type hints (Python)

## License

MIT
