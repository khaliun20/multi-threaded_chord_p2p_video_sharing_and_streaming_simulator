import socket, json

def tcp_client():
    # Set the server address (host and port)
    server_host = '127.0.0.1'  # Change this to your server's IP address or hostname
    server_port = 40000

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_host, server_port))
        print(f"Connected to {server_host}:{server_port}")

        # Send a message to the server
        key = 8
        request = {'type': 'find_successor', 'key': key}

        client_socket.send(json.dumps(request).encode('utf-8'))
        print(f"Sent: {request }")

        # Receive the response from the server
        received_data = client_socket.recv(1024)
        print(f"Received: {received_data.decode('utf-8')}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the socket connection
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    tcp_client()
