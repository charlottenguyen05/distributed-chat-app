class storage:
    def __init__(self, localStorage, serversToInformAboutChanges, serverId, IdOfCoordinator):
        self.localStorage = localStorage
        self.listAllProxies = serversToInformAboutChanges   # [FaultTolerantProxy(serverPort=10000,serverId= 0), FaultTolerantProxy(10001, 0), FaultTolerantProxy(10002, 0), FaultTolerantProxy(10003, 0)]
        self.serverId = int(serverId)
        self.IdOfCoordinator = int(IdOfCoordinator)

    async def put(self, message, senderId, seqNb=None):
        """Add a message """
        if self.serverId == self.IdOfCoordinator:
            await self.localStorage.put(message, seqNb, senderId)
            for idx, proxy in enumerate(self.listAllProxies):
                print("proxy number", idx)
                if idx == self.serverId:
                    continue
                await proxy.put(message, seqNb)
        # If the receiver is the normal server
        else:
            if senderId == self.IdOfCoordinator:
                await self.localStorage.put(message, seqNb, senderId)
            elif senderId == -1: 
                await self.listAllProxies[self.IdOfCoordinator].put(message, seqNb)
            else:
                print("Why two normal server communicate with each other??")


    async def get(self, index):
        """Return an individual message by index (first message index 0)"""
        response = await self.localStorage.get(index)
        return response

    async def getNum(self):
        """Return the total number of messages in board"""
        response = await self.localStorage.getNum()
        return response

    async def getBoard(self):
        """Return a list of all the messages strings of the board"""
        response = await self.localStorage.getBoard()
        return response

    async def modify(self, index, message, senderId, seqNb=None):
        """Change the content of message that has index x"""
        if self.serverId == self.IdOfCoordinator:
            await self.localStorage.modify(index, message, seqNb, senderId)
            for idx, proxy in enumerate(self.listAllProxies):
                print("proxy number", idx)
                if idx == self.serverId:
                    continue
                await proxy.modify(index, message, seqNb)
        else:
            if senderId == self.IdOfCoordinator:
                await self.localStorage.modify(index, message, seqNb, senderId)
            elif senderId == -1:
                await self.listAllProxies[self.IdOfCoordinator].modify(index, message, seqNb)
            else:
                print("Why two normal server communicate with each other??")

    async def delete(self, index, senderId, seqNb=None):
        """Delete message that has index x"""
        if self.serverId == self.IdOfCoordinator:
            await self.localStorage.delete(index, seqNb, senderId)
            for idx, proxy in enumerate(self.listAllProxies):
                print("proxy number", idx)
                if idx == self.serverId:
                    continue
                await proxy.delete(index, seqNb)
        else:
            if senderId == self.IdOfCoordinator:
                await self.localStorage.delete(index, seqNb, senderId)
            elif senderId == -1:
                await self.listAllProxies[self.IdOfCoordinator].delete(index, seqNb)
            else:
                print("Why two normal server communicate with each other??")
      

    async def deleteAll(self, senderId, seqNb=None):
        if self.serverId == self.IdOfCoordinator:
            await self.localStorage.deleteAll(seqNb, senderId)
            for idx, proxy in enumerate(self.listAllProxies):
                print("proxy number", idx)
                if idx == self.serverId:
                    continue
                await proxy.deleteAll(seqNb)
        else:
            if senderId == self.IdOfCoordinator:
                await self.localStorage.deleteAll(seqNb, senderId)
            elif senderId == -1:
                await self.listAllProxies[self.IdOfCoordinator].deleteAll(seqNb)
            else:
                print("Why two normal server communicate with each other??")


    async def close(self):
        pass
