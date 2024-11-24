#encoding:utf-8
import asyncio
import os
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from wechat_ocr.ocr_manager import OcrManager, OCR_MAX_TASK_ID

CurrentDir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WECHAT_OCR_DIR = os.path.join(CurrentDir, "path/WeChatOCR/WeChatOCR.exe")
DEFAULT_WECHAT_DIR = os.path.join(CurrentDir, "path")

async def delayed_task(delay, task_name):
    print(f"{task_name} will start after {delay} seconds.")
    await asyncio.sleep(delay)
    print(f"{task_name} finished after {delay} seconds.")

class WechatOcr:

    def __init__(self,count,total_frames):
        self.count = count
        self.ocrs = []
        self.loop = 0
        self.total_frames = total_frames
        self.results = {}
        self.invalidFiles = []
        self.running = True
        threading.Thread(target=self.deleteFile).start()
        for i in range(count):
            ocr_manager = OcrManager(DEFAULT_WECHAT_DIR)
            # 设置WeChatOcr目录
            ocr_manager.SetExePath(DEFAULT_WECHAT_OCR_DIR)
            # 设置微信所在路径
            ocr_manager.SetUsrLibDir(DEFAULT_WECHAT_DIR)
            # 设置ocr识别结果的回调函数
            ocr_manager.SetOcrResultCallback(self.ocr_result_callback)
            # 启动ocr服务
            ocr_manager.StartWeChatOCR()
            self.ocrs.append(ocr_manager)

    def deleteFile(self):
        while self.running:
            for f in self.invalidFiles:
                path = f["path"]
                t = f["time"]
                if time.time() - t >= 3:
                    if os.path.exists(path):
                        os.remove(path)
                        break
            time.sleep(1)


    def ocr_result_callback(self,img_path: str, results: dict):
        result = " ".join(result['text'] for result in results['ocrResult'])
        frame_num = os.path.basename(img_path)
        frame_num = int(frame_num[:frame_num.index(".")])
        self.results[frame_num] = result
        print(f"已处理完毕第{frame_num}/{self.total_frames}帧")
        self.invalidFiles.append({
            "path": img_path,
            "time": time.time()
        })


    def executeOcr(self,img_path):
        self.ocrs[self.loop].DoOCRTask(img_path)
        self.loop += 1
        if self.loop >= self.count:
            self.loop = 0

    def getResult(self):
        ok = False
        while not ok:
            for ocr in self.ocrs:
                time.sleep(0.1)
                if ocr.m_task_id.qsize() != OCR_MAX_TASK_ID:
                    continue
            ok = True

        return self.results

    def close(self):
        for ocr in self.ocrs:
            ocr.KillWeChatOCR()
        self.running = False



if __name__ == "__main__":
    pass
    # start_time = time.time()

    # w = WechatOcr(1)
    # w.executeOcr(r"C:\users\yyy\Pictures\透明.png")
    #
    # while True:
    #     time.sleep(10)
    # print(str(time.time() - start_time))