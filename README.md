# Secure Chat Application with TLS

This is a secure chat application that uses TLS encryption for secure communication between clients and server.

## Setup Instructions

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Generate TLS certificates (if not already present):
```bash
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt
```

3. Run the server:
```bash
export SERVER_CERT_FILE=certs/server.crt
export SERVER_KEY_FILE=certs/server.key
export CA_CERTS_FILE=certs/ca.crt
python server.py
```

4. Run the client in a separate terminal:
```bash
export CLIENT_CERT_FILE=certs/client.crt
export CLIENT_KEY_FILE=certs/client.key
export CA_CERTS_FILE=certs/ca.crt
python client.py
```

## Security Features

- TLS encryption for all communications
- Server authentication using certificates
- Secure key exchange
- Message integrity protection

## Project Structure

- `server.py`: The secure chat server implementation
- `client.py`: The secure chat client implementation
- `server.crt`: Server certificate
- `server.key`: Server private key
- `requirements.txt`: Project dependencies

## Testing

You can use Wireshark to verify that all communications are encrypted. The TLS handshake will be visible, but the actual message contents will be encrypted. 