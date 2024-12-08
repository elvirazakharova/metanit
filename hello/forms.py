from django import forms
 
class UserForm(forms.Form):
    name = forms.CharField(label="Имя", min_length=2, max_length=20) # ,help_text="Введите свое имя"
    age = forms.IntegerField(label="Возраст", initial=18, min_value=1, max_value=100)
    weight = forms.DecimalField(label="Вес", required=False, min_value=3, max_value=200, decimal_places=2)
    comment = forms.CharField(label="Комментарий", widget=forms.Textarea, required=False)
    field_order = ["age", "name"]

class FieldTypesForm(forms.Form):
    # BooleanField: создает поле <input type="checkbox" >. Возвращает значение Boolean: True - если флажок отмечен и False - если флажок не отмечен.
    BooleanField = forms.BooleanField()
    NullBooleanField = forms.NullBooleanField()
    # Принимает следующие параметры:
    #     max_length: максимальная длина вводимого текста
    #     min_length: минимальная длина вводимого текста
    #     strip: при значении True (по умолчанию) начальные и конечные пробелы удаляются
    #     empty_value: значение, применяемое для представления пустого поля
    CharField = forms.CharField(empty_value ='empty_value', strip =True, widget=forms.FileInput)
    # EmailField: предназначен для ввода адреса электронной почты и применяет те же параметры, что и CharField.
    EmailField = forms.EmailField()
    GenericIPAddressField = forms.GenericIPAddressField()
    RegexField = forms.RegexField(r'r')
    SplitDateTimeField = forms.SplitDateTimeField()
    IntegerField = forms.IntegerField()
    ChoiceField = forms.ChoiceField(choices=((1, "English"), (2, "German"), (3, "French")))
