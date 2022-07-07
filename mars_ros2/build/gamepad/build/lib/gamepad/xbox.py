import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

from inputs import get_gamepad

command = None
commandServo = None
publisher = None
publisherServo = None


class Publisher(Node):

    def __init__(self):
        super().__init__('publisher')
        self.publisher_ = self.create_publisher(String, 'command', 10)

    def pub(self, command):
        msg = String()
        msg.data =  command
        self.publisher_.publish(msg)
        self.get_logger().info('command: ' + msg.data)

class PublisherServo(Node):

    def __init__(self):
        super().__init__('publisherServo')
        self.publisher_ = self.create_publisher(String, 'commandServo', 10)

    def pub(self, command):
        msg = String()
        msg.data =  str(command)
        self.publisher_.publish(msg)
        self.get_logger().info('commandServo: ' + msg.data)

def get_key():
    global command
    global commandServo
    global publisher
    global publisherServo

    while(True):
        events = get_gamepad()

        for event in events:
            print(event.ev_type, event.code, event.state)

            if (event.ev_type == 'Key'):

                if (event.code == 'BTN_SOUTH'):
                    if (event.state == 1):
                        publisherServo.pub('6')
                if (event.code == 'BTN_EAST'):
                    if (event.state == 1):
                        publisherServo.pub('4')
                if (event.code == 'BTN_WEST'):
                    if (event.state == 1):
                        publisherServo.pub('3')
                if (event.code == 'BTN_NORTH'):
                    if (event.state == 1):
                        publisherServo.pub('5')
                if (event.code == 'BTN_TL'):
                    if (event.state == 1):
                        publisherServo.pub('1')
                if (event.code == 'BTN_TR'):
                    if (event.state == 1):
                        publisherServo.pub('2')
                if (event.state == 0):
                    publisherServo.pub('0')  
            
            if (event.ev_type == 'Absolute'):
                if (event.code == "ABS_HAT0Y"):
                    if (event.state == 1):
                        publisher.pub('3')
                    if (event.state == -1):
                        publisher.pub('1')
                if (event.code == "ABS_HAT0X"):
                    if (event.state == 1):
                        publisher.pub('4')
                    if (event.state == -1):
                        publisher.pub('2')
                if (event.state == 0):
                    publisher.pub('0') 
                

def main(args=None):
    global publisher
    global publisherServo

    rclpy.init(args=args)
    publisher = Publisher()
    publisherServo = PublisherServo()

    get_key()

    publisher.destroy_node()
    publisherServo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()