from fastapi import FastAPI
from sqlalchemy import text

from core.database import engine
from core.database import Base
import models
from api.conversation import router as conversations_router
from api.message import router as messages_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Technical Support Assistant",
    description="Backend API for the AI Technical Support Assistant",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#根据当前已经注册的 SQLAlchemy models，在数据库中创建不存在的 tables。
Base.metadata.create_all(bind=engine)
#注册router
app.include_router(conversations_router)
app.include_router(messages_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-technical-support-assistant",
    }


@app.get("/health/db")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
        }

    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "detail": str(e),
        }