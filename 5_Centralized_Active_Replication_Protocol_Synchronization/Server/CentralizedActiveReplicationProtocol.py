import asyncio


class storage:
    def __init__(
        self, messageBoard, proxies, myID, leaderElection=None, sequencer=None
    ):
        self.messageBoard = messageBoard  # AsyncBoardStorage.storage()
        self.proxies = proxies  # List of proxy [proxy(serverPort=10000,serverId= 0), proxy(10001, 0), proxy(10002, 0), proxy(10003, 0)]
        self.myID = myID
        self.leaderElection = leaderElection  # LeaderElection.election(proxies, myID)
        self.sequencer = sequencer
        self.seqNb = 0
        self.nextTaskNbExpected = 1

        self.queue = asyncio.PriorityQueue()
        self.isCoroutineRun = None

    def _ensure_coroutine_run(self):
        """Starts the background worker if it is not currently running."""
        if self.isCoroutineRun is None or self.isCoroutineRun.done():
            self.isCoroutineRun = asyncio.create_task(self.process_queue())

    async def process_queue(self):
        """
        Background task:
        1. Reads seqNb and commands from the queue
        2. Check if the seqNb match the expected one, if not match then put that request back to the queue and wait for until receive a match
        3. If correct seqNb then server update its own message board
        """
        while True:
            try:
                nextRequest = await self.queue.get()
                command = nextRequest[1]
                seqNb = nextRequest[0]
                if seqNb != self.nextTaskNbExpected:
                    await self.queue.put(nextRequest)
                    await asyncio.sleep(0.01)
                else:
                    match command:
                        case "PUT":
                            await self.messageBoard.put(nextRequest[2], seqNb)
                        case "MODIFY":
                            await self.messageBoard.modify(
                                nextRequest[2], nextRequest[3], seqNb
                            )
                        case "DELETE":
                            await self.messageBoard.delete(
                                nextRequest[2], seqNb
                            )
                        case "DELETEALL":
                            await self.messageBoard.deleteAll(seqNb)
                    self.nextTaskNbExpected += 1
            except Exception as ex:
                print(
                    "updateTask - Exception was received.", type(ex).__name__, ex.args
                )

    async def put(self, message, senderID=0, seqNb=None):
        # If sender is client then queue the request 
        if senderID == -1:
            coordinatorProxy = await self.leaderElection.getCoordiator()
            self.seqNb = await coordinatorProxy.getSequenceNumber()
            self._ensure_coroutine_run()
            await self.queue.put((self.seqNb, "PUT", message))
            for idx, proxy in enumerate(self.proxies):
                if idx == self.myID:
                    continue
                await proxy.put(message, seqNb=self.seqNb)
        else:
            await self.queue.put((seqNb, "PUT", message))

    async def get(self, index, senderID=0):
        return await self.messageBoard.get(index)

    async def getNum(self, senderID=0):
        return await self.messageBoard.getNum()

    async def getBoard(self, senderID=0):
        return await self.messageBoard.getBoard()

    async def modify(self, index, message, senderID=0, seqNb=None):
        if senderID == -1:
            coordinatorProxy = await self.leaderElection.getCoordiator()
            self.seqNb = await coordinatorProxy.getSequenceNumber()
            self._ensure_coroutine_run()
            await self.queue.put((self.seqNb, "MODIFY", index, message))
            for idx, proxy in enumerate(self.proxies):
                if idx == self.myID:
                    continue
                await proxy.modify(index, message, self.seqNb)
        else:
            await self.queue.put((seqNb, "MODIFY", index, message))

    async def delete(self, index, senderID=0, seqNb=None):
        if senderID == -1:
            coordinatorProxy = await self.leaderElection.getCoordiator()
            self.seqNb = await coordinatorProxy.getSequenceNumber()
            self._ensure_coroutine_run()
            await self.queue.put((self.seqNb, "DELETE", index))
            for idx, proxy in enumerate(self.proxies):
                if idx == self.myID:
                    continue
                await proxy.delete(index, self.seqNb)
        else:
            await self.queue.put((seqNb, "DELETE", index))

    async def deleteAll(self, senderID=0, seqNb=None):
        if senderID == -1:
            coordinatorProxy = await self.leaderElection.getCoordiator()
            self.seqNb = await coordinatorProxy.getSequenceNumber()
            self._ensure_coroutine_run()
            await self.queue.put((self.seqNb, "DELETEALL"))
            for idx, proxy in enumerate(self.proxies):
                if idx == self.myID:
                    continue
                await proxy.deleteAll(self.seqNb)
        else:
            await self.queue.put((seqNb, "DELETEALL"))

    async def close(self):
        self.messageBoard.close()
        for proxy in self.proxies:
            proxy.close()
