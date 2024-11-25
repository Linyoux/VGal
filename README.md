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
> pip install opencv-contrib-python Pillow  

下载源代码后，选择你要使用的OCR，将他们复制到根目录使用（各自OCR安装流程不同）。

#### 其他：
安卓源码：https://github.com/Linyoux/VGal_app
