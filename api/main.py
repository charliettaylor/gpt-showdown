from fastapi import FastAPI
from pydantic import BaseModel
from assistant import Assistant
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "gpt showdown :)"}


@app.get("/get_gpt_response")
async def get_gpt_response():
    pass
