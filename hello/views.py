from django.http import HttpResponse
  
def index(request):
    host = request.META["HTTP_HOST"] # получаем адрес сервера
    user_agent = request.META["HTTP_USER_AGENT"]    # получаем данные бразера
    path = request.path     # получаем запрошенный путь
     
    return HttpResponse(f"""
        <p>Host: {host}</p>
        <p>Path: {path}</p>
        <p>User-agent: {user_agent}</p>
    """)

def about(request, name, age):
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