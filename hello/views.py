from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, \
HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
  
def index(request):
    host = request.META["HTTP_HOST"] # получаем адрес сервера
    user_agent = request.META["HTTP_USER_AGENT"]    # получаем данные бразера
    path = request.path     # получаем запрошенный путь
     
    return HttpResponse(f"""
        <p>Host: {host}</p>
        <p>Path: {path}</p>
        <p>User-agent: {user_agent}</p>
    """)

def about(request, name ="Undefined", age =0):
    return HttpResponse(f"""
            <h2>О пользователе</h2>
            <p>Имя: {name}</p>
            <p>Возраст: {age}</p>
    """)
 
def contact(request):
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

def contact(request):
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
  
    def __init__(self, name, age, color):
        self.name = name    # имя человека
        self.age = age        # возраст человека
        self.color = color        # возраст человека
 
class PersonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Person):
            return {"name": obj.name, "age": obj.age,  "color": obj.color*2}
            # return obj.__dict__
        return super().default(obj)