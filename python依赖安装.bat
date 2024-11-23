@echo off

echo 正在卸载旧版本opencv...
pip uninstall -y opencv-python opencv-python-headless

echo 正在安装必要的包...
pip install opencv-contrib-python easyocr Pillow

echo 正在检查CUDA版本...
nvidia-smi
set /p cuda_ver="请输入您看到的CUDA版本 (例如看到12.7就输入127): "

if %cuda_ver% GEQ 124 (
    echo 检测到CUDA版本 %cuda_ver%, 使用新版本安装...
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
) else (
    if %cuda_ver% LEQ 118 (
        echo 检测到CUDA版本 %cuda_ver%, 使用CUDA 11.8安装...
        pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 -f https://mirrors.aliyun.com/pytorch-wheels/cu118
    ) else if %cuda_ver% LEQ 121 (
        echo 检测到CUDA版本 %cuda_ver%, 使用CUDA 12.1安装...
        pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 -f https://mirrors.aliyun.com/pytorch-wheels/cu121
    )
)

echo 安装完成!
pause
