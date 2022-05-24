#!/usr/bin/env python

import os
import json
import cv2
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

from ament_index_python.packages import get_package_share_directory


class CameraPublisher(Node):
    def __init__(self, queueFromJson, timerFromJson):
        super().__init__('camera_publisher')
        
        # json 파일에서 읽어온 것으로 publisher생성
        self.publisher_ = self.create_publisher(Image, "/camera0/image_raw", queueFromJson)
        self.create_timer(timerFromJson, self.timer_callback)
        
        self.cam_cap = cv2.VideoCapture(0)
        # self.cam_cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        # self.cam_cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        # self.cam_cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

        self.get_logger().info('\n---- Images are being published... ---')
        
    def timer_callback(self):
        if self.cam_cap.isOpened() == False :
            self.get_logger().error('\n--- Error opening video ---')
            rclpy.shutdown()
            
        else :
            # cam_cap 읽어오기 (0 device)
            ret, frame = self.cam_cap.read()
            #self.get_logger().info('\n--- Images are being published... ---') ## test

            if ret == True:
                # processes image data and converts to ros 2 message
                msg = Image()
                msg.header.stamp = Node.get_clock(self).now().to_msg()
                msg.header.frame_id = 'camera0'
                msg.height = np.shape(frame)[0]
                msg.width = np.shape(frame)[1]
                msg.encoding = "bgr8"
                msg.is_bigendian = False
                msg.step = np.shape(frame)[2] * np.shape(frame)[1]
                msg.data = np.array(frame).tobytes()

                # publishes msg
                self.publisher_.publish(msg)
                
            else :
                self.get_logger().error('\n--- Error opening video ---')
                self.cam_cap.release()
                rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    # conf.json파일 불러오기
    file_ = os.path.join(get_package_share_directory('camera_pub'), "conf.json")
    with open(file_) as setFile:
        settings = json.load(setFile)

    # 읽어온 설정값 넘기면서 생성
    camera_publisher = CameraPublisher(settings["queue_size"], settings["timer"])
    rclpy.spin(camera_publisher)

    camera_publisher.get_logger().warn('\n--- Shutdown ---')
    camera_publisher.destroy_node()
    rclpy.shutdown()
    