import base64
from fastapi import APIRouter

from ..services.braille import testing

from ..services.braille import url_to_braille, testing

router = APIRouter(
    prefix="/braille",
    tags=["braille"]
)

@router.get("/")
def braille_check():
    return testing()

@router.get("/url")
def get_barille(url:str):
    text, braille_text = url_to_braille(url)
    if braille_text is None:
        return {}
    return {'text': text, 'braille': braille_text}