# VGal
#### 介绍：
本项目主要用于实现静态视频播放的体验优化。通过视频分段播放，获得近似视觉小说的体验。

#### 原理：
PC（供给端）：负责录屏，处理分割点。通过OCR识别视频各位置文本，进而获取视频分割点。

安卓（使用端）：通过分割点，实现视频分段播放（点击屏幕，跳转到下一段视频，也就是下一段话），获得类似移植版的体验。

#### 注意：
请勿用于非法用途，
请勿用于已正常移植的游戏，
请勿未经汉化组允许而录屏其译的游戏，
请勿未经录屏者允许而用其录屏。

#### 建议：
通过magpie缩放，让录屏更高清。

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

#### 其他：
###### 安卓源码：
https://github.com/Linyoux/VGal_app
###### Magpie录制说明
https://github.com/Blinue/Magpie
*推荐使用cuNNy效果缩放*
（因为这个效果用视觉小说训练的）
1.**关闭系统缩放**：如果你设置了 DPI 缩放（笔记本默认打开），首先进入该程序的兼容性设置，将“高 DPI 缩放替代”设置为“应用程序”。
2.**关闭游戏缩放**：一些游戏支持调整窗口的大小，但只使用简单的缩放算法，这时请先将其设为原始（最佳）分辨率。
3.**分辨率方面**：一些老游戏使用缩放后，分辨率为1080P。如果你的显示器是2K屏，建议将屏幕分辨率转成1080P进行录制，如果是4K屏，建议使用两个效果缩放。