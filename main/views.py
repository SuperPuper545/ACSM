from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from main.forms import StaffForm, VisitForm, AddStaffForm, WorkScheduleForm, AddWorkScheduleForm, PostsForm, \
    AddPostsForm, DivisionsForm, AddDivisionsForm, AddVisitForm, AddPatternsForm, PatternsForm, \
    AddExplanatoryNotesForm, \
    ExplanatoryNotesForm, TasksForm, AddTasksForm, AddOperatorsForm, OperatorsForm, AddDocsForm, DocsForm, \
    RegistrationForm
from main.models import Staff, Visiting, WorkSchedule, Posts, Divisions, Patterns, ExplanatoryNotes, Tasks, Operators, \
    Docs

'''
Распределение ролей
'''


def superuser_check(user):
    return user.is_superuser


def staff_check(user):
    return user.is_staff


'''
Представления связанные с авторизацией, а именно:
Регистрация, Вход, Информация
'''


# Авторизация
def view_authorization(request):
    if request.method == 'POST':
        # Если запрос отправлен методом POST, создаем экземпляр формы
        form = AuthenticationForm(request, request.POST)
        # Проверяем, валидна ли форма
        if form.is_valid():
            # Получаем очищенные данные из формы (введенные пользователем)
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                # Выполняем вход пользователя
                login(request, user)
                if superuser_check(user):
                    return redirect('main:acms_personal')
                # Иначе, если пользователь является сотрудником
                elif staff_check(user):
                    # Перенаправляем на страницу информации о пользователе
                    return redirect('main:user_info')
    else:
        # Если запрос не отправлен методом POST, создаем пустую форму аутентификации
        form = AuthenticationForm()

    # Рендерим HTML-шаблон страницы аутентификации, передавая форму в контексте
    return render(request, 'authentication_page/authorization_form.html', {'form': form})


# Регистрация
def registration(request):
    # Проверяем метод запроса (GET или POST)
    if request.method == 'POST':
        # Если запрос отправлен методом POST, создаем экземпляр формы регистрации
        # и заполняем его данными из запроса, включая загруженные файлы (если они есть)
        form = RegistrationForm(request.POST, request.FILES)
        # Проверяем, валидна ли форма
        if form.is_valid():
            # Если форма валидна, сохраняем данные из формы в базу данных
            form.save()
            # После успешной регистрации перенаправляем пользователя на ту же страницу,
            # с которой он отправил запрос
            return HttpResponseRedirect(request.path_info)
    else:
        # Если запрос не отправлен методом POST, создаем пустую форму регистрации
        form = RegistrationForm()

    # Создаем контекст, содержащий форму, чтобы передать ее в HTML-шаблон
    context = {
        'form': form,
    }
    # Отображаем HTML-шаблон для регистрации, передавая контекст
    return render(request, 'authentication_page/registration_form.html', context)


# Информация
def information(request):
    # Отображение HTML-шаблона 'information_form.html'
    return render(request, 'authentication_page/information_form.html')


'''
Формы для пользователя
'''


def err(request):
    return render(request, 'acms_page/404.html')


# Это представление доступно только сотрудникам, которые прошли проверку staff_check.
# Если пользователь не прошел проверку, его перенаправят на страницу с ошибкой /404.
@user_passes_test(staff_check, login_url='/404')
def user_info(request):
    # Отображение HTML-шаблона 'user/asd.html'
    return render(request, 'user/asd.html')


@user_passes_test(staff_check, login_url='/404')
def user_info(request):
    # Получение текущего пользователя и передача его в контекст.
    staff_member = request.user
    context = {
        'staff_member': staff_member
    }
    # Отображение HTML-шаблона с данными о текущем пользователе.
    return render(request, 'user/asd.html', context)


@user_passes_test(staff_check, login_url='/404')
def fellow(request):
    # Получение всех объектов Staff и передача их в контекст.
    staff = Staff.objects.all()

    context = {
        "staff": staff,
    }
    # Отображение HTML-шаблона с некоторыми данными о всех сотрудниках.
    return render(request, 'user/fellow.html', context)


@user_passes_test(superuser_check, login_url='/404')
def acms_personal(request):
    staff = Staff.objects.all()
    pattern = Patterns.objects.all()
    divisions = Divisions.objects.all()
    posts = Posts.objects.all()

    context = {
        "staff": staff,
        "pattern": pattern,
        "divisions": divisions,
        "posts": posts,
    }

    return render(request, 'acms_page/index.html', context)


'''
Представления связанные с сотрудниками, а именно:
Добавление, Удаление, Изменение сотрудника
'''


