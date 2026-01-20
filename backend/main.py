from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_ai import Agent
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Code Review Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"

class CodeReviewResponse(BaseModel):
    review: str
    suggestions: list[str]
    severity_level: str

# Initialize the Code Review Agent
code_review_agent = Agent(
    model="openrouter/meta-llama/llama-2-7b-chat",
    system_prompt="""You are an expert code reviewer. Analyze the provided code and:
1. Identify bugs, performance issues, and security concerns
2. Provide specific improvement suggestions
3. Rate severity (critical, high, medium, low)
4. Suggest best practices

Be concise but thorough. Focus on actionable feedback.""",
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Code Review Agent"}

@app.post("/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    """
    Review code using the AI agent.
    
    Args:
        request: CodeReviewRequest containing code and language
        
    Returns:
        CodeReviewResponse with review, suggestions, and severity level
    """
    try:
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")
        
        if len(request.code) > 10000:
            raise HTTPException(status_code=400, detail="Code exceeds 10000 characters")
        
        logger.info(f"Processing code review for {request.language}")
        
        prompt = f"""Review this {request.language} code and provide:
1. A summary review (2-3 sentences)
2. 3-5 specific suggestions for improvement
3. Overall severity level (critical/high/medium/low)

Code:
```{request.language}
{request.code}
```"""
        
        # Call the agent
        result = code_review_agent.run_sync(prompt)
        review_text = result.data if hasattr(result, 'data') else str(result)
        
        # Parse the response
        suggestions = extract_suggestions(review_text)
        severity = determine_severity(review_text)
        
        logger.info("Code review completed successfully")
        
        return CodeReviewResponse(
            review=review_text,
            suggestions=suggestions,
            severity_level=severity
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during code review: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing code review: {str(e)}")

def extract_suggestions(text: str) -> list[str]:
    """Extract suggestions from review text"""
    suggestions = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if any(marker in line.lower() for marker in ['suggest', 'improve', 'consider', 'use']):
            if line.strip():
                suggestions.append(line.strip())
    return suggestions[:5] if suggestions else ["Review the code structure and naming conventions"]

def determine_severity(text: str) -> str:
    """Determine severity level from review text"""
    text_lower = text.lower()
    if 'critical' in text_lower or 'security' in text_lower:
        return 'critical'
    elif 'bug' in text_lower or 'error' in text_lower:
        return 'high'
    elif 'improve' in text_lower or 'refactor' in text_lower:
        return 'medium'
    else:
        return 'low'

@app.post("/batch-review")
async def batch_review(requests: list[CodeReviewRequest]):
    """Review multiple code snippets"""
    results = []
    for req in requests:
        try:
            result = await review_code(req)
            results.append(result)
        except Exception as e:
            logger.error(f"Error in batch review: {str(e)}")
            results.append({"error": str(e)})
    return {"reviews": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
