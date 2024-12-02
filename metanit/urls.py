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

products_patterns = [
    path("", views.products),
    path("new", views.new),
    path("top", views.top),
]

product_patterns = [
    path("", views.product),
    path("comments", views.comments),
    path("questions", views.questions),
]
 
urlpatterns = [
    path('', views.index, name='home'),
    re_path(r'^about', views.about, kwargs={"name":"Tom", "age": 38}),
    re_path(r'^contact', views.contact),
    path('sc', views.sc, name='secret code'),
    path('error', views.error, name='error'),
    path('greetings', views.greetings, name='greetings'),    
    path("user2/", views.user2),   
    # path("user/<name>/<int:age>", views.user),
    # Для представления параметра в шаблоне адреса используется выражение ?P<>. 
    # Общее определение параметру соответствует формату (?P<имя_параметра>регулярное_выражение). 
    # Между угловыми скобками помещается название параметра. После закрывающей угловой скобки идет регулярное выражение, которому дожно соответствовать значение параметра.
    re_path(r"^user/(?P<name>\D+)/(?P<age>\d+)", views.user),
    re_path(r"^user/(?P<name>\D+)", views.user),
    re_path(r"^user", views.user),
    path("products/", include(products_patterns)),
    path("product/<int:id>/", include(product_patterns)),
    path("contact/", views.contact),
    path("details/", views.details),
    path("access/<int:age>", views.access),
    path('jsontest1', views.jsontest1),
    path('jsontest2', views.jsontest2),
]

