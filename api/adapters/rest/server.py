from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.adapters.sqlite.db import create_tables
from api.adapters.rest.task import task_router, project_router

app = FastAPI(
    title="Task Manager API",
    description="Task management and project tracking system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(project_router)


@app.on_event("startup")
async def startup_event():
    create_tables()


@app.get("/")
async def root():
    return {
        "message": "Task Manager API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
