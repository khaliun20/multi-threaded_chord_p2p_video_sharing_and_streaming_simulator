# from flask import Flask, jsonify
# from flask_cors import CORS
#
#
# app = Flask(__name__)
# CORS(app)
#
#
# @app.route('/data', methods=['GET'])
# def send_data():
#     # Your data that you want to send
#     data = {
#         'message': 'Hello from the backend!',
#         'moreData': [1, 2, 3, 4]
#     }
#     return jsonify(data)
#
# if __name__ == '__main__':
#     app.run(debug=True, port=40000)