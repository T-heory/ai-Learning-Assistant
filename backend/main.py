import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from config import settings
from database import init_db, get_profile, save_profile
from models import (
    ChatRequest, ChatResponse,
    AgentRequest, AgentResponse,
    GenerateResourcesRequest,
    PlanPathRequest, EvaluateRequest,
)
from llm.deepseek_client import DeepSeekClient
from agents.orchestrator import Orchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Learning System...")
    if not settings.is_configured:
        logger.warning("DeepSeek API Key not configured!")
    await init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="AI Learning System",
    description="Multi-agent collaborative learning platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = DeepSeekClient()
orchestrator = Orchestrator(llm)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "api_configured": settings.is_configured, "model": settings.DEEPSEEK_MODEL}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        profile = await get_profile(request.session_id)
        context = {
            "message": request.message,
            "session_id": request.session_id,
            "existing_profile": profile,
        }
        if not profile:
            results = await orchestrator.run_workflow("onboarding", context)
            profile_result = results.get("profile_extract", {}).get("result", {})
            if profile_result.get("dimensions"):
                await save_profile(request.session_id, profile_result)
            reply = _format_onboarding_reply(results)
        else:
            profile_result = await orchestrator.run_agent("profile", context)
            if profile_result.get("result", {}).get("needs_update"):
                updated = profile_result["result"]["full_profile"]
                await save_profile(request.session_id, updated)
            messages = [
                {"role": "system", "content": f"You are an AI learning assistant. Student profile: {json.dumps(profile, ensure_ascii=False)}"},
                {"role": "user", "content": request.message},
            ]
            reply = await llm.chat(messages)
        return ChatResponse(reply=reply, profile_updated=True)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    profile = await get_profile(request.session_id)
    messages = [
        {"role": "system", "content": f"You are an AI learning assistant. Profile: {json.dumps(profile, ensure_ascii=False)}"},
        {"role": "user", "content": request.message},
    ]

    async def generate():
        async for chunk in llm.chat_stream(messages):
            yield f"data: {json.dumps({'text': chunk}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/agents/{agent_name}")
async def call_agent(agent_name: str, request: AgentRequest):
    try:
        result = await orchestrator.run_agent(agent_name, request.input_data)
        return AgentResponse(agent_type=agent_name, output_data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Agent error ({agent_name}): {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/resources/generate")
async def generate_resources(request: GenerateResourcesRequest):
    try:
        profile = await get_profile(request.session_id)
        result = await orchestrator.run_agent("resource", {
            "topic": request.topic,
            "profile": profile,
        })
        return result
    except Exception as e:
        logger.error(f"Generate resources error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/path/plan")
async def plan_path(request: PlanPathRequest):
    try:
        profile = await get_profile(request.session_id)
        result = await orchestrator.run_agent("path", {
            "topic": request.topic,
            "profile": profile,
        })
        return result
    except Exception as e:
        logger.error(f"Plan path error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/path/adjust")
async def adjust_path(data: dict):
    try:
        result = await orchestrator.run_agent("path", {
            "evaluation": data.get("evaluation", {}),
            "current_path": data.get("current_path", {}),
            "weaknesses": data.get("weaknesses", []),
        })
        return result
    except Exception as e:
        logger.error(f"Adjust path error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/evaluate")
async def evaluate(request: EvaluateRequest):
    try:
        profile = await get_profile(request.session_id)
        result = await orchestrator.run_agent("evaluator", {
            "answers": request.answers,
            "profile": profile,
            "session_id": request.session_id,
        })
        return result
    except Exception as e:
        logger.error(f"Evaluate error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/profile/{session_id}")
async def get_student_profile(session_id: str):
    profile = await get_profile(session_id)
    return {"session_id": session_id, "profile": profile}


def _format_onboarding_reply(results: dict) -> str:
    profile = results.get("profile_extract", {}).get("result", {})
    dims = profile.get("dimensions", {})
    reply = "Hello! I've learned about your background.\n\n📋 **Profile Summary**\n"
    reply += f"- Knowledge level: {dims.get('knowledge_base', {}).get('level', 'N/A')}\n"
    reply += f"- Learning style: {dims.get('cognitive_style', {}).get('type', 'N/A')}\n"
    reply += f"- Goal: {dims.get('learning_goal', {}).get('short_term', 'N/A')}\n\n"
    reply += "I've prepared learning resources for you. Click 'Learn' to start! 🎯"
    return reply


if __name__ == "__main__":
    import uvicorn
    print(f"""
╔══════════════════════════════════════════╗
║     AI Personalized Learning System      ║
║     Backend: http://localhost:{settings.PORT}              ║
║     API Docs: http://localhost:{settings.PORT}/docs       ║
║     Model: {settings.DEEPSEEK_MODEL}                     ║
╚══════════════════════════════════════════╝
    """)
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
