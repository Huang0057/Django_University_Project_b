import json
import uuid
from subprocess import call
from datetime import datetime, timedelta
from calendar import monthrange
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpRequest, HttpResponse
from .form import UserInfoForm, LoginForm, UserProfileForm
from .models import GameRecord, UserProfile, ArmMetrics, FootMetrics, LimbMetrics, HandMetrics, UserCheckIn

# Create your views here.


def 登入畫面(request):
    return render(request, '登入畫面.html')


@login_required
def 首頁(request):
    return render(request, '首頁.html')


@login_required
def 遊戲選擇畫面(request):
    return render(request, '遊戲選擇畫面.html')


@login_required
def 遊戲難度選擇上肢(request):
    return render(request, '遊戲難度選擇-上肢.html')


@login_required
def 遊戲難度選擇下肢(request):
    return render(request, '遊戲難度選擇-下肢.html')


@login_required
def 遊戲難度選擇四肢(request):
    return render(request, '遊戲難度選擇-四肢.html')


@login_required
def 遊戲難度選擇手部(request):
    return render(request, '遊戲難度選擇-手部.html')


@login_required
def 簽到(request):
    return render(request, '簽到.html')


def get_calendar_data(year, month, current_user):
    num_days = monthrange(year, month)[1]
    calendar_data = []

    for day in range(1, num_days + 1):
        date = datetime(year, month, day).date()
        user_check_in = UserCheckIn.objects.filter(
            user=current_user, date=date).first()
        if user_check_in:
            signed_in = user_check_in.signed_in
        else:
            signed_in = False
        weekday = date.weekday()  # 获取日期的星期几信息
        calendar_data.append(
            {'date': date, 'signed_in': signed_in, 'weekday': weekday})

    return calendar_data


@login_required
def Checkin(request: HttpRequest) -> HttpResponse:
    try:
        current_user = request.user
        creation_date = current_user.date_joined.date()

        today = datetime.today()
        year = today.year
        month = today.month

        try:
            user_check_in = UserCheckIn.objects.get(
                user=current_user, date=today)
        except UserCheckIn.DoesNotExist:
            user_check_in = UserCheckIn.objects.create(
                user=current_user, date=today, signed_in=False)
        if request.method == 'POST':
            signed_date = request.POST.get('signed_date')

            try:
                user_check_in = UserCheckIn.objects.get(
                    user=current_user, date=signed_date)
                user_check_in.signed_in = True
                user_check_in.save()
            except UserCheckIn.DoesNotExist:
                user_check_in = UserCheckIn.objects.create(
                    user=current_user, date=signed_date, signed_in=True)

        calendar_data = get_calendar_data(year, month, current_user)

        first_day_weekday = range(calendar_data[0]['weekday']+1)

        context = {
            'current_user': current_user,
            'calendar_data': calendar_data,
            'creation_date': creation_date,
            'first_day_weekday': first_day_weekday,
        }
        print(calendar_data)
        return render(request, '簽到.html', context)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def 商店(request):
    return render(request, '商店.html')


@login_required
def MetricsTable(request):
    # 获取 ArmMetrics 中的数据
    arm_metrics_data = ArmMetrics.objects.all()
    foot_metrics_data = FootMetrics.objects.all()
    limb_metrics_data = LimbMetrics.objects.all()
    hand_metrics_data = HandMetrics.objects.all()

    return render(request, '紀錄.html', {
        'arm_metrics_data': arm_metrics_data,
        'foot_metrics_data': foot_metrics_data,
        'limb_metrics_data': limb_metrics_data,
        'hand_metrics_data': hand_metrics_data,
    })


