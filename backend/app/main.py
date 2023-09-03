from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import book, notes, sign, braille

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://SpeakUp.chiragghosh.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book.router)
app.include_router(notes.router)
app.include_router(sign.router)
app.include_router(braille.router)

@app.get("/")
def root_check():
    return {"status": "OK", "message": "Welcome to CommunicAble Rest API."}