import socket

def handle_request(client_socket):
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Connection: close\r\n"
        "\r\n"
        "Hello, World!"
    )
    client_socket.sendall(response.encode())
    client_socket.close()

def main():
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind
    server_socket.bind(('', 8080))
    
    # Listen
    server_socket.listen(5)
    print("Server running on http://localhost:8080")

    try:
        while True:
            # Accept connection
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            handle_request(client_socket)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()