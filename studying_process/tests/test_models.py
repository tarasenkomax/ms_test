from django.contrib.auth.models import User
from django.test import TestCase

from studying_process.models import Student, DirectionOfTraining, Group, AcademicDiscipline


class StudentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(first_name='Иван', last_name='Иванов', email='test@test.ru')
        direction = DirectionOfTraining.objects.create(title='Направление 1', curator=user)
        group = Group.objects.create(title='Группа 1', direction=direction)
        Student.objects.create(name='Иван', surname='Иванов', gender='man', group=group)

    def test_object_name(self):
        student = Student.objects.get(name='Иван', surname='Иванов')
        self.assertEquals(student.__str__(), 'Иванов Иван')


class GroupModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(first_name='Иван', last_name='Иванов', email='test@test.ru')
        direction = DirectionOfTraining.objects.create(title='Направление 1', curator=user)
        group = Group.objects.create(title='Группа 1', direction=direction)
        group2 = Group.objects.create(title='Группа 2', direction=direction)
        Student.objects.create(name='Иван', surname='Иванов', gender='man', group=group)
        Student.objects.create(name='Пётр', surname='Петров', gender='man', group=group)
        Student.objects.create(name='Игорь', surname='Петров', gender='man', group=group2)

    def test_object_name(self):
        group = Group.objects.get(title='Группа 1')
        self.assertEquals(group.__str__(), 'Группа 1')

    def test_get_student(self):
        group = Group.objects.get(title='Группа 1')
        self.assertEquals(len(group.get_students()), 2)


class AcademicDisciplineModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        AcademicDiscipline.objects.create(title='Математика')

    def test_object_name(self):
        discipline = AcademicDiscipline.objects.get(title='Математика')
        self.assertEquals(discipline.__str__(), 'Математика')


class DirectionOfTrainingModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(first_name='Иван', last_name='Иванов', email='test@test.ru')
        direction = DirectionOfTraining.objects.create(title='Направление 1', curator=user)
        direction2 = DirectionOfTraining.objects.create(title='Направление 2', curator=user)
        Group.objects.create(title='Группа 1', direction=direction)
        Group.objects.create(title='Группа 2', direction=direction)
        Group.objects.create(title='Группа 3', direction=direction2)

    def test_object_name(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1', )
        self.assertEquals(direction.__str__(), 'Направление 1')

    def test_get_groups(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1', )
        self.assertEquals(len(direction.get_groups()), 2)

