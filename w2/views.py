from django.shortcuts import render, redirect
from subprocess import call
import numpy as np
from .form import UserInfoForm
from .form import LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import GameRecord, UserProfile
from datetime import datetime
import uuid
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.


def 登入畫面(request):
    return render(request, '登入畫面.html')


def 首頁(request):
    return render(request, '首頁.html')


def 遊戲選擇畫面(request):
    return render(request, '遊戲選擇畫面.html')


def 遊戲難度選擇上肢(request):
    return render(request, '遊戲難度選擇-上肢.html')


def 遊戲難度選擇下肢(request):
    return render(request, '遊戲難度選擇-下肢.html')


def 遊戲難度選擇四肢(request):
    return render(request, '遊戲難度選擇-四肢.html')


def 遊戲難度選擇手部(request):
    return render(request, '遊戲難度選擇-手部.html')


def 簽到(request):
    return render(request, '簽到.html')


def 商店(request):
    return render(request, '商店.html')


def 紀錄(request):
    return render(request, '紀錄.html')


def 紀錄上肢(request):
    return render(request, '紀錄上肢.html')


def 紀錄下肢(request):
    return render(request, '紀錄下肢.html')


def 紀錄四肢(request):
    return render(request, '紀錄四肢.html')


def 紀錄手部(request):
    return render(request, '紀錄手部.html')


def 衣櫥(request):
    return render(request, '衣櫥.html')


def 上肢遊戲畫面解說(request):
    return render(request, '上肢遊戲畫面-解說.html')


def 下肢遊戲畫面解說(request):
    return render(request, '下肢遊戲畫面-解說.html')


def 四肢遊戲畫面解說1(request):
    return render(request, '四肢遊戲畫面-解說1.html')


def 四肢遊戲畫面解說2(request):
    return render(request, '四肢遊戲畫面-解說2.html')


def 手部遊戲畫面解說(request):
    return render(request, '手部遊戲畫面-解說.html')


def 遊戲畫面倒數上肢(request):
    return render(request, '遊戲畫面倒數-上肢.html')


def 遊戲畫面倒數下肢(request):
    return render(request, '遊戲畫面倒數-下肢.html')


def 遊戲畫面倒數四肢(request):
    return render(request, '遊戲畫面倒數-四肢.html')


def 遊戲畫面倒數手部(request):
    return render(request, '遊戲畫面倒數-手部.html')


def 遊戲畫面上肢(request):
    call(["python", "test03.py"])
    call(["python", "arm01.py"])
    return render(request, '遊戲畫面-上肢.html')


def 遊戲畫面下肢(request):
    call(["python", "test03.py"])
    call(["python", "leg01.py"])
    return render(request, '遊戲畫面-下肢.html')


def 遊戲畫面四肢(request):
    call(["python", "test03.py"])
    call(["python", "arm01.py"])
    call(["python", "leg01.py"])
    return render(request, '遊戲畫面-四肢.html')


def 遊戲畫面手部(request):
    call(["python", "test03.py"])
    call(["python", "hand01.py"])
    return render(request, '遊戲畫面-手部.html')


def signup(request):

    form = UserInfoForm()

    if request.method == "POST":
        form = UserInfoForm(request.POST)
        if form.is_valid():
            # 創建用戶，設置密碼並保存
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            print(form.cleaned_data['password'])
            # 創建 UserProfile 實例，並生成唯一的 UID
            user_profile = UserProfile(user=user)
            user_profile.Arm_UID = str(uuid.uuid4())[:20]
            user_profile.Foot_UID = str(uuid.uuid4())[:20]
            user_profile.Limb_UID = str(uuid.uuid4())[:20]
            user_profile.Hand_UID = str(uuid.uuid4())[:20]
            user_profile.save()

            return redirect('/signin')

    context = {
        'form': form
    }

    return render(request, 'Signup.html', context)

# 登入


def signin(request):
    form = LoginForm()

    if request.method == "POST":

        if form.is_valid() == False:

            form = LoginForm(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            print(username, password)
            user = authenticate(request, username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect('/home')
            else:
                # 如果登入失敗，則丟出錯誤訊息

                form.add_error(None, "帳號不存在或是密碼錯誤，請再試一次")

            # error_message = "帳號不存在或是密碼錯誤，請再試一次"

            # return render(request, '登入畫面.html', {'error_message': error_message})

    context = {
        'form': form
    }

    return render(request, '登入畫面.html', context)


@csrf_exempt
def gamerecord(request):
    if request.method == 'POST':

        counter = request.POST.get('counter')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        duration_time = request.POST.get('duration_time')
        playpart = request.POST.get('playpart')
        playstage = request.POST.get('playstage')

        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")

        duration = end_time - start_time
        duration_minutes = int(duration.total_seconds() // 60)
        duration_seconds = int(duration.total_seconds() % 60)
        duration_time = f"{duration_minutes:02}:{duration_seconds:02}"

        user_profile = request.user.userprofile

        game_record = GameRecord.objects.create(
            USER_UID=user_profile,
            PlayDate=datetime.now().date(),  # 以当前日期作为PlayDate
            PlayPart=playpart,
            UID=str(uuid.uuid4())[:20],
            PlayStage=playstage,
            StartTime=start_time.time(),
            EndTime=end_time.time(),
            DurationTime=duration_time,
            AddCoin=5,
            ExerciseCount=counter,
        )

        # 执行其他操作，例如增加金币或计算锻炼次数
        # ...

        return render(request, '遊戲畫面-上肢.html')

    return HttpResponse("Method not allowed", status=405)
