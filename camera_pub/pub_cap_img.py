# !/usr/bin/env/ python3
import rclpy
from rclpy.node import Node

import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class ImgCapPublisher (Node):
    frame_num = 0
    def __init__ (self):
        super().__init__("img_cap_pub_node")

        self.publisher = self.create_publisher(Image, "/camera0/image_raw", 10)
        
        self.cv_bridge = CvBridge()
        timer_ = 0.2
        self.timer_ = self.create_timer(timer_, self.img_cap_publish)

        self.cam_cap = cv2.VideoCapture(0)
        # self.cam_cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        # cam_cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        # cam_cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.get_logger().info('\n--- Images are being published... ---')

    def img_cap_publish (self):
        # 캠0번째꺼 가져오기
        if self.cam_cap.isOpened() == False :
            self.get_logger().error('\n--- Error opening video stream ---')
            rclpy.shutdown()

        else:
            ret, frame = self.cam_cap.read() 
            # 축소하기
            #resizedFrame = cv2.resize(frame, (640, 480)) 
            self.get_logger().info('\n--- Images are being published... ---')
            
            if ret == True:
                try:
                    msg = Image()
                    msg = self.cv_bridge.cv2_to_imgmsg(frame, 'bgr8')
                    #msg.header.frame_id = str(self.frame_num)   # 'msg' is a ROS2 sensor_msgs/Image.msg
                    #msg.header.frame_id = 'camera0'
                    #self.frame_num += 1
                    self.publisher.publish(msg)

                except CvBridgeError as e:
                    self.get_logger().info(e)


def main(args=None):
    rclpy.init(args=args)

    img_sensor_publisher = ImgCapPublisher()
    rclpy.spin(img_sensor_publisher)

    img_sensor_publisher.get_logger().warn('\n--- Shutdown ---')
    img_sensor_publisher.destroy_node()
    rclpy.shutdown()
