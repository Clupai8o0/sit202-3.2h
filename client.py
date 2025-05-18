import socket
import ssl
import threading
import logging
import sys

# Setup logging
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class SecureChatClient:
  def __init__(self, host="localhost", port=8443):
    self.host = host
    self.port = port
    self.username = None
    self.setup_client()
  
  def setup_client(self):
    """Set up the client with SSL/TLS"""
    try:
      # Create base socket
      self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      # Create SSL context
      self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
      self.ssl_context.load_cert_chain(certfile="client.crt", keyfile="client.key")
      self.ssl_context.check_hostname = False # for development only
      self.ssl_context.verify_mode = ssl.CERT_REQUIRED
      self.ssl_context.load_verify_locations("server.crt")

      # Wrap socket with SSL
      self.ssl_socket = self.ssl_context.wrap_socket(self.client_socket, server_hostname=self.host)
      
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

  def print_message(self, message):
    """Print a message while preserving the input prompt"""
    # Clear the current line
    sys.stdout.write('\r\033[K')
    # Print the message
    print(message)
    # Reprint the prompt
    sys.stdout.write('> ')
    sys.stdout.flush()

  def receive_messages(self):
    """Receive messages from the server"""
    try:
      while True:
        message = self.ssl_socket.recv(1024).decode('utf-8')
        if not message:
          break
        self.print_message(message)
    except Exception as e:
      logger.error(f"Error receiving message: {e}")
    finally:
      self.ssl_socket.close()
      logger.info("Disconnected from server")

  def start(self):
    """Start the client and handle user input"""
    if not self.connect():
      return
    
    # Get username
    while not self.username:
      self.username = input("Enter your username: ").strip()
      if not self.username:
        print("Username cannot be empty")
    
    # Send join message
    self.send_message("has joined the chat")

    # Start a receive thread
    receive_thread = threading.Thread(target=self.receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    try:
      while True:
        sys.stdout.write('> ')
        sys.stdout.flush()
        message = input()
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