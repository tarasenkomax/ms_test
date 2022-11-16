from django.contrib.auth.models import User
from django.test import TestCase

from studying_process.models import Student, DirectionOfTraining, Group, AcademicDiscipline


class StudentModelTest(TestCase):
    def setUp(self):
        self.user = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'test@test.ru',
        }
        user = User.objects.create(**self.user)
        self.direction = {
            'title': 'Направление 1',
            'curator': user,
        }
        direction = DirectionOfTraining.objects.create(**self.direction)
        self.group = {
            'title': 'Группа 1',
            'direction': direction,
        }
        group = Group.objects.create(**self.group)
        self.student = {
            'name': 'Иван',
            'surname': 'Иванов',
            'gender': 'man',
            'group': group,
        }
        student = Student.objects.create(**self.student)
        self.student_pk = student.pk

    def test_object_name(self):
        student = Student.objects.get(pk=self.student_pk)
        self.assertEquals(student.__str__(), f"{self.student.get('surname')} {self.student.get('name')}")


class GroupModelTest(TestCase):
    def setUp(self):
        self.user = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'test@test.ru',
        }
        user = User.objects.create(**self.user)
        self.direction = {
            'title': 'Направление 1',
            'curator': user,
        }
        direction = DirectionOfTraining.objects.create(**self.direction)
        self.group1 = {
            'title': 'Группа 1',
            'direction': direction,
        }
        self.group2 = {
            'title': 'Группа 2',
            'direction': direction,
        }
        group1 = Group.objects.create(**self.group1)
        self.group1_pk = group1.pk
        group2 = Group.objects.create(**self.group2)
        self.student1 = {
            'name': 'Иван',
            'surname': 'Иванов',
            'gender': 'man',
            'group': group1,
        }
        self.student2 = {
            'name': 'Петр',
            'surname': 'Петров',
            'gender': 'man',
            'group': group1,
        }
        self.student3 = {
            'name': 'Алексей',
            'surname': 'Алексеев',
            'gender': 'man',
            'group': group2,
        }
        Student.objects.create(**self.student1)
        Student.objects.create(**self.student2)
        Student.objects.create(**self.student3)

    def test_object_name(self):
        group = Group.objects.get(pk=self.group1_pk)
        self.assertEquals(group.__str__(), self.group1.get('title'))

    def test_get_student_count(self):
        group = Group.objects.get(pk=self.group1_pk)
        self.assertEquals(group.get_students_count(), 2)


class AcademicDisciplineModelTest(TestCase):
    """ Тест модели AcademicDiscipline """

    def setUp(self):
        self.academic_discipline = {
            'title': 'Математика',
        }
        academic_discipline = AcademicDiscipline.objects.create(**self.academic_discipline)
        self.academic_discipline_pk = academic_discipline.pk

    def test_object_name(self):
        discipline = AcademicDiscipline.objects.get(pk=self.academic_discipline_pk)
        self.assertEquals(discipline.__str__(), self.academic_discipline.get('title'))


class DirectionOfTrainingModelTest(TestCase):
    """ Тест модели DirectionOfTraining """

    def setUp(self):
        self.user = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'test@test.ru',
        }
        user = User.objects.create(**self.user)
        self.direction = {
            'title': 'Направление 1',
            'curator': user,
        }
        direction = DirectionOfTraining.objects.create(**self.direction)
        self.direction_pk = direction.pk

    def test_object_name(self):
        direction = DirectionOfTraining.objects.get(pk=self.direction_pk)
        self.assertEquals(direction.__str__(), self.direction.get('title'))
