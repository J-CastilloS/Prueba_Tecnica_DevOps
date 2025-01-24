class TranscriptResponse:
    def __init__(self, transcript_text: str):
        self.transcript_text = transcript_text

    def __str__(self):
        return self.transcript_text