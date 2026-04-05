import functools

class storage:
    """Local storage for a server"""

    def __init__(self, comparatorForElements = None):
        self.messages = []
        self.comparatorForElementsFunc = comparatorForElements

    async def put(self, message,senderId=0):
        """Add a message to the board"""
        self.messages = self.messages + [message]

    async def get(self, index, senderId=0):
        """Return an individual message by index (first message index 0)"""
        index = int(index)
        if index >= 0 and index < len(self.messages):
            return self.messages[index]
        else:
            raise ValueError("UNKNOWN_INDEX")

    async def getNum(self, senderId=0):
        """Return the total number of messages in board"""
        return len(self.messages)

    async def getBoard(self, senderId=0):
        """Return a list of all the messages strings of the board"""
        if self.comparatorForElementsFunc is not None:
            self.messages.sort(key=functools.cmp_to_key(self.comparatorForElementsFunc))
        return self.messages

    async def modify(self, index, message, senderId=0):
        """Change the content of message that has index x"""
        index = int(index)
        if index >= 0 and index < len(self.messages):
            self.messages[index] = message
        else:
            raise ValueError("UNKNOWN_INDEX")

    async def delete(self, index, senderId=0):
        """Delete message that has index x"""
        index = int(index)
        if index >= 0 and index < len(self.messages):
            self.messages = [
                self.messages[i] for i in range(len(self.messages)) if i != index
            ]
        else:
            raise ValueError("UNKNOWN_INDEX")

    async def deleteAll(self, senderId=0):
        self.messages = []

    async def close(self):
        pass
