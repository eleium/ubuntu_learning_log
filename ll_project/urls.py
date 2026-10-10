from django.contrib import admin
from django.urls import path, include

"""
URL configuration for ll_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
📌 类比一下
两级路由就像“公司 → 部门”：

层级	对应	作用
公司前台	project/urls.py	看你要找哪个部门
部门	app/urls.py	看你要找部门里的哪个人
用户先到前台（project），前台说“你去 learning_logs 部门”，然后部门再匹配具体的人。

📌 为什么要分两级？
好处	说明
解耦	每个 app 管自己的路由，互不干扰
可复用	app 可以整个搬到别的项目里
清晰	project/urls.py 只看“有哪些 app”，不用管细节
命名空间	learning_logs:topics 能区分不同 app 的同名路由
📌 如果只有一个 app 呢？
也可以直接写在一个 urls.py 里，不用分两级。

但项目一大，多个 app 时，分两级是标准做法。

🎯 一句话总结
Django 的路由是两级：先看 project/urls.py，再用 include 把请求转给 app/urls.py，最后匹配到具体视图。
项目管“分发”，app 管“具体匹配”。
"""


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("learning_logs.urls")),
    path("accounts/", include("accounts.urls")),
]
