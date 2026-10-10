from django.urls import path
from . import views

app_name = "learning_logs"
urlpatterns = [
    path("", views.index, name="index"),
    
    #添加主题访问的页面
    path("topics/", views.topics, name="topics"),
    
    # 添加访问特定主题（编号id）的页面url
    path("topics/<int:topic_id>/", views.topic, name="topic"),
    
    #用于添加新主题的网页
    path('new_topic/',views.new_topic,name='new_topic'),
    
    #用于添加新的条目的页面：
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
    
    #添加 用于用户编辑已有的条目的页面：
    path('edit_entry/<int:entry_id>/',views.edit_entry,name='edit_entry'),
    
    #添加用于删除条目的页面
    path('topics/<int:topic_id>/del_topic/',views.del_topic,name='del_topic'),
]
