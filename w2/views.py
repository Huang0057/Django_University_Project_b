import json
import uuid
import csv
import codecs
from subprocess import call
from datetime import datetime, timedelta
from calendar import monthrange
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.db.models import Sum
from django.conf import settings
from .form import UserInfoForm, LoginForm, UserProfileForm
from .models import GameRecord, UserProfile, ArmMetrics, FootMetrics, LimbMetrics, HandMetrics, UserCheckIn

# Create your views here.


def calculate_total_coins(user):
    user_profile = get_object_or_404(UserProfile, user=user)

    user_uid = user_profile.USER_UID

    arm_total_coins = ArmMetrics.objects.filter(USER_UID=user_uid).aggregate(
        total_coins=Sum('TotalGetCoin')).get('total_coins', 0)
    foot_total_coins = FootMetrics.objects.filter(USER_UID=user_uid).aggregate(
        total_coins=Sum('TotalGetCoin')).get('total_coins', 0)
    limb_total_coins = LimbMetrics.objects.filter(USER_UID=user_uid).aggregate(
        total_coins=Sum('TotalGetCoin')).get('total_coins', 0)
    hand_total_coins = HandMetrics.objects.filter(USER_UID=user_uid).aggregate(
        total_coins=Sum('TotalGetCoin')).get('total_coins', 0)

    total_coins = arm_total_coins + foot_total_coins + \
        limb_total_coins + hand_total_coins

    return total_coins


def 登入畫面(request):
    return render(request, '登入畫面.html')


@login_required
def 首頁(request):
    username = request.user.username
    total_coins = calculate_total_coins(request.user)
    try:
        user_check_ins = UserCheckIn.objects.filter(
            user=request.user).order_by('-date')

        consecutive_days = 1
        today = datetime.today().date()
        for check_in in user_check_ins:
            if check_in.date == today - timedelta(days=consecutive_days):
                consecutive_days += 1
            else:
                break
    except UserCheckIn.DoesNotExist:
        consecutive_days = 1

    return render(request, '首頁.html', {'username': username, 'consecutive_days': consecutive_days, 'total_coins': total_coins})


