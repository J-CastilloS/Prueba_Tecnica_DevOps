from src.model.entitites.response import TranscriptResponse
from src.model.main import Transcriptor
import speech_recognition as sr
from fastapi import APIRouter


router = APIRouter()
Transcriptor = Transcriptor()

@router.post("/data_parquet")
async def data_parquet(
    audio_file: sr.AudioFile,
) -> TranscriptResponse:
    """
    Transcribe un archivo .wav a un bucket de Google Cloud Storage
    """
    return Transcriptor.transcribir_audio(audio_file)