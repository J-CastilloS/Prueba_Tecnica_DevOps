from src.model.entities.response import TranscriptResponse
import speech_recognition as sr


class Transcriptor:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribir_audio(
            self,
            audio_file: sr.AudioFile,
        ) -> TranscriptResponse:
        try:
            audio = self.recognizer.record(audio_file)  
            transcript_text = self.recognizer.recognize_google(
                audio,  # Lee todo el audio
                language="es-ES"  # Cambiar 'es-ES' para otro idioma
            )
            return TranscriptResponse(transcript_text)  # Devolvemos la respuesta como un objeto
        except sr.UnknownValueError:
            return TranscriptResponse("No se pudo entender el audio.")  # Devolvemos el error como un objeto
        except Exception as e:  # Captura cualquier otra excepción
            return TranscriptResponse(f"Ocurrió un error: {str(e)}")  # Devuelve el mensaje de error