# API Examples & Testing

## Using the Code Review API

### Local Testing

With backend running on `http://localhost:8000`:

#### Using cURL
```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"world\")",
    "language": "python"
  }'
```

#### Using Python
```python
import requests

response = requests.post('http://localhost:8000/review', json={
    'code': 'def hello():\n    print("world")',
    'language': 'python'
})

print(response.json())
```

#### Using JavaScript/Node
```javascript
fetch('http://localhost:8000/review', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    code: 'function hello() {\n  console.log("world");\n}',
    language: 'javascript'
  })
})
.then(r => r.json())
.then(data => console.log(data))
```

## Sample Test Cases

### Test 1: Python with Issues
```json
{
  "code": "def calc(a,b):\n    x=a+b\n    y=a*b\n    return x,y",
  "language": "python"
}
```

Expected: Suggestions about type hints, spacing, docstring

### Test 2: Good JavaScript
```json
{
  "code": "const add = (a: number, b: number): number => {\n  if (typeof a !== 'number' || typeof b !== 'number') {\n    throw new Error('Both parameters must be numbers');\n  }\n  return a + b;\n};",
  "language": "javascript"
}
```

Expected: Low severity, mostly positive feedback

### Test 3: Security Issue
```json
{
  "code": "import os\npassword = 'secret123'\nos.system('curl https://api.example.com?password=' + password)",
  "language": "python"
}
```

Expected: HIGH or CRITICAL severity, security warnings

## API Response Format

```json
{
  "review": "The function works correctly and has basic error handling. However, there are several areas for improvement:\n\n1. Add type hints for better code clarity\n2. Consider adding docstring to explain parameters and return value\n3. The variable naming could be more descriptive\n4. Consider breaking complex logic into smaller functions",
  "suggestions": [
    "Add type hints: def hello(name: str) -> str:",
    "Add docstring explaining function purpose and parameters",
    "Use more descriptive variable names",
    "Add error handling for edge cases"
  ],
  "severity_level": "low"
}
```

## Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Code Review Agent"
}
```

## Error Responses

### Empty Code
```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "", "language": "python"}'
```

Response (400):
```json
{
  "detail": "Code cannot be empty"
}
```

### Code Too Long
```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "'$(head -c 15000 /dev/urandom | base64)'", "language": "python"}'
```

Response (400):
```json
{
  "detail": "Code exceeds 10000 characters"
}
```

## Batch Review

Review multiple code snippets at once:

```bash
curl -X POST http://localhost:8000/batch-review \
  -H "Content-Type: application/json" \
  -d '[
    {
      "code": "def hello():\n    print(\"world\")",
      "language": "python"
    },
    {
      "code": "function hello() {\n  console.log(\"world\");\n}",
      "language": "javascript"
    }
  ]'
```

## Rate Limiting

Currently no rate limiting is configured. For production, consider:
- Max requests per minute per IP
- Token bucket algorithm
- Cache responses for identical inputs

## Monitoring & Debugging

Check server logs:
```bash
# Local development
python backend/main.py

# Production (Render/Railway)
# View in dashboard → Logs
```

Look for:
- `INFO: Processing code review for python`
- `INFO: Code review completed successfully`
- `ERROR: Error during code review: ...`

## Performance Notes

- **Cold start**: ~2-3 seconds (first request after deployment)
- **Warm request**: 3-5 seconds (depends on code length and LLM response)
- **Backend response**: Usually <500ms (most time is LLM API)
- **Frontend rendering**: <100ms

## Supported Languages

- python
- javascript
- typescript
- java
- cpp
- csharp
- go
- rust

Add more in `App.jsx` select element or extend backend logic.