def 遊戲選擇畫面(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲選擇畫面.html', {'total_coins': total_coins})


def 遊戲難度選擇上肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲難度選擇-上肢.html', {'total_coins': total_coins})


def 遊戲難度選擇下肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲難度選擇-下肢.html', {'total_coins': total_coins})


def 遊戲難度選擇四肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲難度選擇-四肢.html', {'total_coins': total_coins})


def 遊戲難度選擇手部(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲難度選擇-手部.html', {'total_coins': total_coins})


def 遊戲地圖一星上肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖一星-上肢.html', {'total_coins': total_coins})


def 遊戲地圖二星上肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖二星-上肢.html', {'total_coins': total_coins})


def 遊戲地圖三星上肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖三星-上肢.html', {'total_coins': total_coins})


def 遊戲地圖一星下肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖一星-下肢.html', {'total_coins': total_coins})


def 遊戲地圖二星下肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖二星-下肢.html', {'total_coins': total_coins})


def 遊戲地圖三星下肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖三星-下肢.html', {'total_coins': total_coins})


def 遊戲地圖一星四肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖一星-四肢.html', {'total_coins': total_coins})


def 遊戲地圖二星四肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖二星-四肢.html', {'total_coins': total_coins})


def 遊戲地圖三星四肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖三星-四肢.html', {'total_coins': total_coins})


def 遊戲地圖一星手部(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖一星-手部.html', {'total_coins': total_coins})


def 遊戲地圖二星手部(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖二星-手部.html', {'total_coins': total_coins})


def 遊戲地圖三星手部(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲地圖三星-手部.html', {'total_coins': total_coins})


@login_required
def 簽到(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '簽到.html', {'total_coins': total_coins})


def get_calendar_data(year, month, current_user):
    num_days = monthrange(year, month)[1]
    calendar_data = []

    for day in range(1, num_days + 1):
        date = datetime(year, month, day).date()
        user_check_in = UserCheckIn.objects.filter(
            user=current_user, date=date
        ).first()
        if user_check_in:
            signed_in = user_check_in.signed_in
        else:
            signed_in = False
        weekday = date.weekday()
        calendar_data.append(
            {'date': date, 'signed_in': signed_in, 'weekday': weekday}
        )

    return calendar_data


@login_required
def Checkin(request: HttpRequest) -> HttpResponse:
    try:
        total_coins = calculate_total_coins(request.user)
        current_user = request.user
        creation_date = current_user.date_joined.date()
        today = datetime.today()

        if request.method == 'POST':
            signed_date = today.date()  # 使用當下日期作為簽到日期

            try:
                user_check_in = UserCheckIn.objects.get(
                    user=current_user, date=signed_date
                )
                user_check_in.signed_in = True
                user_check_in.save()
            except UserCheckIn.DoesNotExist:
                user_check_in = UserCheckIn.objects.create(
                    user=current_user, date=signed_date, signed_in=True
                )

        year = today.year
        month = today.month
        calendar_data = get_calendar_data(year, month, current_user)
        first_day_weekday = range(calendar_data[0]['weekday']+1)
        years = range(
            current_user.date_joined.year, datetime.today().year + 1
        )
        months = range(1, 13)

        context = {
            'current_user': current_user,
            'calendar_data': calendar_data,
            'creation_date': creation_date,
            'first_day_weekday': first_day_weekday,
            'years': years,
            'months': months,
            'current_year': year,
            'current_month': month,
            'total_coins': total_coins
        }

        return render(request, '簽到.html', context)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def CheckinSearch(request):
    try:
        total_coins = calculate_total_coins(request.user)
        current_user = request.user
        creation_date = current_user.date_joined.date()
        today = datetime.today()

        if request.method == 'POST':
            year = int(request.POST.get('year', today.year))
            month = int(request.POST.get('month', today.month))

        calendar_data = get_calendar_data(year, month, current_user)
        first_day_weekday = range(calendar_data[0]['weekday']+1)
        first_weekday = calendar_data[0]['weekday']
        years = range(current_user.date_joined.year, today.year + 1)
        months = range(1, 13)

        context = {
            'current_user': current_user,
            'calendar_data': calendar_data,
            'creation_date': creation_date,
            'first_day_weekday': first_day_weekday,
            'first_weekday': first_weekday,
            'years': years,
            'months': months,
            'current_year': year,
            'current_month': month,
            'total_coins': total_coins
        }

        return render(request, '簽到.html', context)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def 商店(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '商店.html', {'total_coins': total_coins})


@login_required
def MetricsTable(request):
    current_user_profile = UserProfile.objects.get(user=request.user)

    total_coins = calculate_total_coins(request.user)

    arm_metrics = ArmMetrics.objects.filter(
        USER_UID=current_user_profile.USER_UID)
    foot_metrics = FootMetrics.objects.filter(
        USER_UID=current_user_profile.USER_UID)
    limb_metrics = LimbMetrics.objects.filter(
        USER_UID=current_user_profile.USER_UID)
    hand_metrics = HandMetrics.objects.filter(
        USER_UID=current_user_profile.USER_UID)

    context = {
        'arm_metrics_data': arm_metrics,
        'foot_metrics_data': foot_metrics,
        'limb_metrics_data': limb_metrics,
        'hand_metrics_data': hand_metrics,
        'total_coins': total_coins,
    }

    return render(request, '紀錄.html', context)


def ExportMetricsTableToCSV(request):
    current_user_profile = UserProfile.objects.get(user=request.user)

    arm_metrics_data = ArmMetrics.objects.filter(
        USER_UID=current_user_profile.USER_UID)
    foot_metrics_data = FootMetrics.objects.filter(
        USER_UID=current_user_profile.USER_UID)
    limb_metrics_data = LimbMetrics.objects.filter(
        USER_UID=current_user_profile.USER_UID)
    hand_metrics_data = HandMetrics.objects.filter(
        USER_UID=current_user_profile.USER_UID)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="metrics_data.csv"'

    response.write(codecs.BOM_UTF8)

    writer = csv.writer(response)
    writer.writerow(['運動部位', '最後遊玩關卡', '總遊玩時間(秒)', '總遊玩次數', '動作合格次數', '總獲得金幣'])

    for arm_metric in arm_metrics_data:
        writer.writerow(['上肢', arm_metric.LastStage, arm_metric.TotalPlayTime,
                        arm_metric.TotalPlayCount, arm_metric.PassCount, arm_metric.TotalGetCoin])

    for foot_metric in foot_metrics_data:
        writer.writerow(['下肢', foot_metric.LastStage, foot_metric.TotalPlayTime,
                        foot_metric.TotalPlayCount, foot_metric.PassCount, foot_metric.TotalGetCoin])

    for limb_metric in limb_metrics_data:
        writer.writerow(['四肢', limb_metric.LastStage, limb_metric.TotalPlayTime,
                        limb_metric.TotalPlayCount, limb_metric.PassCount, limb_metric.TotalGetCoin])

    for hand_metric in hand_metrics_data:
        writer.writerow(['手部', hand_metric.LastStage, hand_metric.TotalPlayTime,
                        hand_metric.TotalPlayCount, hand_metric.PassCount, hand_metric.TotalGetCoin])

    return response


@login_required
def ArmRecords(request):
    # 取得目前登入的使用者
    current_user = request.user
    total_coins = calculate_total_coins(request.user)
    try:

        # 根據目前登入使用者的使用者名稱取得相對應的 UserProfile
        user_profile = UserProfile.objects.get(user=current_user)
        user_uid = user_profile.USER_UID

        # 取得符合條件的遊戲紀錄（假設有與使用者相關的遊戲紀錄查詢）
        play_records = GameRecord.objects.filter(
            USER_UID=user_uid, PlayPart='arm').order_by('-PlayDate')

        records_per_page = 5

        paginator = Paginator(play_records, records_per_page)

        page_number = request.GET.get('page')
        try:
            play_records = paginator.page(page_number)
        except PageNotAnInteger:
            play_records = paginator.page(1)
        except EmptyPage:
            play_records = paginator.page(paginator.num_pages)

        return render(request, '紀錄上肢.html', {'play_records': play_records, 'total_coins': total_coins})

    except UserProfile.DoesNotExist:
        return JsonResponse({"status": "error", "message": "UserProfile does not exist."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def FootRecords(request):
    # 取得目前登入的使用者
    current_user = request.user
    total_coins = calculate_total_coins(request.user)

    try:
        # 根據目前登入使用者的使用者名稱取得相對應的 UserProfile
        user_profile = UserProfile.objects.get(user=current_user)
        user_uid = user_profile.USER_UID

        # 取得符合條件的遊戲紀錄（假設有與使用者相關的遊戲紀錄查詢）
        play_records = GameRecord.objects.filter(
            USER_UID=user_uid, PlayPart='foot')

        records_per_page = 5
        paginator = Paginator(play_records, records_per_page)

        page_number = request.GET.get('page')
        try:
            play_records = paginator.page(page_number)
        except PageNotAnInteger:
            play_records = paginator.page(1)
        except EmptyPage:
            play_records = paginator.page(paginator.num_pages)

        return render(request, '紀錄下肢.html',  {'play_records': play_records, 'total_coins': total_coins})

    except UserProfile.DoesNotExist:
        return JsonResponse({"status": "error", "message": "UserProfile does not exist."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def LimbRecords(request):
    # 取得目前登入的使用者
    current_user = request.user
    total_coins = calculate_total_coins(request.user)
    try:
        # 根據目前登入使用者的使用者名稱取得相對應的 UserProfile
        user_profile = UserProfile.objects.get(user=current_user)
        user_uid = user_profile.USER_UID

        # 取得符合條件的遊戲紀錄（假設有與使用者相關的遊戲紀錄查詢）
        play_records = GameRecord.objects.filter(
            USER_UID=user_uid, PlayPart='limb')

        records_per_page = 5
        paginator = Paginator(play_records, records_per_page)

        page_number = request.GET.get('page')
        try:
            play_records = paginator.page(page_number)
        except PageNotAnInteger:
            play_records = paginator.page(1)
        except EmptyPage:
            play_records = paginator.page(paginator.num_pages)

        return render(request, '紀錄四肢.html', {'play_records': play_records, 'total_coins': total_coins})

    except UserProfile.DoesNotExist:
        return JsonResponse({"status": "error", "message": "UserProfile does not exist."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required
def HandRecords(request):
    # 取得目前登入的使用者
    current_user = request.user
    total_coins = calculate_total_coins(request.user)
    try:
        # 根據目前登入使用者的使用者名稱取得相對應的 UserProfile
        user_profile = UserProfile.objects.get(user=current_user)
        user_uid = user_profile.USER_UID

        # 取得符合條件的遊戲紀錄（假設有與使用者相關的遊戲紀錄查詢）
        play_records = GameRecord.objects.filter(
            USER_UID=user_uid, PlayPart='hand')

        records_per_page = 5
        paginator = Paginator(play_records, records_per_page)

        page_number = request.GET.get('page')
        try:
            play_records = paginator.page(page_number)
        except PageNotAnInteger:
            play_records = paginator.page(1)
        except EmptyPage:
            play_records = paginator.page(paginator.num_pages)

        return render(request, '紀錄手部.html',  {'play_records': play_records, 'total_coins': total_coins})

    except UserProfile.DoesNotExist:
        return JsonResponse({"status": "error", "message": "UserProfile does not exist."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def ExportGameRecordsToCSV(request):
    if request.method == 'POST':

        current_user_profile = UserProfile.objects.get(user=request.user)
        user_uid = current_user_profile.USER_UID

        play_part = request.POST.get('play_part')

        if not user_uid or not play_part:
            return HttpResponse('Invalid parameters')

        game_records = GameRecord.objects.filter(
            USER_UID=user_uid, PlayPart=play_part)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{play_part}_game_records.csv"'

        response.write(codecs.BOM_UTF8)
        writer = csv.writer(response)
        writer.writerow(['日期', '關卡', '開始時間', '結束時間',
                        '持續時間', '鍛鍊次數', '獲得金幣'])

        for record in game_records:
            writer.writerow([
                record.PlayDate,
                record.PlayStage,
                record.StartTime,
                record.EndTime,
                record.DurationTime,
                record.ExerciseCount,
                record.AddCoin
            ])

        return response

    return HttpResponse('Invalid request')


@login_required
def 衣櫥(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '衣櫥.html', {'total_coins': total_coins})


def 上肢遊戲畫面1解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '上肢遊戲畫面1-解說.html', {'total_coins': total_coins})


def 上肢遊戲畫面2解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '上肢遊戲畫面2-解說.html', {'total_coins': total_coins})


def 上肢遊戲畫面3解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '上肢遊戲畫面3-解說.html', {'total_coins': total_coins})


def 上肢遊戲畫面4解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '上肢遊戲畫面4-解說.html', {'total_coins': total_coins})


def 上肢遊戲畫面5解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '上肢遊戲畫面5-解說.html', {'total_coins': total_coins})


def 上肢遊戲畫面6解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '上肢遊戲畫面6-解說.html', {'total_coins': total_coins})


def 上肢遊戲畫面7解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '上肢遊戲畫面7-解說.html', {'total_coins': total_coins})


def 上肢遊戲畫面8解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '上肢遊戲畫面8-解說.html', {'total_coins': total_coins})


def 上肢遊戲畫面9解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '上肢遊戲畫面9-解說.html', {'total_coins': total_coins})


def 下肢遊戲畫面1解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '下肢遊戲畫面1-解說.html', {'total_coins': total_coins})


def 下肢遊戲畫面2解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '下肢遊戲畫面2-解說.html', {'total_coins': total_coins})


def 下肢遊戲畫面3解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '下肢遊戲畫面3-解說.html', {'total_coins': total_coins})


def 下肢遊戲畫面4解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '下肢遊戲畫面4-解說.html', {'total_coins': total_coins})


