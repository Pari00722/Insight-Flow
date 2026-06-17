from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

print(">>> OpenAI Key:", os.getenv("OPENAI_API_KEY", "NOT FOUND")[:15] + "...")

from agents.graph import agent
from langchain_core.messages import HumanMessage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        message = body.get("message", "")
        print(f"\n>>> USER SAID: {message}")

        messages = [HumanMessage(content=message)]
        result = agent.invoke({"messages": messages})
        final = result["messages"][-1]
        answer = final.content
        steps = len(result["messages"])

        print(f">>> AGENT REPLIED ({steps} steps): {answer[:120]}")
        return JSONResponse({"response": answer, "steps": steps})

    except Exception as e:
        err = traceback.format_exc()
        print(f">>> EXCEPTION:\n{err}")
        return JSONResponse({"response": f"Error: {str(e)}", "steps": 0})