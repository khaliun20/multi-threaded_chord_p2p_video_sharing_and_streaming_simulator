from flask import Flask, jsonify
from flask_cors import CORS
import socket
import threading
import time

app = Flask(__name__)
CORS(app)

data = []
data_lock = threading.Lock()
socket_server_ready = threading.Event()  # Event to signal when socket server is ready

@app.route('/data')
def send_data():
    # with data_lock:
    print(data, 'why no work')
    return jsonify({"data received": [d.decode() for d in data]})

def run_flask():
    # Wait for the socket server thread to be ready
    socket_server_ready.wait()
    print(data)  # Now, the socket server thread has added data
    app.run(debug=True, port=40000, use_reloader=False)

def run_socket_server(data):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.bind(('localhost', 50002))
    listening_socket.listen()
    
    # Signal that the socket server thread is ready
    socket_server_ready.set()

    while True:
        client_socket, client_address = listening_socket.accept()
        print(f"Connection from {client_address} has been established!")
        with data_lock:
            data.append(client_socket.recv(1024))
        #print(data)
        client_socket.close()
        socket_server_ready.set()

if __name__ == '__main__':
    socket_server_thread = threading.Thread(target=run_socket_server, args=(data,))
    socket_server_thread.start()

    run_flask()


