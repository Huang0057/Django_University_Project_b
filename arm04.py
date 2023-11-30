import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

counter = 0
touching = False

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
    cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    img = cv2.imread('giftbox.png')
    while cap.isOpened():
        # 建立視窗，並讓視窗可以動態調整
        cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)

        success, image = cap.read()

        img = cv2.resize(img, (int(width / 4), int(height / 4)))
        image[0:img.shape[0], 0:img.shape[1]] = img

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # 检查手上的每个节点是否与图像接触
            for landmark in landmarks:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                if x >= 0 and x <= img.shape[1] and y >= 0 and y <= img.shape[0]:
                    touching = True
                    break
                else:
                    touching = False

            # 当手刚开始触碰图像时进行累加
            if touching and not previous_state:
                counter += 1
                print(counter)
                if counter == 10:
                    break
            previous_state = touching

        except:
            pass

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        #在左上角放置一個狀態框
        cv2.rectangle(image,(0,0),(170,73),(245,117,16),-1)#畫方形(pic,左上點,右下點,顏色,粗細(使用填滿功能))
        #cv2.rectangle(image,(277,0),(554,73),(245,117,16),-1)
        #cv2.putText(image, str('Raise left hand, parallel to shoulder.'), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        #顯示次數
        cv2.putText(image,'number of times',(15,12),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)#3:起始座標
        cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Camera', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
