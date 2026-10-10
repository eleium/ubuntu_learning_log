"""
一，环境搭建
1.在项目中创建和激活虚拟环境： powershell : python -m venv ll_venv-->ll_venv/Scripts/activate
                                #  bash: python -m venv ll_venv-->source ll_venv/Scripts/activate

2.pip install django-->django-admin startproject ll_project .
3.python manage.py migrate
4.python manage.py startapp learning_logs
5.ll_project/settings.py -->installed app -->add  'learning_logs',
6.python manage.py makemigrations learning_logs
7.python manage.py migrate
8.learning_logs/models.py--->class Topic(models.Model)/Entry
9.learning_logs/admin.py--->admin.site.register(Topic/Entry)
10.python manage.py createsuperuser(admin)
11,python manage.py runserver

此时，访问http://localhost:8000/admin，可以添加Topic，和Entry
而我选择在后台python manage.py shell 中添加：
1.Topic.objects.create(text='足球')/'篮球'
2.Entry.objects.create(topic_id=1,text='足球是十一个人一对，把球送入对方的大门的游戏。')
3.Entry.objects.create(topic_id=2,text='篮球运动员，个子越大，优势越大。')
4.Entry.object.create(topic_id=1,text='充满对抗的游戏，我喜欢.')

后台添加Topic和Entry的感觉很爽，但是如果想修改，就要重新输入。不好编辑。
 删除一个对象	               正确写法
 删除一个 Topic	           Topic.objects.get(id=1).delete()
 删除一个 Entry	           Entry.objects.get(id=1).delete()
 批量删除	                   Entry.objects.filter(topic_id=1).delete()
 删除全部	                   Topic.objects.all().delete()
 ❌ 错误写法	              Topic.objects.delete()、Entry.objects.delete(...)
 一句话：delete() 是实例方法，必须先查到对象再调用；不能直接在 objects 管理器上调用。
"""

# ----------------------------------------------------------------------------------------------------
"""
二，现在可以创建 学习笔记的主页了：

1.在ll_project/urls.py -->add path('',include('learning_logs.urls))
2.learning_logs/新建urls.py --> app_name='learning_logs'.   urlpatterns=[path('',views.index,name='index')]
3,learning_logs/views.py-->def index(request)-->return render(request,'learning_logs/index.html')
4.创建learning_logs/templates/index.html :
<p>
    Good good study, day day up.
</p>
<!--如果想一行文本换行，在要换行处加 <br>-->
<p>
    <a href="{% url 'learning_logs:index' %}">今天又学到了新知识</a>
</p>

命名空间细节:

1. app_name = 'learning_logs' 的意义
除了给自己命名，它主要用在两个地方：

使用场景	示例	说明
模板中反向解析	{% url 'learning_logs:index' %}	用 命名空间:路由名 找到 URL
视图中反向解析	reverse('learning_logs:index')	用 reverse() 函数生成 URL
为什么需要它？

假设你的项目有两个 app，都有一条 name='index' 的路由：

learning_logs/urls.py
app_name = 'learning_logs'
path('', views.index, name='index')

 blog/urls.py
 app_name = 'blog'
 path('', views.index, name='index')
 如果没有 app_name，模板中写 {% url 'index' %}，Django 不知道你要找哪一个。加上 app_name 后：

 {% url 'learning_logs:index' %}   <!-- 明确指向 learning_logs 的 index -->
 {% url 'blog:index' %}            <!-- 明确指向 blog 的 index -->
 所以 app_name 的核心作用是：避免不同 app 之间的路由名冲突。

path('',views.index,name='index')中的name是路由的意思，指向'index',也可也指向' / ','admin/'
 """

# --------------------------------------------------------------------------------------------------------

