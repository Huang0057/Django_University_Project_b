import threading
import speech_recognition as sr
import cv2
import numpy as np

def is_point_inside_rect(point, rect):
    x, y = point
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

def display_video(stop_event, start_event):
    try:
        # 建立視窗，並讓視窗可以動態調整
        cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
        cap = cv2.VideoCapture(0)

        img_giftbox = cv2.imread("start.png", cv2.IMREAD_UNCHANGED)
        height, width, _ = img_giftbox.shape

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        while not stop_event.is_set():
            ret, frame = cap.read()
            frame_height, frame_width, _ = frame.shape

            if height <= frame_height and width <= frame_width:
                x = int((frame_width - width) / 2)
                y = int((frame_height - height) / 2)
                frame[0:height, 0:width] = img_giftbox

                rect_width, rect_height = 200, 445
                rect_x = int((frame_width - rect_width) / 2)
                rect_y = int((frame_height - rect_height) / 2)+13

                cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 0, 255), 2)

                rects, _ = hog.detectMultiScale(frame)
                is_full_body_inside_rect = False

                for (x, y, w, h) in rects:
                    if is_point_inside_rect((x, y), (rect_x, rect_y, rect_x + rect_width, rect_y + rect_height)) and \
                            is_point_inside_rect((x + w, y + h), (rect_x, rect_y, rect_x + rect_width, rect_y + rect_height)):
                        is_full_body_inside_rect = True
                        break

                if is_full_body_inside_rect:
                    cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 255, 0), 2)

                cv2.imshow("Camera", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print("程式出現異常：", str(e))

def voice_command(stop_event, start_event):
    recognizer = sr.Recognizer()

    while not stop_event.is_set():
        with sr.Microphone() as source:
            print("請說話...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="zh-TW")
            print("辨識結果：", text)

            if "開始" in text:
                print("關閉鏡頭和語音識別")
                stop_event.set()  # 停止视频线程
                start_event.set()  # 设置开始标志
                video_thread.join()  # 等待视频线程完全执行完毕
                break

        except sr.UnknownValueError:
            print("無法辨識語音")
        except sr.RequestError:
            print("無法連線至 Google 語音辨識服務")

if __name__ == "__main__":
    stop_event = threading.Event()
    start_event = threading.Event()

    voice_thread = threading.Thread(target=voice_command, args=(stop_event, start_event))
    video_thread = threading.Thread(target=display_video, args=(stop_event, start_event))

    voice_thread.start()
    video_thread.start()

    voice_thread.join()
    video_thread.join()

    print("所有執行緒已經結束")