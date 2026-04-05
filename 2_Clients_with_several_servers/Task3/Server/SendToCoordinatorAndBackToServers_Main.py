import AsyncBoardProxy
import AsyncBoardStorage
import BoardServer
import logging
import SendToCoordinatorAndBackToServers
import sys

# Ports of the servers of the cluster
serverPorts = [10000, 10001, 10002, 10003]
IdOfCoordinator = 0

# Parameters: ID of cluster to be started, e.g. 0, 1, 2, 3
if len(sys.argv) < 2: # If ID of cluster is not given, then terminate program
        print("StartClusterInformingEachOther.py <ID of server>")
        exit(1)

serverId = int(sys.argv[1]) # Id of this server provided as parameter
port = serverPorts [serverId]

# Configure logging of websockets
logging.basicConfig(
   format= str(serverId) + " %(asctime)s %(message)s", #level=logging.DEBUG,
)

# Create proxies for all servers
otherServersOfCluster = [AsyncBoardProxy.storage(serverPorts[id], serverId) for id in range(len(serverPorts))]

# Create storage containing data of this server. 
localStorage = AsyncBoardStorage.storage() 

# Create object with distribution algorithm 
storage = SendToCoordinatorAndBackToServers.storage(localStorage, otherServersOfCluster, serverId, IdOfCoordinator)    

# Start server
BoardServer.startServer(port, storage, serverId=serverId)