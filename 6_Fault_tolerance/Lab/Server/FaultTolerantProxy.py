import asyncio

class storage: 
    def __init__(self, proxy): 
        self.proxy = proxy  # AsyncBoardProxy instance (e.g: proxy(serverPort=10000,serverId= 0))
        self.queue = asyncio.Queue()
        self.isCoroutineRun = None
    
    def _ensure_coroutine_run(self):
        """Starts the background worker if it is not currently running."""
        if self.isCoroutineRun is None or self.isCoroutineRun.done():
            self.isCoroutineRun = asyncio.create_task(self.process_queue())
    
    async def process_queue(self):
        """
        1. Read operation from the queue
        2. Call the corresponding method in proxy 
         - If called failed (server down): wait 1 second to retry until success
        """
        while True:
            try:
                nextRequest = await self.queue.get()
                command = nextRequest[0]
                while True:
                    try:
                        match command:
                                case "PUT":
                                    await self.proxy.put(nextRequest[1], nextRequest[2])
                                    break
                                case "MODIFY":
                                    await self.proxy.modify(nextRequest[1], nextRequest[2], nextRequest[3])
                                    break
                                case "DELETE":
                                    await self.proxy.delete(nextRequest[1], nextRequest[2])
                                    break
                                case "DELETEALL":
                                    await self.proxy.deleteAll(nextRequest[1])
                                    break
                    except Exception as ex:
                        # Server is down or connection failed
                        print(f"[FaultTolerantProxy] Operation failed: {ex}, retrying in 1 second...")
                        await asyncio.sleep(1)
            except Exception as ex:
                print("[FaultTolerantProxy] Exception was received.", type(ex).__name__, ex.args)


    async def put(self, message, sequenceNumber=None): 
        self._ensure_coroutine_run()
        await self.queue.put(('PUT', message, sequenceNumber))
      
    async def modify(self, index, message, sequenceNumber=None): 
        self._ensure_coroutine_run()
        await self.queue.put(("MODIFY", index, message, sequenceNumber))
        
    async def delete(self, index, sequenceNumber=None): 
        self._ensure_coroutine_run()
        await self.queue.put(("DELETE", index, sequenceNumber))
            
    async def deleteAll(self, sequenceNumber=None): 
        self._ensure_coroutine_run()
        await self.queue.put(("DELETEALL", sequenceNumber))

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