@user_passes_test(superuser_check, login_url='/404')
def staff_detail(request, employee_slug):
    employee = get_object_or_404(Staff, employee_slug=employee_slug)
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            # Сначала сохраняем форму, чтобы получить обновленные данные сотрудника
            employee = form.save(commit=False)
            # Обновляем slug с учетом id
            employee.employee_slug = slugify(employee.id)
            employee.save()
            # Перенаправляем пользователя на страницу деталей с новым slug
            return redirect('main:staff_detail', employee_slug=employee.employee_slug)
    else:
        form = StaffForm(instance=employee)
    # Контекста для формы изменения
    context = {
        'form': form,
        'employee': employee,
    }
    return render(request, 'acms_page/staff/employee_detail.html', context)


@user_passes_test(superuser_check, login_url='/404')
def add_staff(request):
    if request.method == 'POST':
        form_add = AddStaffForm(request.POST, request.FILES)
        if form_add.is_valid():
            form_add.save()
            return redirect('main:acms_personal')  # Перенаправляем на страницу списка сотрудников
    else:
        form_add = AddStaffForm()
    # Контекст для формы добавления
    context = {
        'form_add': form_add,
    }

    return render(request, 'acms_page/staff/add_staff.html', context)


def delete_staff(request, staff_id):
    # Полное удаление объекта
    staff = get_object_or_404(Staff, id=staff_id)
    staff.delete()
    return redirect('main:acms_personal')


'''
Формы связанные с учётом времени, а именно:
Добавление, Удаление, Изменение времени
'''


@user_passes_test(superuser_check, login_url='/404')
def work_schedule_detail(request, time_slug):
    work_schedule = get_object_or_404(WorkSchedule, time_slug=time_slug)
    if request.method == 'POST':
        form = WorkScheduleForm(request.POST, instance=work_schedule)
        if form.is_valid():
            form.save()
            return redirect('main:work_schedule_detail', time_slug=work_schedule.time_slug)
    else:
        form = WorkScheduleForm(instance=work_schedule)

    context = {
        'form': form,
        'work_schedule': work_schedule,
    }
    return render(request, 'acms_page/work_schedule/work_schedule_detail.html', context)


@user_passes_test(superuser_check, login_url='/404')
def add_work_schedule(request):
    if request.method == 'POST':
        form_add = AddWorkScheduleForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            return redirect('main:acms_clock')
    else:
        form_add = AddWorkScheduleForm()

    context = {
        'form_add': form_add,
    }

    return render(request, 'acms_page/work_schedule/add_work_schedule.html', context)


def delete_work_schedule(request, time_slug):
    work_schedule = get_object_or_404(WorkSchedule, time_slug=time_slug)
    work_schedule.delete()
    return redirect('main:acms_clock')


'''
Формы связанные с подразделениями, а именно:
Объявления, Удаление, Изменение подразделений
'''


@user_passes_test(superuser_check, login_url='/404')
def division_detail(request, division_slug):
    divisions = get_object_or_404(Divisions, division_slug=division_slug)
    if request.method == 'POST':
        form = DivisionsForm(request.POST, instance=divisions)
        if form.is_valid():
            form.save()
            return redirect('main:division_detail', division_slug=divisions.division_slug)
    else:
        form = DivisionsForm(instance=divisions)

    context = {
        'form': form,
        'divisions': divisions,
    }
    return render(request, 'acms_page/division/division_detail.html', context)


@user_passes_test(superuser_check, login_url='/404')
def add_division(request):
    if request.method == 'POST':
        form_add = AddDivisionsForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            return redirect('main:acms_personal')
    else:
        form_add = AddDivisionsForm()

    context = {
        'form_add': form_add,
    }

    return render(request, 'acms_page/division/add_division.html', context)


def delete_division(request, division_slug):
    divisions = get_object_or_404(Divisions, division_slug=division_slug)
    divisions.delete()
    return redirect('main:acms_personal')


'''
Формы связанные с подразделениями, а именно:
Объявления, Удаление, Изменение должностей
'''


@user_passes_test(superuser_check, login_url='/404')
def post_detail(request, post_slug):
    posts = get_object_or_404(Posts, post_slug=post_slug)
    if request.method == 'POST':
        form = PostsForm(request.POST, instance=posts)
        if form.is_valid():
            form.save()
            return redirect('main:post_detail', post_slug=posts.post_slug)
    else:
        form = PostsForm(instance=posts)

    context = {
        'form': form,
        'posts': posts,
    }
    return render(request, 'acms_page/post/posts_detail.html', context)


