import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import time
from adafruit_servokit import ServoKit

from sshkeyboard import listen_keyboard

kit = ServoKit(channels=16)

ser0 = 90
ser1 = 90
ser2 = 90



class Subscriber(Node):

    def __init__(self):
        super().__init__('subscriber')
        self.subscription = self.create_subscription(String, 'command', self.listener_callback, 10)
    
    def listener_callback(self, msg):
        global ser0
        global ser1
        global ser2

        self.get_logger().info('I heard: "%s"' % msg.data)
        print(msg.data.encode('UTF-8'))

        if ( msg.data == b'1'):
            ser0 = ser0 - 10
            kit.servo[0].angle = ser0
        if ( msg.data == b'2'):
            ser0 = ser0 + 10
            kit.servo[0].angle = ser0

        if ( msg.data == b'3'):
            ser1 = ser1 - 10
            kit.servo[1].angle = ser1 
        if ( msg.data == b'4'):
            ser1 = ser1 + 10
            kit.servo[1].angle = ser1

        if ( msg.data == b'5'):
            ser2 = ser2 - 10
            kit.servo[2].angle = ser2
        if ( msg.data == b'6'):
            ser2 = ser2 + 10
            kit.servo[2].angle = ser2
        
    time.sleep(1)



def main(args=None):
    rclpy.init(args=args)

    subscriber = Subscriber()

    rclpy.spin(subscriber)

    subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()