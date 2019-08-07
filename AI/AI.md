넷챌린지
========
환경: ubuntu 16.0.4 GPU 미사용

## Anaconda

#### 아나콘다 설치
    https://www.anaconda.com/download
    bash Anaconda3-5.2.0-Linux-x86_64.sh //버전 확인하고 수정
    //ctrl+c 약관 동의로 넘어가기

    source ~/.bashrc
    conda info --env //설치 확인


#### 가상환경+tf
    conda create -n (가상환경이름) python=(버전)
    source activate (가상환경이름)
    source deactivate

    export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.4.0rc1-cp35-cp35m-linux_x86_64.whl
    pip3 install --upgrade $TF_BINARY_URL

    python
    import tensorflow as tf

## OpenCV 설치

개빡셈 ㅅㅂ
    