@user_passes_test(superuser_check, login_url='/404')
def add_post(request):
    if request.method == 'POST':
        form_add = AddPostsForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            return redirect('main:acms_personal')
    else:
        form_add = AddPostsForm()

    context = {
        'form_add': form_add,
    }

    return render(request, 'acms_page/post/add_post.html', context)


def delete_post(request, post_slug):
    posts = get_object_or_404(Posts, post_slug=post_slug)
    posts.delete()
    return redirect('main:acms_personal')


@user_passes_test(superuser_check, login_url='/404')
def acms_clock(request):
    visitor = Visiting.objects.all()
    notes = ExplanatoryNotes.objects.all()
    workschedule = WorkSchedule.objects.all()

    context = {
        "visitor": visitor,
        "workschedule": workschedule,
        "notes": notes,
    }

    return render(request, 'acms_page/clock.html', context)


'''
Формы связанные с посетителем, а именно:
Добавление, Удаление, Изменение посетителя
'''


@user_passes_test(superuser_check, login_url='/404')
def add_visitor(request):
    if request.method == 'POST':
        form_add = AddVisitForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            return redirect('main:acms_clock')
    else:
        form_add = AddVisitForm()

    context = {
        'form_add': form_add,
    }

    return render(request, 'acms_page/visitor/add_visitor.html', context)


@user_passes_test(superuser_check, login_url='/404')
def visitor_detail(request, visitor_slug):
    visitor = get_object_or_404(Visiting, visitor_slug=visitor_slug)
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            return redirect('main:visitor_detail', visitor_slug=visitor.visitor_slug)
    else:
        form = VisitForm(instance=visitor)

    context = {
        'form': form,
        'visitor': visitor,
    }

    return render(request, 'acms_page/visitor/visitor_detail.html', context)


def delete_visitor(request, visitor_slug):
    visitor = get_object_or_404(Visiting, visitor_slug=visitor_slug)
    visitor.delete()
    return redirect('main:acms_clock')


'''
Формы связанные с шаблонами, а именно:
Добавление, Удаление, Изменение шаблона
'''


@user_passes_test(superuser_check, login_url='/404')
def add_pattern(request):
    if request.method == 'POST':
        form_add = AddPatternsForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            return redirect('main:acms_personal')
    else:
        form_add = AddPatternsForm()

    context = {
        'form_add': form_add,
    }

    return render(request, 'acms_page/pattern/add_pattern.html', context)


@user_passes_test(superuser_check, login_url='/404')
def pattern_detail(request, pattern_slug):
    pattern = get_object_or_404(Patterns, pattern_slug=pattern_slug)
    if request.method == 'POST':
        form = PatternsForm(request.POST, instance=pattern)
        if form.is_valid():
            form.save()
            return redirect('main:pattern_detail', pattern_slug=pattern.pattern_slug)
    else:
        form = PatternsForm(instance=pattern)

    context = {
        'form': form,
        'pattern': pattern,
    }

    return render(request, 'acms_page/pattern/pattern_detail.html', context)


def delete_pattern(request, pattern_slug):
    pattern = get_object_or_404(Patterns, pattern_slug=pattern_slug)
    pattern.delete()
    return redirect('main:acms_personal')


'''
Формы связанные с шаблонами, а именно:
Добавление, Удаление, Изменение шаблона
'''


@user_passes_test(superuser_check, login_url='/404')
def add_explanatorynotes(request):
    if request.method == 'POST':
        form_add = AddExplanatoryNotesForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            return redirect('main:acms_clock')
    else:
        form_add = AddExplanatoryNotesForm()

    context = {
        'form_add': form_add,
    }

    return render(request, 'acms_page/explanatorynotes/add_explanatorynotes.html', context)


@user_passes_test(superuser_check, login_url='/path/to/404/')
def explanatorynotes_detail(request, explanatory_slug):
    notes = get_object_or_404(ExplanatoryNotes, explanatory_slug=explanatory_slug)
    if request.method == 'POST':
        form = ExplanatoryNotesForm(request.POST, instance=notes)
        if form.is_valid():
            form.save()
            return redirect('main:explanatorynotes_detail', explanatory_slug=notes.explanatory_slug)
    else:
        form = ExplanatoryNotesForm(instance=notes)

    context = {
        'form': form,
        'notes': notes,
    }

    return render(request, 'acms_page/explanatorynotes/explanatorynotes_detail.html', context)


