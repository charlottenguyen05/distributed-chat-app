import asyncio

class storage: 
    def __init__(self, messageBoard, proxies, myID, leaderElection): 
        self.messageBoard = messageBoard # AsyncBoardStorage.storage() 
        self.proxies = proxies  # List of proxy [proxy(serverPort=10000,serverId= 0), proxy(10001, 0), proxy(10002, 0), proxy(10003, 0)]
        self.myID = myID 
        self.leaderElection = leaderElection # LeaderElection.election(proxies, myID)

        self.queue = asyncio.Queue()
        self.isCoroutineRun = None

    def _ensure_coroutine_run(self):
        """Starts the background worker if it is not currently running."""
        if self.isCoroutineRun is None or self.isCoroutineRun.done():
            self.isCoroutineRun = asyncio.create_task(self.process_queue())
        
    async def process_queue(self):
        """
        Background task:
        1. Reads commands from the queue
        2. Acquires global Mutex from Coordinator
        3. Updates ALL servers
        4. Releases Mutex
        """
        while True:
            try: 
                nextRequest = await self.queue.get()
                command = nextRequest[0]
                while True:
                    coordinatorProxy = await self.leaderElection.getCoordiator()

                    isAcquired = await coordinatorProxy.acquire()
                    if isAcquired:
                        break

                    await asyncio.sleep(0.1)
                
                for proxy in self.proxies:
                    match command:
                        case "PUT":
                            await proxy.put(nextRequest[1])
                        case "MODIFY":
                            await proxy.modify(nextRequest[1], nextRequest[2])
                        case "DELETE":
                            await proxy.delete(nextRequest[1])
                        case "DELETEALL":
                            await proxy.deleteAll()

                await coordinatorProxy.release()

            except Exception as ex: 
                print("updateTask - Exception was received.", type(ex).__name__, ex.args)


    async def put(self, message, senderID=0): 
        # If sender is client then queue the request
        if senderID == -1:
            self._ensure_coroutine_run()
            await self.queue.put(('PUT', message))
        else:
            return await self.messageBoard.put(message)
        
    async def get(self, index, senderID=0): 
        return await self.messageBoard.get(index)
            
    async def getNum(self, senderID=0): 
        return await self.messageBoard.getNum()
        
    async def getBoard(self, senderID=0): 
        return await self.messageBoard.getBoard()
        
    async def modify(self, index, message, senderID=0): 
        if senderID == -1:
            self._ensure_coroutine_run()
            await self.queue.put(("MODIFY", index, message))
        else:
            await self.messageBoard.modify(index, message, senderID)
        
    async def delete(self, index, senderID=0): 
        if senderID == -1:
            self._ensure_coroutine_run()
            await self.queue.put(("DELETE", index))
        else:
            await self.messageBoard.delete(index, senderID)
            
    async def deleteAll(self, senderID=0): 
        if senderID == -1:
            self._ensure_coroutine_run()
            await self.queue.put(("DELETEALL",))
        else:
            await self.messageBoard.deleteAll(senderID)
        
    async def close(self): 
        self.messageBoard.close()
        for proxy in self.proxies:
            proxy.close()