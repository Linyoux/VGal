import time
import tkinter as tk
from PIL import Image, ImageTk

import videoprocess

file_path = ""
region = None
root = None

intervalEntry = None
similarityEntry = None

def button1_action():
    global intervalEntry,similarityEntry,root

    interval = float(intervalEntry.get())
    similarityEntry = float(similarityEntry.get())

    root.destroy()
    start_time = time.time()  # 获取当前时间戳
    text_groups = videoprocess.process_video(file_path,region,interval,similarityEntry)


    if "/" in file_path:
        file_name = file_path[file_path.rindex("/") + 1:]
    else:
        file_name = file_path
    videoprocess.write_to_script(file_name,text_groups,"start.vgs")

    end_time = time.time()  # 获取当前时间戳
    elapsed_time = end_time - start_time  # 计算耗时
    print("处理完成")
    print(f"耗时: {elapsed_time:.4f} 秒")

def reset_action():
    exit()


def show_confirmWindow(tknode,crop_area,file):
    global file_path,region,root,similarityEntry,intervalEntry
    region = crop_area
    file_path = file
    root = tk.Toplevel(tknode)
    root.title("区域确认")

    # 加载图片对象

    image_path = "current_frame.jpg"  # 替换为你的图片路径
    pil_image = Image.open(image_path)
    cropped_image = pil_image.crop(crop_area)
    tk_image = ImageTk.PhotoImage(cropped_image)
    #
    # # 创建标签显示图片
    image_label = tk.Label(root, image=tk_image)
    image_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    label = tk.Label(root, text="处理间隔（单位：秒）:")
    label.grid(row=1, column=0, pady=10 )  # 添加一些垂直间距

    # 创建一个输入框
    default_value = tk.StringVar()
    default_value.set("0.5")  # 设置默认值
    intervalEntry = tk.Entry(root,textvariable=default_value)
    intervalEntry.grid(row=1, column=1, pady=10)


    label2 = tk.Label(root, text="文本相似度:")
    label2.grid(row=2, column=0, pady=10 )  # 添加一些垂直间距

    default_value = tk.StringVar()
    default_value.set("0.6")  # 设置默认值
    # 创建一个输入框
    similarityEntry = tk.Entry(root,textvariable=default_value)
    similarityEntry.grid(row=2, column=1, pady=10 )

    # 创建按钮
    button1 = tk.Button(root, text="确定",command=button1_action)
    button1.grid(row=3, column=0, pady=10 )

    button2 = tk.Button(root, text="取消", command=reset_action)
    button2.grid(row=3, column=1, pady=10)

    # 调整行和列的权重，使组件能够在水平和垂直方向上平均分布
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    root.mainloop()