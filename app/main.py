# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from .database import log_to_db  # 👈 import the DB logger
import os
from fastapi.responses import HTMLResponse
# frontend 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

# frontend 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# front
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# fornt

from fastapi.responses import JSONResponse

@app.get("/logs")
async def get_logs():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT prompt, summary, timestamp FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    logs = []
    for row in rows:
        logs.append({
            "prompt": row[0],
            "summary": row[1],
            "timestamp": row[2]
        })

    return JSONResponse(content={"logs": logs})


@app.post("/summarize")
async def summarize(request: Request):
    data = await request.json()
    prompt = data.get("text", "")
    
    full_prompt = f"Summarize the following text:\n\n{prompt}"
    
    print("📤 Sending prompt to Ollama:", full_prompt)

    try:
        response = requests.post(
            "http://172.23.144.1:11434/api/generate",
            json={"model": "gemma:2b", "prompt": full_prompt, "stream": False}
        )
        print("✅ Got response from Ollama")

        result = response.json()
        summary = result.get("response", "")
        
        
        print("📁 Current working directory:", os.getcwd())

        # ✅ Log to DB
        log_to_db(prompt, summary)

        return {"summary": summary}
    except Exception as e:
        print("❌ Error occurred:", e)
        return {"error": str(e)}
