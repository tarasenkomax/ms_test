from rest_framework import generics

from studying_process.models import AcademicDiscipline
from studying_process.serializers import AcademicDisciplineSerializer


class AcademicDisciplineView(generics.ListCreateAPIView):
    """
    (GET) Получение списка учебных дисциплин
    (GET) Получение списка учебных дисциплин
    (POST) Добавление учебной дисциплины
    """
    serializer_class = AcademicDisciplineSerializer
    queryset = AcademicDiscipline.objects.all()


class AcademicDisciplineDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    (GET) Получение детальной информации по учебной дисциплине
    (PUT) Обновление информации
    (DEL) Удаление
    """
    serializer_class = AcademicDisciplineSerializer
    queryset = AcademicDiscipline.objects.all()
    lookup_field = 'id'
