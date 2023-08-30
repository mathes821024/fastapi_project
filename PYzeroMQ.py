#PYzeroMQ.py
import zmq
from zmq import Context
from threading import Thread
import logging
from typing import Tuple, Optional
import http.client
import json

# Configure logging
logging.basicConfig(level=logging.INFO)

def register_handler(handler_map):
    def decorator(msg_type):
        def wrapper(func):
            handler_map[msg_type] = func
            return func
        return wrapper
    return decorator

class MessageHandler:
    """
    Class for handling different types of messages.
    """

    def __init__(self):
        self.message_handlers = {}  # Store registered handlers
        self.register_handlers()

    def register_handlers(self):
        """
        Register message handlers.
        """
        self.message_handlers["transaction"] = self.handle_transaction
        self.message_handlers["reconciliation"] = self.handle_reconciliation

    @staticmethod
    def parse_message(message: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Parse the incoming message into (message_type, data).
        """
        try:
            msg_type, data = message.split('|', 1)
            return msg_type, data
        except Exception as e:
            logging.error(f"Error parsing message: {e}")
            return None, None

    def handle_message(self, worker_socket, message_frames):
        """
        Handle incoming message frames.
        """
        msg = message_frames[-1].decode('utf-8')
        msg_type, data = self.parse_message(msg)

        if msg_type is None:
            return "Error|Invalid message format"

        # Lookup the message handler based on the message type
        handler = self.message_handlers.get(msg_type)
        if handler:
            result = handler(data)

            # Communicate result with FastAPI service
            fastapi_result = self.communicate_with_fastapi(msg_type, data)
            logging.info(f"FastAPI returned: {fastapi_result}")

            return result
        else:
            return "Error|Unknown message type"

    def handle_transaction(self, data: str) -> str:
        """
        Handle transaction type messages.
        """
        logging.info(f"Handling transaction with data: {data}")
        return "Success|Transaction processed"

    def handle_reconciliation(self, data: str) -> str:
        """
        Handle reconciliation type messages.
        """
        logging.info(f"Handling reconciliation with data: {data}")
        return "Success|Reconciliation processed"

    def communicate_with_fastapi(self, msg_type, data):
        """
        Communicate with FastAPI service through HTTP POST.
        """
        # Define the data payload to send
        payload = {
            "msg_type": msg_type,
            "data": data
        }

        # Convert the payload to a JSON string
        payload_str = json.dumps(payload)

        # Create HTTP connection (Replace this with your FastAPI service details)
        conn = http.client.HTTPConnection("localhost", 8000)

        # Make HTTP POST request
        headers = {'Content-Type': 'application/json'}
        try:
            conn.request("POST", "/api/process/", body=payload_str, headers=headers)
            response = conn.getresponse()
            return response.read().decode()
        except Exception as e:
            logging.error(f"Error communicating with FastAPI: {e}")
            return f"Error|Exception occurred: {str(e)}"




class Worker(Thread):
    """
    Worker thread that handles messages from a ZeroMQ DEALER socket.
    """

    def __init__(self, context: Context, dealer_url: str, message_handler: MessageHandler):
        super().__init__()
        self.ctx = context
        self.dealer_url = dealer_url
        self.message_handler = message_handler

    def run(self) -> None:
        """
        Main loop for the worker thread.
        """
        logging.info(f"Worker started, connecting to {self.dealer_url}")
        worker_socket = self.ctx.socket(zmq.DEALER)
        worker_socket.connect(self.dealer_url)

        while True:
            try:
                msg_frames = worker_socket.recv_multipart()
                logging.info(f"Received message frames: {msg_frames}")

                result = self.message_handler.handle_message(worker_socket, msg_frames)

                logging.info(f"Processed result: {result}")

                worker_socket.send_multipart(msg_frames[:-1] + [result.encode('utf-8')])

            except Exception as e:
                logging.error(f"Error processing message: {e}")
                worker_socket.send_multipart(msg_frames[:-1] + ["Error|not_confirmed".encode('utf-8')])


class ZeroMQServer:
    """
    Main class for ZeroMQ server setup.
    """

    def __init__(self, num_workers: int = 2):
        self.num_workers = num_workers
        self.ctx = Context.instance()

    def start(self) -> None:
        """
        Initialize and start the ZeroMQ server.
        """
        logging.info("Initializing ZeroMQ context...")

        router_socket = self.ctx.socket(zmq.ROUTER)
        router_socket.bind("tcp://*:15555")
        logging.info("Router socket bound to tcp://*:15555")

        dealer_url = "inproc://workers"
        dealer_socket = self.ctx.socket(zmq.DEALER)
        dealer_socket.bind(dealer_url)
        logging.info(f"Dealer socket bound to {dealer_url}")

        message_handler = MessageHandler()

        for i in range(self.num_workers):
            logging.info(f"Starting worker thread {i + 1}")
            worker = Worker(self.ctx, dealer_url, message_handler)
            worker.start()

        logging.info("Starting the ZMQ proxy...")
        zmq.proxy(router_socket, dealer_socket)


if __name__ == "__main__":
    logging.info("Starting the application...")
    server = ZeroMQServer()
    server.start()






