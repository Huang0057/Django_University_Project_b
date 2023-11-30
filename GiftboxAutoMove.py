import cv2
import mediapipe as mp
import numpy as np
import random
import time
import cv2
import uuid
import mediapipe as mp
import numpy as np
import datetime
import requests

id = "123123"
part = "limb"
playstage = "獎勵關卡"
start_time = datetime.datetime.now()
print(f"{part}\n{playstage}\nStart time: {start_time}")

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

counter = 0
touching = False
previous_state = False
x_offset = 0
y_offset = 0
last_position_change_time = 0

# 设置图像移动速度
movement_speed = 10  # 调整这个值来控制移动速度，值越大移动越慢
stay_duration = 5  # 图像停留的时间（秒）


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)  # 创建窗口
    cv2.setWindowProperty('Camera', cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)  # 将窗口设置为全屏

    cap = cv2.VideoCapture(0)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    img = cv2.imread('giftbox3.png')
    img_width = img.shape[1]
    img_height = img.shape[0]

    stay_start_time = time.time()
    start_time = time.time()  # 初始化 start_time 變數

    while cap is not None:
        success, image = cap.read()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # 计算手掌中部分节点的数量
            num_touching_landmarks = sum(
                1 for landmark in landmarks if landmark.visibility > 0.5 and landmark.y < 0.5)

            if num_touching_landmarks > 0 and not previous_state:
                counter += 1  # 累加计数
                stay_start_time = time.time()  # 记录图像停留的起始时间
                print(counter)

            if time.time() - stay_start_time < stay_duration:
                touching = True
            else:
                touching = False

            if not touching:
                current_time = time.time()
                if current_time - last_position_change_time > stay_duration:
                    # 随机选择图像的位置
                    x_offset = random.randint(0, width - img_width)
                    y_offset = random.randint(0, height - img_height)
                    last_position_change_time = current_time

            resized_img = cv2.resize(img, (img_width, img_height))
            image[y_offset:y_offset + img_height,
                  x_offset:x_offset + img_width] = resized_img

            previous_state = touching

        except:
            pass

        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.putText(image, 'Number of touches: {}'.format(counter), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2)

        cv2.imshow('Camera', image)

        if counter >= 10:
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
            print("Counter:", counter)
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
                'ExerciseCount': counter
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

        current_time = time.time()
        if current_time - start_time > 15:  # 檢查程式是否執行超過15秒
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
            print("Counter:", counter)
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
                'ExerciseCount': counter
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
            break  # 超過15秒，退出迴圈

        if cv2.waitKey(10) & 0xFF == ord('q'):
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
            print("Counter:", counter)
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
                'ExerciseCount': counter
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
