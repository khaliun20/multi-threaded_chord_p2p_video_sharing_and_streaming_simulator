from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/video/<bitrate>/<segment>')
def get_video_segment(bitrate, segment):
    # Assuming your videos are in a 'videos' directory
    # video_path = f'videos/{bitrate}/output_{bitrate}_{segment}.mp4'
    # video_path = f'videos/output_{bitrate}_{segment}.mp4'
    video_path = f'videos/video1/{bitrate}/output_{segment}.mp4'
    return send_from_directory('.', video_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
