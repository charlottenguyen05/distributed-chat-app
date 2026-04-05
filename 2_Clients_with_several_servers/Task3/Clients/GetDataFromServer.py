import BoardProxy
import sys
import time

numberMessagesPerServer = 0                  # Number of messages to be sent to each server.
serverPort   = 10000 # Ports of the server to which messages shall be uploaded.

serverProxy = BoardProxy.storage(serverPort) 

def downloadFromServer(): 
    myPort = serverPort
    myProxy = serverProxy
    
    for i in range(numberMessagesPerServer): 
        message = str(i)  # Create messages such as "1"
        print("Download", message)
        myProxy.get(i)
        # myProxy.getBoard()
      

if len(sys.argv) > 1:       # A parameter was given to the program ...
    numberMessagesPerServer = int(sys.argv[1]) # Assume the first parameter is number of packets to sent for each server
else: 
    numberMessagesPerServer = serverProxy.getNum() # Otherwise use default value.

print("Starting downloading using getBoard")        
startTime = time.time()
downloadFromServer()
endTime = time.time()
print("Time for downloading:", (endTime - startTime) * 1000, "ms")