def 下肢遊戲畫面5解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '下肢遊戲畫面5-解說.html', {'total_coins': total_coins})


def 下肢遊戲畫面6解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '下肢遊戲畫面6-解說.html', {'total_coins': total_coins})


def 下肢遊戲畫面7解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '下肢遊戲畫面7-解說.html', {'total_coins': total_coins})


def 下肢遊戲畫面8解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '下肢遊戲畫面8-解說.html', {'total_coins': total_coins})


def 下肢遊戲畫面9解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '下肢遊戲畫面9-解說.html', {'total_coins': total_coins})


def 四肢遊戲畫面1解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面1-解說.html', {'total_coins': total_coins})


def 四肢遊戲畫面2解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面2-解說.html', {'total_coins': total_coins})


def 四肢遊戲畫面3解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面3-解說.html', {'total_coins': total_coins})


def 四肢遊戲畫面4解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面4-解說.html', {'total_coins': total_coins})


def 四肢遊戲畫面5解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面5-解說.html', {'total_coins': total_coins})


def 四肢遊戲畫面6解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面6-解說.html', {'total_coins': total_coins})


def 四肢遊戲畫面7解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面7-解說.html', {'total_coins': total_coins})


def 四肢遊戲畫面8解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面8-解說.html', {'total_coins': total_coins})


