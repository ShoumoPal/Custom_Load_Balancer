import socket
import threading
import http.client
import time

backend_servers = [{'host': 'localhost', 'port': 8080, 'healthy': True},
                   {'host': 'localhost', 'port': 8081, 'healthy': True},
                   {'host': 'localhost', 'port': 8082, 'healthy': True}]
                   

server_index = 0
health_check_period = 10
lock = threading.Lock()

def server_health_check():

    while True:
        for server in backend_servers:
        
             conn = http.client.HTTPConnection(server['host'], server['port'])
             try:
                 conn.request('GET', '/health')
                 response = conn.getresponse()
                 if response.status == 200:
                     server["healthy"] = True
                 else:
                     server["healthy"] = False
             except Exception:
                 server['healthy'] = False
             finally:
                 conn.close()
        time.sleep(health_check_period)




def handle_clients(client : socket.socket):
    global server_index

    #Read the client's http request
    request_data = client.recv(4096)
    if not request_data:
        client.close()
        return

    request_line = request_data.decode().splitlines()[0]
    method, path, _ = request_line.split()

    with lock:
        while backend_servers[server_index]['healthy'] == False:
            server_index = (server_index + 1) % len(backend_servers)

        target_host, target_port= backend_servers[server_index]['host'], backend_servers[server_index]['port']
        server_index = (server_index + 1) % len(backend_servers) # Round robin server selection

    try:
        #Make an HTTP request to a backend server
        conn = http.client.HTTPConnection(target_host, target_port)
        conn.request(method, path)
        response = conn.getresponse()

        response_headers = f"HTTP/1.1 {response.status} {response.reason}\r\n"
        for header, value in response.getheaders():
            response_headers += f"{header}: {value}\r\n"
        response_headers += "\r\n"

        client.sendall(response_headers.encode() + response.read())
        conn.close()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def start_load_balancer(host = "localhost", port = 9000):
    
    threading.Thread(target=server_health_check).start()

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Load balancer running on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client connected from {addr}")
        threading.Thread(target=handle_clients, args=(client_socket,)).start()
        

if __name__ == "__main__":
    start_load_balancer()


