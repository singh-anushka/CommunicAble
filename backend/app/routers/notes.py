import base64
from fastapi import APIRouter

from ..services.notes import note_make, testing

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)

@router.get("/")
def notes_check():
    return testing()

@router.get("/text")
def img_to_bb(url:str):
    text = note_make(url)
    if text is None:
        return {}
    return text

@router.get("/narration")
def note_to_audio(url:str):
    text, audio_path = note_make(url, sound = True)
    if audio_path is None:
        return {}
    with open(audio_path, 'rb') as audio_file:
        encoded_file = base64.b64encode(audio_file.read())
    return {'text': text, 'audio':encoded_file.decode('utf-8', errors='replace')}
