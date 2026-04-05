class storage: 
    """Storage for message board"""
    def __init__(self): 
        self.messages = []
        
    def put(self, message): 
        """Add a message to the board"""
        self.messages = self.messages + [message]
       
    def get(self, index): 
        """Return an individual message by index (first message index 0)"""
        index = int(index)
        if index >= 0 and index < len(self.messages): 
            return self.messages[index]
        else: 
            raise ValueError("Index is unknown.")
            
    def getNum(self): 
        """Return the total number of messages in board"""
        return len(self.messages)
        
    def getBoard(self): 
        """Return a list of all the messages strings of the board"""
        return self.messages
        
    def modify(self, index, message): 
        """Change the content of message that has index x"""
        index = int(index)
        self.messages[index] = message
        
    def delete(self, index): 
        """Delete message that has index x"""
        index = int(index)
        self.messages = [self.messages[i] for i in range(len(self.messages)) if i != index]

    def deleteAll(self): 
        self.messages = []
        
    def close(self): 
        pass