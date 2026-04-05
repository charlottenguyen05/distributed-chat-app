import VectorClock


class storage:
    """Storage for message board"""

    def __init__(
        self, localStorage, serversToInformAboutChanges, serverId, logicalClock
    ):
        self.localStorage = localStorage
        self.clock = logicalClock
        self.listAllProxies = serversToInformAboutChanges  # [proxy(serverPort=10000,serverId= 0), proxy(10001, 0), proxy(10002, 0), proxy(10003, 0)]
        self.serverId = int(serverId)
    
    async def synchronize(self, pairServerID):
        pairStorage = await self.listAllProxies[pairServerID].getBoard()
        myStorage = await self.localStorage.getBoard()
        missing_from_local = []
        missing_from_other_server = []

        for msg in pairStorage:
            if msg not in myStorage:
                missing_from_local.append(msg)
        
        for msg in myStorage:
            if msg not in pairStorage:
                missing_from_other_server.append(msg)

        for msg in missing_from_local:
            await self.localStorage.put(msg)
            
        for msg in missing_from_other_server:
            await self.listAllProxies[pairServerID].put(msg)


    async def put(self, message, senderId, seqNb=None):
        """Add a message"""
        if senderId == -1:
            # Get the COPY of the self.clock.getTime() instead a reference
            my_time = self.clock.getTime()[:]
            msg_time_list = [my_time, message]
            await self.localStorage.put(msg_time_list)
        else:
            await self.localStorage.put(message)

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
        if senderId == -1:
            msg_with_time = await self.localStorage.get(index)
            new_msg = [msg_with_time[0], message]
            await self.localStorage.modify(index, new_msg)
            # for idx, proxy in enumerate(self.listAllProxies):
            #     if idx == self.serverId:
            #         continue
            #     await proxy.modify(index, new_msg)
        else:
            await self.localStorage.modify(index, message)

    async def delete(self, index, senderId, seqNb=None):
        """Delete message that has index x"""
        await self.localStorage.delete(index)
        # if senderId == -1:
        #     for idx, proxy in enumerate(self.listAllProxies):
        #         if idx == self.serverId:
        #             continue
        #         await proxy.delete(index)

    async def deleteAll(self, senderId, seqNb=None):
        await self.localStorage.deleteAll()
        # if senderId == -1:
        #     for idx, proxy in enumerate(self.listAllProxies):
        #         if idx == self.serverId:
        #             continue
        #         await proxy.deleteAll()

    def compareMessages(self, m1: list, m2: list):
        return VectorClock.totalOrder(m1[0], m2[0])

    async def close(self):
        pass
