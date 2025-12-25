# Secure TLS Chat (Python)
TLS-encrypted console chat server/client with mutual certificate authentication.

## What it does
- Starts a threaded TCP chat server secured with TLS.
- Connects clients over TLS, authenticating both server and client certificates.
- Broadcasts messages to all connected peers with timestamps.
- Provides a helper script to generate self-signed cert/key pairs for local use.

## Key features
- **Mutual TLS:** Server requires client certificates; client verifies the server certificate (hostname check disabled for dev).
- **Broadcast chat:** Server relays each message to all connected clients.
- **Threaded handling:** Each client runs on its own thread for concurrency.
- **Certificate tooling:** `generate_cert.py` produces `server.crt/key` and `client.crt/key`.
- **Logging:** INFO-level logging for connections, certificates, and messages.
- **Graceful prompts:** Client preserves the input prompt when new messages arrive.

## Tech stack
- Python 3 (socket, ssl, threading, logging)
- cryptography (certificate generation)
- pyOpenSSL (listed dependency)

## Architecture overview
Simple threaded TCP server wrapped in TLS. Each accepted socket is upgraded to TLS, tracked, and broadcast to peers.
```
[client] ==TLS==> [server:8443] ==TLS==> [client]
             \__ thread per client __/
```

## Getting started (local)
### Prerequisites
- Python 3.x
- pip

### Install
```bash
pip install -r requirements.txt
```

### Generate certificates
Run once to create local dev certs/keys in the project root:
```bash
python generate_cert.py
```
This produces `server.crt`, `server.key`, `client.crt`, `client.key` (gitignored).

### Run the server
```bash
python server.py
```
- Listens on `localhost:8443` by default; adjust `host`/`port` in `SecureChatServer` if needed.
- Expects `server.crt`, `server.key`, and `client.crt` in the working directory.

### Run a client
In separate terminals:
```bash
python client.py
```
- Uses `localhost:8443` by default; adjust `host`/`port` in `SecureChatClient` if needed.
- Expects `client.crt`, `client.key`, and `server.crt` in the working directory.
- Enter a username when prompted; type messages to broadcast or `quit` to disconnect.

## Usage
1. Start the server.
2. Launch one or more clients after generating certificates.
3. Provide usernames and chat; messages show as `username: message` with server-side timestamps for logs.
4. Type `quit` to leave; server logs disconnections.

## Testing / Quality
- No automated tests or linters are included in the repository.

## Deployment
- No deployment configuration is provided; current setup targets local development with self-signed certificates.
