from django.contrib import admin
from main.models import Staff, WorkSchedule, Divisions, Posts, Patterns, Visiting, ExplanatoryNotes, Tasks, Operators, \
    Docs

'''
Регистрация модели Подразделения
'''


@admin.register(Divisions)
class DivisionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'division', 'division_number', 'division_description')  # Видимые поля в администрирование
    prepopulated_fields = {'division_slug': ('division',)}  # Конвертация поля подразделения в slug


'''
Регистрация модели График работы
'''


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time')  # Видимые поля в администрирование
    prepopulated_fields = {'time_slug': ('time_name',)}  # Конвертация поля график работы в slug


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'email', 'phone_number', 'dob', 'division', 'time', 'post', 'pattern')
    search_fields = ('fio', 'email', 'phone_number', 'dob')
    prepopulated_fields = {'employee_slug': ('fio',)}


@admin.register(Visiting)
class VisitingAdmin(admin.ModelAdmin):
    prepopulated_fields = {'visitor_slug': ('visitor',)}


@admin.register(Patterns)
class PatternsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'pattern_slug': ('access_pattern',)}


@admin.register(ExplanatoryNotes)
class ExplanatoryNotesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'explanatory_slug': ('doc_type',)}


@admin.register(Operators)
class OperatorsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'operator_slug': ('login',)}


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    prepopulated_fields = {'task_slug': ('name_of_task',)}


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'post_slug': ('post',)}


@admin.register(Docs)
class DocsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'doc_slug': ('doc_name',)}
