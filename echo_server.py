import socket
import threading

def handle_client(client, addr, port):
    print(f"[{port}] Connection from {addr}")
    with client:
        while True:
            data = client.recv(1024)
            if not data:
                break
            client.sendall(f"[{port}]: Echo: ".encode() + data)

def start_backend_server(port):
    server_socket = socket.socket()
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"Backend server running on port {port}")
    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client, addr, port)).start()

# Start servers for 8001, 8002, 8003
ports = [8080, 8081, 8082]
for port in ports:
    threading.Thread(target=start_backend_server, args=(port,), daemon=True).start()

# Keep the main thread alive
print("All backend servers are running.")
while True:
    pass  # or use `time.sleep(1)` if you want less CPU usage