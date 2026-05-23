from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

# Flat import — routes.py is in the same folder
from routes import router as api_router

app = FastAPI(title="Resume AI Screening Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def serve_frontend():
    html_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"status": "ok", "message": "API running. Open index.html in browser."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*52)
    print("  Resume AI starting...")
    print("  Open in browser: http://localhost:8000")
    print("  API Docs:        http://localhost:8000/docs")
    print("="*52 + "\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
