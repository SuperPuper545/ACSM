from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from main import views
from main.views import delete_staff, user_info


app_name = 'main'

urlpatterns = [
    #Маршрут ошибки
    path('404/', views.err, name='404'),

    # Маршруты для регистрации, отображения информации, входа пользователя
    path('registration/', views.registration, name='registration'),
    path('info/', views.information, name='info'),
    path('login/', views.view_authorization, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('main:login')), name='logout'),

    # Маршрут для авторизованного пользователя
    path('user/', views.user_info, name='user_info'),
    path('fellow/', views.fellow, name='fellow'),

    # Маршруты для отображения главных страниц
    path('', views.acms_personal, name='acms_personal'),
    path('clock/', views.acms_clock, name='acms_clock'),
    path('monitoring/', views.acms_monitoring, name='acms_monitoring'),
    path('settings/', views.acms_settings, name='acms_settings'),

    # Маршруты для добавления, отображения информации, удаления пользователя
    path('add_staff/', views.add_staff, name='add_staff'),
    path('staff/<slug:employee_slug>/', views.staff_detail, name='staff_detail'),
    path('delete_staff/<uuid:staff_id>/', delete_staff, name='delete_staff'),

    # Маршруты для добавления, отображения информации, удаления времени
    path('add_work_schedule/', views.add_work_schedule, name='add_work_schedule'),
    path('work_schedule/<slug:time_slug>/', views.work_schedule_detail, name='work_schedule_detail'),
    path('delete_work_schedule/<slug:time_slug>/', views.delete_work_schedule, name='delete_work_schedule'),

    # Маршруты для объявления, отображения информации, удаления подразделений
    path('add_division/', views.add_division, name='add_division'),
    path('division/<slug:division_slug>/', views.division_detail, name='division_detail'),
    path('delete_division/<slug:division_slug>/', views.delete_division, name='delete_divisions'),

    # Маршруты для объявления, отображения информации, удаления должностей
    path('add_post/', views.add_post, name='add_posts'),
    path('post/<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('delete_post/<slug:post_slug>/', views.delete_post, name='delete_posts'),

    # Маршруты для отображения информации о посетителе
    path('add_visitor/', views.add_visitor, name='add_visitor'),
    path('visitor/<slug:visitor_slug>/', views.visitor_detail, name='visitor_detail'),
    path('delete_visitor/<slug:visitor_slug>/', views.delete_visitor, name='delete_visitor'),

    # Маршруты для отображения информации о шаблоне доступа
    path('add_pattern/', views.add_pattern, name='add_pattern'),
    path('pattern/<slug:pattern_slug>/', views.pattern_detail, name='pattern_detail'),
    path('delete_pattern/<slug:pattern_slug>/', views.delete_pattern, name='delete_pattern'),

    # Маршруты для отображения информации об объяснительных
    path('add_explanatorynotes/', views.add_explanatorynotes, name='add_explanatorynotes'),
    path('explanatorynotes/<slug:explanatory_slug>/', views.explanatorynotes_detail, name='explanatorynotes_detail'),
    path('delete_explanatorynotes/<slug:explanatory_slug>/', views.delete_explanatorynotes, name='delete_explanatorynotes'),

    # Маршруты для отображения информации о заданиях
    path('add_task/', views.add_task, name='add_task'),
    path('tasks/<slug:task_slug>/', views.task_detail, name='task_detail'),
    path('delete_task/<slug:task_slug>/', views.delete_task, name='delete_task'),

    # Маршруты для отображения информации об операторах
    path('add_operator/', views.add_operator, name='add_operator'),
    path('operators/<slug:operator_slug>/', views.operator_detail, name='operator_detail'),
    path('delete_operator/<slug:operator_slug>/', views.delete_operator, name='delete_operator'),

    # Маршруты для отображения информации о документах
    path('add_doc/', views.add_doc, name='add_doc'),
    path('docs/<slug:doc_slug>/', views.doc_detail, name='doc_detail'),
    path('delete_doc/<slug:doc_slug>/', views.delete_doc, name='delete_doc'),
]