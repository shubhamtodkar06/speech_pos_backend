# stt_pos/consumers.py
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from google.cloud import speech
import nltk
from nltk.tokenize import word_tokenize
import json

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

CREDENTIALS_PATH = 'big-buttress-457415-v1-2a505cf38889.json'

class STTPOSEndpoint(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connected")

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, bytes_data=None):
        if bytes_data:
            try:
                client = speech.SpeechClient.from_service_account_file(CREDENTIALS_PATH)

                audio = speech.RecognitionAudio(content=bytes_data)
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                    sample_rate_hertz=48000,
                    language_code="en-IN",
                )

                operation = client.long_running_recognize(config=config, audio=audio)
                print("Waiting for Google STT operation to complete...")
                response = await asyncio.to_thread(operation.result, timeout=30)

                transcript = ""
                for result in response.results:
                    transcript += result.alternatives[0].transcript

                if transcript:
                    print(f"Google STT Transcript: {transcript}")
                    await self.send(text_data=json.dumps({'transcript': transcript}))  # Send raw transcript first
                    tagged_output_html = self.perform_pos_tagging(transcript)
                    await asyncio.sleep(0.1)  # Small delay before sending tags
                    await self.send(text_data=json.dumps({'transcript_tags': tagged_output_html}))
                else:
                    await self.send(text_data=json.dumps({'error': 'Google Speech-to-Text failed to transcribe.'}))

            except Exception as e:
                await self.send(text_data=json.dumps({'error': f'Backend processing error: {e}'}))

    def perform_pos_tagging(self, text):
        tokens = word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        output_html = ""
        for word, tag in tagged:
            output_html += f'<span class="{tag.lower()}">{word}/{tag}</span> '
        return output_html