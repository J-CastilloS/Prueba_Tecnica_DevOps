from src.model.entities.response import TranscriptResponse
from model.transcriptor import Transcriptor
import speech_recognition as sr
from fastapi import APIRouter


router = APIRouter()
Transcriptor = Transcriptor()

@router.post("/transcript_audio")
async def transcript_audio(
    audio_file: sr.AudioFile,
) -> TranscriptResponse:
    """
    Transcribe un archivo .wav a un bucket de Google Cloud Storage
    """
    return Transcriptor.transcribir_audio(audio_file)