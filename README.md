# Distributed Message Board (Chat App)

## Overview
This repository contains the coursework for a Distributed Systems class (Winter Term 25/26). It implements a distributed message board (chat application) using Python and WebSockets. Throughout the project, the system evolves from a simple single-server architecture to a robust, fault-tolerant cluster of servers implementing various distributed system algorithms to ensure data consistency, synchronization, and reliability.

---

## Prerequisites
To run the code in this repository, you need to install the following Python WebSocket libraries:

- **websocket-client** (used for the synchronous client operations):
```bash
  pip install websocket-client
```
- **websockets** (used for the asynchronous server and coroutines):
```bash
  pip install websockets
```

---

## Codebase Structure & Distributed System Techniques

The codebase is organized into progressively advanced modules, each corresponding to a specific lesson and distributed systems technique:

### 1. `1_Clients_with_single_servers`
- **Technique:** Basic Client-Server Communication & RPC
- **Details:** Introduces the base architecture using the WebSocket protocol for full-duplex communication. It implements the Proxy and Stub architectural pattern to hide network communication, allowing the client to execute Remote Procedure Calls (RPC) as if they were local methods.

### 2. `2_Clients_with_several_servers`
- **Technique:** Server Clustering & Basic Consistency
- **Details:** Scales the application to a cluster of servers to handle more clients. It implements two approaches to synchronize message boards:
  - **Forwarding:** Every server broadcasts update operations to all other servers.
  - **Coordinator:** Updates are serialized by routing them through a single Coordinator server, which then forwards them to the cluster to guarantee the same order of messages.

### 3. `3_Mutex_Election`
- **Technique:** Mutual Exclusion & Leader Election
- **Details:** Ensures that only one update operation is processed at a time across the entire cluster.
  - Implements a non-blocking Mutex hosted by a coordinator.
  - Implements the **Bully Algorithm** to automatically elect a new coordinator (leader) via remote procedure calls if the current one crashes or fails.

### 4. `4_Vector_clock`
- **Technique:** Causal Ordering with Vector Clocks
- **Details:** Replaces the strict mutex approach by allowing distributed updates mapped to Vector Clocks. When a message is created, it gets a timestamp vector. Servers then sort their message boards based on the total order of these timestamps to ensure all clients eventually see messages in the exact same causal order.

### 5. `5_Centralized_Active_Replication_Protocol_Synchronization`
- **Technique:** Active Replication & Bayou-inspired Synchronization
- **Details:** Explores two new consistency protocols:
  - **Centralized Active Replication:** Uses a central "Sequencer" to assign a unique, monotonically increasing global sequence number to each update. Servers buffer updates in a Priority Queue and strictly execute them in order.
  - **Synchronization:** Inspired by the Bayou system, servers act independently without continuous synchronization. Instead, clients explicitly trigger a synchronization process between pairs of servers to resolve missing messages.

### 6. `6_Fault_tolerance`
- **Technique:** Checkpointing & RPC Semantics (At-Least-Once / At-Most-Once)
- **Details:** Hardens the system against server crashes and network packet loss:
  - **Checkpointing:** Servers write their message board state to a JSON file after every update and reload it upon restart to prevent data loss.
  - **At-Least-Once Semantics:** Implements timeouts and automatic retransmission of requests if a server is unreachable or a message is lost (simulated via a lossy WebSocket module).
  - **At-Most-Once Semantics:** Uses sequence numbers and caching to filter out duplicate remote procedure calls, ensuring non-idempotent operations (like creating a message) are only executed once.

---

## How to Launch the System

Because the project builds upon itself, each folder has its own `Server` and `Clients` directories. To test a specific implementation, navigate to its respective folder.

### 1. Start the Server Cluster

Most tasks require running a cluster of 4 servers (typically assigned IDs `0`, `1`, `2`, and `3`) bound to ports `10000`, `10001`, `10002`, and `10003`.

Start them manually by running the respective `_Main.py` file in separate terminal windows, passing the Server ID as an argument:
```bash
python InformAllOtherServers_Main.py 0
python InformAllOtherServers_Main.py 1
python InformAllOtherServers_Main.py 2
python InformAllOtherServers_Main.py 3
```

> Alternatively, you can use the provided batch scripts like `startServers.bat` or `startServers2.bat` found in the directories to boot up the cluster simultaneously.

### 2. Start the Client

Once the servers are running, navigate to the `Clients` folder and run:
```bash
python UserInterface.py
```

This will launch the chat interface where you can connect to a specific server port (e.g., `10000`) and test commands like `put`, `get`, `modify`, `delete`, and `getboard`.

> You can also use the `startUI.bat` script.

### 3. Run Automated Tests

To test replication, consistency, and performance across the cluster:
```bash
# Upload 4 messages concurrently to each server
python SendDataToSeveralServers.py 4

# Upload 1000 messages for stress testing
python SendDataToSeveralServers.py 1000
```

> **Note:** Some later folders use `SendDataToSeveralServersWithSynchronisation.py` to specifically test the Bayou-inspired peer-to-peer sync mechanisms.
