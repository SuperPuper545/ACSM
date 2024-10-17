from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ClearableFileInput, TimeInput, DateTimeInput, DateInput

from .models import Staff, Visiting, WorkSchedule, Posts, Divisions, Patterns, ExplanatoryNotes, Tasks, Operators, Docs

'''
Формы для работы с авторизацией пользователей
'''


class StaffLoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email')  # Объявление поля электронной почты
    password = forms.CharField(label='pass')  # Объявление поля пароля

    def clean(self):
        # Получаем введенные пользователем данные из формы
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        # Проверяем, предоставлены ли адрес электронной почты и пароль
        if email is not None and password:
            # Аутентифицируем пользователя
            self.user_cache = authenticate(self.request, email=email, password=password)
            # Если пользователь не аутентифицирован, вызываем ошибку
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                # Проверяем, активен ли пользователь
                self.confirm_login_allowed(self.user_cache)
        # Возвращаем очищенные данные формы
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        # Проверяем, активен ли пользователь, если нет - вызываем исключение
        if not user.is_active:
            raise forms.ValidationError('This account is inactive.', code='inactive')

    def get_user(self):
        # Возвращаем объект пользователя из кэша
        return self.user_cache


'''
Формы для работы с регистрацией сотрудника/пользователя
'''


class RegistrationForm(forms.ModelForm):
    # Поля формы для регистрации нового сотрудника

    # Поле для ввода пароля с использованием виджета PasswordInput
    # и с помощью атрибута placeholder устанавливается подсказка для пользователя
    # Помогает убедиться, что пароль введен надежно
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
                               help_text="Пароль должен содержать минимум 8 букв и быть не слишком простым", )
    # Поле для повторного ввода пароля с аналогичными настройками
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
                                      help_text="Пароли не совпадают")

    class Meta:
        # Определение модели, с которой связана форма
        model = Staff
        # Указание полей модели, которые будут отображаться в форме
        fields = ['fio', 'image', 'password', 'repeat_password', 'email', 'dob', 'division']


'''
Формы для работы с полями сотрудника
'''

class WorkScheduleChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Объединяем название графика и время, чтобы использовать это как подсказку
        return f"{obj.time_name} ({obj.start_time} - {obj.end_time})"


