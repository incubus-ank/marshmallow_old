from sshkeyboard import listen_keyboard

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

command = None
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
        msg.data =  command
        self.publisher_.publish(msg)
        self.get_logger().info('commandServo: ' + msg.data)

def press(key):
    global command
    global publisher
    global publisherServo

    if ( key == 'w'):
        command = '1'
        publisher.pub(command)
    if ( key == 's'):
        command  = '3'
        publisher.pub(command)
    if ( key == 'd'):
        command  = '4'
        publisher.pub(command)
    if ( key == 'a'):
        command  = '2'
        publisher.pub(command)
    if ( key == 'q'):
        command  = '5'
        publisher.pub(command)
    if ( key == 'e'):
        command  = '6'
        publisher.pub(command)
    if ( key == 'h'):
        command  = '7'
        publisher.pub(command)
    if ( key == 'j'):
        command  = '8'
        publisher.pub(command)
    if ( key == 'k'):
        command  = '9'
        publisher.pub(command)
    if ( key == 'space'):
        command  = '0'
        publisher.pub(command)

    if ( key == 'r'):
        commandServo  = '1'
        publisherServo.pub(commandServo)
    if ( key == 't'):
        commandServo  = '2'
        publisherServo.pub(commandServo)
    if ( key == 'f'):
        commandServo  = '3'
        publisherServo.pub(commandServo)
    if ( key == 'g'):
        commandServo  = '4'
        publisherServo.pub(commandServo)
    if ( key == 'v'):
        commandServo  = '5'
        publisherServo.pub(commandServo)
    if ( key == 'b'):
        commandServo  = '6'
        publisherServo.pub(commandServo)

    
    

def main(args=None):
    global publisher
    global publisherServo

    rclpy.init(args=args)
    publisher = Publisher()
    publisherServo = PublisherServo()
    listen_keyboard(on_press=press)

    publisher.destroy_node()
    publisherServo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
