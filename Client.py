import socket


class Client:
    def __init__(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ''  # Replace with your server's public IP address
        self.port = 9999
        self.start_client()

    def start_client(self):
        self.client_socket.connect((self.host, self.port))

    def send_message(self, message):
        self.client_socket.send(message.encode('utf-8'))

    def receive_message(self):
        return self.client_socket.recv(1024).decode('utf-8')

    def close_connection(self):
        self.client_socket.close()

if __name__ == "__main__":
    
    conn = Client()
