import VectorClock

class storage:
    """Storage for message board"""

    def __init__(self, localStorage, serversToInformAboutChanges, serverId, logicalClock):
        self.localStorage = localStorage
        self.clock = logicalClock
        self.listAllProxies = serversToInformAboutChanges   # [proxy(serverPort=10000,serverId= 0), proxy(10001, 0), proxy(10002, 0), proxy(10003, 0)]
        self.serverId = int(serverId)

    async def put(self, message, senderId, seqNb=None):
        """Add a message """
        # If this request comes from client then update other servers by calling proxy of each server
        # Else, this request come from other server, so don't call this for loop again to not be in an infinite loop
        if senderId == -1:
            # Get the COPY of the self.clock.getTime() instead a reference
            my_time = self.clock.getTime()[:]
            msg_time_list = [my_time,message]
            await self.localStorage.put(msg_time_list, senderId=senderId)
            for idx, proxy in enumerate(self.listAllProxies):
                if idx == self.serverId:
                    continue
                await proxy.put(msg_time_list)
        else:
            await self.localStorage.put(message, senderId=senderId)

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
            msg_with_time = await self.localStorage.get(index, senderId=senderId)
            new_msg = [msg_with_time[0], message]
            await self.localStorage.modify(index, new_msg, senderId=senderId)
            for idx, proxy in enumerate(self.listAllProxies):
                if idx == self.serverId:
                    continue
                await proxy.modify(index, new_msg)
        else:
            await self.localStorage.modify(index, message, senderId=senderId)

    async def delete(self, index, senderId, seqNb=None):
        """Delete message that has index x"""
        await self.localStorage.delete(index, senderId=senderId)
        if senderId == -1:
            for idx, proxy in enumerate(self.listAllProxies):
                if idx == self.serverId:
                    continue
                await proxy.delete(index)

    async def deleteAll(self, senderId, seqNb=None):
        await self.localStorage.deleteAll(senderId=senderId)
        if senderId == -1:
            for idx, proxy in enumerate(self.listAllProxies):
                if idx == self.serverId:
                    continue
                await proxy.deleteAll()
    
    @staticmethod
    def compareMessages(m1:list, m2:list):
        return VectorClock.totalOrder(m1[0], m2[0])


    async def close(self):
        pass
