import cv2
import uuid
import mediapipe as mp
import numpy as np
import datetime
import requests
import math

id = "123123"
part = "hand"
playstage = "手部握拳"
start_time = datetime.datetime.now()
print(f"{part}\n{playstage}\nStart time: {start_time}")


def detect_hand_landmarks(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            return hand_landmarks
    return None


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)


cv2.namedWindow('Hand Gesture Recognition', cv2.WINDOW_NORMAL)  # 创建窗口
cv2.setWindowProperty('Hand Gesture Recognition',
                      cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  # 将窗口设置为全屏
cap = cv2.VideoCapture(0)
right_fist_count = 0
hand_opened = True
fist_closed = False

# 调整图像大小和距离阈值
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
DISTANCE_THRESHOLD = 0.1

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))  # 调整图像大小

    hand_landmarks = detect_hand_landmarks(frame)

    if hand_landmarks:
        hand_landmarks_list = hand_landmarks.landmark

        # 检测右手拇指和食指的位置
        thumb = hand_landmarks_list[mp_hands.HandLandmark.THUMB_TIP]
        index_finger = hand_landmarks_list[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # 计算拇指和食指的距离
        distance = abs(thumb.x - index_finger.x) + \
            abs(thumb.y - index_finger.y)

        if not fist_closed and distance < DISTANCE_THRESHOLD:
            fist_closed = True
        elif fist_closed and distance > DISTANCE_THRESHOLD + 0.02:
            hand_opened = True
            fist_closed = False

        if hand_opened and distance < DISTANCE_THRESHOLD:
            right_fist_count += 1
            hand_opened = False
        # 在左上角放置一個狀態框
        # 畫方形(pic,左上點,右下點,顏色,粗細(使用填滿功能))
        cv2.rectangle(frame, (0, 0), (170, 73), (245, 117, 16), -1)
        # cv2.rectangle(image,(277,0),(554,73),(245,117,16),-1)
        # cv2.putText(image, str('Raise left hand, parallel to shoulder.'), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        # 顯示次數
        cv2.putText(frame, 'number of times', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)  # 3:起始座標
        cv2.putText(frame, str(right_fist_count), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(frame, f"Right Fist Count: {right_fist_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # 繪製手部骨架線條
        mp_drawing.draw_landmarks(
            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('Hand Gesture Recognition', frame)
    if right_fist_count == 10:
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        duration_time_str = str(duration)

        PlayDate = start_time.strftime('%Y-%m-%d')
        StartTime = start_time.strftime('%H:%M:%S')
        EndTime = end_time.strftime('%H:%M:%S')
        UID = str(uuid.uuid4())
        duration_formatted = duration.total_seconds()
        hours, remainder = divmod(duration_formatted, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str_formatted = "{:02}:{:02}:{:02}".format(
            int(hours), int(minutes), int(seconds))

        print("id:", id)
        print("Counter:", right_fist_count)
        print("part:", part)
        print("UID:", UID)
        print("PlayStage:", playstage)
        print("Start Time:", StartTime)
        print("End time:", EndTime)
        print("Duration Time:", duration_str_formatted)

        url = 'http://127.0.0.1:8000/add_gamerecord/'  # 替換為你的Django應用程式的URL和端點

        data = {
            'USER_UID': id,
            'PlayDate': PlayDate,
            'PlayPart': part,
            'UID': UID,
            'PlayStage': playstage,
            'StartTime': StartTime,
            'EndTime': EndTime,
            'DurationTime': duration_str_formatted,
            'AddCoin': "5",
            'ExerciseCount': right_fist_count
        }
        header = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=data, headers=header)
        print(response.text)
        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print("Failed to send data.")
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        duration_time_str = str(duration)

        PlayDate = start_time.strftime('%Y-%m-%d')
        StartTime = start_time.strftime('%H:%M:%S')
        EndTime = end_time.strftime('%H:%M:%S')
        UID = str(uuid.uuid4())
        duration_formatted = duration.total_seconds()
        hours, remainder = divmod(duration_formatted, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_str_formatted = "{:02}:{:02}:{:02}".format(
            int(hours), int(minutes), int(seconds))

        print("id:", id)
        print("Counter:", right_fist_count)
        print("part:", part)
        print("UID:", UID)
        print("PlayStage:", playstage)
        print("Start Time:", StartTime)
        print("End time:", EndTime)
        print("Duration Time:", duration_str_formatted)

        url = 'http://127.0.0.1:8000/add_gamerecord/'  # 替換為你的Django應用程式的URL和端點

        data = {
            'USER_UID': id,
            'PlayDate': PlayDate,
            'PlayPart': part,
            'UID': UID,
            'PlayStage': playstage,
            'StartTime': StartTime,
            'EndTime': EndTime,
            'DurationTime': duration_str_formatted,
            'AddCoin': "5",
            'ExerciseCount': right_fist_count
        }
        header = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=data, headers=header)
        print(response.text)
        if response.status_code == 200:
            print("Data sent successfully.")
        else:
            print("Failed to send data.")
        break

cap.release()
cv2.destroyAllWindows()

# 返回右手握拳次数
print("Right Fist Count:", right_fist_count)
