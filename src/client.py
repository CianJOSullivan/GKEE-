import socket
import select


class Client:
    def __init__(self, host='', port=9999):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.setblocking(False)
        self.host = host
        self.port = port
        self.message_queues = []
        self.outputs = []
        self.start_client()

    def start_client(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except BlockingIOError:
            pass  # Non-blocking connect will raise this error initially
        print(f"Attempting to connect to server at {self.host}:{self.port}")

    def handle_communication(self):
        d = None
        readable, writable, exceptional = select.select([self.client_socket], self.outputs, [self.client_socket], 0)

        for s in readable:
            data = s.recv(1024).decode('utf-8')
            d = data
            if data:
                print(f"Received message: {data}")

        for s in writable:
            if self.message_queues:
                next_msg = self.message_queues.pop(0)
                s.send(next_msg.encode('utf-8'))
                if not self.message_queues:
                    self.outputs.remove(s)

        for s in exceptional:
            print(f"Handling exceptional condition for {s.getpeername()}")
            self.close_connection()

        return d

    def send_message(self, message):
        self.message_queues.append(message)
        if self.client_socket not in self.outputs:
            self.outputs.append(self.client_socket)

    def close_connection(self):
        print(f"Closing connection to server")
        self.client_socket.close()