"""
三，创建其他网页
1，learning_logs/templates/learning_logs/-->新建 base.html:
<p>
<a href="{% url 'learning_logs:index' %}">I love python ! Be happy ！base</a>
</p>

{% block content%}{% endblock content %}
<!--上面的{% block content%}{% endblock content %}是个占位符，等待其他的内容填充-->

2.修改index.html:
{% extends learning_logs/base.html %}
<!--django 从templates/下开始查找，所以不要写上 learning_logs/templates/-->

{%block content%}

<p>
    今天去南山街，碰到了两只小猫。
</p>
{% endblock content %}

访问http://localhost:8000/--->I love python ! Be happy ！base   今天去南山街，碰到了两只小猫。

{% block content %},其中的content是这个要插入的块的名字，可以随意更换。比如main,page,abc,
但是，子模版的名字必须有要与base.html的名字一致。

2.添加可以显示所有主题的网页：
learning_logs/urls.py-->path('topics',views.topics,name='topics')--->
修改views.py:添加： from .models import Topic
def topics(request):
    topics=Topic.objects.order_by(date_added)
    #topics是一个查询集：所有的Topic,用创建时间升序排列
    
    context={'topics':topics}
    return render(request,'learning_logs/topics.html',context)
    
    
#-------------------------------------- 
context={'topics':topics}   的意义与应用
context 是一个字典，它的作用是把数据从视图（View）传递给模板（Template）。
简单说：你在视图里把数据打包成字典，传给模板，模板就能用这个数据渲染页面。
| 部分                | 含义 |
| `context`           | 上下文，一个字典 |
| `'topics'`          | 键（key），模板中使用的名字 |
| `topics`            | 值（value），视图中查询出的数据（查询集） |


### 完整流程
视图 `views.py`：
def index(request):
    topics = Topic.objects.order_by('date_added')  # 从数据库取数据
    context = {'topics': topics}                    # 打包成字典
    return render(request, 'learning_logs/index.html', context)  # 传给模板

**模板 `index.html`：**
{% for topic in topics %}          <!-- 用 'topics' 这个键 -->
    <li>{{ topic.text }}</li>
{% endfor %}

**对应关系：**
| 视图中的键     | 模板中的变量 |
| `'topics'`     | `topics` |
| `'name'`       | `name` |
| `'entries'`    | `entries` |

### 为什么需要 context？

| 原因                          | 说明 |
| **视图和模板分离**            | 视图负责取数据，模板负责显示，数据通过 context 传递 |
| **模板不能直接查数据库**      | 模板没有 Python 逻辑，只能接收视图传来的数据 |
| **可以有多个变量**            | 一个 context 可以传多个键值对 |

**示例：传多个变量**
```python
context = {
    'topics': topics,
    'entries': entries,
    'user': request.user,
}
return render(request, 'index.html', context)


模板中可以分别使用：
{{ user.username }}
{% for topic in topics %}...{% endfor %}
{% for entry in entries %}...{% endfor %}

### 更简洁的写法
如果变量名和键名相同，可以直接传字典字面量：
return render(request, 'index.html', {'topics': topics})

甚至可以用 `locals()`（不推荐，容易混乱）：

return render(request, 'index.html', locals())
### 总结

| 你的问题 | 答案 |
|----------|------|
| `context` 是什么？          | 一个字典，用于把数据从视图传给模板 |
| 键是什么？                  | 模板中使用的变量名 |
| 值是什么？                  | 视图中查询出的数据 |
| 为什么需要它？              | 模板不能直接查数据库，必须通过 context 接收数据 |
| 可以传多个吗？              | ✅ 可以，一个 context 可以有多个键值对 |

**一句话**：`context` 是视图和模板之间的“数据包裹”，视图把数据装进去，模板从里面取出来用。
    
排序规则
写法	                            含义
order_by('date_added')	            按 date_added 升序（旧 → 新）
order_by('-date_added')	            按 date_added 降序（新 → 旧），字段名前加 -
order_by('text')	                按 text 字段升序（字母顺序 A → Z）
order_by('-text')	                按 text 字段降序（Z → A）
order_by('text', 'date_added')	    先按 text 升序，text 相同再按 date_added 升序

"""
# 新建learning_logs/topics.html：--------------------------------------------------
"""
{% extends 'learning_logs/base.html' %}
{% block content %}
<p>Topics 主题们</p>
<ul>
    {% for topic in topics %}
    <li>{{ topic.text }}</li>
    {% empty %}
    <li>No topics have been added yet.</li>
    {% endfor %}
</ul>
{% endblock content %}
________________________________________________________

<li>{{ topic.text }}</li>
| 部分                                | 类型                         | 含义 |
| `<li>`                              | HTML 标签                    | 列表项（list item），表示列表中的一项 |
| `{{ topic.text }}`                  | Django 模板变量              | 输出 `topic` 对象的 `text` 属性值 |
| `</li>`                             | HTML 标签                    | 列表项结束 |

### 1. `<li>` 是什么？

`<li>` 是 HTML 的**列表项标签**，必须放在 `<ul>` 或 `<ol>` 里面：
<ul>                              <!-- 无序列表 -->
    <li>苹果</li>                 <!-- 列表项 1 -->
    <li>香蕉</li>                 <!-- 列表项 2 -->
    <li>橙子</li>                 <!-- 列表项 3 -->
</ul>
渲染效果：
> - 苹果
> - 香蕉
> - 橙子

### 2. `{{ }}` 是什么？
`{{ }}` 是 Django 模板的**变量输出语法**。它会：

1. 从 context 中找到 `topic` 对象
2. 访问它的 `text` 属性
3. 把值输出到 HTML 中

**示例**：假设 `topic.text = "足球"`，那么：

<li>{{ topic.text }}</li>
会被渲染成：
<li>足球</li>
浏览器显示：
> - 足球

### 3. 对比：`{{ }}` 和 `{% %}`
| 语法              | 用途                             | 示例 |
| `{{ }}`           | 输出**变量**的值                 | `{{ topic.text }}` |
| `{% %}`           | 执行**逻辑**（循环、判断等）     | `{% for topic in topics %}` |

**记忆方法**：
- `{{ }}` → 双大括号，输出**值**
- `{% %}` → 百分号，执行**逻辑**

### 4. 完整例子
**视图：**
topics = Topic.objects.all()
context = {'topics': topics}
return render(request, 'index.html', context)

**模板：**
<ul>
    {% for topic in topics %}
        <li>{{ topic.text }}</li>
    {% endfor %}
</ul>

**渲染结果**（假设有 3 个主题）：
<ul>
    <li>足球</li>
    <li>篮球</li>
    <li>乒乓球</li>
</ul>

### 总结

| 你的问题                         | 答案 |
| `<li></li>` 是列表吗？           | ✅ 是列表项，必须放在 `<ul>` 或 `<ol>` 里 |
| 里面为啥是双大括号？             | `{{ }}` 是 Django 模板语法，用于输出变量的值 |
| `{{ topic.text }}` 是什么？      | 输出 `topic` 对象的 `text` 属性 |
| `{{ }}` 和 `{% %}` 区别？        | `{{ }}` 输出值，`{% %}` 执行逻辑 |

**一句话**：`<li>` 是 HTML 列表项，`{{ topic.text }}` 是 Django 模板变量，两者结合，就能把数据库里的数据渲染成 HTML 列表。

1. HTML 的 <ul> 是“无序列表”
HTML 的“有序/无序”指的是显示时有没有编号，和数据的排列顺序无关。<ul> 显示圆点，<ol> 显示数字，两者都可以加 id。
标签	全称	                        含义	               显示效果
<ul>	Unordered List	                无序列表	           每项前面是圆点 •，没有编号
<ol>	Ordered List	                有序列表	           每项前面是数字 1. 2. 3.
<li>	List Item	                    列表项	               列表里的每一项

修改base.html
<p>
    <a href="{% url 'learning_logs:index'%}">I love python ! Be happy ！base.</a> -
    <a href ="{% url 'learning_logs:topics' %}"">Topics</a>
</p>

{% block content %}{% endblock content %}

base.html 是母版，在它里面加链接，等于给所有页面加了导航。
子模板继承后自动拥有这些链接，不用重复写。
这就是模板继承的最大好处——一次修改，全站生效。

子模板显示自己独有的内容，同时共享母版的导航栏，可以跳转到其他页面。
#添加访问特定主题（编号id）的页面url
    path('topics/<int:topic_id>/',views.topic,name='topic'),      
    <int:topic_id>:
****为什么用 <int:...>？
<int:...> 是 Django URL 的路径转换器，固定用法。它做两件事：

作用	         说明
限制类型	     只匹配整数，/topics/abc/ 不会匹配
自动转换	     把 URL 中的字符串 '1' 转换成 Python 整数 1

所以 <int:topic_id> 的意思是：
URL 中这个位置必须是整数
匹配后，把值以整数类型传给视图函数

---------------在views.py中添加topic的函数：
def topic(request,topic_id):
    #显示特定id主题的所有条目：
    
    topic=Topic.objects.get(id=topic_id)
    #获取id为topic_id的Topic 的一个对象：id=1-->足球 ，id=2-->篮球
    
    entries=topic.entry_set.order_by('-date_added')
    #等价于：topic.entry_set.all().order_bu(),all()可以省略。
    #返回的是一个查询集（QuerySet），里面装的是 Entry 对象，按创建时间从新到旧排列。
    # 这些对象里包含 text、date_added 等字段，不是 URL，跟url没有关系。
    
    context={'topic':topic,'entries':entries}

    return render(request,'learning_logs/topic.html',context)
    ---------------------------------------------
    request 是 Django 自动传入的“请求包裹”，里面装着这次请求的所有信息。
    视图可以用它来获取用户、方法、数据，也可以直接传给模板。即使不用，也必须写
    
   ----------------------------------------------------------------------- 
    #编写topic.html:
    {% extends 'learning_logs/base.html' %}
{% block content %}
<p>Topic:{{ topic.text }}
</p>
  <!--大双括号表示告诉django,现在要输出一个变量的值-->不能写{{ }},不管是在段落内还是之外，都会是空的大双括号，报错
<p>
    Entries:</p>

    <ul>
        {% for entry in entries %}
        <li>
            <p>{{ entry.date_added|date:'M d, Y H:i'}}</p>
            <p>{{entry.text|linebreaks }}</p>
        </li>
        {% empty %}
        <li>There are no entries for this topic yet.</li>
        {% endfor %}
    </ul>

    {% endblock content %}
    
--------------------------------------
完整流程：

步骤	    发生什么
1	        用户访问 /topics/1/
2	        URL 匹配 <int:topic_id>，把 1 传给视图
3	        视图 topic(request, topic_id=1) 被调用
4	        视图用 topic_id=1 查询数据库，得到 topic 对象
5	        视图把 topic 对象放入 context，传给模板
6	        模板用 {{ topic.text }} 输出这个对象的文本
topic_id 的作用是“告诉视图查询哪个主题”，topic 对象是查询结果。模板拿到的是结果（topic 对象），不需要再关心 topic_id。


"""


