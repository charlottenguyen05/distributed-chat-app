import asyncio

class storage: 
    def __init__(self, proxy): 
        self.proxy = proxy

    async def put(self, message, sequenceNumber=None): 
        return await self.proxy.put(message, sequenceNumber)
      
    async def modify(self, index, message, sequenceNumber=None): 
        return await self.proxy.modify(index, message, sequenceNumber)
        
    async def delete(self, index, sequenceNumber=None): 
        return await self.proxy.delete(index, sequenceNumber)
            
    async def deleteAll(self, sequenceNumber=None): 
        return await self.proxy.deleteAll(sequenceNumber)

    async def get(self, index): 
        return await self.proxy.get(index)
            
    async def getNum(self): 
        return await self.proxy.getNum()
        
    async def getBoard(self): 
        return await self.proxy.getBoard()
        
    async def acquire(self):
        return await self.proxy.acquire()
        
    async def release(self): 
        return await self.proxy.release() 
        
    async def areYouAlive(self):
        return await self.proxy.areYouAlive()
        
    async def election(self):
        return await self.proxy.election()
        
    async def setCoordinator(self, coordinatorID):
        return await self.proxy.setCoordinator(coordinatorID)
        
    async def getSequenceNumber(self):
        return await self.proxy.getSequenceNumber()

    async def close(self): 
        self.proxy.close()