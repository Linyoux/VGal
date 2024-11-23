@echo off

echo ����ж�ؾɰ汾opencv...
pip uninstall -y opencv-python opencv-python-headless

echo ���ڰ�װ��Ҫ�İ�...
pip install opencv-contrib-python easyocr Pillow

echo ���ڼ��CUDA�汾...
nvidia-smi
set /p cuda_ver="��������������CUDA�汾 (���翴��12.7������127): "

if %cuda_ver% GEQ 124 (
    echo ��⵽CUDA�汾 %cuda_ver%, ʹ���°汾��װ...
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
) else (
    if %cuda_ver% LEQ 118 (
        echo ��⵽CUDA�汾 %cuda_ver%, ʹ��CUDA 11.8��װ...
        pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 -f https://mirrors.aliyun.com/pytorch-wheels/cu118
    ) else if %cuda_ver% LEQ 121 (
        echo ��⵽CUDA�汾 %cuda_ver%, ʹ��CUDA 12.1��װ...
        pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 -f https://mirrors.aliyun.com/pytorch-wheels/cu121
    )
)

echo ��װ���!
pause
