from django.shortcuts import render, redirect
from django.urls import path
from .models import Topic,Entry
from django import forms
from .forms import TopicForm, EntryForm

"""
一，创建表单：新建一个forms.py文件
让客户可以在任何地方访问，注册，撤销属于客户的页面内容。

先从最开始的，创建一个表单开始。这个表单是django的forms模块的forms.ModelForm 类来自动完成，需要指定这个表单是给谁创造的，
指定给谁创造，django的forms.ModelForm模块会根据模型自动创造表单"""


  #在同目录中，导入同目录中的models.py 中的Topic模型

class TopicForm(forms.ModelForm):
    #继承 ModelForm，自动根据模型生成表单
    class Meta:
        #内部类，配置表单的元信息
        model=Topic
        #告诉表单：基于 Topic 模型生成
        field=['text']
        #只生成 text 字段的表单控件
        labels={'text':''}
        #text 字段的标签设为空字符串
        
        

'''
TopicForm 会自动生成：
一个 text 输入框（因为是 CharField）,forms.ModelForm类根据 CharField,自动生成一个文字输入框。
没有标签文字（因为 labels 设成了空）
提交时会自动验证并保存到 Topic 模型

TopicForm 基于 Topic 模型自动生成表单，只包含 text 字段，并把这个字段的标签设为空。
它负责“生成表单控件 + 验证 + 保存”，是连接用户输入和数据库的桥梁。
'''

# 二，匹配路由，在urls.py 中添加匹配的路由
# path('new_topic/',views.new_topic,name='new_topic')


# 三，创建视图函数，在views.py 中添加new_topic()函数
#此时就可以编辑views.py 的new_topic函数了：
#在views.py 中，要先导入 
# from django.shortcuts  import render,redirect 

def new_topic(request):
    """添加新的主题"""
    if request.method != 'POST':
        #未提交数据，就创建一个新的表单：
        form=TopicForm()

    else:
        #Post 提交的数据，就对提交的数据进行处理：
        form=TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    #显示空表单，或指出表单数据无效：
    context={'form':form}
    return render(request,'learning_logs/new_topic.html',context)

"""
逐行解释：def new_topic(request): 定义一个new_topic视图函数，用djang发起的request做参数
if request.method != 'POST': 如果访问请求不是post，就可能是get类，就新建一个空的表单：
form=TopicForm(),这个实例没有参数传进去，是空的。这个表单也是空的。

这时候就继续将上下文context={'form':form}传给后面的new_topic.html了。
将表单放入字典： 键 'form' 是模板中使用的名字，值 form 是实际的表单对象

并返回用new_topic.html模板用上下文context填充后，根据request请求的内容，渲染的网页。

如果浏览器提出的访问请求是POST类型，就处理数据：
form=TopicForm(data=request.Post) :根据request带来的Post 数据，创建新表单
if form.is_valid()-->form.save()如果表单合法，就存到数据库。因为是 继承ModelForm类，会自动创建 Topic 实例
并把浏览器重新定位到topic/.
传递上下文context-->渲染网页。"""


