from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from config import settings



app = FastAPI(
    title="Multi-Agent AI Research Assistant API",
    description=(
        "Production-ready AI research service powered by "
        "LangGraph, OpenAI, Tavily Search, and ChromaDB."
    ),
    version="1.0.0",
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Why allow_origins=["*"]?

For development, it's convenient.

For production, you'll typically restrict it, for example:

allow_origins=[
    "https://myresearchassistant.com",
]

We'll keep "*" for now because it's a development environment."""

app.include_router(router)