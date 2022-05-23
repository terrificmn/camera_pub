#!/usr/bin/env python

import cv2
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        
        # initialize publisher
        self.publisher_ = self.create_publisher(Image, "/camera0/image_raw", 10)
        timer_period = 0.2
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

        # set image counter and videocapture object
        self.i = 0
        self.frame_num = 0
        self.get_logger().info('\n---- Images are being published... ---')
        
    def timer_callback(self):
        if self.capture.isOpened() == False :
            self.get_logger().error('\n--- Error opening video stream ---')
            rclpy.shutdown()
            
        else :
            # reads image data
            ret, frame = self.capture.read()
            
            if ret == True:
                # processes image data and converts to ros 2 message
                msg = Image()
                msg.header.stamp = Node.get_clock(self).now().to_msg()
                msg.header.frame_id = str(self.frame_num)
                msg.height = np.shape(frame)[0]
                msg.width = np.shape(frame)[1]
                msg.encoding = "bgr8"
                msg.is_bigendian = False
                msg.step = np.shape(frame)[2] * np.shape(frame)[1]
                msg.data = np.array(frame).tobytes()
                self.frame_num += 1

                # publishes message
                self.publisher_.publish(msg)
                
            else :
                self.get_logger().error('\n--- 11Error opening video stream ---')
                self.capture.release()
                rclpy.shutdown()
        
        # image counter increment
        self.i += 1
        
        return None


def main(args=None):
    rclpy.init(args=args)

    camera_publisher = CameraPublisher()
    rclpy.spin(camera_publisher)

    camera_publisher.destroy_node()
    rclpy.shutdown()
    
    return None


if __name__ == '__main__':
    main()
