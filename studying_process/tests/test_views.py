import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from django.urls import reverse
from rest_framework import status

from studying_process.models import AcademicDiscipline, DirectionOfTraining


class AcademicDisciplineViewTest(TestCase):
    url = '/api/academic_disciplines/'
    generated_url = 'studying_process:academic_disciplines_list'

    @classmethod
    def setUpTestData(cls):
        AcademicDiscipline.objects.create(title='Математика')
        AcademicDiscipline.objects.create(title='Физика')
        admin = get_user_model().objects.create_user(username='test', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='test_2', password='Some_password123')
        curator.profile.is_curator = True

    def test_view_url_exists_at_desired_location_for_admin(self):
        self.client.login(username='test', password='Some_password123')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_view_url_accessible_by_name_for_admin(self):
        self.client.login(username='test', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_curator(self):
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_for_admin(self):
        self.client.login(username='test', password='Some_password123')
        resp = self.client.post(reverse(self.generated_url), data=json.dumps({'title': 'Алгебра'}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AcademicDiscipline.objects.filter(title='Алгебра').exists())

    def test_post_for_curator(self):
        self.client.login(username='test_2', password='Some_password123')
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
        admin = get_user_model().objects.create_user(username='test', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='test_2', password='Some_password123')
        curator.profile.is_curator = True

    def test_view_url_exists_at_desired_location_for_admin(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.get(self.url + str(discipline.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_admin(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': discipline.id}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_exists_at_desired_location_for_curator(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.get(self.url + str(discipline.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_url_accessible_by_name_for_curator(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': discipline.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_for_admin(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': discipline.id}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AcademicDiscipline.objects.filter(title='Физика').exists())

    def test_delete_for_curator(self):
        discipline = AcademicDiscipline.objects.get(title='Физика')
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': discipline.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(AcademicDiscipline.objects.filter(title='Физика').exists())


class DirectionOfTrainingViewTest(TestCase):
    url = '/api/direction_of_training/'
    generated_url = 'studying_process:direction_of_training_list'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='test', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='test_2', password='Some_password123')
        curator.profile.is_curator = True
        DirectionOfTraining.objects.create(title='Направление 1', curator=curator)
        DirectionOfTraining.objects.create(title='Направление 2', curator=curator)
        DirectionOfTraining.objects.create(title='Направление 3', curator=curator)

    def test_view_url_exists_at_desired_location_for_admin(self):
        self.client.login(username='test', password='Some_password123')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 3)

    def test_view_url_accessible_by_name_for_admin(self):
        self.client.login(username='test', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # def test_view_url_accessible_by_name_for_curator(self):
    #     self.client.login(username='test_2', password='Some_password123')
    #     resp = self.client.get(reverse(self.generated_url))
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_post_for_admin(self):
        user = User.objects.get(username='test')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.post(reverse(self.generated_url), data=json.dumps({'title': 'Напр 1', 'curator': user.id}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(DirectionOfTraining.objects.filter(title='Напр 1').exists())

    def test_post_for_curator(self):
        user = User.objects.get(username='test')
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.post(reverse(self.generated_url), data=json.dumps({'title': 'Напр 1', 'curator': user.id}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class DirectionOfTrainingDetailViewTest(TestCase):
    url = '/api/direction_of_training/'
    generated_url = 'studying_process:direction_of_training_detail'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='test', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='test_2', password='Some_password123')
        curator.profile.is_curator = True
        DirectionOfTraining.objects.create(title='Направление 1', curator=curator)

    def test_view_url_exists_at_desired_location_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.get(self.url + str(direction.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': direction.id}))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_exists_at_desired_location_for_curator(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.get(self.url + str(direction.id) + '/')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_url_accessible_by_name_for_curator(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.get(reverse(self.generated_url, kwargs={'id': direction.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_for_admin(self):
        AcademicDiscipline.objects.create(title='История')
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_for_curator(self):
        AcademicDiscipline.objects.create(title='История')
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_update_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': direction.id}))
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DirectionOfTraining.objects.filter(title='Направление 1').exists())

    def test_delete_for_curator(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.delete(reverse(self.generated_url, kwargs={'id': direction.id}))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(DirectionOfTraining.objects.filter(title='Направление 1').exists())


class DeleteDisciplineFromDirectionOfTrainingViewTest(TestCase):
    url = '/api/direction_of_training/'
    generated_url = 'studying_process:del_discipline_from_direction_of_training'

    @classmethod
    def setUpTestData(cls):
        admin = get_user_model().objects.create_user(username='test', password='Some_password123', is_staff=True)
        curator = get_user_model().objects.create_user(username='test_2', password='Some_password123')
        curator.profile.is_curator = True
        discipline = AcademicDiscipline.objects.create(title='История')
        direction = DirectionOfTraining.objects.create(title='Направление 1', curator=curator)
        direction.disciplines.add(discipline)

    def test_update_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_invalid_update_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'Химия'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_in_url_for_admin(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test', password='Some_password123')
        resp = self.client.put(self.url + str(direction.id) + '/delete_discipline/',
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_for_curator(self):
        direction = DirectionOfTraining.objects.get(title='Направление 1')
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.put(reverse(self.generated_url, kwargs={'id': direction.id}),
                               data=json.dumps({'title': 'История'}), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
