import logging
import json
from typing import Optional

import websockets

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings

from .utils import validate_ticker_name, get_ticker, get_messages

logger = logging.getLogger(__name__)


class AsyncCryptoConsumer(AsyncJsonWebsocketConsumer):
    ticker: Optional[str] = None

    async def connect(self):
        await super().connect()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.ticker, self.channel_name)

    async def send_content(self, data):
        await self.send_json(content=data['content'])

    async def subscribe(self, ticker):
        if self.ticker:
            await self.channel_layer.group_discard(self.ticker, self.channel_name)
        if not validate_ticker_name(ticker):
            await self.send_json({"status": "error", "message": "Invalid ticker name"})
        self.ticker = ticker
        await self.channel_layer.group_add(self.ticker, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if content.get('action') == 'subscribe':
            await self.subscribe(content.get('params'))


class AsyncPolygonConsumer(AsyncJsonWebsocketConsumer):
    async def connect_polygon(self, *args, **kwargs):
        async for websocket in websockets.connect(settings.POLYGON_CRYPTO_URL):
            await self.authenticate(websocket)
            await self.subscribe_tickers(websocket)
            try:
                async for messages in websocket:
                    messages = json.loads(messages)
                    if messages:
                        await self.channel_layer.group_send(
                            get_ticker(messages),
                            {
                                "type": "send.content",
                                "content": get_messages(messages)
                            }
                        )
            except websockets.ConnectionClosed:
                logger.error("Connection to polygon lost! Retrying..")

    @staticmethod
    async def authenticate(websocket):
        await websocket.send(json.dumps({"action": "auth", "params": settings.POLYGON_KEY}))

    @staticmethod
    async def subscribe_tickers(websocket):
        for ticker in settings.POLYGON_TICKERS:
            await websocket.send(json.dumps({"action": "subscribe", "params": ticker}))
