import AsyncBoardProxy
import AsyncBoardStorage
import BoardServer
import InformAllOtherServers
import logging
import sys

# Ports of the servers of the cluster
serverPorts = [10000, 10001, 10002, 10003]

# Parameters: ID of cluster to be started, e.g. 0, 1, 2, 3
if len(sys.argv) < 2:  # If ID of cluster is not given, then terminate program
    print("StartClusterInformingEachOther.py <ID of server>")
    exit(1)

serverId = int(sys.argv[1])  # Id of this server provided as parameter
port = serverPorts[serverId]

# Configure logging of websockets
logging.basicConfig(
    format=str(serverId) + " %(asctime)s %(message)s",
    level=logging.DEBUG,
)


# Create a list of proxies for all the servers
serversToInformAboutChanges = [
    AsyncBoardProxy.storage(serverPorts[id], serverId) for id in range(len(serverPorts))
]

# Create storage containing data of this server.
localStorage = AsyncBoardStorage.storage()

# Create object with distribution algorithm
storage = InformAllOtherServers.storage(
    localStorage, serversToInformAboutChanges, serverId
)

# Start server
BoardServer.startServer(port, storage, serverId=serverId)

# Explain what does InformAllOtherServers_Main and InformAllOtherServers do:
# Start server id 0 (python InformAllOtherServers_Main.py 0) includes:
# 1. Create a list of proxies = [proxy(serverPort=10000,serverId= 0), proxy(10001, 0), proxy(10002, 0), proxy(10003, 0)]
# 2. Create local storage for server id 0
# 3. Create a InformAllOtherServers.storage object that know the localStorage of that server 0,
# has the list of all proxies to talk to other servers, know the ID of the current server (sender server)

