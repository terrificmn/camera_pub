# ROS2 camera publish node 설치
자신의 워크스페이스의 src디렉토리에 git clone 을 만들어 줍니다
```
cd ~/colcon/src
git clone https://github.com/terrificmn/camera_pub.git
```
그리고 빌드
```
cd ~/colcon_ws 
colcon build --symlink-install
```

<br/>

## 2가지의 노드 중 한개 실행

1. ROS2의 cv_bridge를 이용한 pub_cam_node 실행
```
ros2 run camera_pub pub_cam_node
```

또는   

2. cv_bridge를 사용하지 않고 opencv로만 publish 하는 노드 사용하려면 아래의 노드를 실행  

```
ros2 run camera_pub pub_opencv_cam_node
```

- pub_opencv_cam_node는 *conf.json* 파일에서 퍼블리싱 타이머와, 큐사이즈를 수정해 줄 수 있습니다.   
아무래도 라즈베리파이에서는 ssh로 접속을 해서 해야하기 때문에 vi로 좀 더 편하게 수정가능 
```json
{
"queue_size" : 10,
"timer" : 0.2
}
```

<br/>

## 카메라 사용
- 보통의 웹캠 usb캠을 사용

> Remote PC ubuntu에서는 1번 노드 원활히 작동이 잘 되나,   
라즈베리파이에서는 부하가 많이 걸리고 퍼블리싱을 원할하게 안되는 것 같다.   
오히려 2번 노드가 라즈베리파이에서 더 퍼블리싱이 잘 된다. 

- Raspberry Pi Camera Module로는 더 좋은 결과가 나올지 추후 테스트를 할 예정  
(CSI interface를 사용해서 굉장히 빠른 data rates와 픽셀 데이터를 보낼 수 있다고 함)
