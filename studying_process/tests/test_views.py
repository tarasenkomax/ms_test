import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse
from rest_framework import status

from studying_process.models import AcademicDiscipline


class AcademicDisciplineViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AcademicDiscipline.objects.create(title='Математика')
        AcademicDiscipline.objects.create(title='Физика')
        admin = get_user_model().objects.create_user(username='test', password='Some_password123', first_name='Иван',
                                                     last_name='Иванов', is_staff=True)
        curator = get_user_model().objects.create_user(username='test_2', password='Some_password123',
                                                       first_name='Андрей', last_name='Андреев')
        curator.profile.is_curator = True

    def test_view_url_exists_at_desired_location_for_admin(self):
        self.client.login(username='test', password='Some_password123')
        resp = self.client.get('/api/academic_disciplines/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_admin(self):
        self.client.login(username='test', password='Some_password123')
        resp = self.client.get(reverse('studying_process:academic_disciplines_list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_view_url_accessible_by_name_for_curator(self):
        self.client.login(username='test_2', password='Some_password123')
        resp = self.client.get(reverse('studying_process:academic_disciplines_list'))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        self.client.login(username='test', password='Some_password123')
        self.client.post(reverse('studying_process:academic_disciplines_list'), data=json.dumps({'title': 'Алгебра'}),
                         content_type='application/json')
        self.assertTrue(AcademicDiscipline.objects.filter(title='Алгебра').exists())
