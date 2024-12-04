"""
URL configuration for metanit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, re_path, include
from hello import views
 
urlpatterns = [
    # Уроки
    path("lessons", views.lessons),
    path("page01_text", views.page01_text),
    path("page02_html", views.page02_html),
    re_path(r'^page03_re_path', views.page03_re_path),
    path("page04_kwargs", views.page04_kwargs, kwargs={"arg1":"Green", "arg2":"Day"}),
    path("page05_SecretCode", views.page05_SecretCode),
    path("page06_StatusResponse400", views.page06_StatusResponse400),
    path("page07_name/<str:name>", views.page07_name),
    re_path(r"^page08_count_animals/(?P<count>\d+)/(?P<animals>\D+)", views.page08_count_animals),
    re_path(r"^page08_count_animals/(?P<count>\d+)", views.page08_count_animals),
    re_path(r"^page08_count_animals/", views.page08_count_animals),
    path("page09_query_string_parameters/", views.page09_query_string_parameters),
    path("page10_user_exist/<int:id>", views.page10_user_exist),
    path("page11_access/<int:age>", views.page11_access),
    path("page12_json", views.page12_json),
    path("page13_set_cookie", views.page13_set_cookie),
    path("page14_get_cookie", views.page14_get_cookie),
    # основные страницы 
    path("", views.about),
    path("about/", views.about),
    path("awesome/", views.awesome),
    path("cat/", views.cat),
    path("skill/", views.skill),
]

