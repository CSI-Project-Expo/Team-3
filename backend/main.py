from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import logs_collection
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

from layers.keyword_layer import KeywordLayer
from layers.ai_layer import AILayer
from layers.llm_service import LLMService
print(">>> MAIN.PY LOADED <<<")


app = FastAPI(title="Protected AI Chatbot - Dual Layer Defense")

@app.on_event("startup")
async def test_mongo():
    try:
        await logs_collection.database.command("ping")
        print("✅ MongoDB Connected✅")
    except Exception as e:
        print("❌ MongoDB Connection Failed❌:", e)

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
        await logs_collection.insert_one({
            "message": request.message,
            "safe": False,
            "blocked_by": "ai",
            "ai_reason": ai_result["reason"],
            "keyword_flag": keyword_result["flagged"],
            "keyword_reason": keyword_result["reason"],
            "timestamp": datetime.utcnow()
        })

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

    await logs_collection.insert_one({
    "message": request.message,
    "safe": True,
    "blocked_by": None,
    "ai_reason": "Passed AI analysis",
    "keyword_flag": keyword_result["flagged"],
    "keyword_reason": keyword_result["reason"],
    "response_preview": response[:200],
    "timestamp": datetime.utcnow()
})

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




@app.get("/logs")
async def get_logs(
    safe: bool = None,
    search: str = None
):
    query = {}

    if safe is not None:
        query["safe"] = safe

    if search:
        query["message"] = {"$regex": search, "$options": "i"}

    logs = await logs_collection.find(query)\
        .sort("timestamp", -1)\
        .limit(200)\
        .to_list(200)

    # 🔥 Convert ObjectId to string
    for log in logs:
        log["_id"] = str(log["_id"])

    return logs

@app.get("/test-route")
async def test_route():
    return {"message": "TEST ROUTE WORKING"}