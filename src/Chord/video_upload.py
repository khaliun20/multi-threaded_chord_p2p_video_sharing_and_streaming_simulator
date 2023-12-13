from flask import Flask, jsonify
from flask_cors import CORS
import socket
import threading

app = Flask(__name__)
CORS(app)

data = []
data_lock = threading.Lock()

@app.route('/data')
def send_data():
    with data_lock:
        return jsonify({"data received": [d.decode() for d in data]})

def run_flask():
    app.run(debug=True, port=40000, use_reloader=True)

def run_socket_server(data):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.bind(('localhost', 50001))
    listening_socket.listen()

    while True:
        client_socket, client_address = listening_socket.accept()
        print(f"Connection from {client_address} has been established!")
        with data_lock:
            data.append(client_socket.recv(1024))
        client_socket.close()

if __name__ == '__main__':
    socket_server_thread = threading.Thread(target=run_socket_server, args=(data,))
    socket_server_thread.start()
    run_flask()

