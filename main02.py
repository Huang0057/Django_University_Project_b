import subprocess
import speech_recognition as sr
import cv2
import numpy as np


def start_arm01():
    return subprocess.Popen(["python", "arm01.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)



def voice_command():
    recognizer = sr.Recognizer()

    p1 = None
    running = False


    while True:


        with sr.Microphone() as source:
            print("請說話...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="zh-TW")
            print("辨識結果：", text)

            if "開始" in text and not running:
                print("開始手部運動第一關執行...")
                p1 = start_arm01()
                running = True


            elif "重新開始" in text:
                print("重新執行手部運動程式...")
                if p1:
                    p1.terminate()
                p1 = start_arm01()
                running = True


            elif "結束" in text:
                print("結束程式執行...")
                # 結束所有腳本的執行
                try:
                    if p1:
                        p1.terminate()
                        print(p1.communicate()[0])
                except AttributeError:
                    pass
                break  # 跳出迴圈，結束程式
        except sr.UnknownValueError:
            print("無法辨識語音")
        except sr.RequestError:
            print("無法連線至 Google 語音辨識服務")

if __name__ == "__main__":
    voice_command()
