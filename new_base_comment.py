"""
<!DOCTYPE html>
<html lang="en">
此网页用英文
    <head>
        <meta charset="utf-8">        ---->编码用utf-8,中英文不乱码
        <meta name="viewport" content="width=device-width,initial-scale=1">        --->视窗随设备大小变化

        <title>学习笔记</title>        --->页面的标签，最上方
        {% load django_bootstrap5 %}
        {% bootstrap_css %}
        加载bootstrap5的样式
    </head>

    <body>
        <nav class="navbar navbar-expand-md navbar-light bg-light mb-4 border">
        nav <nav>：是 HTML 标签。它的作用是语义化，告诉浏览器“这块区域是导航用的”。
        class:class="navbar..."：是 Bootstrap 的类名。它的作用是给这个区域加样式和布局。

        navbar: 基础 class，任何 Bootstrap 导航栏都必须加。
        它负责导航栏的基础样式（内边距、字体、布局等）。没有它，后面的 navbar-expand-md、navbar-light 都不生效。

        navbar-expand-md:响应式折叠：宽屏展开，窄屏折叠。>=768,展开。否则，汉堡折叠
        md 代表 Medium，Bootstrap 定义的响应式断点，阈值是 768px（这是 Bootstrap 5 中 md 的起始点）

        navbar-light: 浅色主题，文字深色    bg-light: 背景浅色 mb-4: 距离下面4个单位   border: 加一圈框，更清晰。

            <div class="container-fluid">
                <a class="navbar-brand" href="{% url 'learning_log:index' %}">learning_log</a>
                <button class="navbar-toggler"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarCollapse"
                        aria-controls="navbarCollapse"
                        aria-expanded="false"
                        aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarCollapse">
                    <ul class="navbar-nav me-auto mb-2 mb-md-0">
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'learning_log:topics' %}">Topics主题</a>
                        </li>
                    </ul>
                    <!-- 定义导航栏左侧连接的代码到此结束。-->
                </div>
                <!--定义导航栏可以折叠部分的代码到此结束。-->
            </div>
            <!--定义导航栏容器的代码到此结束。-->
        </nav>
        <!--定义导航栏的代码到此结束。-->
        {% block content %}
        {% endblock content %}

        {% bootstrap_javascript %}
        JavaScript 是网页的“行为”脚本语言，让页面能响应用户操作、动起来。没有 JavaScript，网页就是一张“静态海报”——只能看，不能交互。
    </body>
</html>
"""
