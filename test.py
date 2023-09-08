import subprocess
import speech_recognition as sr

def voice_command():
    recognizer = sr.Recognizer()

    p1 = None
    p2 = None
    p3 = None
    p4 = None
    p5 = None
    p6 = None
    p7 = None
    p8 = None
    p9 = None

    while True:
        with sr.Microphone() as source:
            print("請說話...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="zh-TW")
            print("辨識結果：", text)

            if "開始手的運動第一關" in text:
                print("開始手部運動第一關執行...")
                p1 = subprocess.Popen(["python", "arm01.py"], stdout=subprocess.PIPE, text=True)  # 開啟 arm01.py 腳本


            elif "開始手部運動第二關" in text:

                print("開始手部運動第二關執行...")
                p2 = subprocess.Popen(["python", "arm02.py"], stdout=subprocess.PIPE, text=True)




            elif "開始手部運動第三關" in text:
                print("開始手部運動第三關執行...")
                p3 = subprocess.Popen(["python", "arm03.py"], stdout=subprocess.PIPE, text=True)


            elif "開始手部運動第四關" in text:

                print("開始手部運動第四關執行...")

                p4 = subprocess.Popen(["python", "arm04.py"], stdout=subprocess.PIPE, text=True)


            elif "開始手掌運動第一關" in text:

                print("開始手掌運動第一關執行...")

                p5 = subprocess.Popen(["python", "hand01.py"], stdout=subprocess.PIPE, text=True)


            elif "開始手掌運動第二關" in text:

                print("開始手掌運動第二關執行...")

                p6 = subprocess.Popen(["python", "hand02.py"], stdout=subprocess.PIPE, text=True)


            elif "開始腳部運動第一關" in text:

                print("開始腳部運動第一關執行...")

                p7 =subprocess.Popen(["python", "leg01.py"], stdout=subprocess.PIPE, text=True)


            elif "開始腳部運動第二關" in text:

                print("開始腳部運動第二關執行...")

                p8 = subprocess.Popen(["python", "leg02.py"], stdout=subprocess.PIPE, text=True)


            elif "開始腳部運動第三關" in text:

                print("開始腳部運動第三關執行...")

                p9 = subprocess.Popen(["python", "leg03.py"], stdout=subprocess.PIPE, text=True)



            elif "結束" in text:
                print("結束程式執行...")
                # 結束所有腳本的執行
                try:
                    p1.terminate()
                    print(p1.communicate()[0])
                except AttributeError:
                    pass
                try:
                    p2.terminate()
                    print(p2.communicate()[0])
                except AttributeError:
                    pass
                try:
                    p3.terminate()
                    print(p3.communicate()[0])
                except AttributeError:
                    pass
                try:
                    p4.terminate()
                    print(p4.communicate()[0])
                except AttributeError:
                    pass
                try:
                    p5.terminate()
                    print(p5.communicate()[0])
                except AttributeError:
                    pass
                try:
                    p6.terminate()
                    print(p6.communicate()[0])
                except AttributeError:
                    pass
                try:
                    p7.terminate()
                    print(p7.communicate()[0])
                except AttributeError:
                    pass
                try:
                    p8.terminate()
                    print(p8.communicate()[0])
                except AttributeError:
                    pass
                try:
                    p9.terminate()
                    print(p9.communicate()[0])
                except AttributeError:
                    pass
                break  # 跳出迴圈，結束程式

        except sr.UnknownValueError:
            print("無法辨識語音")
        except sr.RequestError:
            print("無法連線至 Google 語音辨識服務")

if __name__ == "__main__":
    voice_command()
