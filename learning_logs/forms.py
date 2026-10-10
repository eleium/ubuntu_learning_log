from django import forms 
from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    class Meta:
        #表单必须套用 Meta
        model=Topic
        fields=['text']
        labels={'text':'给你脸啦'}
#forms.ModelForm 是 Django 提供的基类，它规定：
# “你告诉我要基于哪个模型、包含哪些字段，我就自动生成表单。”
# 这些信息（模型、字段、标签、widgets）属于“元信息”，Django 约定把它们放在 class Meta 里。
# 没有 class Meta，Django 根本不知道这个 Form 基于哪个模型。

# Meta 是定义在 Form 类内部的“配置类”，它依附于具体的 Form，不是一个可以独立 import 的模块。
# 每个 Form 有自己的 Meta，Django 通过它知道“这个 Form 基于哪个模型、包含哪些字段”。
# 想复用得用继承，不是 import。


        
# fields = ['text'] 里的 'text' 是模型字段名，不是用户填的内容。
# 用户填的“游泳”是数据，会存进 text 这个字段里。
# labels 只是把字段的显示名改成“新的博客”，让用户看着更清楚。

# fields = ['text']   # 👈 告诉 Django：把 Blog 的 text 字段做成表单
# fields = ['text'] 的意思是：这个表单只包含 Blog 模型里的 text 字段。


class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['text']
        labels={'text':'猴子称大王'}
        
        widgets={'text':forms.Textarea(attrs={'cols':80})}
        #这行代码是给 Django 表单的某个字段自定义显示样式，具体是：
        # 把 text 字段渲染成一个 80 列宽的多行文本域（Textarea）。不写widgets,就是单行的文字框。
        
# widgets	Django 表单 Meta 中的一个配置项，用来指定字段用什么 HTML 控件。
# widgets 是 Django 表单的“控件配置”，决定每个字段渲染成什么 HTML 元素。

# 'text'	键，表示要自定义的字段名是 text
# forms.Textarea	值，表示用多行文本域来渲染这个字段
# attrs={'cols': 80}	传给 Textarea 的 HTML 属性，cols=80 表示宽度 80 列