"""
用户在浏览器中输入http://localhost:8000/topics/1, django拿到topics/1，去url中匹配，
而app/urls.py 有path("topic/<int:topic_id>",views.topic,name='topic'),<int:topic_id>就是把topic的id 整数化，得到一个整数。
topic/1可以匹配路由并调用视图函数中的topic函数。
 （可以通过for topic in topics-->print(topic.id,topic)可以得知有几个topic_id.（前面又先topics=Topic.objects.all()).）
视图函数通过Topic.objects.get(id=1),与django 传来的<int:topic_id)也就是1 去匹配，
如果视图函数get(id=1)，就可以正确匹配。如果get(id)不存在，就报错404.
views.py 中的topic=Topic.objects.get(id=topic_id), django 把<int:topic_id>传入，具体是哪一个id,也就是 1 .
函数得到topic_1的所有属性，比如text,date_added,等，传入topic.html
topic.html操作的就都是topic_1的数据了。而不用再单独指出是来自哪一个topic_id。 

用户输入 /topics/1/
    ↓
Django 提取路径 /topics/1/
    ↓
主路由匹配 topics/ → 交给 learning_logs.urls
    ↓
子路由匹配 <int:topic_id> → topic_id = 1（整数）
    ↓
调用 views.topic(request, topic_id=1)
    ↓
视图执行 topic = Topic.objects.get(id=1)
    ↓
如果 id=1 存在 → 拿到 Topic 对象 → 传给模板
如果 id=1 不存在 → DoesNotExist → 404
    ↓
模板用 {{ topic.text }} 显示这个对象的数据

URL 路由负责“把 URL 里的数字提取成 topic_id”，视图负责“用这个 topic_id 去数据库查记录”。
两步各司其职，任何一步失败都会导致 404。需要把“URL 匹配”和“数据库查询”分开看。
"""