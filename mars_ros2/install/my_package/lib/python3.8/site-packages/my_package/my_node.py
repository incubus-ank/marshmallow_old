from flask import Flask, Response
import cv2

import rclpy
from rclpy.node import Node

app = Flask(__name__)
video = cv2.VideoCapture(0)

@app.route('/')
def index():
    return "Default Message"

def gen(video):
    while True:
        success, image = video.read()
        frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.equalizeHist(frame_gray)

        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/cam')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    

if __name__ == '__main__':
    main()
    
def main(args=None):
    rclpy.init(args=args)
    app.run(host='0.0.0.0', port=2024, threaded=True)
