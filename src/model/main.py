from src.model.entitites.response import TranscriptResponse
import speech_recognition as sr
from fastapi import File


class Transcriptor:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribir_audio(
            self,
            audio_file: File,
        ) -> TranscriptResponse:
        try:
            audio = self.recognizer.record(sr.AudioFile(audio_file))  
            return self.recognizer.recognize_google(
                audio, # Lee todo el audio
                language="es-ES" # Cambiar 'es-ES' para otro idioma
            )  
        except sr.UnknownValueError:
            return "No se pudo entender el audio."