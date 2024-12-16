from django.http import HttpResponse, \
HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.template.response import TemplateResponse
from .forms import UserForm, FieldTypesForm
from .models import Person
import asyncio
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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
    
def page15_user_form(request):
    return render(request, "user_form.html")   

def page15_postuser(request):
    # получаем из данных запроса POST отправленные через форму данные
    name = request.POST.get("name", "Undefined")
    age = request.POST.get("age", 1)
    langs = request.POST.getlist("languages", ["python"])
    colors = request.POST.getlist("colors", ["Pink"])    
    return HttpResponse(f"""
                <div>Name: {name}  Age: {age}</div>
                <div>Languages: {langs}</div>
                <div>Colors: {colors}</div>
            """)

def page16_user_form_django(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            name = request.POST.get("name")
            age = request.POST.get("age")
            return HttpResponse(f"<h2>Привет, {name}, твой возраст: {age}.</h2>")
        else:
            return HttpResponse("Invalid data")
    else:
        userform = UserForm(field_order = ["comment", "age", "name"])
        userform_FieldTypes = FieldTypesForm()
        return render(request, "user_form_django.html", {"form": userform, "FieldTypesForm": userform_FieldTypes})
    
def page17_select(request):
    # получаем все объекты
    people = Person.objects.all() 
    # получаем объекты с именем Tom
    people = people.filter(name = "Tom") 
    # получаем объекты с возрастом, равным 31
    people = people.filter(age = 31)
    html_code = f'<p>Запрос:</p><p>{people.query}</p>'   
    html_code = html_code + f'<p>Результат запроса:</p>' 
    # здесь происходит выполнения запроса в БД
    for person in people:
       html_code = html_code + f'<p>{person.id}.{person.name} - {person.age}</p>'
    return HttpResponse(html_code)

def page18_create_record(request):
    return render(request, "create_person.html")   

async def acreate_person(name, age):
    new_person = await Person.objects.acreate(name=name, age=age)  

def create_person(request):
    # получаем из данных запроса POST отправленные через форму данные
    name = request.POST.get("name")
    age = request.POST.get("age")
    if request.POST:
        if '_' in request.POST:
            new_person = Person.objects.create(name=name, age=age)
            return HttpResponse(f"""
                                <div>Создана новая запись Person</div>
                                <div>Name: {new_person.name}  Age: {new_person.age}</div> 
                                """)
        elif '_async' in request.POST:
            asyncio.run(acreate_person(name, age)) 
            return HttpResponse(f"<div>Запущен процесс создания записи Person</div>")
        elif '_save' in request.POST:
            new_person = Person(name=name, age=age)
            new_person.save()
            return HttpResponse(f"""
                                <div>Создана новая запись Person</div>
                                <div>Name: {new_person.name}  Age: {new_person.age} id: {new_person.id}</div> 
                                """)
        elif '_bulk_create' in request.POST:
            age1 = int(age) + 1
            age2 = int(age) + 2
            people = Person.objects.bulk_create([
                Person(name=name + '_1', age=age1),
                Person(name=name + '_2', age=age2),
            ])
            http_code = ''
            for person in people:
                http_code = http_code + f"<p>id: {person.id} Name: {person.name} Age: {person.age}</p>"
            return HttpResponse(http_code)
    
def page19_get_records(request):
    return render(request, "get_person.html")   

def get_person(request):    
    name = request.POST.get("name")
    age = request.POST.get("age")
    if request.POST:
        if 'get' in request.POST: 
            http_code = '<h2>get</h2>'              
            try:
                http_code = f"<p>filter name: {name} filter age: {age}</p>"
                if name != None and age != None and name != '' and age != '':                    
                    person = Person.objects.get(name=name, age=age)
                    http_code = http_code + f"<p>id: {person.id} name: {person.name} age: {person.age}</p>"   
                elif name != None and name != '':     
                    person = Person.objects.get(name=name)
                    http_code = http_code + f"<p>id: {person.id} name: {person.name} age: {person.age}</p>"   
                elif age != None and age != '':     
                    person = Person.objects.get(age=age)
                    http_code = http_code + f"<p>id: {person.id} name: {person.name} age: {person.age}</p>"       
                else:
                    http_code = http_code + "<p>Пустой параметр</p>"
            except ObjectDoesNotExist:
                http_code = http_code + "<p>Объект не существует</p>"
            except MultipleObjectsReturned:
                http_code = http_code + "<p>Найдено более одного объекта</p>"
            return HttpResponse(http_code) 
        elif 'get_or_create' in request.POST: 
            http_code = '<h2>get_or_create</h2>'      
            try:
                http_code = http_code + f"<p>filter name: {name} filter age: {age}</p>"
                if name != None and age != None and name != '' and age != '':    
                    new_person, created = Person.objects.get_or_create(name=name, age=age)
                    if created:
                        http_code = http_code + '<p>Создана новая запись</p>'
                    else:
                        http_code = http_code + '<p>найдена существующая запись</p>'
                    http_code = http_code + f"<p>id: {new_person.id} name: {new_person.name} age: {new_person.age}</p>"       
                else:
                    http_code = http_code + "<p>Пустой параметр</p>"

            except MultipleObjectsReturned:
                http_code = http_code + "<p>Найдено более одного объекта</p>"
            return HttpResponse(http_code) 
        elif 'all' in request.POST: 
            http_code = '<h2>all</h2>'   
            people = Person.objects.all() 
            for person in people:
                http_code = http_code + f"<p>id: {person.id} name: {person.name} age: {person.age}</p>"       
            return HttpResponse(http_code) 
        elif 'filter' in request.POST: 
            http_code = '<h2>filter</h2>'  
            http_code = http_code + f"<p>filter name: {name} filter age: {age}</p>"
            if name != None and age != None and name != '' and age != '':   
                people = Person.objects.filter(name=name, age=age)
                for person in people:
                    http_code = http_code + f"<p>id: {person.id} name: {person.name} age: {person.age}</p>"   
            else:
                http_code = http_code + "<p>Пустой параметр</p>"
            return HttpResponse(http_code) 
        elif 'exclude' in request.POST: 
            http_code = '<h2>exclude</h2><p>С указанным именем, но исключая указанный возраст</p><p>... и это не работает ожидаемым образом по неизвестным мне причинам</p>'  
            http_code = http_code + f"<p>filter name: {name} filter age: {age}</p>"
            if name != None and age != None and name != '' and age != '': 
                people = Person.objects.filter(name=name).exclude(age=age)
                for person in people:
                    http_code = http_code + f"<p>id: {person.id} name: {person.name} age: {person.age}</p>"      
            else:
                    http_code = http_code + "<p>Пустой параметр</p>"
            return HttpResponse(http_code) 
        elif 'in_bulk' in request.POST: 
            http_code = '<h2>in_bulk</h2>'       
            # http_code = f"<p>filter name: {name} filter age: {age}</p>"
            people = Person.objects.in_bulk() 
            for id in people:
                http_code = http_code + f"<p>id: {people[id].id} name: {people[id].name} age: {people[id].age}</p>"  
            return HttpResponse(http_code) 
        elif 'offset_limit' in request.POST:             
            http_code = '<h2>offset_limit</h2><p>Выбираем первые 5 объектов, пропуская первые 5 объектов.</p>'    
            people = Person.objects.all()[5:10]
            for person in people:
                http_code = http_code + f"<p>id: {person.id} name: {person.name} age: {person.age}</p>"  
            return HttpResponse(http_code) 
        
def page20_py_types(request):    
    http_code = ''
    a = True
    http_code = http_code + f'<h2>bool</h2><p>code: a = True<br>a = {a}<br>a.__class__.__name__ = {a.__class__.__name__}</p>'
    a = 1
    http_code = http_code + f'<h2>int</h2><p>code: a = 1<br>a = {a}<br>a.__class__.__name__ = {a.__class__.__name__}</p>'
    a = 0b1011
    http_code = http_code + f'<p>code: a = 0b1011<br>a = {a:b}<br>a.__class__.__name__ = {a.__class__.__name__}<br>description: int в двоичной системе</p>'
    a = 0o17
    http_code = http_code + f'<p>code: a = 0o17<br>a = {a:o}<br>a.__class__.__name__ = {a.__class__.__name__}<br>description: int в восьмиричной системе</p>'
    a = 0xA1
    http_code = http_code + f'<p>code: a = 0xA1<br>a = {a:x}<br>a.__class__.__name__ = {a.__class__.__name__}<br>description: int в шестнадцатеричной системе</p>'
    a = -1.23
    http_code = http_code + f'<h2>float</h2><p>code: a = -1.23<br>a = {a}<br>a.__class__.__name__ = {a.__class__.__name__}<br>description: Число float может иметь только 18 значимых символов</p>'
    a = .23
    http_code = http_code + f'<p>code: a = .23<br>a = {a}<br>a.__class__.__name__ = {a.__class__.__name__}</p>'
    a = 3.9e3
    http_code = http_code + f'<p>code: a = 3.9e3<br>a = {a}<br>a.__class__.__name__ = {a.__class__.__name__}</p>'
    a = ("Laudate omnes gentes laudate "
         "Magnificat in secula ")
    http_code = http_code + f'<h2>str</h2><p>code: a = ("Laudate omnes gentes laudate "<br>"Magnificat in secula ")<br>a = {a}<br>a.__class__.__name__ = {a.__class__.__name__}</p>'
    a = "Message:\n\"Hello World\""
    http_code = http_code + r'<p>code: a = "Message:\n\"Hello World\""' + f'<br>a = {a}<br>a.__class__.__name__ = {a.__class__.__name__}</p>'    
    return HttpResponse(http_code)
           
def page21_py_arithmetic_operations(request):  
    http_code = ''
    a = 2 + 2
    http_code = http_code + f'<h2>+</h2><p>code: a = 2 + 2<br>a = {a}</p>'
    a += 2
    http_code = http_code + f'<p>code: a += 2<br>a = {a}<br>description: Присвоение результата сложения</p>'
    a = 10 - 10
    http_code = http_code + f'<h2>-</h2><p>code: a = 10 - 10<br>a = {a}</p>'
    a -= 3
    http_code = http_code + f'<p>code: a -= 3<br>a = {a}<br>description: Присвоение результата вычитания</p>'
    a = 10 * 10
    http_code = http_code + f'<h2>*</h2><p>code: a = 10 * 10<br>a = {a}</p>'
    a *= 0.36
    http_code = http_code + f'<p>code: a *= 0.36<br>a = {a}<br>description: Присвоение результата умножения</p>'
    a = 10 / 10
    http_code = http_code + f'<h2>/</h2><p>code: a = 10 / 10<br>a = {a}</p>'
    a = 2.0001 / 5
    http_code = http_code + f'<p>code: a = 2.0001 / 5<br>a = {a}</p><br>description: Погрешности никто не отменял'
    a /= 3
    http_code = http_code + f'<p>code: a /= 3<br>a = {a}<br>description: Присвоение результата деления</p>'
    a = 7 // 2
    http_code = http_code + f'<h2>//</h2><p>code: a = 7 // 2<br>a = {a}<br>description: Целочисленное деление двух чисел</p>'
    a //= 3
    http_code = http_code + f'<p>code: a //= 3<br>a = {a}<br>description: Присвоение результата целочисленного деления</p>'
    a = 7 ** 2
    http_code = http_code + f'<h2>**</h2><p>code: a = 7 ** 2<br>a = {a}<br>description: Возведение в степень</p>'
    a **= 3
    http_code = http_code + f'<p>code: a = 7 ** 2<br>a = {a}<br>description: Присвоение степени числа</p>'
    a = 11 % 3
    http_code = http_code + f'<h2>%</h2><p>code: a = 11 % 3<br>a = {a}<br>description: Получение остатка от деления</p>'
    a %= 2
    http_code = http_code + f'<p>code: a %= 2<br>a = {a}<br>description: Присвоение остатка от деления</p>'
    http_code = http_code + f'<h2>round()</h2>'
    a = round(2.49)
    http_code = http_code + f'<p>code: a = round(2.49)<br>a = {a}<br>description: Округление до ближайшего целого 2</p>'
    a = round(2.51)
    http_code = http_code + f'<p>code: a = round(2.51)<br>a = {a}<br>description: Округление до ближайшего целого 3</p>'
    http_code = http_code + f'<p>Если округляемая часть равна одинаково удалена от двух целых чисел, то округление идет к ближайшему четному</p>'
    a = round(2.5)
    http_code = http_code + f'<p>code: a = round(2.5)<br>a = {a}<br>description: 2 - ближайшее четное</p>'
    a = round(3.5)
    http_code = http_code + f'<p>code: a = round(3.5)<br>a = {a}<br>description: 4 - ближайшее четное</p>' 
    a = round(2.655, 2)
    http_code = http_code + f'<p>code: a = round(2.655, 2)<br>a = {a}<br>description: 2.65 - округление не до четного. Потомучто.</p>'
    return HttpResponse(http_code)       

def page22_py_in(request):  
    http_code = ''
    http_code = http_code + f'<h2>in</h2><p>code: "hello" in "hello world!"<br>a = {"hello" in "hello world!"}<br>description: Можно искать подстроку с помощью in</p>'
    http_code = http_code + f'<p>code: "gold" in "hello world!"<br>a = {"gold" in "hello world!"}</p>'
    return HttpResponse(http_code)  

def page23_py_function_parameters(request):  
    http_code = ''
    def boo(*, arg1): return arg1
    a = boo(arg1=1)    
    http_code = http_code + f'<p>code:<br>"def boo(*, arg1): return arg1 <br> a = boo(arg1=1)"<br>a = {a}<br>description: После "*, " идут именованные параметры</p>'
    def bar(arg1, /): return arg1
    a = bar(2) 
    http_code = http_code + f'<p>code:<br>"def bar(arg1, /): return arg1 <br> a = bar(2)"<br>a = {a}<br>description: Параметры до символа ", /"  являются позиционными</p>'
    def foo(arg1, /, arg2 = 10, *, arg3): return arg1 + arg2 + arg3
    a = foo(1, 2, arg3 = 3) 
    http_code = http_code + f'<p>code:<br>"def foo(arg1, /, arg2 = 10, *, arg3): return arg1 + arg2 + arg3 <br> a = foo(1, 2, arg3 = 3)"<br>a = {a}<br>description: Позиционный обязательный / позиционный необзятальный * именованный'
    a = foo(1, arg3 = 3) 
    http_code = http_code + f'<br>a = foo(1, arg3 = 3)<br>a = {a}'
    a = foo(1, arg3 = 3, arg2 = 7) 
    http_code = http_code + f'<br>a = foo(1, arg3 = 3, arg2 = 7)<br>a = {a}</p>'
    def far(*arg1):
        result = 0
        for i in arg1:
            result += i
        return result
    a = far(11, 12, 13)       
    http_code = http_code + f'<p>code:<br>def far(*arg1):<br> for i in arg1:<br>result += i<br>a = far(11, 12, 13)<br>return result"<br>a = {a}<br>description: * перед именем параметра означает неопределенное количество значений</p>'
    return HttpResponse(http_code)  

def page24_py_lambda(request):  
    http_code = ''
    def boo(a, b):
        return a * b
    def select_operation(choice):
        if choice == 1:
            return lambda a, b: a + b
        elif choice == 2:
            return boo
    operation = select_operation(1) 
    a = operation(3, 2)
    http_code = http_code + f'''<p><pre>code:
def boo(a, b):
    return a * b
def select_operation(choice):
    if choice == 1:
        return lambda a, b: a + b
    elif choice == 2:
        eturn boo
operation = select_operation(1) 
a = operation(3, 2)<pre>a = {a}</p>'''
    operation = select_operation(2) 
    a = operation(3, 2)
    http_code = http_code + f'<p>operation = select_operation(2)<br>a = operation(3, 2)<br>a = {a}</p>'   
    return HttpResponse(http_code)  

def page25_py_global_nonlocal(request):  
    http_code = ''
    local_a = 'local_a'
    def boo():
        nonlocal local_a
        local_a = 'local_a`'
    boo()
    http_code = http_code + f'''<h2>nonlocal</h2><p><pre>code:
local_a = 'local_a'
def boo():
    nonlocal local_a
    local_a = 'local_a`'
boo()<pre>local_a = {local_a}<br>description: nonlocal позволяет работать с переменными в ближайшей видимости</p>'''  
    def bar():
        global global_b
        global_b = 'global_b'
    bar()
    http_code = http_code + f'''<h2>global</h2><p><pre>code:
def bar():
    global global_b
    global_b = 'global_b'
bar()<pre>global_b = {global_b}<br>description: global позволяет создавать и обращаться к глобальным переменным</p>'''
    return HttpResponse(http_code)  

def page26_py_string(request): 
    http_code = '<h2>5.1</h2><p>Напишите с заглавной буквы слово, которое начинается с буквы m:</p>'
    song = """When an eel grabs your arm,
And it causes great harm, 
That's - a moray!"""
    http_code = http_code + f'<p><pre>{song}</pre></p>'
    result = song.replace(' m', ' M')
    http_code = http_code +"<p>code:</p><p><pre>result = song.replace(' m', ' M')</pre></p>"
    http_code = http_code + f'<p>result:</p><p><pre>{result}</pre></p>'  
    http_code = http_code + '<h2>5.2</h2><p>Выведите на экран все вопросы из списка, а так же правильные ответы в таком виде:</p>'
    http_code = http_code + "<p>Q: вопрос</p><p>A: ответ</p>"
    questions = [ 
"We don't serve strings around here. Are you a string?", 
"What is said on Father's Day in the forest?", 
"What makes the sound 'Sis! Boom! Bah!'?" ] 
    answers = [ "An exploding sheep.", 
"No, I'm a frayed knot.", 
"'Pop!' goes the weasel." ]  
    http_code = http_code + f'<p>{questions =}</p>'
    http_code = http_code + f'<p>{answers =}</p>'
    result = ''
    q_a = ((0, 1), (1, 2), (2, 0)) 
    for q, a in q_a:
        result = result + f'Q: {questions[q]}\n'
        result = result + f'A: {answers[a]}\n'
    http_code = http_code +'''<p>code:</p><p>
<pre>result = ''
q_a = ((0, 1), (1, 2), (2, 0)) 
for q, a in q_a:
    result = result + f'Q: {questions[q]}\\n'
    result = result + f'A: {answers[a]}\\n'</pre></p>'''
    http_code = http_code + f'<p>result:</p><p><pre>{result}</pre></p>'  
    base_name = ["Spitz", "Duck", "Pumpkin"] 
    result = ''
    for item in base_name:
        result = result + '%sy Mc%sface\n' % (item, item)
    http_code = http_code + '<h2>5.4</h2><p>Форматирование в старом стиле</p>'
    http_code = http_code +'''<p>code:</p><p>
<pre>for item in base_name:
result = result + '%sy Mc%sface\\n' % (item, item)</pre></p>'''
    http_code = http_code + f'<p>result:</p><p><pre>{result}</pre></p>'  
    result = ''
    for item in base_name:
        result = result + '{}y Mc{}face\n'.format(item, item)
    http_code = http_code + '<h2>5.5</h2><p>Форматирование в новом стиле</p>'
    http_code = http_code +'''<p>code:</p><p>
<pre>for item in base_name:
result = result + '{}y Mc{}face\\n' % (item, item)</pre></p>'''
    http_code = http_code + f'<p>result:</p><p><pre>{result}</pre></p>'  
    result = ''
    for item in base_name:
        result = result + f'{item} Mc{item}yface\n'
    http_code = http_code + '<h2>5.6</h2><p>Форматирование с использованием f-строк</p>'
    http_code = http_code +'''<p>code:</p><p>
<pre>for item in base_name:
result = result + f'{item}y Mc{item}face\\n'</pre></p>'''
    http_code = http_code + f'<p>result:</p><p><pre>{result}</pre></p>'  

    return HttpResponse(http_code)  

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




 
