import os
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import language_v1beta2 as language_v1

def transcribe_and_analyze_audio():
    try:
        # Configura las credenciales de autenticación de Google Cloud
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "myCredentials.json"

        # Convierte el archivo de audio a mono
        audio = AudioSegment.from_wav("audioPrueba1.wav")
        audio = audio.set_channels(1)  # Convierte a mono
        audio.export("audioPrueba1_mono.wav", format="wav")

        # Crea un cliente de Speech-to-Text
        speech_client = speech.SpeechClient()

        # Configura la configuración de reconocimiento de audio
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="es-ES",
        )

        # Lee el archivo de audio
        with open("audioPrueba1_mono.wav", "rb") as audio_file:
            content = audio_file.read()

        # Crea una solicitud de reconocimiento de audio
        audio = speech.RecognitionAudio(content=content)

        # Realiza la solicitud de reconocimiento de audio
        response = speech_client.recognize(config=config, audio=audio)

        # Crea un cliente de Natural Language
        language_client = language_v1.LanguageServiceClient()

        # Combina todas las transcripciones en un solo texto
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])

        # Analiza el sentimiento del texto transcribido
        document = language_v1.Document(content=transcript, type_=language_v1.Document.Type.PLAIN_TEXT, language="es")
        sentiment_response = language_client.analyze_sentiment(document=document, encoding_type=language_v1.EncodingType.UTF8)

        # Imprime el sentimiento del texto
        print("Sentimiento del texto:", sentiment_response.document_sentiment.score)

    except Exception as e:
        print("Ocurrió un error: ", e)

# Llama a la función para transcribir y analizar el audio
transcribe_and_analyze_audio()