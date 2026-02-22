from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from layers.keyword_layer import KeywordLayer
from layers.ai_layer import AILayer
from layers.llm_service import LLMService
print(">>> MAIN.PY LOADED <<<")
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Protected AI Chatbot - Dual Layer Defense")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

keyword_layer = KeywordLayer()
ai_layer = AILayer()
llm_service = LLMService()


class MessageRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: MessageRequest):
    print(">>> CHAT ENDPOINT HIT <<<")

    # -------- Layer 1: Keyword Flag --------
    keyword_result = keyword_layer.scan(request.message)

    # -------- Layer 2: AI Judge --------
    ai_result = await ai_layer.analyze(request.message)

    if not ai_result["safe"]:
        return {
            "safe": False,
            "blocked_by": "ai",
            "reason": ai_result["reason"],
            "keyword_flag": keyword_result["flagged"],
            "keyword_reason": keyword_result["reason"],
            "response": None
        }

    # -------- Main LLM --------
    response = await llm_service.generate(request.message)

    return {
        "safe": True,
        "blocked_by": None,
        "reason": None,
        "keyword_flag": keyword_result["flagged"],
        "keyword_reason": keyword_result["reason"],
        "response": response
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}