from src.model.main import Transcriptor

def test_transcribir_audio():
    transcriptor = Transcriptor()
    resultado = transcriptor.transcribir_audio("test_audio.wav")
    assert isinstance(resultado, str)  # Asegúrate de que devuelva un string