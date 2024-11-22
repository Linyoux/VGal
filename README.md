# VGal
#### 介绍：
本项目主要用于实现静态视频播放的体验优化。通过视频分段播放，获得近似视觉小说的体验。

#### 注意：
请勿用于非法用途，
请勿用于已正常移植的游戏，
请勿未经汉化组允许而录屏其译的游戏，
请勿未经录屏者允许而用其录屏。

#### 建议：
通过magpie缩放，让录屏更高清。

#### 原理：
PC（供给端）：负责录屏，处理分割点。通过OCR识别视频各位置文本，进而获取视频分割点。

安卓（使用端）：通过分割点，实现视频分段播放（点击屏幕，跳转到下一段视频，也就是下一段话），获得类似移植版的体验。

#### 安装：

> pip uninstall opencv-python opencv-python-headless  
> pip install opencv-contrib-python easyocr Pillow  
> pip install torch torchvision torchaudio  
>#以下是GPU版本  
> pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 -f https://mirrors.aliyun.com/pytorch-wheels/cu118

在C:\Users\你的用户名\.EasyOCR\model中，安装craft_mlt_25k，english_g2，zh_sim_g2的PTH文件

安卓源码：https://github.com/Linyoux/VGal_app
