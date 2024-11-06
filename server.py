
import socket
import threading
import os

# Configure server
HOST, PORT = 'localhost', 8088

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        request = conn.recv(1024).decode('utf-8')
        headers = request.splitlines()
        if len(headers) > 0 and headers[0].startswith('GET'):
            file_requested = headers[0].split(' ')[1].strip('/')
            if file_requested == '':
                file_requested = 'hello.html'
            
            if os.path.exists(file_requested):
                with open(file_requested, 'r') as f:
                    content = f.read()
                response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + content
            else:
                response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>'
            conn.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server started at http://{HOST}:{PORT}")
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