class StaffForm(forms.ModelForm):
    time = WorkScheduleChoiceField(
        queryset=WorkSchedule.objects.all(),
        required=False,
        label="График работы"
    )

    class Meta:
        # Указывает модель, с которой связана форма
        model = Staff
        # Указание полей модели, которые будут отображаться в форме
        fields = ['fio', 'email', 'phone_number', 'dob', 'division', 'time', 'post', 'pattern', 'image']
        # Специальный виджет для удобного отображения поля фото
        widgets = {
            'image': ClearableFileInput(attrs={'clearable': False, 'initial_text': ''}),
            'dob': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


class AddStaffForm(forms.ModelForm):
    time = WorkScheduleChoiceField(
        queryset=WorkSchedule.objects.all(),
        required=False,
        label="График работы"
    )

    class Meta:
        # Указывает модель, с которой связана форма
        model = Staff
        # Указание полей модели, которые будут отображаться в форме
        fields = ['fio', 'email', 'phone_number', 'dob', 'division', 'time', 'post', 'pattern', 'image']
        widgets = {
            'dob': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


'''
Формы для работы с полями времени
'''


class WorkScheduleForm(forms.ModelForm):
    start_time = forms.TimeField(
        label='Тип графика с',
        widget=TimeInput(format='%H:%M', attrs={'type': 'time'})
    )
    end_time = forms.TimeField(
        label='Тип графика до',
        widget=TimeInput(format='%H:%M', attrs={'type': 'time'})
    )

    class Meta:
        model = WorkSchedule
        fields = ['start_time', 'end_time', 'time_name', 'time_description', 'time_status', 'division']


class AddWorkScheduleForm(forms.ModelForm):
    start_time = forms.TimeField(
        label='Тип графика с',
        widget=TimeInput(format='%H:%M', attrs={'type': 'time'})
    )
    end_time = forms.TimeField(
        label='Тип графика до',
        widget=TimeInput(format='%H:%M', attrs={'type': 'time'})
    )

    class Meta:
        model = WorkSchedule
        fields = ['start_time', 'end_time', 'time_name', 'time_description', 'time_status', 'division']


class DeleteWorkScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = []


'''
Формы для работы с полями подразделений
'''


class DivisionsForm(forms.ModelForm):
    class Meta:
        model = Divisions
        fields = ['division', 'division_number', 'division_description']


class AddDivisionsForm(forms.ModelForm):
    class Meta:
        model = Divisions
        fields = ['division', 'division_number', 'division_description']


class DeleteDivisionsForm(forms.ModelForm):
    class Meta:
        model = Divisions
        fields = []


'''
Формы для работы с полями должностей
'''


class PostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['post', 'post_description']


class AddPostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['post', 'post_description']


class DeletePostsForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = []


'''
Формы для работы с посетителями
'''


class VisitForm(forms.ModelForm):

    class Meta:
        model = Visiting
        fields = ['visitor', 'start_date', 'end_date', 'maintainer', 'division']
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(VisitForm, self).__init__(*args, **kwargs)
        # Устанавливаем формат отображения дат в виджетах
        self.fields['start_date'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_date'].input_formats = ('%Y-%m-%dT%H:%M',)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Проверка, что дата начала не позже даты окончания
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Дата начала должна быть раньше даты окончания.")

        return cleaned_data


class AddVisitForm(forms.ModelForm):
    class Meta:
        model = Visiting
        fields = ['visitor', 'start_date', 'end_date', 'maintainer', 'division']
        widgets = {
            'start_date': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_date': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(AddVisitForm, self).__init__(*args, **kwargs)
        # Устанавливаем формат отображения дат в виджетах
        self.fields['start_date'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_date'].input_formats = ('%Y-%m-%dT%H:%M',)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Проверка, что дата начала не позже даты окончания
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Дата начала должна быть раньше даты окончания.")

        return cleaned_data



'''
Формы для работы с пропусками
'''


class PatternsForm(forms.ModelForm):
    class Meta:
        model = Patterns
        fields = ['access_pattern', 'access_description']


class AddPatternsForm(forms.ModelForm):
    class Meta:
        model = Patterns
        fields = ['access_pattern', 'access_description']


'''
Формы для работы с объяснительными
'''


class ExplanatoryNotesForm(forms.ModelForm):
    class Meta:
        model = ExplanatoryNotes
        fields = ['doc_type', 'add_work_hours', 'fine', 'employee']


class AddExplanatoryNotesForm(forms.ModelForm):
    class Meta:
        model = ExplanatoryNotes
        fields = ['doc_type', 'add_work_hours', 'fine', 'employee']


'''
Формы для работы с заданиями
'''


class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name_of_task', 'time_of_cmlt', 'status_task', 'date_task']
        widgets = {
            'date_task': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }


class AddTasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name_of_task', 'time_of_cmlt', 'status_task', 'date_task']
        widgets = {
            'date_task': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }


'''
Формы для работы с операторами
'''


class OperatorsForm(forms.ModelForm):
    class Meta:
        model = Operators
        fields = ['login', 'post_operator', 'operator_description', 'employee']


class AddOperatorsForm(forms.ModelForm):
    class Meta:
        model = Operators
        fields = ['login', 'post_operator', 'operator_description', 'employee']


'''
Формы для работы с документами
'''


class DocsForm(forms.ModelForm):
    class Meta:
        model = Docs
        fields = ['doc_name', 'operator_doc', 'division', 'doc_file']

    def clean_doc_file(self):
        doc_file = self.cleaned_data.get('doc_file')
        if doc_file and not doc_file.name.lower().endswith('.pdf'):
            raise forms.ValidationError('Пожалуйста, загрузите только PDF файл.')
        return doc_file


class AddDocsForm(forms.ModelForm):
    class Meta:
        model = Docs
        fields = ['doc_name', 'operator_doc', 'division', 'doc_file']

    def clean_doc_file(self):
        doc_file = self.cleaned_data.get('doc_file')
        if doc_file and not doc_file.name.lower().endswith('.pdf'):
            raise forms.ValidationError('Пожалуйста, загрузите только PDF файл.')
        return doc_file