#四，创建new_topic模板： 新建new_topic.html:
"""
{%block content %}

<p>Add a new topic here :</p>
<!--增加提示语：-->

<form action="{% url 'learning_logs:new_topic' %}" method='post'>
    {% csrf_token %}
    {{ form.as_div }}
    <button name='submit'>Add topic</button>
</form>
<form></form>是一个完整的表单，用来收集用户输入并提交给服务器。中间是表单里的控件（输入框、按钮等）
{% endblock content %}

2. <form action="..." method="post"> 是什么？
<form action="{% url 'learning_logs:new_topic' %}" method='post'>
属性	值	                                       含义
action	{% url 'learning_logs:new_topic' %}	       表单提交到哪个 URL
method	post	                                   用 POST 方法提交
action 的作用：告诉浏览器“表单数据提交到哪个地址”。

{% url 'learning_logs:new_topic' %} 会解析成 /new_topic/，所以：
<form action="/new_topic/" method="post">
用户点击提交后，浏览器会把数据 POST 到 /new_topic/

3. {% csrf_token %} 是什么？
CSRF 是跨站请求伪造（Cross-Site Request Forgery）的缩写，{% csrf_token %} 是 Django 的安全令牌。

作用	说明
防止 CSRF 攻击	防止恶意网站伪造用户请求
Django 要求	所有 POST 表单必须包含这个标签
生成隐藏字段	渲染后会变成一个隐藏的 <input>
渲染后的 HTML：
<input type="hidden" name="csrfmiddlewaretoken" value="随机字符串">
如果没有这个标签，Django 会拒绝 POST 请求，报错：
CSRF verification failed. Request aborted.

4. {{ form.as_div }} 是什么？
form 是视图传过来的表单对象，as_div 是它的一个方法，用来把表单渲染成 HTML。

写法	                            渲染结果
{{ form.as_p }}	                    每个字段包在 <p> 里
{{ form.as_div }}	                每个字段包在 <div> 里
{{ form.as_table }}                	每个字段包在 <tr> 里
{{ form.as_ul }}	                每个字段包在 <li> 里
as_div 渲染示例：

<div>
    <label for="id_text">Text:</label>
    <input type="text" name="text" id="id_text" maxlength="200" required>
</div>
它自动生成：
标签（<label>）
输入框（<input>）
验证属性（如 required、maxlength）

5. <button name='submit'>Add topic</button> 是什么？
提交按钮，用户点击后触发表单提交。

部分	含义
<button>	        按钮标签
name='submit'	    按钮的名字（可选）
Add topic	        按钮上显示的文字
点击后：浏览器把表单数据 POST 到 action 指定的 URL。

1. 用户访问 /new_topic/
2. 视图渲染 new_topic.html，显示空表单
3. 用户填写表单，点击 "Add topic"
4. 浏览器把数据 POST 到 /new_topic/
5. 视图接收 POST 数据，验证表单
6. 如果合法，保存到数据库，重定向到 /topics/
7. 如果不合法，重新渲染表单，显示错误


"""
#五，在主题中添加链：
# 接写好了new_topic.html之后，将其在topics.html中增加一个链接，可以在topics/下跳转到new_topic/
# <a href="{% url 'learning_logs:new_topic' %}">Add a new topic</a>

##################################################################################################################


#下面将给特定的id的topic增加新的条目，比如，给足球主题添加条目。(足球的id=1)
# 同样的:  在forms.py 中添加EntryForm类 --->添加urls.py--->定义views.py--->编写entries.html,--->将链接绑定到topics.html中

#一，在forms.py中新定义一个类：
class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['text']
        labels={'text':'猴子称大王'}
        widgets={'text':forms.Textarea(attrs={'cols':80})}
        
        
#------------------------------------------------------------------------------------------------------------------       
#二，在urls.py中添加'entry/':
path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry')
#用<int:topic_id>表明，现在添加的是哪一个主题的条目

