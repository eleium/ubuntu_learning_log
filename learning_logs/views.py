from django.contrib.auth.decorators import login_required

# decorator: 装饰器的意思。直译：油漆匠，裱糊匠
from django.db import models
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import EntryForm, TopicForm
from .models import Entry, Topic

# Create your views here.


def index(request):
    return render(request, "learning_logs/index.html")


"""
 此处装饰器：login_required 的作用： 登录的用户可以查看主题列表(执行： topics())。
 未登录用户访问 topics 视图s时， @login_required 检查发现 request.user.is_authenticated 是 False
 把用户重定向到 settings.py 中设定LOGIN_URL 指定的地址，也就是 accounts app 里 name='login' 的那个 URL
 跳转时还会带上 ?next=/topics/，记住用户原本想去哪
 """


#  这个网站中，只有主页和注册页，可以让用户无需登录就可以浏览和注册，其他页面，都不给未登录的用户开放。
# 所以，index主页的视图函数和django 内置的注册视图函数不需要加上@login_required 装饰器，其他的都加上。


@login_required
def topics(request):
    # 显示所有的主题：
    # topics = Topic.objects.order_by("date_added")

    # 只允许登录用户访问自己的所属的主题：
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    # 获取所有 Topic，按 date_added 升序排列（最早创建的在前）。
    # 返回类型：查询集（QuerySet），不是单个实例。
    context = {"topics": topics}
    # context 把数据形成字典，传递给template处理
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    # 显示特定id主题的所有条目：
    topic = Topic.objects.get(id=topic_id)

    # 确认请求的主题属于当前登录的用户：
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by("-date_added")
    # 返回的是一个查询集（QuerySet），里面装的是 所有Entry 对象，按创建时间从新到旧排列。
    # 这些对象里包含 text、date_added 等字段，不是 URL。

    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """添加新的主题"""
    if request.method != "POST":
        # 未提交数据，就创建一个新的表单：
        form = TopicForm()

    else:
        # Post 提交的数据，就对提交的数据进行处理：
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # 创建新的主题new_topic,必须知道这个topic属于谁，也就是learning_log_topic.user不能是null空的。
            # 将new_topic手动指定字段，也就是new_topic的id是request.user
            # form.save()
            # 原来没有用户，是superuser,可以直接form.save()。有了登录用户，就要指出是哪一个用户的哪一个主题
            return redirect("learning_logs:topics")
    # 显示空表单，或指出表单数据无效：
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    # 形参多了一个topic_id,因为要针对特定的主题来增加条目
    """在特定的主题中新增条目："""
    topic = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        # 没有提交数据，就创建一个新的表单：
        form = EntryForm()
    else:
        # post提交了数据，就对数据进行处理：
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            # form.save(commit=False) 是“先造对象，暂不入库”，让你有机会手动补充表单里没有的字段（如 topic），
            # 填完再调用 .save() 正式保存。
            # form.save(commit=False) 创建 Entry 对象，但 topic 字段为空

            new_entry.topic = topic
            # new_entry.topic = topic 就是“把 topic 这个对象，挂到 new_entry 的 topic 外键上”。
            # Django 保存时会自动把 topic.id 写入数据库的 topic_id 列。
            # 所以 new_entry.topic 是对象，new_entry.topic_id 是整数，两者指向同一条数据。
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)
            # 用redirect()函数，参数不用加上url.如果是模板.html,需要加上url

    # 显示空表单或者指出表单数据无效：
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    # 编辑既有的条目：
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # entry.topic 确实是一个属性，不是方法。 它是 Django 在模型层自动生成的外键访问器。
    # 在 Entry 里写了 topic = models.ForeignKey(Topic, ...)，Django 就为这条外键自动生成两个属性：

    # 属性	                    位置	                  作用
    # entry.topic	            在 Entry 实例上	          正向查询：从条目找到它所属的主题
    # topic.entry_set	        在 Topic 实例上	          反向查询：从主题找到它下面的所有条目
    # 所以 entry.topic 能用，是因为你在 Entry 模型里定义了 topic 这个外键字段，不是凭空冒出来的。
    # 方向	写法	含义
    # 正向        （从 Entry 到 Topic）	        entry.topic	这个条目属于哪个主题
    # 反向        （从 Topic 到 Entry）	        topic.entry_set.all()	这个主题下有哪些条目
    # 之前的 topic.entry_set.order_by(...) 用的是反向，现在 entry.topic 用的是正向。

    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        # 初次请求，使用当前的条目填充表单：
        form = EntryForm(instance=entry)

    else:
        # post 提交的数据，对数据进行处理：
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)
            #  URL 参数	entry_id
            # 视图签名	def edit_entry(request, entry_id):
            # 重定向	redirect('learning_logs:topic', topic_id=entry.topic.id)
            # 视图只有 entry_id，没有 topic_id。 要拿到主题 ID，必须通过 entry.topic.id。

            # entry = Entry.objects.get(id=entry_id)   # 先查到条目
            # topic = entry.topic                       # 通过外键拿到主题对象
            # topic_id = entry.topic.id                  # 拿到主题 ID
            # 因为 entry 有 topic 外键，所以能通过 entry.topic 找到它的主题。

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)


@login_required
def del_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method == "POST":
        topic.delete()
        return redirect("learning_logs:topics")

    context = {"topic": topic}
    return render(request, "learning_logs/del_topic.html", context)


# 用户点“确认删除”
#     ↓
# 浏览器把表单数据 POST 到 /topics/2/del_topic/
#     ↓
# Django 收到 POST 请求，调用 views.del_topic
#     ↓
# 视图函数里：topic.delete()
#     ↓
# Django 执行 SQL：DELETE FROM learning_logs_topic WHERE id = 2
#     ↓
# 数据库里这条记录被删除
#     ↓
# 视图返回 redirect('learning_logs:topics')
#     ↓
# 浏览器跳转到主题列表页
