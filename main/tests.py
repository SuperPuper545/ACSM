from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .forms import StaffForm
from .models import Divisions, Posts, Patterns, Staff, ExplanatoryNotes, Tasks, Operators, Docs

class DivisionsModelTest(TestCase):
    def setUp(self):
        # Создаем тестовый объект в таблице Divisions
        self.division = Divisions.objects.create(
            division='Отдел экономики',
            division_number='123456789',
            division_description='Отдел по вопросам финансов'
        )

    def test_division_creation(self):
        # Проверяем, что объект успешно создан и корректно представляет строковое представление
        self.assertTrue(isinstance(self.division, Divisions))
        self.assertEqual(self.division.__str__(), self.division.division)

class PostsModelTest(TestCase):
    def setUp(self):
        # Создаем тестовый объект в таблице Posts
        self.post = Posts.objects.create(
            post='Главный бухгалтер',
            post_description='Управляет финансовыми операциями'
        )

    def test_post_creation(self):
        # Проверяем, что объект успешно создан и корректно представляет строковое представление
        self.assertTrue(isinstance(self.post, Posts))
        self.assertEqual(self.post.__str__(), self.post.post)

    def test_post_description_required(self):
        # Проверяем, что создание поста без описания вызывает ValidationError
        with self.assertRaises(ValidationError):
            empty_desc_post = Posts(
                post='Позиция без описания',
                post_description=''  # Пустое описание
            )
            empty_desc_post.full_clean()  # Валидируем объект

class PatternsModelTest(TestCase):
    def setUp(self):
        # Создаем тестовый объект в таблице Patterns
        self.pattern = Patterns.objects.create(
            access_pattern='Полный',
            access_description='Доступ ко всем ресурсам'
        )

    def test_pattern_creation(self):
        # Проверяем, что объект успешно создан и корректно представляет строковое представление
        self.assertTrue(isinstance(self.pattern, Patterns))
        self.assertEqual(self.pattern.__str__(), self.pattern.access_pattern)

    def test_pattern_access_pattern_max_length(self):
        # Проверяем, что слишком длинный паттерн вызывает ValidationError
        with self.assertRaises(ValidationError):
            long_pattern = Patterns(
                access_pattern='Слишком длинное название для паттерна доступа' * 10,
                access_description='Длинное описание тоже'
            )
            long_pattern.full_clean()  # Валидируем объект

class ExplanatoryNotesModelTest(TestCase):
    def setUp(self):
        # Создаем связанный объект в таблице Staff для использования в ExplanatoryNotes
        self.staff = Staff.objects.create(
            fio='Семенов Семен Семенович',
            email='semenov@example.com',
            phone_number='765432198'
        )
        # Создаем тестовый объект в таблице ExplanatoryNotes
        self.note = ExplanatoryNotes.objects.create(
            doc_type='Служебная командировка',
            add_work_hours='Добавлять',
            fine='В календарных днях включая праздничные',
            employee=self.staff
        )

    def test_explanatory_notes_creation(self):
        # Проверяем, что объект успешно создан и корректно представляет строковое представление
        self.assertTrue(isinstance(self.note, ExplanatoryNotes))
        self.assertEqual(self.note.__str__(), f"{self.note.doc_type} - {self.note.employee}")

class TasksModelTest(TestCase):
    def setUp(self):
        # Создаем тестовый объект в таблице Tasks
        self.task = Tasks.objects.create(
            name_of_task='Резервное копирование базы данных',
            time_of_cmlt='Пятница',
            status_task='Запланировано'
        )

    def test_tasks_creation(self):
        # Проверяем, что объект успешно создан и корректно представляет строковое представление
        self.assertTrue(isinstance(self.task, Tasks))
        self.assertEqual(self.task.__str__(), f"{self.task.name_of_task} - {self.task.status_task}")

class OperatorsModelTest(TestCase):
    def setUp(self):
        # Создаем связанный объект в таблице Staff для использования в Operators
        self.staff = Staff.objects.create(
            fio='Миронов Мирон Миронович',
            email='mironov@example.com',
            phone_number='1010101010'
        )
        # Создаем тестовый объект в таблице Operators
        self.operator = Operators.objects.create(
            login='main_admin',
            post_operator='Главный администратор',
            employee=self.staff
        )

    def test_operators_creation(self):
        # Проверяем, что объект успешно создан и корректно представляет строковое представление
        self.assertTrue(isinstance(self.operator, Operators))
        self.assertEqual(self.operator.__str__(), f"{self.operator.employee}")

class DocsModelTest(TestCase):
    def setUp(self):
        # Создаем связанные объекты в таблицах Divisions и Staff для использования в Docs
        self.division = Divisions.objects.create(
            division='Отдел разработки',
            division_number='234567890',
            division_description='Программное обеспечение'
        )
        self.staff = Staff.objects.create(
            fio='Кузнецов Кузьма Кузьмич',
            email='kuznetsov@example.com',
            phone_number='9988776655'
        )
        # Создаем тестовый объект в таблице Docs
        self.doc = Docs.objects.create(
            doc_name='Техническая документация',
            operator_doc=self.staff,
            division=self.division
        )

    def test_docs_creation(self):
        # Проверяем, что объект успешно создан и корректно представляет строковое представление
        self.assertTrue(isinstance(self.doc, Docs))
        self.assertEqual(self.doc.__str__(), f"{self.doc.doc_name},{self.doc.operator_doc}")


