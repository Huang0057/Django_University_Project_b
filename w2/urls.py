from django.urls import path

from . import views

urlpatterns = [
    path('', views.signin, name="登入畫面"),
    path('signin', views.signin, name="登入畫面"),
    path('首頁', views.首頁, name="首頁"),
    path('遊戲選擇畫面', views.遊戲選擇畫面, name="遊戲選擇畫面"),
    path('簽到', views.簽到, name="簽到"),
    path('商店', views.商店, name="商店"),
    path('衣櫥', views.衣櫥, name="衣櫥"),
    path('紀錄', views.紀錄, name="紀錄"),
    path('上肢遊戲畫面-解說', views.上肢遊戲畫面解說, name="上肢遊戲畫面-解說"),
    path('遊戲畫面倒數-上肢', views.遊戲畫面倒數上肢, name="遊戲畫面倒數-上肢"),
    path('遊戲畫面-上肢/', views.遊戲畫面上肢, name="遊戲畫面-上肢"),
    path('signup', views.signup, name="signup"),
    path('home', views.首頁, name="首頁"),
]