#三，创建视图函数：views.py
def new_entry(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if request.method !='POST':
        form=EntryForm()
    else:
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            # commit=False 的作用	先创建对象，不保存，手动补 topic 后再保存
            new_entry.topic=topic
            new_entry.save()           
            return redirect('learning_logs:topic',topic_id=topic_id)


    context={'topic':topic,'form':form}
    #context是将要传递给new_entry.html的一段内容，是一个上下文。
    # 有了这个上下文，new_entry.html才能根据具体的模型名字的实例来“才能根据具体的模型实例来渲染页面”
    # context 中 'topic': topic	键是模板用的名字，值是实例
    return render(request,'learning_logs/new_entry.html',context)

#这个函数new_entry()的参数，增加了一个topic_id,因为要明确是给哪一个topic添加条目。

"""
因为 `TopicForm` 是一个 `ModelForm`，它**包含了所有必填字段**，所以验证通过后可以直接保存。

### 为什么 `new_topic` 可以 `form.save()`，而 `new_entry` 不行？
| 对比                              | `TopicForm`         | `EntryForm` |
| 关联模型                          | `Topic`             | `Entry` |
| 表单包含的字段                    | `text`              | `text` |
| 模型必填字段                      | `text`              | `text`、`topic` |
| 表单是否包含所有必填字段          | ✅ 是              | ❌ 否（缺少 `topic`） |
| 能否直接 `save()`                 | ✅ 能              | ❌ 不能，需要 `commit=False` |

**关键区别**：
- `Topic` 模型只有 `text` 一个必填字段，`TopicForm` 正好包含它 → 直接保存
- `Entry` 模型有 `text` 和 `topic` 两个必填字段，但 `EntryForm` 只包含 `text` → 需要手动补 `topic`

### `new_topic` 的完整流程
def new_topic(request):
    if request.method != "POST":
        form = TopicForm()                    # ① 显示空表单
    else:
        form = TopicForm(data=request.POST)   # ② 用 POST 数据创建表单
        if form.is_valid():                   # ③ 验证数据
            form.save()                       # ④ 直接保存到数据库
            return redirect('learning_logs:topics')
  
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


| 步骤   | 发生什么 |
| ①     | 用户访问页面，显示空表单 |
| ②     | 用户提交，用 POST 数据创建表单 |
| ③     | 验证数据（如 `text` 是否为空、是否超过 200 字符） |
| ④     | 验证通过，直接保存，Django 自动创建 `Topic` 实例 |

### 为什么 `form.save()` 能直接保存？
因为 `TopicForm` 是 `ModelForm`，它知道：
| 信息               | 来源 |
| 关联哪个模型       | `model = Topic` |
| 包含哪些字段       | `fields = ['text']` |
| 如何验证           | 根据模型的字段类型自动生成规则 |
| 如何保存           | 自动创建 `Topic` 实例并写入数据库 |

**`form.save()` 做的事**：
1. 从表单数据中提取 `text` 的值
2. 创建一个 `Topic` 实例
3. 写入数据库
4. 返回这个实例


### 对比 `new_entry` 为什么不能直接 `save()`
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    
    if request.method == 'POST':
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)   # 不能直接 save()
            new_entry.topic = topic                # 手动补 topic
            new_entry.save()                       # 再保存


**因为 `EntryForm` 的 `fields = ['text']`，不包含 `topic`**，而 `Entry` 模型的 `topic` 是必填外键。
如果直接 `form.save()`，会报错：
IntegrityError: NOT NULL constraint failed: learning_logs_entry.topic_id

**所以必须用 `commit=False` 先创建对象，手动补 `topic`，再保存。**


### 总结

| 你的问题                                           | 答案 |
| 为什么 `new_topic` 可以直接 `form.save()`？        | 因为 `TopicForm` 包含了 `Topic` 的所有必填字段 |
| `form.save()` 做什么？                             | 自动创建 `Topic` 实例并写入数据库 |
| 为什么 `new_entry` 不行？                          | 因为 `EntryForm` 缺少 `topic` 字段 |
| `new_entry` 怎么做？                               | 用 `commit=False`，手动补 `topic`，再 `save()` |

**一句话**：`form.save()` 能直接用的前提是“表单包含了模型的所有必填字段”。
`TopicForm` 满足这个条件，所以直接保存；`EntryForm` 缺少 `topic`，所以需要 `commit=False` 手动补。
-----------------------------------------------------------------------------------------------------------------------------

entry 模型有 topic 外键
    ↓
Entry 实例必须有 topic 属性
    ↓
EntryForm 的 model = Entry
    ↓
所以 EntryForm 创建的实例也需要 topic
    ↓
但 EntryForm 的 fields = ['text']，不包含 topic
    ↓
所以 form.save() 会失败（缺少 topic）
    ↓
必须用 commit=False，手动补 topic，再 save()

 一句话：因为 Entry 模型有必填外键 topic，而 EntryForm 只包含 text，所以 form.save() 会因缺少 topic 失败。
 必须用 commit=False 先创建对象，手动补 topic，再调用 save()。你的推理完全正确！
 """
 
 #四，创建new_entry.html文件
"""
 {% extends 'learning_logs/base.html' %}
 继承父模板

{% block content %}
<p><a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a></p>
{{ topic }} 是什么？
它是链接上显示的文字，显示的就是这个主题的 text 值。假如主题是'足球'，这里渲染后显示的就是 '足球'.
点击“足球”，跳转到 /topics/1/。

{{ topic }} 啥作用？	     显示链接上的文字
显示的是什么？         	     topic 的 __str__() 返回值，通常是 text
和 href 什么关系？	         href 决定跳去哪，{{ topic }} 决定显示什么
不用 {{ topic }} 行吗？	     ✅ 行，但用户不知道链接指向哪个主题
一句话：<a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a> 中，
href 是“跳转地址”，{{ topic }} 是“链接上显示的文字”。
两者配合，用户看到“足球”这个链接，点击后跳转到足球的详情页。

<p>Add a new entry to the topic:</p>
<form action="{% url 'learning_logs:new_entry' topic.id %}" method ='post'>
把表单交给这个地址的url,方式用post方式。
    {% csrf_token%}
    安全令牌，防止跨站伪装，所有 POST 表单必须加这个标签，否则 Django 会拒绝请求。
    {{ form.as_div }}
    把这个表单，用div区域的形式渲染（div可以写大段文字）
    <button name='submit'>Add entry here</button>
    按钮默认就是提交按钮，点击后触发表单提交”
    
    这段代码是 Django 表单的标准写法。
    <form> 定义提交地址和方法，{% csrf_token %} 保证安全，{{ form.as_div }} 自动渲染表单字段。
    用户填写后点击提交，数据 POST 到 new_entry 的 URL，由视图处理。你的理解完全正确！
    
    
</form>
{%endblock content %}
"""

#五，把这个链接添加到topic.html中，以便可以在topic页面中跳转访问。
#而不是添加到topics.html中。因为new_entry是给具体的某一个topic服务的，不是给所有的topics服务。

#     <p>
#         <a href="{% url 'learning_logs:new_entry' topic.id %}">Add new entry </a>
#     </p>

#------------------------------------------------------------------------------------------------------------------
#以上完成了对某一个特定的topic的条目添加。现在让用户可以编辑已经添加的条目。要点：条目的id.

#同样的操作： urls.py添加path--->views.py中定义视图函数--->编辑edit_entry.html模板--->添加链接到topic.html中

#一，在urls.py 中添加path:
path('edit_entry/int:entry_id/',views.edit_entry,name='edit_entry') ,

#二，在views.py中添加视图函数：
#要先导入Entry模型
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)

    topic=entry.topic
    
    if request.method !='POST':
        form = EntryOForm(instance=entry)
        #EntryForm：说明这是一个EntryForm类的表单，是一个条目类的，而不是主题类的表单
        #instance=entry: 告诉表单：“用 entry 这个实例的现有数据来填充表单”
        # 效果：表单字段会自动填入 entry 的当前值，用户看到的是已填好的表单，可以直接修改
        #form = entry 不行，因为 entry 是一个模型实例，不是表单对象，需要通过EntryForm翻译，才能填充entry的数据。
        
    else:
        form=EntryForm(instance=entry,date=request.POST)
        #把entry的数据改写后，提交给服务器。
        #instance=entry 是“改哪条”，data=request.POST 是“改成什么”。编辑记录时，两者缺一不可。
        # 只写 instance，用户改了也白改；只写 data，会变成新建一条记录。两个一起写，才是“用新数据更新原记录”。
        
         #参数	                    作用	                                回答什么问题
         # instance=entry	        告诉表单“要更新哪个对象”	            更新哪条记录？
         # data=request.POST	    告诉表单“用户提交了什么数据”	        更新成什么？
         # instance 决定“改谁”，data 决定“改成什么”
         
         #Get method是从浏览器给服务器发请求，读取，拿取。而Post method 是把通过楼兰其把数据交给服务器，等着回应。
         #GET 和 POST 都是浏览器发给服务器的请求。GET 是“我要看这个页面”，POST 是“我要提交这些数据”。方向都是浏览器 → 服务器，
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
            #注意这个topic_id = topic.id 因为path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry')
            #只有entry_id，而不知道topic_id,要拿到主题 ID，必须通过 entry.topic.id找出来。
            
    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)     



#三，创建edit_entry.html模板：

"""
{% extends 'learning_logs/base.html' %}
#继承父模板
{% block content %}
<p><a href="{% url 'learning_logs:topic' topic.id}">{{ topic }}</a></p>|
#先增加一个跳转到特定主题的链接。并显示特定主题的变量值是 足球 
#因为这个编辑的条目就是挂在这个特定主题下面的。

<p> 欢迎来到编辑页面，重新编辑这些条目</p>

<form action="{% url 'learning_logs:edit_entry' entry.id %}" method='post'>
    {% csrf_token %}
    {{ form.as_div }}
    <button name='submit'>Save change</button>
</form>

{% endblock content %}"""

#四，在topic.html 中添加关于edit_entry的链接：

# <p><a href="{% url 'learning_logs:edit_entry entry.id %}">编辑条目</a></p>
#注意，这个链接应该放到列表中，跟新增加的entry在一起。