def delete_explanatorynotes(request, explanatory_slug):
    explanatorynotes = get_object_or_404(ExplanatoryNotes, explanatory_slug=explanatory_slug)
    explanatorynotes.delete()
    return redirect('main:acms_clock')


@user_passes_test(superuser_check, login_url='/404')
def acms_monitoring(request):
    return render(request, 'acms_page/monitoring.html')


@user_passes_test(superuser_check, login_url='/404')
def acms_settings(request):
    tasks = Tasks.objects.all()
    operators = Operators.objects.all()
    docs = Docs.objects.all()

    context = {
        "tasks": tasks,
        "operators": operators,
        "docs": docs,
    }

    return render(request, 'acms_page/settings.html', context)


'''
Формы связанные с задачами, а именно:
Добавление, Удаление, Изменение задачи
'''


@user_passes_test(superuser_check, login_url='/404')
def add_task(request):
    if request.method == 'POST':
        form_add = AddTasksForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            return redirect('main:acms_settings')
    else:
        form_add = AddTasksForm()

    context = {
        'form_add': form_add,
    }

    return render(request, 'acms_page/tasks/add_tasks.html', context)


@user_passes_test(superuser_check, login_url='/404')
def task_detail(request, task_slug):
    tasks = get_object_or_404(Tasks, task_slug=task_slug)
    if request.method == 'POST':
        form = TasksForm(request.POST, instance=tasks)
        if form.is_valid():
            form.save()
            return redirect('main:task_detail', task_slug=tasks.task_slug)
    else:
        form = TasksForm(instance=tasks)

    context = {
        'form': form,
        'tasks': tasks,
    }

    return render(request, 'acms_page/tasks/tasks_detail.html', context)


def delete_task(request, task_slug):
    tasks = get_object_or_404(Tasks, task_slug=task_slug)
    tasks.delete()
    return redirect('main:acms_settings')


'''
Формы связанные с задачами, а именно:
Добавление, Удаление, Изменение задачи
'''


@user_passes_test(superuser_check, login_url='/404')
def add_operator(request):
    if request.method == 'POST':
        form_add = AddOperatorsForm(request.POST)
        if form_add.is_valid():
            form_add.save()
            return redirect('main:acms_settings')
    else:
        form_add = AddOperatorsForm()

    context = {
        'form_add': form_add,
    }

    return render(request, 'acms_page/operators/add_operator.html', context)


@user_passes_test(superuser_check, login_url='/404')
def operator_detail(request, operator_slug):
    operators = get_object_or_404(Operators, operator_slug=operator_slug)
    if request.method == 'POST':
        form = OperatorsForm(request.POST, instance=operators)
        if form.is_valid():
            form.save()
            return redirect('main:operator_detail', operator_slug=operators.operator_slug)
    else:
        form = OperatorsForm(instance=operators)

    context = {
        'form': form,
        'operators': operators,
    }

    return render(request, 'acms_page/operators/operator_detail.html', context)


def delete_operator(request, operator_slug):
    operator = get_object_or_404(Operators, operator_slug=operator_slug)

    # Начало транзакции
    with transaction.atomic():
        if operator.employee:
            # Сброс прав перед удалением оператора
            employee = operator.employee
            employee.is_superuser = False
            employee.is_admin = False
            employee.save()

        operator.delete()

    return redirect('main:acms_settings')


'''
Формы связанные с задачами, а именно:
Добавление, Удаление, Изменение задачи
'''


@user_passes_test(superuser_check, login_url='/404')
def add_doc(request):
    if request.method == 'POST':
        form_add = AddDocsForm(request.POST, request.FILES)
        if form_add.is_valid():
            form_add.save()
            return redirect('main:acms_settings')
    else:
        form_add = AddDocsForm()

    context = {
        'form_add': form_add,
    }

    return render(request, 'acms_page/docs/add_doc.html', context)


@user_passes_test(superuser_check, login_url='/404')
def doc_detail(request, doc_slug):
    docs = get_object_or_404(Docs, doc_slug=doc_slug)
    if request.method == 'POST':
        form = DocsForm(request.POST, request.FILES, instance=docs)
        if form.is_valid():
            form.save()
            return redirect('main:doc_detail', doc_slug=docs.doc_slug)
    else:
        form = DocsForm(instance=docs)

    context = {
        'form': form,
        'docs': docs,
    }

    return render(request, 'acms_page/docs/doc_detail.html', context)


def delete_doc(request, doc_slug):
    docs = get_object_or_404(Docs, doc_slug=doc_slug)
    docs.delete()
    return redirect('main:acms_settings')
