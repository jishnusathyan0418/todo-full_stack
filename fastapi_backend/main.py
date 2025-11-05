from functools import lru_cache
from typing import Union
from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from routers import todos
from database import engine, Base
import models 
import config
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the app starts
    Base.metadata.create_all(bind=engine)
    yield
    # Code after yield runs when app shuts down (leave empty for now)

app = FastAPI(lifespan=lifespan)
app.include_router(todos.router)

# FIXED CORS CONFIGURATION - Use your correct frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://todo-full-stack-dcit87ndm-jishnusathyan0418s-projects.vercel.app",  # ✅ CORRECTED
        "http://localhost:3000",  # Local development
        "http://localhost:3001",  # Alternative local port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# global http exception handler, to handle errors
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(f"{repr(exc)}")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/")
def read_root(settings: config.Settings = Depends(get_settings)):
    return "Hello world"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)