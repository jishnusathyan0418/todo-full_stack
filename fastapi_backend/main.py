from functools import lru_cache
from typing import Union
from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from routers import todos
from database import engine, Base  # ← ADD THIS LINE
import models 
import config
from contextlib import asynccontextmanager


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the app starts
    Base.metadata.create_all(bind=engine)
    yield
    # Code after yield runs when app shuts down (leave empty for now)

app = FastAPI(lifespan=lifespan)
app.include_router(todos.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://todo-full-stack-ijvd0bftm-jishnusathyan0418s-projects.vercel.app/"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# global http exception handler, to handle errors   (not mandatory)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(f"{repr(exc)}")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/")
def read_root(settings: config.Settings = Depends(get_settings)):
    # print(settings.DATABASE_NAME)
    return "Hello world"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id":item_id, "q": q}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)