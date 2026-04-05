class sequencer: 
    def __init__(self): 
        self.number = 0
        
    async def getSequenceNumber(self): 
        """
        Returns the next sequence number. 
        The first call of this function returns 1. The second call returns 2, and so on. 
        """
        self.number += 1
        return self.number
        