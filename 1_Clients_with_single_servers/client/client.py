import websocket 


ws = websocket.WebSocket()
ws.connect("ws://localhost:10000")
ws.send("ping")
print("ping")
# Waiting for the response of the server
response = ws.recv() 
print(response)
ws.close()
