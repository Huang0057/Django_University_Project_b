import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils#有關於任何需要繪製的東西
mp_pose = mp.solutions.pose

# 初始化计数器和标志位
counter = 0
stage = None

#11:LEFT_SHOULDER；13:LEFT_ELBOW手肘；15:LEFT_WRIST手腕
#計算角度
def calculate_angle(a,b,c):#分別為肩，手肘，手腕
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    #得到兩個向量之間的角度
    radains = np.arctan2(c[1]-b[1],c[0]-b[0])#弧度(y,x)
    angle = np.abs(radains*180.0/np.pi)#弧度->角度
    if angle > 180.0:
        angle = 360-angle#>180度代表手是垂下來的
    return angle

# 定义MediaPipe姿势识别模型
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:#想要偵測得更具體可以提高信度
    # 建立視窗，並讓視窗可以動態調整
    cv2.namedWindow('MediaPipe Pose', cv2.WINDOW_NORMAL)

    # 打开摄像头
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        # 读取帧
        success, image = cap.read()


        # mediapipe需要要RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False#設定是否可寫

        # 检测姿势
        results = pose.process(image)

        # opencv需要BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        # 提取關節點landmark
        try:
                landmarks = results.pose_landmarks.landmark
                #get coordinates# 取得左膝、左腳踝、左髖關節的坐標
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y] #25 # landmarks獲取座標(取左肩X值，取Y值)
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]#27
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]#23

                #calculate angle
                angle = calculate_angle(left_hip,left_knee, left_ankle)

                #visualize視覺化 angle
                #cv2.putText(image, str(angle), tuple(np.multiply(left_knee, [640, 480]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5, cv2.LINE_AA)#用中間點*頁面大小

                #counter:raise arm time
                if angle > 130:
                    stage = "down"
                if angle < 120 and stage == 'down':  # 希望做動作時是由down的狀態往up的狀態，不希望手直接舉高
                    stage = "up"
                    counter += 1
                    print(counter)
                    if counter == 10:
                        break
                # if counter == 5:
                #     cv2.putText(image, 'DONE!!', (320, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        except:
                pass  # 如果有錯誤不會影響整個循環



        #在左上角放置一個狀態框
        cv2.rectangle(image,(0,0),(170,73),(245,117,16),-1)#畫方形(pic,左上點,右下點,顏色,粗細(使用填滿功能))
        #cv2.rectangle(image,(277,0),(554,73),(245,117,16),-1)
        #cv2.putText(image, str('Raise left hand, parallel to shoulder.'), (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        #顯示次數
        cv2.putText(image,'number of times',(15,12),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)#3:起始座標
        cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        # # 顯示次數
        # cv2.putText(image, 'STAGE', (65, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)  # 3:起始座標
        # cv2.putText(image, stage, (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # 關節點可視化
        mp_drawing.draw_landmarks(image, results.pose_landmarks,mp_pose.POSE_CONNECTIONS)  # 分別可以印出後兩個參數試試，可以看到關節點座標與各關節點如何連接

        # 显示图像
        cv2.imshow('MediaPipe Pose', image)
        # 按下q键退出
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # 释放摄像头和窗口
    cap.release()
    cv2.destroyAllWindows()




