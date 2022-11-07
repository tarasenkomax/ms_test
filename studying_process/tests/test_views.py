import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from studying_process.models import AcademicDiscipline, DirectionOfTraining, Group, Profile, Student


class AcademicDisciplineViewTest(TestCase):
    url = '/api/academic_disciplines/'
    generated_url = 'studying_process:academic_disciplines_list'

    @classmethod
    def setUpTestData(cls):
        AcademicDiscipline.objects.create(title='Математика')
        AcademicDiscipline.objects.create(title='Физика')
        admin = get_user_model().objects.create_user(username='admin', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='curator', password='Some_password123')
        Profile.objects.filter(user=curator).update(is_curator=True)

    def test_view_url_exists_at_desired_location_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_view_url_accessible_by_name_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_curator(self):
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.post(reverse(self.generated_url), data=json.dumps({'title': 'Алгебра'}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AcademicDiscipline.objects.filter(title='Алгебра').exists())

    def test_post_for_curator(self):
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.post(reverse(self.generated_url), data=json.dumps({'title': 'Алгебра'}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class AcademicDisciplineDetailViewTest(TestCase):
    url = '/api/academic_disciplines/'
    generated_url = 'studying_process:academic_discipline_detail'

    @classmethod
    def setUpTestData(cls):
        AcademicDiscipline.objects.create(title='Математика')
        AcademicDiscipline.objects.create(title='Физика')
        admin = get_user_model().objects.create_user(username='admin', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='curator', password='Some_password123')
        Profile.objects.filter(user=curator).update(is_curator=True)

    def test_view_url_exists_at_desired_location_for_admin(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(self.url + str(discipline.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_admin(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': discipline.id}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_curator(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': discipline.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_for_admin(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': discipline.id}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AcademicDiscipline.objects.filter(title='Физика').exists())

    def test_delete_for_curator(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': discipline.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(AcademicDiscipline.objects.filter(title='Физика').exists())


class DirectionOfTrainingViewTest(TestCase):
    url = '/api/direction_of_training/'
    generated_url = 'studying_process:direction_of_training_list'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='admin', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='curator', password='Some_password123')
        Profile.objects.filter(user=curator).update(is_curator=True)
        DirectionOfTraining.objects.create(title='Направление 1', curator=curator)
        DirectionOfTraining.objects.create(title='Направление 2', curator=curator)
        DirectionOfTraining.objects.create(title='Направление 3', curator=curator)

    def test_view_url_exists_at_desired_location_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 3)

    def test_view_url_accessible_by_name_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_curator(self):
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_post_for_admin(self):
        user = User.objects.get(username='admin')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.post(reverse(self.generated_url), data=json.dumps({'title': 'Напр 1', 'curator': user.id}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(DirectionOfTraining.objects.filter(title='Напр 1').exists())

    def test_post_for_curator(self):
        user = User.objects.get(username='admin')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.post(reverse(self.generated_url), data=json.dumps({'title': 'Напр 1', 'curator': user.id}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class DirectionOfTrainingDetailViewTest(TestCase):
    url = '/api/direction_of_training/'
    generated_url = 'studying_process:direction_of_training_detail'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='admin', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='curator', password='Some_password123')
        Profile.objects.filter(user=curator).update(is_curator=True)
        DirectionOfTraining.objects.create(title='Направление 1', curator=curator)

    def test_view_url_exists_at_desired_location_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(self.url + str(direction.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': direction.id}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_curator(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': direction.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_for_admin(self):
        AcademicDiscipline.objects.create(title='История')
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_for_curator(self):
        AcademicDiscipline.objects.create(title='История')
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_update_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': direction.id}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DirectionOfTraining.objects.filter(title='Направление 1').exists())

    def test_delete_for_curator(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': direction.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(DirectionOfTraining.objects.filter(title='Направление 1').exists())


class DeleteDisciplineFromDirectionOfTrainingViewTest(TestCase):
    url = '/api/direction_of_training/'
    generated_url = 'studying_process:del_discipline_from_direction_of_training'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='admin', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='curator', password='Some_password123')
        Profile.objects.filter(user=curator).update(is_curator=True)
        discipline = AcademicDiscipline.objects.create(title='История')
        direction = DirectionOfTraining.objects.create(title='Направление 1', curator=curator)
        direction.disciplines.add(discipline)

    def test_update_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_invalid_update_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'Химия'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_in_url_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.put(self.url + str(direction.id) + '/delete_discipline/',
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_for_curator(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class GroupViewTest(TestCase):
    url = '/api/groups/'
    generated_url = 'studying_process:groups_list'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='admin', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='curator', password='Some_password123')
        Profile.objects.filter(user=curator).update(is_curator=True)
        direction = DirectionOfTraining.objects.create(title='Направление 1', curator=curator)
        Group.objects.create(title='Группа 1', direction=direction)
        Group.objects.create(title='Группа 2', direction=direction)

    def test_view_url_exists_at_desired_location_for_curator(self):
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_view_url_accessible_by_name_for_curator(self):
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_for_curator(self):
        self.client.login(username='curator', password='Some_password123')
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        resp = self.client.post(reverse(self.generated_url),
                                data=json.dumps({'title': 'Гр.1', 'direction': direction.id}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Group.objects.filter(title='Гр.1').exists())

    def test_post_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        resp = self.client.post(reverse(self.generated_url),
                                data=json.dumps({'title': 'Гр.1', 'direction': direction.id}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Group.objects.filter(title='Гр.1').exists())


class GroupDetailViewTest(TestCase):
    url = '/api/groups/'
    generated_url = 'studying_process:groups_detail'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='admin', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='curator', password='Some_password123')
        Profile.objects.filter(user=curator).update(is_curator=True)
        direction = DirectionOfTraining.objects.create(title='Направление 1', curator=curator)
        Group.objects.create(title='Группа 1', direction=direction)
        Group.objects.create(title='Группа 2', direction=direction)

    def test_view_url_exists_at_desired_location_for_curator(self):
        group = Group.objects.get(title='Группа 1')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(self.url + str(group.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_curator(self):
        group = Group.objects.get(title='Группа 1')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': group.id}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_admin(self):
        group = Group.objects.get(title='Группа 1')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': group.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_for_curator(self):
        group = Group.objects.get(title='Группа 1')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': group.id}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Group.objects.filter(title='Группа 1').exists())

    def test_delete_for_admin(self):
        group = Group.objects.get(title='Группа 1')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': group.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Group.objects.filter(title='Группа 1').exists())


class StudentViewTest(TestCase):
    url = '/api/students/'
    generated_url = 'studying_process:student_list'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='admin', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='curator', password='Some_password123')
        Profile.objects.filter(user=curator).update(is_curator=True)
        direction = DirectionOfTraining.objects.create(title='Направление 1', curator=curator)
        group = Group.objects.create(title='Группа 1', direction=direction)
        Student.objects.create(name='Иван', surname='Иванов', gender='man', group=group)
        Student.objects.create(name='Пётр', surname='Петров', gender='man', group=group)

    def test_view_url_exists_at_desired_location_for_curator(self):
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_view_url_accessible_by_name_for_curator(self):
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_for_curator(self):
        self.client.login(username='curator', password='Some_password123')
        group = Group.objects.get(title='Группа 1')
        resp = self.client.post(reverse(self.generated_url), data=json.dumps(
            {'name': 'Тест', 'surname': 'Тестовый', 'gender': 'man', 'group': group.id}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Student.objects.filter(surname='Тестовый').exists())

    def test_post_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        group = Group.objects.get(title='Группа 1')
        resp = self.client.post(reverse(self.generated_url), data=json.dumps(
            {'name': 'Тест', 'surname': 'Тестовый', 'gender': 'man', 'group': group.id}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Student.objects.filter(surname='Тестовый').exists())

    def test_max_length_in_group(self):
        self.client.login(username='curator', password='Some_password123')
        group = Group.objects.get(title='Группа 1')
        for i in range(group.max_length):
            Student.objects.create(name=f'name_{i}', surname=f's_{i}', gender='man', group=group)
        resp = self.client.post(reverse(self.generated_url), data=json.dumps(
            {'name': 'Тест', 'surname': 'Тестовый', 'gender': 'man', 'group': group.id}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(resp.data['group'][0]), f'Максимальное количество студентов в группе:{group.max_length}')


class StudentDetailViewTest(TestCase):
    url = '/api/students/'
    generated_url = 'studying_process:student_detail'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='admin', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='curator', password='Some_password123')
        Profile.objects.filter(user=curator).update(is_curator=True)
        direction = DirectionOfTraining.objects.create(title='Направление 1', curator=curator)
        group = Group.objects.create(title='Группа 1', direction=direction)
        Student.objects.create(name='Иван', surname='Иванов', gender='man', group=group)
        Student.objects.create(name='Пётр', surname='Петров', gender='man', group=group)

    def test_view_url_exists_at_desired_location_for_curator(self):
        student = Student.objects.get(name='Иван')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(self.url + str(student.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_curator(self):
        student = Student.objects.get(name='Иван')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': student.id}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_admin(self):
        student = Student.objects.get(name='Иван')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': student.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_for_curator(self):
        student = Student.objects.get(name='Иван')
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': student.id}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(name='Иван').exists())

    def test_delete_for_admin(self):
        student = Student.objects.get(name='Иван')
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': student.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Student.objects.filter(name='Иван').exists())


class CreateReportViewTest(TestCase):
    url = '/api/report/'
    generated_url = 'studying_process:create_report'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='admin', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='curator', password='Some_password123')
        Profile.objects.filter(user=curator).update(is_curator=True)

    def test_view_url_exists_at_desired_location_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    def test_view_url_accessible_by_name_for_admin(self):
        self.client.login(username='admin', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    def test_view_url_accessible_by_name_for_curator(self):
        self.client.login(username='curator', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
