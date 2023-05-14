import logging
import asyncio
from websockets.server import serve
import websockets


logging.basicConfig()
LOGGER = logging.getLogger("ws_server")
LOGGER.setLevel(logging.DEBUG)


connections = []


async def receive(websocket):
    try:
        if websocket not in connections:
            connections.append(websocket)

        async for message in websocket:
            LOGGER.info(message)
            websockets.broadcast(connections, message)

    except Exception as e:
        LOGGER.error(e)


async def main():
    async with serve(receive, "localhost", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
