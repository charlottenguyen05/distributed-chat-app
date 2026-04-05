import asyncio

class storage: 
    """AtLeastOnceProxy wraps AsyncBoardProxy (3 second timeout + 5 retry attempts)"""
    
    def __init__(self, proxy): 
        self.proxy = proxy    # AsyncBoardProxy object
        self.max_attempts = 5

    async def put(self, message, sequenceNumber=None): 
        """
        1. Tries to call proxy.put() with a 3-second timeout
        2. If timeout occurs, retries up to 5 times total
        3. If all attempts fail, raises an exception
        4. On success, returns immediately
        """
        for attempt in range(self.max_attempts):
            try:
                result = await asyncio.wait_for(self.proxy.put(message, sequenceNumber), timeout=3)
                return result  # Success break the retry process
                    
            except asyncio.TimeoutError:
                if attempt == self.max_attempts - 1:
                    # Last attempt failed
                    raise Exception(f"put() failed after {self.max_attempts} attempts")
                # Otherwise, continue to next attempt
                
            except Exception as e:
                if attempt == self.max_attempts - 1:
                    raise Exception(f"put() failed after {self.max_attempts} attempts: {e}")
      
    async def modify(self, index, message, sequenceNumber=None): 
        for attempt in range(self.max_attempts):
            try:
                result = await asyncio.wait_for(self.proxy.modify(index, message, sequenceNumber), timeout=3)
                return result
                    
            except asyncio.TimeoutError:
                if attempt == self.max_attempts - 1:
                    raise Exception(f"modify() failed after {self.max_attempts} attempts")
                    
            except Exception as e:
                if attempt == self.max_attempts - 1:
                    raise Exception(f"modify() failed after {self.max_attempts} attempts: {e}")
        
    async def delete(self, index, sequenceNumber=None): 
        for attempt in range(self.max_attempts):
            try:
                result = await asyncio.wait_for(self.proxy.delete(index, sequenceNumber), timeout=3)
                return result
                    
            except asyncio.TimeoutError:
                if attempt == self.max_attempts - 1:
                    raise Exception(f"delete() failed after {self.max_attempts} attempts")
                    
            except Exception as e:
                if attempt == self.max_attempts - 1:
                    raise Exception(f"delete() failed after {self.max_attempts} attempts: {e}")
            
    async def deleteAll(self, sequenceNumber=None): 
        for attempt in range(self.max_attempts):
            try:
                result = await asyncio.wait_for(self.proxy.deleteAll(sequenceNumber), timeout=3)
                return result
                    
            except asyncio.TimeoutError:
                if attempt == self.max_attempts - 1:
                    raise Exception(f"deleteAll() failed after {self.max_attempts} attempts")
                    
            except Exception as e:
                if attempt == self.max_attempts - 1:
                    raise Exception(f"deleteAll() failed after {self.max_attempts} attempts: {e}")

    async def get(self, index): 
        for attempt in range(self.max_attempts):
            try:
                result = await asyncio.wait_for(self.proxy.get(index), timeout=3)
                return result
                    
            except asyncio.TimeoutError:
                print(f"[AtLeastOnceProxy] get({index}) attempt {attempt + 1} timed out")
                if attempt == self.max_attempts - 1:
                    raise Exception(f"get() failed after {self.max_attempts} attempts")
                    
            except Exception as e:
                print(f"[AtLeastOnceProxy] get({index}) attempt {attempt + 1} error: {e}")
                if attempt == self.max_attempts - 1:
                    raise Exception(f"get() failed after {self.max_attempts} attempts: {e}")
            
    async def getNum(self): 
        for attempt in range(self.max_attempts):
            try:
                result = await asyncio.wait_for(self.proxy.getNum(), timeout=3)
                return result
                    
            except asyncio.TimeoutError:
                print(f"[AtLeastOnceProxy] getNum() attempt {attempt + 1} timed out")
                if attempt == self.max_attempts - 1:
                    raise Exception(f"getNum() failed after {self.max_attempts} attempts")
                    
            except Exception as e:
                print(f"[AtLeastOnceProxy] getNum() attempt {attempt + 1} error: {e}")
                if attempt == self.max_attempts - 1:
                    raise Exception(f"getNum() failed after {self.max_attempts} attempts: {e}")
        
    async def getBoard(self): 
        for attempt in range(self.max_attempts):
            try:
                result = await asyncio.wait_for(self.proxy.getBoard(), timeout=3)
                return result
                    
            except asyncio.TimeoutError:
                print(f"[AtLeastOnceProxy] getBoard() attempt {attempt + 1} timed out")
                if attempt == self.max_attempts - 1:
                    raise Exception(f"getBoard() failed after {self.max_attempts} attempts")
                    
            except Exception as e:
                print(f"[AtLeastOnceProxy] getBoard() attempt {attempt + 1} error: {e}")
                if attempt == self.max_attempts - 1:
                    raise Exception(f"getBoard() failed after {self.max_attempts} attempts: {e}")
    
    
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