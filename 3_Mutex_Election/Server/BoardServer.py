#!/usr/bin/env python
import asyncio
import json
import sys
import websockets
from websockets.asyncio.server import serve

# UseMutexForUpdates.storage(localStorage, otherServersOfCluster, serverID, leaderElection)
storage = None
# Port number on which the server has to be started.
port = -1  # Changed in function startServer

'''
First point in the server (= server API) to receive the request 
(from both client proxy and other server proxy)
'''

'''
Case 1: If COMMAND is UPDATE operations (put, delete, deleteAll, modify):
+ Stub matchs the COMMAND and call the correct method inside UseMutexForUpdates.storage()
+ This storage has a queue an a corountine (background worker) to update the AsyncBoardStorage (its own local storage) and
talk to proxy of other server if needed
+ ACQUIRE and RELEASE commands are only called by the proxy of other server (this call is done in the corountine inside UseMutexForUpdates)
'''

'''
Case 2: If COMMAND = ACQUIRE / RELEASE:
+ Stub calls myMutex.acquire() / myMutex.storage() as myMutex an instance of Mutex
+ Raise Error if myMutex is None
Testing in a: Start server, create proxy from AsyncBoardProxy and call the method acquire/release
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
        senderId = int(request_object.get("MYID", -1))
        result_data = None 

        # 2. Call the correct storage method
        # storage = UseMutexForUpdates.storage(localStorage, otherServersOfCluster, serverID, leaderElection)
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

            case "ACQUIRE":
                if myMutex is None:
                    raise ValueError("ERROR because Mutex is None and Acquire is called")
                result_data = await myMutex.acquire()  

            case "RELEASE":
                if myMutex is None:
                    raise ValueError("ERROR because Mutex is None and Release is called")
                await myMutex.release()
                result_data = "DONE"
            
            case "AREYOUALIVE":
                result_data = "YES"

            case "ELECTION":
                if leaderElec is None:
                    raise ValueError("ERROR")
                result_data = await leaderElec.election()

            case "SETCOORDINATOR":
                if leaderElec is None:
                    raise ValueError("ERROR")
                coord_id = request_object["COORDINATORID"] 
                await leaderElec.setCoordinator(coord_id)
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
    async with websockets.serve(handler, "localhost", port, ping_interval=None) as server:
        print(f"[Server] started at {port}")
        await server.serve_forever()


# Called by the main module to start the server
def startServer(portToUse, storageToUse, serverId=0, mutex=None, leaderElection=None):
    global port
    global storage
    global myID
    global myMutex
    global leaderElec

    port = portToUse
    myID = serverId
    storage = storageToUse
    myMutex = mutex
    leaderElec = leaderElection

    asyncio.run(serverMain())
