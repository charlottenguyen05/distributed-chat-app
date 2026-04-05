import logging
import asyncio
import websockets

ANOTHER_SERVER_PORT = 10001

async def handler(websocket_from_server):
    """Handler request from the server (in server.py, which act as client)"""
    async for request_msg in websocket_from_server:
        print("another service receive:", request_msg)
        if request_msg == "ping":
            await websocket_from_server.send("pong")


async def main():
    """
    Start and keep the server running forever
    A new instance of handler task function will be created to handle
    each client connected to this server
    """
    async with websockets.serve(handler, "localhost", ANOTHER_SERVER_PORT) as another_server:
        print(f"another server started at ws://localhost:{ANOTHER_SERVER_PORT}")
        await another_server.serve_forever()


logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

if __name__ == "__main__":
    asyncio.run(main())