def 四肢遊戲畫面9解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面9-解說.html', {'total_coins': total_coins})


def 獎勵關卡解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '獎勵關卡-解說.html', {'total_coins': total_coins})


def 下肢遊戲畫面解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '下肢遊戲畫面-解說.html', {'total_coins': total_coins})


def 四肢遊戲畫面解說1(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面-解說1.html', {'total_coins': total_coins})


def 四肢遊戲畫面解說2(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '四肢遊戲畫面-解說2.html', {'total_coins': total_coins})


def 手部遊戲畫面解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '手部遊戲畫面-解說.html', {'total_coins': total_coins})


def 手部遊戲畫面1解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '手部遊戲畫面1-解說.html', {'total_coins': total_coins})


def 手部遊戲畫面2解說(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '手部遊戲畫面2-解說.html', {'total_coins': total_coins})


def 遊戲畫面倒數上肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面倒數-上肢.html', {'total_coins': total_coins})


def 遊戲畫面倒數下肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面倒數-下肢.html', {'total_coins': total_coins})


def 遊戲畫面倒數四肢(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面倒數-四肢.html', {'total_coins': total_coins})


def 遊戲畫面倒數手部(request):
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面倒數-手部.html', {'total_coins': total_coins})


def 遊戲畫面上肢1(request):
    call(["python", "test03.py"])
    call(["python", "arm01_1.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-上肢1.html', {'total_coins': total_coins})


def 遊戲畫面上肢2(request):
    call(["python", "test03.py"])
    call(["python", "arm01_2.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-上肢2.html', {'total_coins': total_coins})


def 遊戲畫面上肢3(request):
    call(["python", "test03.py"])
    call(["python", "arm01_3.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-上肢3.html', {'total_coins': total_coins})


def 遊戲畫面上肢4(request):
    call(["python", "test03.py"])
    call(["python", "arm02_1.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-上肢4.html', {'total_coins': total_coins})


def 遊戲畫面上肢5(request):
    call(["python", "test03.py"])
    call(["python", "arm02_2.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-上肢5.html', {'total_coins': total_coins})


def 遊戲畫面上肢6(request):
    call(["python", "test03.py"])
    call(["python", "arm02_3.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-上肢6.html', {'total_coins': total_coins})


def 遊戲畫面上肢7(request):
    call(["python", "test03.py"])
    call(["python", "arm03_1.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-上肢7.html', {'total_coins': total_coins})


def 遊戲畫面上肢8(request):
    call(["python", "test03.py"])
    call(["python", "arm03_2.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-上肢8.html', {'total_coins': total_coins})


def 遊戲畫面上肢9(request):
    call(["python", "test03.py"])
    call(["python", "arm03_3.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-上肢9.html', {'total_coins': total_coins})


def 遊戲畫面下肢1(request):
    call(["python", "test03.py"])
    call(["python", "leg01_1.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-下肢1.html', {'total_coins': total_coins})


def 遊戲畫面下肢2(request):
    call(["python", "test03.py"])
    call(["python", "leg01_2.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-下肢2.html', {'total_coins': total_coins})


def 遊戲畫面下肢3(request):
    call(["python", "test03.py"])
    call(["python", "leg01_3.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-下肢3.html', {'total_coins': total_coins})


def 遊戲畫面下肢4(request):
    call(["python", "test03.py"])
    call(["python", "leg02_1.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-下肢4.html', {'total_coins': total_coins})


def 遊戲畫面下肢5(request):
    call(["python", "test03.py"])
    call(["python", "leg02_2.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-下肢5.html', {'total_coins': total_coins})


def 遊戲畫面下肢6(request):
    call(["python", "test03.py"])
    call(["python", "leg02_3.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-下肢6.html', {'total_coins': total_coins})


def 遊戲畫面下肢7(request):
    call(["python", "test03.py"])
    call(["python", "leg03_1.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-下肢7.html', {'total_coins': total_coins})


def 遊戲畫面下肢8(request):
    call(["python", "test03.py"])
    call(["python", "leg03_2.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-下肢8.html', {'total_coins': total_coins})


def 遊戲畫面下肢9(request):
    call(["python", "test03.py"])
    call(["python", "leg03_3.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-下肢9.html', {'total_coins': total_coins})


def 遊戲畫面四肢(request):
    call(["python", "test03.py"])
    call(["python", "arm01_1.py"])
    call(["python", "leg01_1.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-四肢.html', {'total_coins': total_coins})


def 遊戲畫面四肢1(request):
    call(["python", "test03.py"])
    call(["python", "arm02_1.py"])
    call(["python", "leg02_1.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-四肢1.html', {'total_coins': total_coins})


def 遊戲畫面四肢2(request):
    call(["python", "test03.py"])
    call(["python", "arm03_1.py"])
    call(["python", "leg03_1.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-四肢2.html', {'total_coins': total_coins})


def 遊戲畫面四肢3(request):
    call(["python", "test03.py"])
    call(["python", "arm01_2.py"])
    call(["python", "leg01_2.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-四肢3.html', {'total_coins': total_coins})


def 遊戲畫面四肢4(request):
    call(["python", "test03.py"])
    call(["python", "arm02_2.py"])
    call(["python", "leg02_2.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-四肢4.html', {'total_coins': total_coins})


def 遊戲畫面四肢5(request):
    call(["python", "test03.py"])
    call(["python", "arm03_2.py"])
    call(["python", "leg03_2.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-四肢5.html', {'total_coins': total_coins})


def 遊戲畫面四肢6(request):
    call(["python", "test03.py"])
    call(["python", "arm01_3.py"])
    call(["python", "leg01_3.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-四肢6.html', {'total_coins': total_coins})


def 遊戲畫面四肢7(request):
    call(["python", "test03.py"])
    call(["python", "arm02_3.py"])
    call(["python", "leg02_3.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-四肢7.html', {'total_coins': total_coins})


def 遊戲畫面四肢8(request):
    call(["python", "test03.py"])
    call(["python", "arm03_3.py"])
    call(["python", "leg03_3.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-四肢8.html', {'total_coins': total_coins})


def 遊戲畫面獎勵關卡(request):
    call(["python", "test03.py"])
    call(["python", "GiftboxAutoMove.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-獎勵關卡.html', {'total_coins': total_coins})


def 遊戲畫面手部1(request):
    call(["python", "test03.py"])
    call(["python", "hand01.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-手部1.html', {'total_coins': total_coins})


def 遊戲畫面手部2(request):
    call(["python", "test03.py"])
    call(["python", "hand02.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-手部2.html', {'total_coins': total_coins})


def 遊戲畫面手部3(request):
    call(["python", "test03.py"])
    call(["python", "hand01.py"])
    call(["python", "hand02.py"])
    total_coins = calculate_total_coins(request.user)
    return render(request, '遊戲畫面-手部3.html', {'total_coins': total_coins})


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


def update_user_profile(request):
    total_coins = calculate_total_coins(request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            # redirect to a success page or back to the form
            return redirect('some-success-url')
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'path_to_template.html', {'form': form}, {'total_coins': total_coins})


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
            metrics_instance.TotalPlayCount += 1
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
