import cv2
import math
import uuid
import mediapipe as mp

import datetime
import requests

id = "123123"
part = "hand"
playstage = "食指訓練"
start_time = datetime.datetime.now()
print(f"{part}\n{playstage}\nStart time: {start_time}")


def detect_hand_landmarks(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            return hand_landmarks
    return None


def count_finger_bends(hand_landmarks):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    finger_joints = [
        mp_hands.HandLandmark.INDEX_FINGER_DIP,
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.INDEX_FINGER_MCP
    ]

    bends = [0, 0, 0]  # 初始化三个关节的弯曲角度为0

    for i, joint in enumerate(finger_joints):
        joint_coord = hand_landmarks.landmark[joint]
        joint_x = joint_coord.x
        joint_y = joint_coord.y

        # 计算关节与手腕之间的距离（欧氏距离）
        dist = math.sqrt((wrist.x - joint_x)**2 + (wrist.y - joint_y)**2)

        # 计算关节与手腕之间的直线距离（y轴方向上的距离）
        vertical_dist = wrist.y - joint_y

        # 计算关节的弯曲角度（弧度）
        angle_rad = math.atan2(vertical_dist, dist)

        # 将弯曲角度转换为角度（度数）
        angle_deg = math.degrees(angle_rad)

        bends[i] = angle_deg  # 将计算得到的弯曲角度保存到列表中

    return bends


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

cap = cv2.VideoCapture(0)
left_index_finger_bends = 0
finger_down = False  # 手指放下标志

while True:
    ret, frame = cap.read()

    hand_landmarks = detect_hand_landmarks(frame)

    if hand_landmarks:
        bends = count_finger_bends(hand_landmarks)

        # 判断食指弯曲的条件：第二关节和第一关节的弯曲角度大于第三关节的弯曲角度
        if not finger_down and bends[1] > bends[2] > bends[0]:
            left_index_finger_bends += 1
            finger_down = True
        elif finger_down and bends[0] > bends[1]:
            finger_down = False

        # 在左上角放置一個狀態框
        cv2.rectangle(frame, (0, 0), (170, 73), (245, 117, 16), -1)
        # 顯示次數
        cv2.putText(frame, 'number of times', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, str(left_index_finger_bends), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # 繪製手部骨架線條
        mp_drawing.draw_landmarks(
            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Gesture Recognition', frame)

    if left_index_finger_bends == 10:
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
        print("Counter:", left_index_finger_bends)
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
            'ExerciseCount': left_index_finger_bends
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
        print("Counter:", left_index_finger_bends)
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
            'ExerciseCount': left_index_finger_bends
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

# 返回左手食指弯曲次数
print("Left Index Finger Bends:", left_index_finger_bends)
