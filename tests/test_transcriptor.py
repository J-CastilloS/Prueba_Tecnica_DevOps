import pytest
from unittest.mock import MagicMock, patch
from src.model.transcriptor import Transcriptor
from src.model.entities.response import TranscriptResponse

# Test para verificar que se transcribe correctamente
@patch('speech_recognition.Recognizer.recognize_google')
@patch('speech_recognition.Recognizer.record')
def test_transcribir_audio(mock_record, mock_recognize_google):
    # Configura los mocks
    mock_audio = MagicMock()
    mock_record.return_value = mock_audio
    mock_recognize_google.return_value = "Texto transcrito correctamente"

    transcriptor = Transcriptor()
    
    # Llamar a la función que estamos probando
    resultado = transcriptor.transcribir_audio(mock_audio)

    # Verifica que el resultado es el esperado
    assert resultado.transcript_text == "Texto transcrito correctamente"  # Compara el texto de la transcripción
    mock_record.assert_called_once_with(mock_audio)  # Verifica que 'record' haya sido llamado
    mock_recognize_google.assert_called_once_with(mock_audio, language="es-ES")  # Verifica que 'recognize_google' haya sido llamado

# Test para verificar el manejo de excepciones
@patch('speech_recognition.Recognizer.recognize_google')
@patch('speech_recognition.Recognizer.record')
def test_transcribir_audio_exception(mock_record, mock_recognize_google):
    # Configura el mock para que lance una excepción
    mock_audio = MagicMock()
    mock_record.return_value = mock_audio
    mock_recognize_google.side_effect = Exception("API error")

    transcriptor = Transcriptor()
    
    # Llamar a la función que estamos probando
    resultado = transcriptor.transcribir_audio(mock_audio)

    # Verifica que el mensaje de error se devuelve correctamente
    assert resultado.transcript_text == "Ocurrió un error: API error"  # Compara el texto de la transcripción