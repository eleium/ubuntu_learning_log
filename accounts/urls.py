from django.urls import path, include
from . import views

app_name = "accounts"

# django 默认的身份验证url，包含具名 的url模式,如 'login'和'logout','password_change'和'password_reset':
# 对应的url:  http://localhost:8000/login/  (logout/password_change/password_reset/)


urlpatterns = [
    # 使用django默认的url身份验证（Django 官方提供的、用于“用户认证”的 URL 配置
    # contrib : contributed 的缩写，贡献的、提供的,  authentication，认证)
    path("", include("django.contrib.auth.urls")),
    # 既然已经有对应的url: http://localhost:8000/login，并且是具名的login,相当于name='login',就可以编辑视图函数。
    # 但是，这个login()，由django提供，不需要自己编写。
    # 自己只需要编写模板 login.html

    path('register/',views.register,name='register')
]
