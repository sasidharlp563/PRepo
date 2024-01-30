from __future__ import annotations

import os
from datetime import datetime
from typing import List

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from messages.messages_router import messages_router

tags_metadata = [
  { 
    "name": "Messages API",
    "description": "Messages API.",
  },
  { 
    "name": "health",
    "description": "Operations for health.",
  },
  {
    "name": "time",
    "description": "Operations for time.",
  },
]

app = FastAPI(
  title="Messages API",
  description="REST API doc for Messages API.",
  contact={'email': 'sureshperumal41@gmai.com'},
  version="0.1",
  servers=[
    {'url': os.environ.get('BASE_URL') or 'http://127.0.0.1:8000'}
  ],
  openapi_tags=tags_metadata
)

origins = [
  os.environ.get('BASE_URL') or 'http://127.0.0.1:8000',
  os.environ.get('FRONTEND_URL') or 'http://127.0.0.1:8000/docs'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(messages_router)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
  return JSONResponse(dict(messasge=str(exc.detail)), status_code=exc.status_code)

@app.get("/time/", tags=["time"])
async def get_time():
  return datetime.now().isoformat()

@app.get("/health-check/", tags=["health"])
async def get_health():
  return f"{app.title} Still Alive... O:)"

if __name__ == '__main__':
  uvicorn.run(app, port=8000)
