# Information on the websocket-client is available at
# https://websocket-client.readthedocs.io/en/latest/


import json
import websocket


class storage:
    def __init__(self, port):
        self.port = port
        self.ws = None

    def doOperation(self, request):
        """
        Encodes the request in JSON, sends it to the server,
        waits for the response and decodes this JSON message.
        This function now handles one full transaction:
        connect, send, receive, and close.
        """
        request_json = json.dumps(request)
        # Default error response in case of connection failure
        response_object = {
            "status": "ERROR",
            "error": "Failed to connect after 1 attempt",
        }
        try:
            if self.ws is None:
                self.ws = websocket.WebSocket()
                self.ws.connect(f"ws://localhost:{self.port}/")
            try:
                self.ws.send(request_json)
                response_json = self.ws.recv()
                response_object = json.loads(response_json)
            except websocket.WebSocketConnectionClosedException:
                self.ws = None
                response_object = {
                    "status": "ERROR",
                    "error": "Connection broken, retry needed",
                }

        except ConnectionRefusedError:
            print("Connection refused. Server not running")

        except websocket._exceptions.WebSocketException as e:
            print(f"A WebSocket error occurred: {e}")

        # 7. Return the final response object (e.g., {"status": "OK", ...})
        return response_object

    def put(self, message):
        request = {"COMMAND": "PUT", "MESSAGE": message}
        response_object = self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")

    def get(self, index):
        request = {"COMMAND": "GET", "INDEX": index}
        response_object = self.doOperation(request)
        if response_object["status"] == "ERROR":
            raise ValueError(response_object["error"])
        return response_object["result"]

    def getNum(self):
        request = {"COMMAND": "GETNUM"}
        response_object = self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")
            return 0
        return response_object["result"]

    def getBoard(self):
        request = {"COMMAND": "GETBOARD"}
        response_object = self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")
            return []
        return response_object["result"]

    def modify(self, index, message):
        request = {"COMMAND": "MODIFY", "INDEX": index, "MESSAGE": message}
        response_object = self.doOperation(request)
        if response_object["status"] == "ERROR":
            raise ValueError(response_object["error"])

    def delete(self, index):
        request = {"COMMAND": "DELETE", "INDEX": index}
        response_object = self.doOperation(request)
        if response_object["status"] == "ERROR":
            raise ValueError(response_object["error"])

    def deleteAll(self):
        request = {"COMMAND": "DELETEALL"}
        response_object = self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")
    
    def synchronize(self, pairServerID):
        request = {"COMMAND": "SYNCHRONIZE", "MESSAGE": pairServerID}
        response_object = self.doOperation(request)
        if response_object["status"] == "ERROR":
            print(f"Server Error: {response_object['error']}")

    def close(self):
        if self.ws is not None:
            self.ws.close()
