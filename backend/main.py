from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

# Demo mode - simulated code review without API
def get_demo_review(code: str, language: str) -> CodeReviewResponse:
    """Simulate AI review without actual API call"""
    suggestions = []
    review = f"Code Review for {language}:\n\n"
    
    # Analyze code patterns
    if len(code) < 50:
        review += "✓ Code is concise\n"
        suggestions.append("Consider adding more documentation")
        severity = "low"
    elif "import" in code.lower() or "require" in code.lower():
        review += "✓ Proper dependency imports detected\n"
        suggestions.append("Ensure all imports are used")
        suggestions.append("Consider organizing imports at the top")
        severity = "low"
    else:
        review += "✓ Basic code structure looks reasonable\n"
        suggestions.append("Add type hints or annotations")
        suggestions.append("Consider adding docstrings")
        severity = "medium"
    
    if "error" in code.lower() or "except" in code.lower():
        review += "✓ Error handling detected\n"
    else:
        suggestions.append("Add error handling")
        severity = "medium"
    
    suggestions.append(f"Review code style and naming conventions for {language}")
    
    return CodeReviewResponse(
        review=review,
        suggestions=suggestions[:5],
        severity_level=severity
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Code Review Agent"}

@app.post("/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    """
    Review code using demo mode (no API key needed for testing).
    In production, this would use Pydantic AI with OpenRouter.
    
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
        
        # Use demo mode (simulated review without API)
        result = get_demo_review(request.code, request.language)
        
        logger.info("Code review completed successfully")
        
        return result
        
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
