import socket
import select

class Server:
    def __init__(self, host='0.0.0.0', port=9999):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.server_socket.setblocking(False)
        self.inputs = [self.server_socket]
        self.outputs = []
        self.message_queues = {}

    def handle_connections(self):
        readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, 0)
        output = ""
        
        for s in readable:
            if s is self.server_socket:
                client_socket, addr = s.accept()
                print(f"Got a connection from {addr}")
                client_socket.setblocking(False)
                self.inputs.append(client_socket)
                self.message_queues[client_socket] = []
            else:
                data = s.recv(1024).decode('utf-8')
                if data:
                    print(f"Received message: {data}")
                    output += data
                    self.message_queues[s].append("Message received")
                    if s not in self.outputs:
                        self.outputs.append(s)
                else:
                    self.close_connection(s)
                

        for s in writable:
            if self.message_queues[s]:
                next_msg = self.message_queues[s].pop(0)
                s.send(next_msg.encode('utf-8'))
                if not self.message_queues[s]:
                    self.outputs.remove(s)

        for s in exceptional:
            self.close_connection(s)

        return output
    
    def send_message(self, client_socket, message):
        if client_socket in self.message_queues:
            self.message_queues[client_socket].append(message)
            if client_socket not in self.outputs:
                self.outputs.append(client_socket)
        else:
            print(f"Cannot send message, no such client: {client_socket}")


    def broadcast_message(self, message):
        for client_socket in self.message_queues:
            self.send_message(client_socket, message)


    def close_connection(self, s):
        print(f"Closing connection to {s.getpeername()}")
        self.inputs.remove(s)
        if s in self.outputs:
            self.outputs.remove(s)
        s.close()
        del self.message_queues[s]

    def stop_server(self):
        for s in self.inputs:
            s.close()
        self.server_socket.close()
        print("Server stopped")

