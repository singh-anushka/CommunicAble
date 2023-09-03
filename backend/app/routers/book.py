from fastapi import APIRouter
import base64
from ..services.book import testing, narrateBook

router = APIRouter(
    prefix="/book",
    tags=["book"]
)

@router.get("/")
def book_check():
    return testing()

@router.get("/text")
def book_text(url: str):
    return narrateBook(url)

@router.get("/narration")
def book_narration(url: str):
    audioPath = narrateBook(url, sound=True)
    with open(audioPath, 'rb') as audioFile:
        encoded_image = base64.b64encode(audioFile.read())
    return {'audio': encoded_image.decode('utf-8', errors='replace')}
