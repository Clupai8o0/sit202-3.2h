import socket
import ssl
import threading
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SecureChatClient:
    def __init__(self, host='localhost', port=8443):
        self.host = host
        self.port = port
        self.username = None
        self.setup_client()

    def setup_client(self):
        """Set up the client socket with SSL/TLS"""
        try:
            # Create base socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Create SSL context
            self.ssl_context = ssl.create_default_context()
            # For development/testing only - in production, you should verify the certificate
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE
            
            # Wrap socket with SSL
            self.ssl_socket = self.ssl_context.wrap_socket(
                self.client_socket,
                server_hostname=self.host
            )
            
            logger.info("Client initialized")
        except Exception as e:
            logger.error(f"Error setting up client: {e}")
            raise

    def connect(self):
        """Connect to the server"""
        try:
            self.ssl_socket.connect((self.host, self.port))
            logger.info(f"Connected to server at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to server: {e}")
            return False

    def receive_messages(self):
        """Receive messages from the server"""
        try:
            while True:
                message = self.ssl_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"\n{message}")
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
        finally:
            self.ssl_socket.close()
            logger.info("Disconnected from server")

    def send_message(self, message):
        """Send a message to the server"""
        try:
            # Format message with username
            formatted_message = f"{self.username}: {message}"
            self.ssl_socket.send(formatted_message.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
        return True

    def start(self):
        """Start the client and handle user input"""
        if not self.connect():
            return

        # Get username
        while not self.username:
            self.username = input("Enter your username: ").strip()
            if not self.username:
                print("Username cannot be empty!")

        # Send join message
        self.send_message("has joined the chat")

        # Start receive thread
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        try:
            while True:
                message = input("> ")
                if message.lower() == 'quit':
                    self.send_message("has left the chat")
                    break
                if not self.send_message(message):
                    break
        except KeyboardInterrupt:
            logger.info("Client shutting down...")
            self.send_message("has left the chat")
        finally:
            self.ssl_socket.close()

if __name__ == "__main__":
    client = SecureChatClient()
    client.start()