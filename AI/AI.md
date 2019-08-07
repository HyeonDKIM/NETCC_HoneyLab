넷챌린지
========
환경: ubuntu 16.0.4 GPU 미사용

## Anaconda

참고: https://light-tree.tistory.com/59

#### 아나콘다 설치
    https://www.anaconda.com/download
    $ bash Anaconda3-5.2.0-Linux-x86_64.sh //버전 확인하고 수정
    //ctrl+c 약관 동의로 넘어가기

    $ source ~/.bashrc
    $ conda info --env //설치 확인


#### 가상환경+tf
    $ conda create -n (가상환경이름) python=(버전)
    $ source activate (가상환경이름)
    $ source deactivate

    $ export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.4.0rc1-cp35-cp35m-linux_x86_64.whl
    $ pip3 install --upgrade $TF_BINARY_URL

    $ python
    import tensorflow as tf

## OpenCV 

개빡셈 ㅅㅂ
참고: https://jsh93.tistory.com/53

#### 패키지 업데이트
    $ sudo apt-get update && sudo apt-get upgrade
    
#### 기본 환경 구축
    $ sudo apt-get -y purge  libopencv* python-opencv
    $ sudo apt-get -y install build-essential cmake vim
    $ sudo apt-get -y install pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev
    $ sudo apt-get -y install libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libxine2-dev libv4l-dev
    $ sudo apt-get -y install v4l-utils libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libqt4-dev
    $ sudo apt-get -y install libgtk2.0-dev libgtk-3-dev mesa-utils libgl1-mesa-dri libqt4-opengl-dev
    $ sudo apt-get -y install libatlas-base-dev gfortran libeigen3-dev python3-dev python3-numpy python-dev python-numpy libatlas-base-dev gfortran

#### Opencv-3.4.2 Download
    $ wget -O opencv.zip https://github.com/opencv/opencv/archive/3.4.2.zip
    $ unzip opencv.zip
    $ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.2.zip
    $ unzip opencv_contrib.zip
    
#### 빌드 & install
    $ cd ~/opencv-3.4.2/
    $ mkdir build
    $ cd build
    $ cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D WITH_TBB=OFF \
    -D WITH_IPP=OFF \
    -D WITH_1394=OFF \
    -D BUILD_WITH_DEBUG_INFO=OFF \
    -D BUILD_DOCS=OFF \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D WITH_QT=OFF \
    -D WITH_GTK=ON \
    -D WITH_OPENGL=ON \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.4.2/modules \
    -D WITH_V4L=ON  \
    -D WITH_FFMPEG=ON \
    -D WITH_XINE=ON \
    -D BUILD_NEW_PYTHON_SUPPORT=ON \
    ../

    $ time make
    $ sudo make install
    
## YOLO

참고: https://juni-94.tistory.com/9

#### 설치 및 설정
    $ git clone https://github.com/pjreddie/darknet.git
    $ cd darknet
    $ make
    $ vi Makefile
    OPENCV 1로 변경. Cudnn Gpu 사용시 해당 부분도 1로 변경.
    
    $ make
    $ wget https://pjreddie.com/media/files/yolov3.weights
    $ ./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg
#### Tiny YOLO
    $ wget https://pjreddie.com/media/files/yolov3-tiny.weights
    $ ./darknet detect cfg/yolov3-tiny.cfg yolov3-tiny.weights data/dog.jpg
#### Webcam 및 동영상
    $ ./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights
    $ ./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights <video file>

#### keras-yolo3
참고 : https://github.com/qqwweee/keras-yolo3
    $ wget https://pjreddie.com/media/files/yolov3.weights
    $ python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5
    $ python yolo_video.py --input [video_path]
