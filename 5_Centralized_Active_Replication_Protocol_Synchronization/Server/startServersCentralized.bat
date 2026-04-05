@echo off
echo Starting 4 Board Servers...

:: Start servers
start "Server 0" cmd /k python CentralizedActiveReplicationProtocol_Main.py 0
start "Server 1" cmd /k python CentralizedActiveReplicationProtocol_Main.py 1
start "Server 2" cmd /k python CentralizedActiveReplicationProtocol_Main.py 2
start "Server 3" cmd /k python CentralizedActiveReplicationProtocol_Main.py 3

echo All servers are running