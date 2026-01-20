# Architecture Overview

## Project Structure

```
PotPie AI Assignment/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Pydantic AI agent & FastAPI app
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   └── app.yaml            # Google Cloud deployment
│
├── frontend/               # React/Vite frontend
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── index.css      # Styling
│   │   └── main.jsx       # Entry point
│   ├── index.html         # HTML template
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
│
├── README.md              # Project documentation
├── DEPLOYMENT.md          # Deployment guide
├── SUBMISSION.md          # Submission checklist
└── setup.sh              # Automated setup script
```

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                              │
├─────────────────────────────────────────────────────────────┤
│  React Frontend (Vercel)                                    │
│  - UI for code input                                        │
│  - Language selector                                        │
│  - Loading/Error states                                    │
│  - Results display                                         │
└──────────────┬──────────────────────────────────────────────┘
               │ HTTP POST /review
               │ { code, language }
               │
┌──────────────▼──────────────────────────────────────────────┐
│  FastAPI Backend (Render/Railway)                           │
├──────────────────────────────────────────────────────────────┤
│  POST /review                                               │
│  1. Validate input (max 10k chars)                          │
│  2. Create agent prompt                                    │
│  3. Call Pydantic AI Agent                                │
└──────────────┬──────────────────────────────────────────────┘
               │ HTTP POST
               │ 
┌──────────────▼──────────────────────────────────────────────┐
│  OpenRouter API (Free tier)                                 │
├──────────────────────────────────────────────────────────────┤
│  - Llama 2 7B (Free)                                        │
│  - Claude 3 Sonnet (Credits available)                     │
│  - Mistral (Free options)                                  │
└──────────────┬──────────────────────────────────────────────┘
               │ AI response
               │
┌──────────────▼──────────────────────────────────────────────┐
│  Pydantic AI Agent Processing                               │
├──────────────────────────────────────────────────────────────┤
│  1. Parse AI response                                       │
│  2. Extract suggestions                                    │
│  3. Determine severity level                               │
│  4. Format for frontend                                    │
└──────────────┬──────────────────────────────────────────────┘
               │ JSON response
               │ {review, suggestions, severity_level}
               │
└──────────────▼──────────────────────────────────────────────┘
```

## Tech Stack Details

### Backend
- **FastAPI**: Async web framework, automatic API docs, built-in validation
- **Pydantic AI**: Agent framework, handles LLM communication, structured output
- **OpenRouter**: Multi-model LLM provider with free tier
- **Python**: Type hints, async/await support

### Frontend
- **React 18**: Modern UI library, hooks, fast renders
- **Vite**: Fast build tool, instant HMR, optimized production
- **Fetch API**: Lightweight HTTP client
- **CSS3**: Gradients, animations, responsive design

### Deployment
- **Vercel**: Frontend hosting, auto git integration, serverless
- **Render/Railway**: Backend hosting, free tier, PostgreSQL-ready
- **GitHub**: Source control, CI/CD integration

## API Contract

### Request
```json
POST /review
{
  "code": "def hello():\n    print('world')",
  "language": "python"
}
```

### Response
```json
{
  "review": "Good basic function. Consider adding: 1) Docstring explaining purpose 2) Type hints 3) Return statement 4) Error handling",
  "suggestions": [
    "Add docstring to document function purpose",
    "Add type hints for parameters and return",
    "Consider adding return statement",
    "Add error handling"
  ],
  "severity_level": "low"
}
```

## Pydantic AI Integration

The agent is configured with:
- **Model**: `openrouter/meta-llama/llama-2-7b-chat` (free)
- **System Prompt**: Expert code reviewer persona
- **Input Validation**: Max 10k characters, non-empty
- **Error Handling**: Try-catch with detailed logging
- **Output Parsing**: Extracts structured data from LLM

## Development Workflow

1. **Local**: Backend runs on :8000, Frontend on :5173
2. **Testing**: Full API testing in browser
3. **Deployment**: 
   - Push to GitHub
   - Render/Railway auto-deploys backend
   - Vercel auto-deploys frontend
4. **Monitoring**: Logs available in platform dashboards

## Performance Considerations

- **Frontend**: Lazy loading, code splitting, optimized CSS
- **Backend**: Connection pooling, request validation, error recovery
- **API**: 3-5 second response time (model dependent)
- **Caching**: Could add response caching for identical inputs (future)

## Security

- **CORS**: Configured for all origins (can restrict to frontend domain)
- **Input Validation**: Max 10k chars prevents abuse
- **Error Messages**: No stack traces exposed to frontend
- **API Key**: Stored in server environment, not sent to client
- **HTTPS**: Enforced on all deployments
