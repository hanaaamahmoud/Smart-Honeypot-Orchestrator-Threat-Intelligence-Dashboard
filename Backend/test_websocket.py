import asyncio
import websockets


async def test():

    uri = "ws://127.0.0.1:8001/ws"

    async with websockets.connect(uri) as websocket:

        print("Connected to WebSocket")

        while True:

            message = await websocket.recv()

            print("Received:")
            print(message)


asyncio.run(test())