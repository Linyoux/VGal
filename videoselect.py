import cv2
import tkinter as tk
from tkinter import filedialog
import confirmRegion
import sys
rect_start = None
rect_end = None
drawing = False
paused = False
current_frame = None
root = None
running = False
file_path = None

def select_video():
    global root,file_path
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
    if file_path:
        preview_video(file_path)
    root.destroy()


def draw_rectangle(event, x, y, flags, param):
    global rect_start, rect_end, drawing, current_frame, running, file_path

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        rect_start = (x, y)
        rect_end = rect_start

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # 使用当前帧的副本来绘制矩形
            temp_frame = current_frame.copy()
            rect_end = (x, y)
            cv2.rectangle(temp_frame, rect_start, rect_end, (255, 0, 0), 2)
            cv2.imshow("Video Preview", temp_frame)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rect_end = (x, y)

        # 排序坐标
        x1, y1 = rect_start
        x2, y2 = rect_end
        left = min(x1, x2)
        right = max(x1, x2)
        top = min(y1, y2)
        bottom = max(y1, y2)

        # 更新为排序后的区域
        rect_start = (left, top)
        rect_end = (right, bottom)

        cv2.rectangle(current_frame, rect_start, rect_end, (255, 0, 0), 2)
        cv2.imshow("Video Preview", current_frame)

        # 选择完区域后直接退出程序
        if rect_start and rect_end:
            print("选择的区域坐标：", rect_start, rect_end)
            cv2.imwrite('current_frame.jpg', current_frame)
            cv2.destroyAllWindows()  # 关闭窗口
            running = False
            confirmRegion.show_confirmWindow(root, (left, top, right, bottom), file_path)
            exit()  # 退出程序


def preview_video(file_path):
    global current_frame, paused, running
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print("Error opening video file")
        return

    # 创建一个全屏窗口
    cv2.namedWindow("Video Preview", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Video Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("Video Preview", draw_rectangle)
    running = True

    while running:
        if not paused:
            ret, current_frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重置视频到开头
                continue

        # 显示视频帧
        cv2.imshow("Video Preview", current_frame)

        # 处理键盘输入
        key = cv2.waitKey(25) & 0xFF
        if key == 27:  # ESC键
            break
        elif key == 32:  # 空格键
            paused = not paused
            print("暂停状态：", "已暂停" if paused else "已恢复")

        # 检查窗口是否关闭
        if cv2.getWindowProperty("Video Preview", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    select_video()
