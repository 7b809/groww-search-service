# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.api.ws_routes import router as ws_router
from app.core.config import settings


app = FastAPI(
    title="Groww Option Search Service",
    version="1.0.0"
)

testing_flag = True
# -----------------------------
# CORS Configuration
# -----------------------------


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include Routers
# -----------------------------

app.include_router(router)
app.include_router(ws_router)