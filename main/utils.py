from django.contrib.auth.decorators import login_required, user_passes_test

# Утилиты для определения ролей пользователей
def is_admin(user):
    return user.is_authenticated and user.is_admin

def is_staff(user):
    return user.is_authenticated and user.is_staff

# Декораторы для авторизации
admin_required = user_passes_test(is_admin)
staff_required = user_passes_test(is_staff)