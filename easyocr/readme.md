#### 安装：
建议先换源为国内镜像站，
参考：pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
> pip uninstall opencv-python opencv-python-headless  
> pip install opencv-contrib-python easyocr Pillow  

查看GPU的CUDA版本后，选择合适的版本安装pytorch  

> pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 #Cuda版本大于124使用（目前没有镜像站）  

> pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 -f https://mirrors.aliyun.com/pytorch-wheels/cu118 #Cuda版本小于121时使用，最后三个数字填版本数（使用镜像站安装）  

> pip install torch torchvision torchaudio #CPU版本，不推荐

在C:\Users\你的用户名\ .EasyOCR\model中，安装craft_mlt_25k，english_g2，zh_sim_g2这三个PTH文件