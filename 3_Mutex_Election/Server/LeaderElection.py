import asyncio

class election: 
    def __init__(self, proxies, myID): 
        """
        Constructs a new object for leader election. 
        Parameter proxies: List with the proxies of all servers ordered by their ID (0, 1, 2, 3, ...)
        Parameter myID: ID of the server in which the object is created. 
        """
        self.proxies = proxies
        self.myID = myID
        self.coordinatorID = 3
        self.election_event = asyncio.Event()
        self.election_event.set()
        
    async def getCoordiator(self): 
        """
        Returns the proxy of the coordinator.
        If there is no coordinator, a new coordinator is elected 
        and the function waits for that.
        Hence it always returns the proxy of a coordinator. 
        """
        isAlive = await self.callAreYouAlive(self.coordinatorID)
        if not isAlive:
            # Block future calls
            self.election_event.clear() 
            await self.startElection()
            # Block here until setCoordinator() calls self.election_event.set()
            await self.election_event.wait()
        return self.proxies[self.coordinatorID]

    async def startElection(self):
        """
        This function starts the election process. 
        When this coroutines ends, a new coordinator has been elected. 
        """
        print(f"Start election in {self.myID}")
        higher_id = []
        for i in range(len(self.proxies)):
            if i > self.myID:
                higher_id.append(i)
        if len(higher_id) == 0:
            self.coordinatorID = self.myID
            await self.callSetCoordinatorInAllServers(self.myID)
            self.election_event.set()
        else:
            list_take_over_res = await asyncio.gather(*[self.callElection(serverId) for serverId in higher_id])
            if "Take-Over" in list_take_over_res:
                return
            
            self.coordinatorID = self.myID
            await self.callSetCoordinatorInAllServers(self.myID)
            self.election_event.set()
    
               
    async def callAreYouAlive(self, serverID): 
        """
        Calls the function areYouAlive() on the server with the serverID.
        Parameter serverID: ID of the server to check if it is alive. 
        Returns True if the server is alive and False otherwise. 
        """
        res = await self.proxies[serverID].areYouAlive()
        return res
            
    async def callElection(self, serverID): 
        """
        Calls the the function election() on the a server with the serverID.
        Parameter serverID: ID of the server in which the method shall be called. 
        Returns the response of the server if the server responded and False otherwise. 
        """        
        res = await self.proxies[serverID].election()
        return res

    async def callSetCoordinator(self, serverID, coordinatorID): 
        """
        Calls the function setCoordinator() on the a server with the serverID.
        Parameter serverID: ID of the server in which the method shall be called. 
        Parameter coordinatorID: ID of the new coordinator to be announce. 
        Returns True if this was successfull or False if a ConnectionRefusedError was thrown.
        """
        res = await self.proxies[serverID].setCoordinator(coordinatorID)
        return res

    async def callSetCoordinatorInAllServers(self, coordinatorID): 
        """ 
        Informs all servers about the new coordinator. 
        Parameter coordinatorID: ID of the new coordinator to be announce. 
        The function is implemented by calling setCoordinator() on all servers.
        """
        tasks = []
        for idx, proxy in enumerate(self.proxies):
            if idx == self.myID:
                continue
            isServerAlive = await self.callAreYouAlive(idx)
            if isServerAlive:
                tasks.append(proxy.setCoordinator(coordinatorID))
        
        if tasks:
            await asyncio.gather(*tasks)
        return 
    
    ########################################################
    # Methods to be called from other servers via the stub #
    ########################################################
        
    async def election(self):
        """
        Called from other servers to start the election process. 
        Always retuns "Take-Over".
        """
        # Run the startElection in the background and return Take-Over immediately
        asyncio.create_task(self.startElection())
        return "Take-Over"                     
        
    async def setCoordinator(self, coordinatorID):
        """
        Called from to coordinator to inform the server about that it is coordinator. 
        Parameter coordinatorID: ID of the new coordinator. 
        """
        self.coordinatorID = coordinatorID
        self.election_event.set()
            
