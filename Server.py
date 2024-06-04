import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'  # Listen on all interfaces
    port = 9999
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started at {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Got a connection from {addr}")
        
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                print(f"Received message: {data}")
                response = "Message received"
                client_socket.send(response.encode('utf-8'))
            except ConnectionResetError:
                break

        client_socket.close()

if __name__ == "__main__":
    start_server()
