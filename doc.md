# 大作业说明文档

## 项目简介
使用python语言开发一个网站服务，向有权限的用户提供某一摄像头的监控画面，要求应用人工智能技术对监控画面做处理，将分析结果显示到网页上

## 环境
* python 3.6.5
    - Django 2.1.1
    - Keras 2.2.2
    - tensorflow 1.10.0
    - channels 2.1.3
    - opencv-python 3.4.3.18

## 功能点
实现的功能点如下
### 网站显示摄像头画面
* 网站服务搭建：使用django + channels
### 网站访问鉴权
### python读取摄像头画面
* 使用opencv-python打开系统usb摄像头
* 使用opencv-python打开RTSP协议的网络摄像头(加分项)
    - 若要使用RTSP协议的摄像头，请把`template\info.html`文件中的第24行的内容更换为25行的内容
    - `template\info.html`中第24行的内容如下
    ```JavaScript
        img.src = 'http://127.0.0.1:8000/video/play/[url]';
    ```
    通过修改`[url]`中的内容，可以播放任意摄像头或本地视频，注意问号要使用{\questionmark}转义。比如一个打开网络摄像头的写法如下
    ```JavaScript
    img.src = 'http://127.0.0.1:8000/video/play/rtsp://admin:admin@59.66.68.38:554/cam/realmonitor{\questionmark}channel=1&subtype=0';
    ```

### 网页端显示监控画面
* 使用流媒体技术向前端推送视频流(加分项)
    - 使用django的StreamingHttpResponse
    - 使用M-JPEG
    - 为了节约资源，一个session只能同时被推送最多一个视频流，如果一个session请求了两个视频流，那么后面那个请求将会返回403forbidden
### 使用人工智能技术分析监控视频

### 提供报警功能
* 使用pythonpython实现基于主动推送而不是轮询的消息提醒(加分项)
    - 使用channels实现websocket，从而实现主动推送
        - 在加载页面时，前端请求建立一个websocket，然后向后端发送session id。
        - 当警报发生时，后端通过session id查找到对应的websocket，使用它向前端推送消息。
        - 前端接到消息之后，把消息放到对应标签内。
* 用户可以查看历史警示记录，可以删除选定的记录使其不再显示
