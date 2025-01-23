from src.model.entitites.response import TranscriptResponse
from src.model.main import Transcriptor
from fastapi import (
    APIRouter,
    HTTPException, 
    UploadFile,
    File,
    Query, 
)


router = APIRouter()
Transcriptor = Transcriptor()

@router.post("/data_parquet")
async def data_parquet(
    api_key: str = Query(..., description="Token de acceso en formato string"),
    audio_file: UploadFile = File(..., description="Archivo .wav a subir"),
) -> TranscriptResponse:
    """
    Transcribe un archivo .wav a un bucket de Google Cloud Storage
    """
    if api_key != 'bcd4d613-fb88-491d-1571e':
        raise HTTPException(status_code=401, detail=f"API key invalid")
    return Transcriptor.transcribir_audio(audio_file)