import socket
import ssl
import threading
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SecureChatServer:
    def __init__(self, host='localhost', port=8443):
        self.host = host
        self.port = port
        self.clients = []
        self.setup_server()

    def setup_server(self):
        """Set up the server socket with SSL/TLS"""
        try:
            # Create base socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

            # Create SSL context
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            self.ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")
            
            logger.info(f"Server initialized and listening on {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Error setting up server: {e}")
            raise

    def handle_client(self, client_socket, address):
        """Handle individual client connections"""
        try:
            # Wrap socket with SSL
            ssl_socket = self.ssl_context.wrap_socket(client_socket, server_side=True)
            logger.info(f"Secure connection established with {address}")
            
            # Add client to list
            self.clients.append(ssl_socket)
            
            while True:
                try:
                    # Receive message
                    message = ssl_socket.recv(1024).decode('utf-8')
                    if not message:
                        break
                    
                    # Log and broadcast message
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    formatted_message = f"[{timestamp}] {address}: {message}"
                    logger.info(formatted_message)
                    
                    # Broadcast to all clients
                    self.broadcast(formatted_message, ssl_socket)
                    
                except ssl.SSLError as e:
                    logger.error(f"SSL Error: {e}")
                    break
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"Error handling client {address}: {e}")
        finally:
            # Clean up
            if ssl_socket in self.clients:
                self.clients.remove(ssl_socket)
            ssl_socket.close()
            logger.info(f"Connection closed with {address}")

    def broadcast(self, message, sender_socket=None):
        """Broadcast message to all connected clients except sender"""
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    logger.error(f"Error broadcasting to client: {e}")
                    if client in self.clients:
                        self.clients.remove(client)

    def start(self):
        """Start the server and accept connections"""
        logger.info("Server started. Waiting for connections...")
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                logger.info(f"New connection from {address}")
                
                # Start new thread for each client
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            logger.info("Server shutting down...")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = SecureChatServer()
    server.start()