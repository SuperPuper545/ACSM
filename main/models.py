import os
import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models, transaction
from django.template.defaultfilters import slugify

from ACMS import settings


class Divisions(models.Model):
    # Значения для подразделений
    DIVISIONS = [
        ('Руководство', 'Руководство'),
        ('Отдел разработки', 'Отдел разработки'),
        ('Отдел бухгалтерии', 'Отдел бухгалтерии'),
        ('Отдел экономики', 'Отдел экономики'),
    ]
    # Подразделения
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    division = models.CharField(max_length=75, choices=DIVISIONS, default="ГД", verbose_name='Подразделение')
    division_number = models.CharField(max_length=12, blank=True, null=True, verbose_name='Подразделение - телефон')
    division_description = models.CharField(max_length=100, blank=True, null=True,
                                            verbose_name='Описание подразделения')
    division_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')

    # Представления для администрирования
    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def save(self, *args, **kwargs):
        # Генерируем slug из поля id
        self.division_slug = slugify(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.division


class Posts(models.Model):
    # Значения для должностей
    POST = [
        ('Генеральный директор', 'Генеральный директор'),
        ('Главный инженер', 'Главный инженер'),
        ('Главный бухгалтер', 'Главный бухгалтер'),
        ('Экономист', 'Экономист'),
        ('Бухгалтер', 'Бухгалтер'),
        ('Менеджер по продажам', 'Менеджер по продажам'),
    ]

    # Должности
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    post = models.CharField(max_length=75, choices=POST, default="Р", verbose_name='Должность')
    post_description = models.CharField(max_length=50, blank=True, null=True, verbose_name='Описание Должности')
    post_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')

    # Представления для администрирования
    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def save(self, *args, **kwargs):
        # Генерируем slug из поля id
        self.post_slug = slugify(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.post}"


class Patterns(models.Model):
    # Значения для шаблона доступа
    PATTERNS = [
        ('Полный', 'Полный'),
        ('Охрана', 'Охрана'),
        ('Уборщики', 'Уборщики'),
        ('Посетители', 'Посетители'),
        ('Бухгалтерия', 'Бухгалтерия'),
        ('Менеджер', 'Менеджер'),
    ]
    # Шаблон доступа
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    access_pattern = models.CharField(max_length=50, choices=PATTERNS, default="П", verbose_name='Шаблон доступа')
    access_description = models.CharField(max_length=100, blank=True, null=True, verbose_name='Описание доступа')
    pattern_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')

    # Представления для администрирования
    class Meta:
        verbose_name = 'Шаблоны доступа'
        verbose_name_plural = 'Шаблон доступа'

    def save(self, *args, **kwargs):
        # Генерируем slug из поля id
        self.pattern_slug = slugify(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.access_pattern


class WorkSchedule(models.Model):
    # Значения для графика работы
    STATUS_TIME = [
        ('Активен', 'Активен'),
        ('Устарел', 'Устарел'),
        ('Отключен', 'Отключен'),
    ]

    # График работы
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    start_time = models.TimeField(blank=True, null=True, verbose_name='Тип графика с:')
    end_time = models.TimeField(blank=True, null=True, verbose_name='Тип графика до:')
    time_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Название графика')
    time_description = models.CharField(max_length=150, blank=True, null=True, verbose_name='Описание рабочего графика')
    time_status = models.CharField(max_length=25, choices=STATUS_TIME, default="А", verbose_name='Статус графика')
    time_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')
    # вложенный элемент
    division = models.ForeignKey(Divisions, on_delete=models.SET_NULL, default='Отдел логистики', null=True,
                                 blank=True,
                                 verbose_name='Подразделение')

    # Представления для администрирования
    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'График работы'

    def save(self, *args, **kwargs):
        # Генерируем slug из поля id
        self.time_slug = slugify(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


def get_default_image_path():
    return os.path.join(settings.MEDIA_ROOT, 'static/img/default_user.jpg')


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Staff(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    fio = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(max_length=254, unique=True, verbose_name='E-mail')
    phone_number = models.CharField(max_length=12, unique=True, null=True, blank=True, verbose_name='Номер телефона')
    dob = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    employee_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')
    date_join = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Дата последнего входа', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(upload_to='personal_photo', null=True, blank=True, verbose_name='Фотография')

    division = models.ForeignKey(Divisions, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Подразделение')
    time = models.ForeignKey(WorkSchedule, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип графика')
    post = models.ForeignKey(Posts, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Должность')
    pattern = models.ForeignKey(Patterns, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Шаблон доступа')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio']

    class Meta:
        verbose_name = 'Персонал'
        verbose_name_plural = 'Сотрудники'

    def save(self, *args, **kwargs):
        self.employee_slug = slugify(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.fio


class Visiting(models.Model):
    # Посетители
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    visitor = models.CharField(max_length=150, verbose_name='Посетитель')
    start_date = models.DateTimeField(blank=True, null=True, verbose_name='Временный пропуск с:')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='Временный пропуск по:')
    visitor_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')
    # вложенные элементы
    maintainer = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True,
                                   blank=True,
                                   verbose_name='Сопровождающий')
    division = models.ForeignKey(Divisions, on_delete=models.SET_NULL, default='Отдел логистики', null=True,
                                 blank=True,
                                 verbose_name='Подразделение')

    # Представления для администрирования
    class Meta:
        verbose_name = 'Посетителя'
        verbose_name_plural = 'Посещения'

    def save(self, *args, **kwargs):
        # Генерируем slug из поля id
        self.visitor_slug = slugify(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.visitor} - {self.maintainer}"


class ExplanatoryNotes(models.Model):
    # Значения для объяснительных
    DOC = [
        ('Служебная командировка', 'Служебная командировка'),
        ('Отпуск по беременности и родам', 'Отпуск по беременности и родам'),
    ]

    AWH = [
        ('Добавлять', 'Добавлять'),
        ('Не добавлять', 'Не добавлять'),
    ]

    FINE = [
        ('В календарных днях включая праздничные', 'В календарных днях включая праздничные'),
        ('В рабочих днях', 'В рабочих днях'),
    ]
    # Объяснительные
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    doc_type = models.CharField(max_length=75, choices=DOC, default="СК", verbose_name='Название типа документа')
    add_work_hours = models.CharField(max_length=75, choices=AWH, default="НД",
                                      verbose_name='Добавление к рабочему времени')
    fine = models.CharField(max_length=75, choices=FINE, default="РД", verbose_name='Способ исчисления')
    explanatory_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')
    # вложенные элементы
    employee = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True,
                                 blank=True,
                                 verbose_name='Сотрудник')

    # Представления для администрирования
    class Meta:
        verbose_name = 'Объяснительная'
        verbose_name_plural = 'Объяснительные'

    def save(self, *args, **kwargs):
        # Генерируем slug из поля id
        self.explanatory_slug = slugify(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doc_type} - {self.employee}"


class Tasks(models.Model):
    TASK = [
        ('Резервное копирование базы данных', 'Резервное копирование базы данных'),
        ('Задача', 'Задача'),
    ]

    WEEK = [
        ('Понедельник', 'Понедельник'),
        ('Втроник', 'Втроник'),
        ('Среда', 'Среда'),
        ('Четверг', 'Четверг'),
        ('Пятница', 'Пятница'),
        ('Суббота', 'Суббота'),
        ('Воскресенье', 'Воскресенье'),
    ]

    STT = [
        ('Выполнено', 'Выполнено'),
        ('Запланировано', 'Запланировано'),
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name_of_task = models.CharField(max_length=75, choices=TASK, default="РК", verbose_name='Название задачи')
    time_of_cmlt = models.CharField(max_length=75, choices=WEEK, default="ПН", verbose_name='Когда выполнять')
    status_task = models.CharField(max_length=75, choices=STT, default="Запланировано",
                                   verbose_name='Статус выполнения')
    date_task = models.DateTimeField(blank=True, null=True, verbose_name='Дата')
    task_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')

    # Представления для администрирования
    class Meta:
        verbose_name = 'Задание системы'
        verbose_name_plural = 'Задания'

    def save(self, *args, **kwargs):
        # Генерируем slug из поля id
        self.task_slug = slugify(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name_of_task} - {self.status_task}"


class Operators(models.Model):
    ROLE = [
        ('Главный администратор', 'Главный администратор'),
        ('Администратор', 'Администратор'),
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    login = models.CharField(max_length=150, verbose_name='Логин')
    post_operator = models.CharField(max_length=75, choices=ROLE, default="МА", verbose_name='Роль')
    operator_description = models.CharField(max_length=100, blank=True, null=True, verbose_name='Описание оператора')
    operator_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')
    # вложенные элементы
    employee = models.ForeignKey(Staff, on_delete=models.PROTECT, null=True, blank=True,
                                 verbose_name='Оператор')

    class Meta:
        verbose_name = 'Оператор'
        verbose_name_plural = 'Операторы'

    def save(self, *args, **kwargs):
        # Генерируем slug из поля id
        self.operator_slug = slugify(self.id)
        super().save(*args, **kwargs)

        # Начало транзакции
        with transaction.atomic():
            super().save(*args, **kwargs)  # Сначала сохраняем оператора

            if self.employee:
                # Обновление связанного сотрудника в зависимости от роли оператора
                if self.post_operator == 'Главный администратор':
                    self.employee.is_superuser = True
                    self.employee.is_admin = False  # Убедитесь, что этот флаг должен быть False для главного администратора
                elif self.post_operator == 'Администратор':
                    self.employee.is_admin = True
                    self.employee.is_superuser = False  # Убедитесь, что этот флаг должен быть False для администратора

                # Обязательно сохраняем изменения в сотруднике
                self.employee.save()

    def __str__(self):
        return f"{self.employee}"


class Docs(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    doc_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Наименование документа')
    doc_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name='URL')
    # вложенные элементы
    operator_doc = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True,
                                     blank=True,
                                     verbose_name='Оператор')
    division = models.ForeignKey(Divisions, on_delete=models.SET_NULL, default='Отдел логистики', null=True,
                                 blank=True,
                                 verbose_name='Подразделение')
    doc_file = models.FileField(upload_to='docs/', verbose_name='Файл документа', blank=True, null=True)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def save(self, *args, **kwargs):
        # Генерируем slug из поля id
        self.doc_slug = slugify(self.id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doc_name},{self.operator_doc}"
