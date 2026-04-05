class storage:
    def __init__(self, localStorage, serversToInformAboutChanges, serverId, IdOfCoordinator):
        self.localStorage = localStorage
        self.listAllProxies = serversToInformAboutChanges   # [proxy(serverPort=10000,serverId= 0), proxy(10001, 0), proxy(10002, 0), proxy(10003, 0)]
        self.serverId = int(serverId)
        self.IdOfCoordinator = int(IdOfCoordinator)

    async def put(self, message, senderId):
        """Add a message """
        if self.serverId == self.IdOfCoordinator:
            await self.localStorage.put(message)
            # couroutines sends concurently asyncio.gather()
            for idx, proxy in enumerate(self.listAllProxies):
                print("proxy number", idx)
                if idx == self.serverId:
                    continue
                await proxy.put(message)
        # If the receiver is the normal server
        else:
            if senderId == self.IdOfCoordinator:
                await self.localStorage.put(message)
            elif senderId == -1: 
                await self.listAllProxies[self.IdOfCoordinator].put(message)
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

    async def modify(self, index, message, senderId):
        """Change the content of message that has index x"""
        if self.serverId == self.IdOfCoordinator:
            await self.localStorage.modify(index, message)
            for idx, proxy in enumerate(self.listAllProxies):
                print("proxy number", idx)
                if idx == self.serverId:
                    continue
                await proxy.modify(index, message)
        else:
            if senderId == self.IdOfCoordinator:
                await self.localStorage.modify(index, message)
            elif senderId == -1:
                await self.listAllProxies[self.IdOfCoordinator].modify(index, message)
            else:
                print("Why two normal server communicate with each other??")

    async def delete(self, index, senderId):
        """Delete message that has index x"""
        if self.serverId == self.IdOfCoordinator:
            await self.localStorage.delete(index)
            for idx, proxy in enumerate(self.listAllProxies):
                print("proxy number", idx)
                if idx == self.serverId:
                    continue
                await proxy.delete(index)
        else:
            if senderId == self.IdOfCoordinator:
                await self.localStorage.delete(index)
            elif senderId == -1:
                await self.listAllProxies[self.IdOfCoordinator].delete(index)
            else:
                print("Why two normal server communicate with each other??")
      

    async def deleteAll(self, senderId):
        if self.serverId == self.IdOfCoordinator:
            await self.localStorage.deleteAll()
            for idx, proxy in enumerate(self.listAllProxies):
                print("proxy number", idx)
                if idx == self.serverId:
                    continue
                await proxy.deleteAll()
        else:
            if senderId == self.IdOfCoordinator:
                await self.localStorage.deleteAll()
            elif senderId == -1:
                await self.listAllProxies[self.IdOfCoordinator].deleteAll()
            else:
                print("Why two normal server communicate with each other??")


    async def close(self):
        pass
