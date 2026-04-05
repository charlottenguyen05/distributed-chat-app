# Information on the websocket-client is available at
# https://websocket-client.readthedocs.io/en/latest/
"""
Connection of the current server to talk to other server
"""

import json
import asyncio
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed


class storage:
    def __init__(self, port, senderId, logicalClock=None):
        """
        port: the port number of the destination server this proxy need to communicate to
        senderId: sender server ID
        logicalClock: the Vector Clock object of the current server
        """
        self.port = port
        self.senderId = senderId
        self.clock = logicalClock
        self.lock = asyncio.Lock()
        self.ws = None

    async def doOperation(self, request):
        """
        Add MYID key: id of sender (the Encodes the request in JSON, sends it to all another servers,
        waits for the response and decodes this JSON message.
        Add TIME key: vector clock list of the server to send as the sender's clock to other server
        This function now handles one full transaction:
        connect, send, receive, and close.
        """
        request["MYID"] = self.senderId
        if self.clock is not None:
            request["TIME"] = self.clock.getTime()
        request_json = json.dumps(request)

        response_object = {"status": "ERROR", "error": ""}
        async with self.lock:
            # If no connection, or the previous one closed, open a new one.
            if self.ws is None:
                try:
                    self.ws = await connect(f"ws://localhost:{self.port}/")
                    print(f"[Proxy] Connected to {self.port}")
                except Exception as e:
                    return {
                        "status": "ERROR",
                        "error": f"Connection Refused: {str(e)}",
                    }

            # Reuse connection
            try:
                await self.ws.send(request_json)
                response_json = await self.ws.recv()
                response_object = json.loads(response_json)
                # Update my clock with received time
                if "TIME" in response_object and self.clock:
                    self.clock.updateTime(response_object["TIME"])

            except ConnectionClosed:
                # set self.ws to None so reconnect on the next call
                self.ws = None
                response_object = {
                    "status": "ERROR",
                    "error": "Connection broken, retry needed",
                }

        return response_object

    async def put(self, message, seqNb=None):
        request = {"COMMAND": "PUT", "MESSAGE": message}
        request["SEQNB"] = seqNb
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")

    async def get(self, index):
        request = {"COMMAND": "GET", "INDEX": index}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            raise ValueError(response_object["error"])
        return response_object["result"]

    async def getNum(self):
        request = {"COMMAND": "GETNUM"}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")
            return 0
        return response_object["result"]

    async def getBoard(self):
        request = {"COMMAND": "GETBOARD"}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")
            return []
        return response_object["result"]

    async def modify(self, index, message,seqNb=None):
        request = {"COMMAND": "MODIFY", "INDEX": index, "MESSAGE": message}
        request["SEQNB"] = seqNb
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            raise ValueError(response_object["error"])

    async def delete(self, index,seqNb=None):
        request = {"COMMAND": "DELETE", "INDEX": index}
        request["SEQNB"] = seqNb
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            raise ValueError(response_object["error"])

    async def deleteAll(self,seqNb=None):
        request = {"COMMAND": "DELETEALL"}
        request["SEQNB"] = seqNb
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")

    async def acquire(self):
        request = {"COMMAND": "ACQUIRE"}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")
        return response_object["result"]

    async def release(self):
        request = {"COMMAND": "RELEASE"}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")
        return response_object["result"]

    async def election(self):
        request = {"COMMAND": "ELECTION"}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            return False
        return response_object["result"]

    async def areYouAlive(self):
        request = {"COMMAND": "AREYOUALIVE"}
        response_object = await self.doOperation(request)
        if response_object["status"] == "OK":
            return True
        else:
            return False

    async def setCoordinator(self, coordinatorID):
        request = {"COMMAND": "SETCOORDINATOR", "COORDINATORID": coordinatorID}
        response_object = await self.doOperation(request)
        if response_object["status"] == "ERROR":
            return False
        return True
    
    async def getSequenceNumber(self):
        request = {"COMMAND": "GETSEQUENCENUMBER"}
        response_object = await self.doOperation(request)
        if response_object["status"] == "OK":
            return response_object["result"]
        else:
            return False

    async def close(self):
        self.ws.close()
