# app/main.py
from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(title="Secure User API", version="0.1.0")

@app.get("/health")
def health():
    return "OK"     # pragma: no cover

# Include the user router
app.include_router(user_router)
