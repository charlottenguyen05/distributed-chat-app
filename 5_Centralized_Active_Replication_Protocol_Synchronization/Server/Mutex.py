class mutex: 
    def __init__(self): 
        self.isAcquired = False
        
    async def acquire(self): 
        """
        Acquires the mutex. 
        If the mutex is already aquired, the method returns False. Then a coroutine must not enter its critical section. 
        Returns True, if the mutex was is free. Returns False if the mutex is acquired but not released.
        """
        if self.isAcquired: 
            return False
        else:
            self.isAcquired = True
            return self.isAcquired
        
    async def release(self): 
        """
        Frees the mutex. 
        If it is acquired afterwards, method acquire() return True.
        """
        if self.isAcquired:
            self.isAcquired = False
        return 