@login_required
def ArmRecords(request):
    # 取得目前登入的使用者
    current_user = request.user

    try:
        # 根據目前登入使用者的使用者名稱取得相對應的 UserProfile
        user_profile = UserProfile.objects.get(user=current_user)
        user_uid = user_profile.USER_UID

        # 取得符合條件的遊戲紀錄（假設有與使用者相關的遊戲紀錄查詢）
        play_records = GameRecord.objects.filter(
            USER_UID=user_uid, PlayPart='arm')

        records_per_page = 5
        paginator = Paginator(play_records, records_per_page)

        page_number = request.GET.get('page')
        try:
            play_records = paginator.page(page_number)
        except PageNotAnInteger:
            play_records = paginator.page(1)
        except EmptyPage:
            play_records = paginator.page(paginator.num_pages)

        return render(request, '紀錄上肢.html', {'play_records': play_records})

    except UserProfile.DoesNotExist:
        return JsonResponse({"status": "error", "message": "UserProfile does not exist."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def 紀錄下肢(request):
    return render(request, '紀錄下肢.html')


@login_required
def 紀錄四肢(request):
    return render(request, '紀錄四肢.html')


@login_required
def 紀錄手部(request):
    return render(request, '紀錄手部.html')


@login_required
def 衣櫥(request):
    return render(request, '衣櫥.html')


@login_required
def 上肢遊戲畫面解說(request):
    return render(request, '上肢遊戲畫面-解說.html')


@login_required
def 下肢遊戲畫面解說(request):
    return render(request, '下肢遊戲畫面-解說.html')


@login_required
def 四肢遊戲畫面解說1(request):
    return render(request, '四肢遊戲畫面-解說1.html')


@login_required
def 四肢遊戲畫面解說2(request):
    return render(request, '四肢遊戲畫面-解說2.html')


@login_required
def 手部遊戲畫面解說(request):
    return render(request, '手部遊戲畫面-解說.html')


@login_required
def 遊戲畫面倒數上肢(request):
    return render(request, '遊戲畫面倒數-上肢.html')


@login_required
def 遊戲畫面倒數下肢(request):
    return render(request, '遊戲畫面倒數-下肢.html')


@login_required
def 遊戲畫面倒數四肢(request):
    return render(request, '遊戲畫面倒數-四肢.html')


@login_required
def 遊戲畫面倒數手部(request):
    return render(request, '遊戲畫面倒數-手部.html')


@login_required
def 遊戲畫面上肢(request):
    call(["python", "test03.py"])
    call(["python", "arm01.py"])
    return render(request, '遊戲畫面-上肢.html')


@login_required
def 遊戲畫面下肢(request):
    call(["python", "test03.py"])
    call(["python", "leg01.py"])
    return render(request, '遊戲畫面-下肢.html')


@login_required
def 遊戲畫面四肢(request):
    call(["python", "test03.py"])
    call(["python", "arm01.py"])
    call(["python", "leg01.py"])
    return render(request, '遊戲畫面-四肢.html')


@login_required
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


def arm_play_records(request):
    user = request.user
    arm_play_records = GameRecord.objects.filter(USER_UID=user, PlayPart='ARM')
    return render(request, '紀錄上肢.html', {'play_records': arm_play_records})


def update_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            # redirect to a success page or back to the form
            return redirect('some-success-url')
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'path_to_template.html', {'form': form})


def add_gamerecord(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # 資料處理
            user_uid = data.get('USER_UID')
            play_date = data.get('PlayDate')
            play_part = data.get('PlayPart')
            uid = data.get('UID')
            play_stage = data.get('PlayStage')
            start_time = data.get('StartTime')
            end_time = data.get('EndTime')
            duration_str = data.get('DurationTime')
            add_coin = data.get('AddCoin')
            exercise_count = data.get('ExerciseCount')
            # 資料處理
            # Convert the duration string to a timedelta object
            hours, minutes, seconds = map(int, duration_str.split(':'))
            duration_time = timedelta(
                hours=hours, minutes=minutes, seconds=seconds)

            game_record = GameRecord(
                USER_UID=user_uid,
                PlayDate=play_date,
                PlayPart=play_part,
                UID=uid,
                PlayStage=play_stage,
                StartTime=start_time,
                EndTime=end_time,
                DurationTime=duration_time,
                AddCoin=add_coin,
                ExerciseCount=exercise_count,
            )

            game_record.save()
            print("GameRecord added successfully.")

            return redirect(update_metrics, user_uid=user_uid, play_date=play_date, play_part=play_part)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Failed to decode JSON."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid method."})


