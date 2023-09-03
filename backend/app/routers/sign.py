import base64
from fastapi import APIRouter
from fastapi.responses import FileResponse
from ..services.sign import testing, getSignVideo

router = APIRouter(
    prefix="/sign",
    tags=["sign"]
)

@router.get("/")
def sign_check():
    return testing()

@router.get("/video")
def sign_video(url:str):
    videoPath = getSignVideo(url)
    return FileResponse(videoPath)