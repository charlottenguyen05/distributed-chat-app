#!/usr/bin/env python

import asyncio
import json
import sys
import websockets
from websockets.asyncio.server import serve

# InformAllOtherServers.storage()
storage = None

# Port number on which the server has to be started.
port = -1  # Changed in function startServer

'''
First point in the server (= server API) to receive the request 
(from both client proxy and other server proxy)
+ Stub matchs the COMMAND and call the correct method inside SendToCoordinatorAndBackToServers.storage()
+ This storage then update the AsyncBoardStorage (its own local storage) and
talk to proxy of other server if needed
'''


#########################################################
# Stub calling the methods on one storage object
# depending on the type of message received.
#########################################################
async def stub(request):
    """
    Stub: When it receives a request it calls the
    corresponding method in the storage.

    Parameter request: Request message that is already parsed.
                       It is a dictionary mapping the name of a field into its value.
                       Example: {"COMMAND": "PUT", "MESSAGE": "How are you?"}
    Returns the response message. It is not yet encoded as JSON message.
    """
    try:
        request_object = json.loads(request)
        method = request_object['COMMAND']
        print("request_object: ", request_object)
        senderId = int(request_object.get("MYID", -1))
        result_data = None 

        # 2. Call the correct storage method
        match method:
            case "PUT":
                # storage.put() returns "DONE"
                await storage.put(request_object["MESSAGE"], senderId)
                result_data = "DONE"     

            case "GET":
                # storage.get() returns a string or raises ValueError
                result_data = await storage.get(request_object["INDEX"])
            
            case "GETNUM":
                # storage.getNum() returns an int
                result_data = await storage.getNum()
            
            case "GETBOARD":
                # storage.getBoard() returns a list
                result_data = await storage.getBoard()
            
            case "MODIFY":
                # storage.modify() returns None on success or raises ValueError
                await storage.modify(request_object["INDEX"], request_object["MESSAGE"], senderId)
                result_data = "DONE" 
            
            case "DELETE":
                # storage.delete() returns None on success or raises ValueError
                await storage.delete(request_object["INDEX"], senderId)
                result_data = "DONE"
            
            case "DELETEALL":
                # storage.deleteAll() returns "DONE"
                await storage.deleteAll(senderId)
                result_data = "DONE"
            
            case _:
                # Handle any unknown commands
                raise ValueError(f"Unknown command: {method}")

        # Format the SUCCESS response.
        response_dict = {
            "status": "OK",
            "result": result_data
        }

    except ValueError as e:
        # 4. Format the ERROR response (e.g., "UNKNOWN_INDEX")
        response_dict = {
            "status": "ERROR",
            "error": str(e)
        }
    except KeyError as e:
        # 5. Handle cases where "MESSAGE" or "INDEX" is missing
        response_dict = {
            "status": "ERROR",
            "error": f"Missing field in request: {str(e)}"
        }
    except Exception as e:
        # 6. Catch-all for any other unexpected error
        response_dict = {
            "status": "ERROR",
            "error": f"An unexpected server error occurred: {str(e)}"
        }
        
    # 7. Return the formatted dictionary
    return response_dict


#########################################################
# Handler for performing server tasks of one client connection
#########################################################
async def handler(websocket):
    async for request in websocket:
        print("Server receive:", request)
        response_dict = await stub(request)
        response_json = json.dumps(response_dict)
        await websocket.send(response_json)

#########################################################
# Code for starting the server
#########################################################
async def serverMain():
    async with websockets.serve(handler, "localhost", port) as server:
        print(f"[Server] started at {port}")
        await server.serve_forever()


# Called by the main module to start the server
def startServer(portToUse, storageToUse, serverId=0):
    global port
    global storage
    global myID

    port = portToUse
    myID = serverId
    storage = storageToUse

    asyncio.run(serverMain())
