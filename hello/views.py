from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, \
HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.template.response import TemplateResponse
  

def index(request):
    header = "Данные пользователя"              # обычная переменная
    langs = ["Python", "Java", "C#"]            # список
    user ={"name" : "Tom", "age" : 23}          # словарь
    address = ("Абрикосовая", 23, 45)           # кортеж
  
    data = {"header": header, "langs": langs, "user": user, "address": address}
    return render(request, "index.html", context=data)
 
def about(request):
    return render(request, "about.html")   

def skill(request):
    return render(request, "skill.html")   

def cat(request):
    return render(request, "cat.html")   

def awesome(request):
    return render(request, "awesome.html")   

def about3(request):
    return render(request, "about3.html", context = {"person": Person("Tom")})   

def contact(request):
    header = "Данные пользователя"              # обычная переменная
    langs = ["Python", "Java", "C#"]            # список
    user ={"name" : "Tom", "age" : 23}          # словарь
    address = ("Абрикосовая", 23, 45)           # кортеж
  
    data = {"header": header, "langs": langs, "user": user, "address": address}
    return TemplateResponse(request,  "contact.html", data)

def index3(request):
    host = request.META["HTTP_HOST"] # получаем адрес сервера
    user_agent = request.META["HTTP_USER_AGENT"]    # получаем данные бразера
    path = request.path     # получаем запрошенный путь
     
    return HttpResponse(f"""
        <p>Host: {host}</p>
        <p>Path: {path}</p>
        <p>User-agent: {user_agent}</p>
    """)

def about2(request, name ="Undefined", age =0):
    return HttpResponse(f"""
            <h2>О пользователе</h2>
            <p>Имя: {name}</p>
            <p>Возраст: {age}</p>
    """)
 
def contact2(request):
    return HttpResponse("<h2>Контакты</h2>")

def sc(request):
    return HttpResponse("Hello METANIT.COM", headers={"SecretCode": "21234567"})

def error(request):
    return HttpResponse("Произошла ошибка", status=400, reason="Incorrect data")

def greetings(request):
    return HttpResponse("<h1>Hello</h1>", content_type="text/plain", charset="utf-8")

# def user(request, name):
#     return HttpResponse(f"<h2>Имя: {name}</h2>")

def user(request, name="Undefined", age =0):
    return HttpResponse(f"<h2>Имя: {name}  Возраст:{age}</h2>")

def products(request):    
    return HttpResponse("Список товаров")
 
def new(request):
    return HttpResponse("Новые товары")
 
def top(request):
    return HttpResponse("Наиболее популярные товары")

def product(request, id):
    return HttpResponse(f"Товар {id}")
 
def comments(request, id):
    return HttpResponse(f"Комментарии о товаре {id}")
 
def questions(request, id):
    return HttpResponse(f"Вопросы о товаре {id}")

def user2(request):
    age = request.GET.get("age", 0)
    name = request.GET.get("name", "Undefined")
    return HttpResponse(f"<h2>Имя: {name}  Возраст: {age}</h2>")

def contact2(request):
    return HttpResponseRedirect("/about")
 
def details(request):
    return HttpResponsePermanentRedirect("/")

def access(request, age):
    # если возраст НЕ входит в диапазон 1-110, посылаем ошибку 400
    if age not in range(1, 111):
        return HttpResponseBadRequest("Некорректные данные")
    # если возраст больше 17, то доступ разрешен
    if(age > 17):
        return HttpResponse("Доступ разрешен")
    # если нет, то возвращаем ошибку 403
    else:
        return HttpResponseForbidden("Доступ заблокирован: недостаточно лет")
    
def jsontest1(request):
    return JsonResponse({"name": "Tom", "age": 38})

def jsontest2(request):
    bob = Person("Bob", 41, 'blue')
    return JsonResponse(bob, safe=False, encoder=PersonEncoder)
 
class Person:
  
    def __init__(self, name, age =20, color ='blue'):
        self.name = name    # имя человека
        self.age = age        # возраст человека
        self.color = color        # возраст человека
 
class PersonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Person):
            return {"name": obj.name, "age": obj.age,  "color": obj.color*2}
            # return obj.__dict__
        return super().default(obj)
    
def set(request):
    # получаем из строки запроса имя пользователя
    username = request.GET.get("username", "Undefined")
    # создаем объект ответа
    response = HttpResponse(f"Hello {username}")
    # передаем его в куки
    response.set_cookie("username", username)
    return response

def get(request):
    # получаем куки с ключом username
    username = request.COOKIES["username"]
    return HttpResponse(f"I know you, {username}!")