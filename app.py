import asyncio

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from consumer.data_consumer import consume_forever
from routers import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_init():
    current_loop = asyncio.get_running_loop()
    current_loop.create_task(consume_forever())


app.include_router(api_router)

import uvicorn

uvicorn.run(app)
