from django.http import HttpResponse, \
HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.template.response import TemplateResponse

# уроки
  
def lessons(request): 
    return render(request, "lessons.html")   

def page01_text(request):
    return HttpResponse("Это обычный текст")

def page02_html(request):
    return HttpResponse("<h2>Это код html</h2>")

def page03_re_path(request):
    return HttpResponse("Ты можешь добавлять к адресу page03_re_path любой постфикс, но все равно попадешь на эту страницу")

def page04_kwargs(request, arg1, arg2):
    return HttpResponse(f"""
            <h2>С помощью параметра kwargs передан словарь с двумя значениями</h2>
            <p>Значение 1: {arg1}</p>
            <p>Значение 2: {arg2}</p>
    """)

def page05_SecretCode(request):
    return HttpResponse("В headers есть поле SecretCode", headers={"SecretCode": "21234567"})

def page06_StatusResponse400(request):
    return HttpResponse("Произошла ошибка", status=400, reason="Incorrect data")

def page07_name(request, name ='Герман'):
    return HttpResponse(f"<p>Если после page07_name/ написать имя, то оно отобразится в строке ниже</p><h2>Имя: {name}</h2>")

def page08_count_animals(request, count =99, animals ='Default'):
    return HttpResponse(f'''<p>Если после page08_count_animals/ написать количество, а еще через / название животного, то это будет отображено в строке ниже</p>
                        <h2>Количество: {count}</h2>
                        <h2>Животное: {animals}</h2>
                        <p>Адрес работает как при отсутвии параметров после page08_count_animals/, так и только с одним количеством, например page08_count_animals/7</p>''')

def page09_query_string_parameters(request):
    param1 = request.GET.get("param1", 0)
    param2 = request.GET.get("param2", "Undefined")
    return HttpResponse(f'''<p>В строке запроса можно изменять параметры param1 и param2</p>
                        <h2>Параметр 1: {param1}</h2>  
                        <h2>Параметр 2: {param2}</h2>
                        <p>Если не задать параметр или оба параметра, то будет использовано значение по умолчанию</p>''')

def page10_user_exist(request, id):
    users = ["Tom", "Bob", "Sam"]
    # если пользователь найден, возвращаем его
    if id in range(0, len(users)):
        return HttpResponse(f'<p>Список пользователей: ["Tom", "Bob", "Sam"] Нумерация с 0</p><h2> Найден пользователь: {users[id]}')
    # если нет, то возвращаем ошибку 404
    else:
        return HttpResponseNotFound("Not Found")
 
def page11_access(request, age):
    # если возраст НЕ входит в диапазон 1-110, посылаем ошибку 400
    if age not in range(1, 111):
        return HttpResponseBadRequest("Некорректные данные. Ошибка 400")
    # если возраст больше 17, то доступ разрешен
    if(age > 17):
        return HttpResponse("Доступ разрешен")
    # если нет, то возвращаем ошибку 403
    else:
        return HttpResponseForbidden("Доступ заблокирован: недостаточно лет. Ошибка 403")
    
class Tree:
  
    def __init__(self, name, age =20, color ='green'):
        self.name = name    
        self.age = age       
        self.color = color       
 
class TreeEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tree):
            return {"name": obj.name, "age": obj.age,  "color": obj.color}
            # return obj.__dict__
        return super().default(obj)

def page12_json(request):
    bob = Tree("Hazel", 12, 'Burgundy')
    return JsonResponse(bob, safe=False, encoder=TreeEncoder) 
    
def page13_set_cookie(request):
    # получаем из строки запроса имя пользователя
    username = request.GET.get("username", "Undefined")
    # создаем объект ответа
    response = HttpResponse(f"Hello {username}")
    # передаем его в куки
    response.set_cookie("username", username)
    return response

def page14_get_cookie(request):
    # получаем куки с ключом username
    username = request.COOKIES.get("username", None)
    if username != None:
        return HttpResponse(f"I know you, {username}!")
    else:
        return HttpResponse('''Who's here? (cookie "username" not found)''')

# def index(request):
#     header = "Данные пользователя"              # обычная переменная
#     langs = ["Python", "Java", "C#"]            # список
#     user ={"name" : "Tom", "age" : 23}          # словарь
#     address = ("Абрикосовая", 23, 45)           # кортеж
  
#     data = {"header": header, "langs": langs, "user": user, "address": address}
#     return render(request, "index.html", context=data)
 
def about(request):
    return render(request, "about.html")   

def skill(request):
    return render(request, "skill.html")   

def cat(request):
    return render(request, "cat.html")   

def awesome(request):
    return render(request, "awesome.html")   




 
