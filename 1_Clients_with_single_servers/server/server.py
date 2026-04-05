import logging
import asyncio
import websockets
from websockets.asyncio.client import connect

port_nb_input = input("port number to wait for connections: ")
port_nb_output = input("port number to forward to: ")
PORT_OUPUT = ""
if port_nb_output.strip() != "":
    PORT_OUPUT = "ws://localhost:" + port_nb_output
    print(PORT_OUPUT)
PORT_INPUT = port_nb_input.strip() or 10000


async def client_handler(websocket_from_client):
    """Receives ping from a client, forwards it to Server B,
    waits for pong, and sends it back."""
    try:
        # This loop keeps the connection client-server alive and handles multiple messages
        # If don't use this loop, when all line of code execute, the connection auto shut down so the client can not process the response
        async for request_msg_from_client in websocket_from_client:
            if PORT_OUPUT != "":
                # Open a new connection to another server
                connection = await connect(PORT_OUPUT) 
                await connection.send(request_msg_from_client)
                response_from_another_server = await connection.recv()
                await websocket_from_client.send(response_from_another_server)
                await connection.close()
            else:
                print("No foward to another server")
                await websocket_from_client.send("pong")
    except websockets.exceptions.ConnectionClosed:
        print("[Server] Client disconnected.")


async def main():
    async with websockets.serve(client_handler, "localhost", PORT_INPUT) as server:
        print(f"[Server] started at {PORT_INPUT}")
        await server.serve_forever()


logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

if __name__ == "__main__":
    asyncio.run(main())
