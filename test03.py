import threading
import speech_recognition as sr
import cv2
import numpy as np
import sys
import atexit

def is_point_inside_rect(point, rect):
    x, y = point
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

def display_video(stop_event):
    try:
        # 建立視窗，並讓視窗可以動態調整
        cv2.namedWindow('correct', cv2.WINDOW_NORMAL)

        cap = cv2.VideoCapture(0)

        # 讀取giftbox圖片
        img_giftbox = cv2.imread("start.png", cv2.IMREAD_UNCHANGED)

        # 獲取圖片的寬度和高度
        height, width, _ = img_giftbox.shape

        # 建立HOG描述子，行人檢測
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        while not stop_event.is_set():
            # 從鏡頭讀取影像
            ret, frame = cap.read()

            # 取得影像大小
            frame_height, frame_width, _ = frame.shape

            # 確保img_giftbox的大小小於等於frame的大小
            if height <= frame_height and width <= frame_width:
                # 計算放置在影像中間的左上角座標
                x = int((frame_width - width) / 2)
                y = int((frame_height - height) / 2)

                # 將img_giftbox放回左上角
                frame[0:height, 0:width] = img_giftbox

                # 繪製綠色矩形框架在畫面的中央位置
                rect_width, rect_height = 200, 445
                rect_x = int((frame_width - rect_width) / 2)
                rect_y = int((frame_height - rect_height) / 2) + 13

                # 繪製紅色矩形
                cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 0, 255), 2)

                # 使用HOG描述子進行人體檢測
                rects, _ = hog.detectMultiScale(frame)

                # 檢查是否有完整的人體骨架在紅色框內
                is_full_body_inside_rect = False
                for (x, y, w, h) in rects:
                    if is_point_inside_rect((x, y), (rect_x, rect_y, rect_x + rect_width, rect_y + rect_height)) and \
                            is_point_inside_rect((x + w, y + h), (rect_x, rect_y, rect_x + rect_width, rect_y + rect_height)):
                        is_full_body_inside_rect = True
                        break

                # 如果有完整的人體骨架在紅色框內，將矩形框改為綠色
                if is_full_body_inside_rect:
                    cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 255, 0), 2)

            else:
                print("警告：giftbox.png圖片太大，無法放置在影像中間")

            # 顯示影像
            cv2.imshow("correct", frame)

            # 設定按鍵Q為結束條件
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print("程式出現異常：", str(e))

def voice_command(stop_event):
    recognizer = sr.Recognizer()

    while not stop_event.is_set():
        # 辨識語音
        with sr.Microphone() as source:
            print("請說話...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="zh-TW")
            print("辨識結果：", text)

            if "開始" in text:
                print("關閉提示視窗")
                stop_event.set()
                break  # 當辨識到「開始」指令時，立即跳出迴圈

        except sr.UnknownValueError:
            print("無法辨識語音")
        except sr.RequestError:
            print("無法連線至 Google 語音辨識服務")


# 创建一个全局的 stop_event
stop_event = threading.Event()

# 创建全局的 video_thread 和 voice_thread
video_thread = None
voice_thread = None

# 创建全局的摄像头对象
cap = cv2.VideoCapture(0)


def cleanup():
    global stop_event, video_thread, voice_thread, cap  # 声明全局变量
    # 设置 stop_event 以停止其他线程
    stop_event.set()

    # 等待线程完成
    if video_thread:
        video_thread.join()
    if voice_thread:
        voice_thread.join()

    # 释放摄像头资源
    if cap.isOpened():
        cap.release()


atexit.register(cleanup)


def main():
    global stop_event, video_thread, voice_thread  # 声明全局变量
    video_thread = threading.Thread(target=display_video, args=(stop_event,))
    voice_thread = threading.Thread(target=voice_command, args=(stop_event,))

    video_thread.start()
    voice_thread.start()

    try:
        while not stop_event.is_set():  # 添加退出程序的条件
            pass
    except KeyboardInterrupt:
        print("用户中断")
    finally:
        cleanup()  # 确保在退出程序时执行清理操作
        sys.exit()  # 强制退出程序


if __name__ == "__main__":
    main()