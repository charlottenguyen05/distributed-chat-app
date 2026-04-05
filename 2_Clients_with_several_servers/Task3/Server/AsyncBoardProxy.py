# Information on the websocket-client is available at
# https://websocket-client.readthedocs.io/en/latest/
"""
Handle client connection to other servers
"""

import json
import asyncio
from websockets.asyncio.client import connect

class storage:
    def __init__(self, port, senderId):
        """
        port: the port number of the destination server this proxy need to communicate to
        senderId: sender server ID
        """
        self.port = port
        self.senderId = senderId
        self.lock = asyncio.Lock()
        self.ws = None
    
    async def doOperation(self, request):
        """
        Add MYID key: id of sender (the Encodes the request in JSON, sends it to the server, 
        waits for the response and decodes this JSON message.
        This function now handles one full transaction:
        connect, send, receive, and close.
        """
        request["MYID"] = self.senderId
        request_json = json.dumps(request)
        response_object = {"status": "ERROR", "error": ""}
        async with self.lock:
            try:
                async with connect(f"ws://localhost:{self.port}/") as self.ws:
                        await self.ws.send(request_json)
                        response_json = await self.ws.recv()
                        response_object = json.loads(response_json)
                        print(f"[Board Proxy] Received: '{response_json}'")

            except ConnectionRefusedError:
                    response_object = {"status": "ERROR", "error": "Connection refused"}
            
            # 7. Return the final response object (e.g., {"status": "OK", ...})
        return response_object

    async def put(self, message):
        request = {"COMMAND": "PUT", "MESSAGE": message}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")

    async def get(self, index):
        request = {"COMMAND":"GET", "INDEX":index} 
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            raise ValueError(response_object["error"])
        return response_object["result"]

    async def getNum(self):
        request = {"COMMAND":"GETNUM"} 
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")
            return 0 
        return response_object["result"]

    async def getBoard(self):
        request = {"COMMAND":"GETBOARD"}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")
            return [] 
        return response_object["result"]

    async def modify(self, index, message):
        request = {"COMMAND":"MODIFY", "INDEX": index, "MESSAGE": message}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            raise ValueError(response_object["error"])

    async def delete(self, index):
        request = {"COMMAND":"DELETE", "INDEX": index}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            raise ValueError(response_object["error"])

    async def deleteAll(self):
        request = {"COMMAND":"DELETEALL"}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")
    

    async def close(self):
        self.ws.close()
