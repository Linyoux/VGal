# encoding:utf-8
import os.path
import re
import shutil
from concurrent.futures import ThreadPoolExecutor

import cv2
import easyocr
from difflib import SequenceMatcher
import json
import wechatocr

class TextGroup:
    def __init__(self):
        self.texts = []  # 文本列表
        self.timestamps = []  # 时间戳列表


def calculate_similarity(str1, str2):
    """计算两个字符串的相似度"""
    return SequenceMatcher(None, str1, str2).ratio()


def filter(text):
    japanese_pattern = r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FA5]'
    chinese_pattern = r'[\u4e00-\u9fa5]'

    newtext = re.sub(japanese_pattern, "", text)
    newtext = re.sub(chinese_pattern, "", newtext)

    return text != newtext


def format_timestamp(seconds):
    """将秒数转换为 HH:MM:SS.milliseconds 格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)  # 获取毫秒部分
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


text_results = []


def executeOcr(reader, roi, current_timestamp, frame_num, total_frames,batch_size):
    results = reader.readtext(roi,batch_size=batch_size)
    current_text = " ".join([result[1] for result in results])
    if not current_text or not filter(current_text):
        return

    text_results.append((
        current_timestamp,
        current_text
    ))
    print(f"正在处理第{frame_num}/{total_frames}帧")


def delete_directory(path):
    # 检查路径是否存在
    if not os.path.exists(path):
        print(f"目录 {path} 不存在")
        return
    # 遍历目录
    for root, dirs, files in os.walk(path, topdown=False):
        # 删除文件
        for name in files:
            df = os.path.join(root, name)
            if os.path.exists(df):
                os.remove(df)

        # 删除目录
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    # 删除根目录
    os.rmdir(path)

def process_video_old(video_path, region, interval=0.5, similarity_threshold=0.6, batch_size=1):
    """处理视频并提取文本"""
    reader = easyocr.Reader(['ch_sim', 'en'], download_enabled=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    text_groups = []
    last_text = ""

    interval_frames = int(fps * interval)

    with ThreadPoolExecutor(max_workers=batch_size) as executor:

        for frame_num in range(0, total_frames, interval_frames):
            current_timestamp = frame_num / fps
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

            ret, frame = cap.read()
            if not ret:
                break

            roi = frame[region[1]:region[3],
                  region[0]:region[2]]

            executor.submit(executeOcr,reader, roi, current_timestamp, frame_num, total_frames,batch_size)
    cap.release()


    sorted(text_results, key=lambda x: x[0])
    for text in text_results:
        current_timestamp = text[0]
        current_text = text[1]
        if not text_groups:
            new_group = TextGroup()
            new_group.texts.append(current_text)
            new_group.timestamps.append(current_timestamp)
            text_groups.append(new_group)
            last_text = current_text
            continue

        similarity = calculate_similarity(last_text, current_text)

        if similarity >= similarity_threshold:
            text_groups[-1].texts.append(current_text)
            text_groups[-1].timestamps.append(current_timestamp)
        else:
            new_group = TextGroup()
            new_group.texts.append(current_text)
            new_group.timestamps.append(current_timestamp)
            text_groups.append(new_group)

        last_text = current_text


    return text_groups

def process_video(video_path, region, interval=0.5, similarity_threshold=0.6, batch_size=1):
    """处理视频并提取文本"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    text_groups = []
    last_text = ""

    w = wechatocr.WechatOcr(batch_size,total_frames)
    temp_path = 'temp/'
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    interval_frames = int(fps * interval)

    with ThreadPoolExecutor(max_workers=batch_size * 2) as executor:

        for frame_num in range(0, total_frames, interval_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

            ret, frame = cap.read()
            if not ret:
                break

            roi = frame[region[1]:region[3],
                  region[0]:region[2]]

            path = temp_path + str(frame_num) +'.jpg'
            cv2.imwrite(path, roi)
            w.executeOcr(path)
            # executor.submit(executeOcr,reader, roi, current_timestamp, frame_num, total_frames,batch_size)
    cap.release()

    results = w.getResult()

    delete_directory(temp_path)

    text_results = []
    for frame,result in results.items():
        current_timestamp = frame / fps
        text_results.append((
            current_timestamp,
            result
        ))

    w.close()
    sorted(text_results, key=lambda x: x[0])
    for text in text_results:
        current_timestamp = text[0]
        current_text = text[1]

        if current_text.strip() == "":
            continue

        if not text_groups:
            new_group = TextGroup()
            new_group.texts.append(current_text)
            new_group.timestamps.append(current_timestamp)
            text_groups.append(new_group)
            last_text = current_text
            continue

        similarity = calculate_similarity(last_text, current_text)

        if similarity >= similarity_threshold:
            text_groups[-1].texts.append(current_text)
            text_groups[-1].timestamps.append(current_timestamp)
        else:
            new_group = TextGroup()
            new_group.texts.append(current_text)
            new_group.timestamps.append(current_timestamp)
            text_groups.append(new_group)

        last_text = current_text


    return text_groups

def write_to_script(videoName, text_groups, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("play " + videoName)
        f.write("\n")
        f.write("proc")
        f.write("\n")
        f.write("\n")

        for i, group in enumerate(text_groups, 1):
            time = round(group.timestamps[-1], 2)
            text = group.texts[-1]

            f.write("text " + text)
            f.write("\n")
            f.write("time " + str(time))
            f.write("\n")
            f.write("proc\n\n")


def write_to_file(text_groups, output_file):
    dats = []
    """将文本分组写入文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, group in enumerate(text_groups, 1):
            f.write(f"Group {i}:\n")
            for j, (text, timestamp) in enumerate(zip(group.texts, group.timestamps)):
                f.write(f"  Timestamp: {format_timestamp(timestamp)} - Text: {text}\n")
            f.write("\n")

            dats.append({
                "time": round(group.timestamps[-1], 2),
                "text": group.texts[-1]
            })
        with open("script.json", "w", encoding="utf-16") as f:
            json.dump(dats, f, indent=4, ensure_ascii=False)


def main():
    video_path = 'game.mp4'  # 替换为你的视频路径
    output_file = 'output.txt'  # 输出文件名
    region = [00, 0, 2560, 496]  # 示例区域，根据实际需求调整

    text_groups = process_video(video_path, region, 0.5, batch_size=10)
    write_to_file(text_groups, output_file)

    print(f"结果已写入 {output_file}")


if __name__ == "__main__":
    main()
