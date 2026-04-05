import asyncio
import functools
import json
import os

class storage:
    """Local storage for a server"""

    def __init__(self, comparatorForElements = None, checkpointing=False, serverId = None):
        self.messages = [] 
        self.comparatorForElementsFunc = comparatorForElements
        self.checkpointing = checkpointing
        self.serverId = serverId
        self.fileName = None

        # Load the old messages from json checkpoint file
        if self.checkpointing:
            self.fileName = "checkpoint_"+ str(self.serverId) + ".json"
            if os.path.exists(self.fileName):
                try:
                    with open(self.fileName, "r") as f:
                        self.messages = json.load(f)
                except Exception as e:
                    print(f"Error loading checkpoint of server {self.serverId}: {e}")
                    self.messages = []

    # write to checkpoint file after a UPDATE methods
    async def writeCheckpoint(self):
        try:
            with open(self.fileName, "w") as f:
                json.dump(self.messages, f, indent=2)
            print(f"[Server {self.serverId}] Checkpoint written with {len(self.messages)} messages")
        except Exception as e:
            print(f"Error writing to checkpoint file of server {self.serverId}: {e}")

    async def put(self, message, seqNb=None, senderId=0):
        """Add a message to the board"""
        self.messages = self.messages + [message]
        if self.checkpointing:
            await self.writeCheckpoint()

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

    async def modify(self, index, message, seqNb=None, senderId=0):
        """Change the content of message that has index x"""
        index = int(index)
        if index >= 0 and index < len(self.messages):
            self.messages[index] = message
            if self.checkpointing:
                await self.writeCheckpoint()
        else:
            raise ValueError("UNKNOWN_INDEX")

    async def delete(self, index, seqNb=None, senderId=0):
        """Delete message that has index x"""
        index = int(index)
        if index >= 0 and index < len(self.messages):
            self.messages = [
                self.messages[i] for i in range(len(self.messages)) if i != index
            ]
            if self.checkpointing:
                await self.writeCheckpoint()            
        else:
            raise ValueError("UNKNOWN_INDEX")

    async def deleteAll(self, seqNb=None, senderId=0):
        self.messages = []
        if self.checkpointing:
            await self.writeCheckpoint()

    async def close(self):
        pass
