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

#### 安装： 

通用依赖
> pip uninstall opencv-python opencv-python-headless  
> pip install opencv-contrib-python Pillow  

下载源代码，选择你使用的OCR，将其复制到根目录，之后各自的安装流程不同。

#### 其他：
###### Magpie录制说明  
通过**magpie**缩放，让录屏更**高清**： https://github.com/Blinue/Magpie  
推荐使用cuNNy效果缩放  
（因为这个效果是用**视觉小说**训练的）  
1.**关闭系统缩放**：如果你设置了 DPI 缩放（笔记本默认打开），首先进入该程序的兼容性设置，将“高 DPI 缩放替代”设置为“应用程序”。  
2.**关闭游戏缩放**：一些游戏支持调整窗口的大小，但只使用简单的缩放算法，这时请先将其设为原始（最佳）分辨率。  
3.**分辨率方面**：一些老游戏使用缩放后，分辨率为1080P。如果你的显示器是2K屏，推荐将屏幕分辨率转成1080P进行录制（因为2K视频不受待见）；如果是4K屏，推荐使用两个效果缩放（效果可以叠加）。  
4.**剪辑方面**：推荐使用LosslessCut处理，这个剪辑软件不需要重编码视频，免去了冗长的视频剪切和拼接时间，分钟间解决问题。
###### 安卓源码：
https://github.com/Linyoux/VGal_app  

**录屏分享**：https://www.123865.com/s/Jr6qVv-uuaXv  
