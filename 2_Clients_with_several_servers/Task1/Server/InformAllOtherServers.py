class storage:
    """Storage for message board"""

    def __init__(self, localStorage, serversToInformAboutChanges, serverId):
        self.localStorage = localStorage
        self.listAllProxies = serversToInformAboutChanges   # [proxy(serverPort=10000,serverId= 0), proxy(10001, 0), proxy(10002, 0), proxy(10003, 0)]
        self.serverId = int(serverId)

    async def put(self, message, senderId):
        """Add a message """
        await self.localStorage.put(message)
        # If this request comes from client then update other servers by calling proxy of each server
        # Else, this request come from other server, so don't call this for loop again to not be in an infinite loop
        if senderId == -1:
            for idx, proxy in enumerate(self.listAllProxies):
                print("proxy number", idx)
                if idx == self.serverId:
                    continue
                await proxy.put(message)


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
        await self.localStorage.modify(index, message)
        if senderId == -1:
            for idx, proxy in enumerate(self.listAllProxies):
                if idx == self.serverId:
                    continue
                await proxy.modify(index, message)

    async def delete(self, index, senderId):
        """Delete message that has index x"""
        await self.localStorage.delete(index)
        if senderId == -1:
            for idx, proxy in enumerate(self.listAllProxies):
                if idx == self.serverId:
                    continue
                await proxy.delete(index)

    async def deleteAll(self, senderId):
        await self.localStorage.deleteAll()
        if senderId == -1:
            for idx, proxy in enumerate(self.listAllProxies):
                if idx == self.serverId:
                    continue
                await proxy.deleteAll()

    async def close(self):
        pass
