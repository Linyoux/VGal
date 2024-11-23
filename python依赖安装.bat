@echo off

REM Uninstall existing opencv packages
pip uninstall -y opencv-python opencv-python-headless

REM Install required packages
pip install opencv-contrib-python easyocr Pillow

REM Check CUDA version
nvidia-smi
set /p cuda_ver="Please input CUDA number (for example: 12.7 input 127): "

if %cuda_ver% LSS 15 (
    echo Error: You need input full number. For example: CUDA 12.7 should input 127
    pause
    exit
)

if %cuda_ver% GEQ 124 (
    echo Installing for CUDA %cuda_ver%
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
) else (
    if %cuda_ver% LEQ 118 (
        echo Installing for CUDA 11.8
        pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 -f https://mirrors.aliyun.com/pytorch-wheels/cu118
    ) else if %cuda_ver% LEQ 121 (
        echo Installing for CUDA 12.1
        pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 -f https://mirrors.aliyun.com/pytorch-wheels/cu121
    )
)

pause
