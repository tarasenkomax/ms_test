from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from settings.permissions import IsCuratorReadOnly
from studying_process.models import AcademicDiscipline, DirectionOfTraining
from studying_process.serializers import AcademicDisciplineSerializer, DirectionOfTrainingSerializer, \
    CreateDirectionOfTrainingSerializer


class AcademicDisciplineView(generics.ListCreateAPIView):
    """
    (GET) Получение списка учебных дисциплин
    (POST) Добавление учебной дисциплины
    """
    permission_classes = [permissions.IsAdminUser | IsCuratorReadOnly]
    serializer_class = AcademicDisciplineSerializer
    queryset = AcademicDiscipline.objects.all()


class AcademicDisciplineDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    (GET) Получение детальной информации по учебной дисциплине
    (PUT) Обновление информации
    (DEL) Удаление
    """
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = AcademicDisciplineSerializer
    queryset = AcademicDiscipline.objects.all()
    lookup_field = 'id'


class DirectionOfTrainingView(generics.ListCreateAPIView):
    """
    (GET) Получение списка направлений подготовки
    (POST) Добавление направления подготовки
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = DirectionOfTraining.objects.all()
    serializer_class = CreateDirectionOfTrainingSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = DirectionOfTrainingSerializer
        return super().get(request, *args, **kwargs)


class DirectionOfTrainingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    (GET) Получение детальной информации по направлению подготовки
    (PUT) Добавление дисиплины в направление подготовки
    (DEL) Удаление направления подготовки
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = DirectionOfTraining.objects.all()
    serializer_class = AcademicDisciplineSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        self.serializer_class = DirectionOfTrainingSerializer
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            self.get_object().disciplines.add(AcademicDiscipline.objects.get(title=request.data["title"]))
        except AcademicDiscipline.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return self.get(request, *args, **kwargs)


class DeleteDisciplineFromDirectionOfTrainingView(generics.RetrieveUpdateAPIView):
    """
    (GET) Получение детальной информации по направлению подготовки
    (PUT) Удаление дисиплины из направления подготовки
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = DirectionOfTraining.objects.all()
    serializer_class = AcademicDisciplineSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        self.serializer_class = DirectionOfTrainingSerializer
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            self.get_object().disciplines.remove(AcademicDiscipline.objects.get(title=request.data["title"]))
        except AcademicDiscipline.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return self.get(request, *args, **kwargs)
