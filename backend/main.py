from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from layers.keyword_layer import KeywordLayer
from layers.ai_layer import AILayer
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Dual-Layer Defense System")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize defense layers
keyword_layer = KeywordLayer()
ai_layer = AILayer()


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    safe: bool
    layer: str
    reason: str


@app.get("/")
async def root():
    return {"message": "Dual-Layer Defense System API"}


@app.post("/check-message", response_model=MessageResponse)
async def check_message(request: MessageRequest):
    """
    Check message through dual-layer defense:
    1. Layer 1: Keyword/Regex scanning
    2. Layer 2: AI-based analysis
    """
    try:
        # Layer 1: Keyword scanning
        keyword_result = keyword_layer.scan(request.message)
        if not keyword_result["safe"]:
            return MessageResponse(
                safe=False,
                layer="keyword",
                reason=keyword_result["reason"]
            )
        
        # Layer 2: AI analysis
        ai_result = await ai_layer.analyze(request.message)
        return MessageResponse(
            safe=ai_result["safe"],
            layer="ai",
            reason=ai_result["reason"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
