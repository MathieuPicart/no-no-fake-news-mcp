from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.database import engine, Base
from app.models import analysis  # Required to register models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="No No Fake News",
    description="API for analyzing credibility of news articles",
    version="0.1.0"
)

from app.api import routes

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Include API routes
app.include_router(routes.router, prefix="/api")

# Templates configuration
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

from fastapi import Request

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
