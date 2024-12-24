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
    path("strange_things", views.strange_things),
    path("default_value_of_a_mutable_type", views.default_value_of_a_mutable_type),    
    path("add_new_instance_attribute", views.add_new_instance_attribute),   
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
    path("page15_user_form", views.page15_user_form),
    re_path(r'page15_postuser', views.page15_postuser),
    path("page16_user_form_django", views.page16_user_form_django),
    path("page17_select", views.page17_select),
    path("page18_create_record", views.page18_create_record),
    re_path(r'create_person', views.create_person),
    path("page19_get_records", views.page19_get_records),
    re_path(r'get_person', views.get_person),
    path("page20_py_types", views.page20_py_types),
    path("page21_py_arithmetic_operations", views.page21_py_arithmetic_operations),
    path("page22_py_in", views.page22_py_in),
    path("page23_py_function_parameters", views.page23_py_function_parameters),
    path("page24_py_lambda", views.page24_py_lambda),
    path("page25_py_global_nonlocal", views.page25_py_global_nonlocal),
    path("page26_py_string", views.page26_py_string),
    path("page27_py_list_tuple", views.page27_py_list_tuple),
    path("page28_py_dict_set", views.page28_py_dict_set),
    path("page29_py_functions", views.page29_py_functions),
    path("page30_py_objects_classes", views.page30_py_objects_classes),    
    # основные страницы 
    path("", views.about),
    path("about/", views.about),
    path("awesome/", views.awesome),
    path("cat/", views.cat),
    path("skill/", views.skill),
]

