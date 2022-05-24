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

> 일반 remote PC에서는 cv_bridge를 이용한 1번 노드가 원할하게 잘 되괴 
2번 노드는 timer가 잘 맞지를 않게 작동을 하는데  
오히려 라즈베리파이에서는 1번 노드가 퍼블리싱이 잘 안되는 현상이 발생   
그런데 2번 노드는 라즈베리파이에서는 더 잘 된다.   
