from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from subprocess import Popen, PIPE
from subprocess import call
import subprocess
import cv2
import numpy as np
import threading
import time
import base64
from .form import UserInfoForm
from .form import LoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def 登入畫面(request):
    return render(request, '登入畫面.html')


def 首頁(request):
    return render(request, '首頁.html')


def 遊戲選擇畫面(request):
    return render(request, '遊戲選擇畫面.html')


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
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            print(form.cleaned_data['password'])
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
