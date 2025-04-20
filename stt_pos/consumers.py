# stt_pos/consumers.py
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class STTPOSEndpoint(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connected")

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, bytes_data=None):
        if bytes_data:
            print(f"Received audio data: {len(bytes_data)} bytes")
            # Placeholder for STT processing
            await self.send(text_data={'message': 'Received audio, processing...'})

    async def send_transcript_with_tags(self, message):
        await self.send(text_data=message)