def update_arm_metrics(request, user_uid, play_date):
    try:
        latest_game_record = GameRecord.objects.filter(
            USER_UID=user_uid, PlayPart='arm', PlayDate=play_date).order_by('-StartTime').first()

        user_profile = UserProfile.objects.get(
            USER_UID=latest_game_record.USER_UID)
        arm_uid = user_profile.Arm_UID

        arm_metrics = ArmMetrics.objects.get(
            USER_UID=user_uid, Arm_UID=arm_uid)

        # 取得相關遊戲紀錄的資料
        play_stage = latest_game_record.PlayStage
        duration_time = latest_game_record.DurationTime
        exercise_count = latest_game_record.ExerciseCount
        add_coin = latest_game_record.AddCoin
        uid = latest_game_record.UID

        duration_seconds = duration_time.total_seconds()

        # 處理更新 ArmMetrics 資料表
        arm_metrics.LastStage = play_stage
        arm_metrics.TotalPlayTime += duration_seconds
        arm_metrics.TotalPlayCount += exercise_count
        arm_metrics.PassCount += exercise_count
        arm_metrics.TotalGetCoin += add_coin
        arm_metrics.LastRecordId = uid
        arm_metrics.save()

        return JsonResponse({"status": "success", "message": "ArmMetrics updated successfully."})

    except UserProfile.DoesNotExist:
        return JsonResponse({"status": "error", "message": "UserProfile does not exist."})
    except ArmMetrics.DoesNotExist:
        return JsonResponse({"status": "error", "message": "ArmMetrics does not exist."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


table_mapping = {
    'arm': ArmMetrics,
    'foot': FootMetrics,
    'limb': LimbMetrics,
    'hand': HandMetrics,
}


def update_metrics(request, user_uid, play_date, play_part):
    try:
        # 確認 play_part 是否存在於映射字典中
        if play_part in table_mapping:
            MetricsModel = table_mapping[play_part]

            # 根據 play_part 選擇要操作的資料表
            latest_game_record = GameRecord.objects.filter(
                USER_UID=user_uid, PlayPart=play_part, PlayDate=play_date).order_by('-StartTime').first()

            user_profile = UserProfile.objects.get(
                USER_UID=latest_game_record.USER_UID)

            metrics_instance = MetricsModel.objects.get(
                USER_UID=user_uid, **{f"{play_part.title()}_UID": user_profile.__dict__[f"{play_part.capitalize()}_UID"]})

            duration_time = latest_game_record.DurationTime
            exercise_count = latest_game_record.ExerciseCount
            add_coin = latest_game_record.AddCoin

            duration_seconds = duration_time.total_seconds()

            metrics_instance.LastStage = latest_game_record.PlayStage
            metrics_instance.TotalPlayTime += duration_seconds
            metrics_instance.TotalPlayCount += exercise_count
            metrics_instance.PassCount += exercise_count
            metrics_instance.TotalGetCoin += add_coin
            metrics_instance.LastRecordId = latest_game_record.UID
            metrics_instance.save()

            return JsonResponse({"status": "success", "message": f"{play_part.capitalize()}Metrics updated successfully."})

        else:
            return JsonResponse({"status": "error", "message": "Invalid play part."})

    except UserProfile.DoesNotExist:
        return JsonResponse({"status": "error", "message": "UserProfile does not exist."})
    except MetricsModel.DoesNotExist:
        return JsonResponse({"status": "error", "message": f"{play_part.capitalize()}Metrics does not exist."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
