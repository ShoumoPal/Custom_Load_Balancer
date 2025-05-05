import socket
from urllib import response


def run_client():
    host = 'localhost'
    port = 9000
    
    client_socket = socket.socket()
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")
    while True:
        message = input("Enter the message or 'exit' to exit: ")
        if(message.lower() == 'exit'):
            break
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024)
        print(f"Response: {response.decode()}")

run_client()
