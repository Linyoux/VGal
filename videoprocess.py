# encoding:utf-8
import re

import cv2
import easyocr
from difflib import SequenceMatcher
import json

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


def process_video(video_path, region, interval=0.5, similarity_threshold=0.6):
    """处理视频并提取文本"""
    reader = easyocr.Reader(['ch_sim', 'en'],download_enabled=False)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    text_groups = []
    last_text = ""

    interval_frames = int(fps * interval)

    for frame_num in range(0, total_frames, interval_frames):
        current_timestamp = frame_num / fps
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        print(f"正在处理第{frame_num}/{total_frames}帧")



        ret, frame = cap.read()
        if not ret:
            break

        roi = frame[region[1]:region[3],
              region[0]:region[2]]

        results = reader.readtext(roi)
        current_text = " ".join([result[1] for result in results])

        if not current_text or not filter(current_text):
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
        #
        # if frame_num > 50:
        #     break

    cap.release()

    return text_groups

def write_to_script(videoName,text_groups, output_file):
    with open(output_file,"w",encoding="utf-8") as f:
        f.write("play " + videoName)
        f.write("\n")
        f.write("proc")
        f.write("\n")
        f.write("\n")

        for i, group in enumerate(text_groups, 1):
            time = round(group.timestamps[-1],2)
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
                "time": round(group.timestamps[-1],2) -0.05,
                "text": group.texts[-1]
            })
        with open("script.json","w",encoding="utf-16") as f:
            json.dump(dats,f,indent=4,ensure_ascii=False)

def main():
    video_path = 'b.mp4'  # 替换为你的视频路径
    output_file = 'output.txt'  # 输出文件名
    region = [00, 0, 2560, 496]  # 示例区域，根据实际需求调整

    text_groups = process_video(video_path, region,0.5)
    write_to_file(text_groups, output_file)

    print(f"结果已写入 {output_file}")


if __name__ == "__main__":
    main()
