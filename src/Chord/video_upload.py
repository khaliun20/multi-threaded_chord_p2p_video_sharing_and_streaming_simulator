from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import socket
import threading
import json

app = Flask(__name__)
CORS(app)

data = []
data_lock = threading.Lock()
socket_server_ready = threading.Event()  # Event to signal when socket server is ready
global indx
indx = 0

@app.route('/data/<segment>')
def send_data(segment):
    dic = {0: 50, 1:100, 2:200, 3:500, 4:1000}
    with data_lock:
        # return jsonify({"data received": [d.decode() for d in data]})
        for d in data:
            data_dict = json.loads(d.decode())
            played_queue_list = data_dict.get("played_queue", [])
            # print(played_queue_list)
    print(played_queue_list)
    global indx
    indx = int(segment)
    bitrate = dic[played_queue_list[int(indx)]]
    segment = str(indx).zfill(3)
    video_path = f'videos/video1/{bitrate}/output_{segment}.mp4'
    print(video_path)
    return send_from_directory('.', video_path)
    

    
@app.route('/video/<bitrate>/<segment>')
def get_video_segment(bitrate, segment):
    video_path = f'videos/video1/{bitrate}/output_{segment}.mp4'
    return send_from_directory('.', video_path)


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


