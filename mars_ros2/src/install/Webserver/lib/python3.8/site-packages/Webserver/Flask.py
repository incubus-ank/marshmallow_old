from flask import Flask, Response
import cv2
from cv_bridge import CvBridge

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

app = Flask(__name__)
video = cv2.VideoCapture(0)

image_publisher = None

class Publisher(Node):
    def __init__(self):
        super().__init__('publisher')
        self.publisher_ = self.create_publisher(Image, 'cam', 10)
        self.bridge = CvBridge()
    
    def pub(self, frame):
        frame = frame
        self.publisher_.publish(self.bridge.cv2_to_imgmsg(frame, "bgr8"))


@app.route('/')
def index():
    return "Default Message"
    
def gen(video):
    global image_publisher

    while True:
        success, image = video.read()
        if success == True:
            image_publisher.pub(image)

        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
               
@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
                    

def main(args=None):
    global image_publisher
  
    rclpy.init(args=args)
    image_publisher = Publisher()
    app.run(host='0.0.0.0', port=2204, threaded=True)
    image_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    