import datetime

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from settings.permissions import IsCuratorReadOnly, IsCurator
from studying_process.models import AcademicDiscipline, DirectionOfTraining, Group, Student
from studying_process.serializers import AcademicDisciplineSerializer, DirectionOfTrainingSerializer, \
    CreateDirectionOfTrainingSerializer, GroupsSerializer, CreateGroupsSerializer, StudentSerializer
from studying_process.tasks import create_report


class AcademicDisciplineView(generics.ListCreateAPIView):
    """
    (GET) Получение списка учебных дисциплин
    (POST) Добавление учебной дисциплины
    """
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = AcademicDisciplineSerializer
    queryset = AcademicDiscipline.objects.all()


class AcademicDisciplineDetailView(generics.RetrieveDestroyAPIView):
    """
    (GET) Получение детальной информации по учебной дисциплине
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
    permission_classes = [permissions.IsAdminUser | IsCuratorReadOnly]
    queryset = DirectionOfTraining.objects.all()
    serializer_class = CreateDirectionOfTrainingSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = DirectionOfTrainingSerializer
        return super().get(request, *args, **kwargs)


class DirectionOfTrainingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    (GET) Получение детальной информации по направлению подготовки
    (PUT) Добавление дисциплины в направление подготовки
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


class DeleteDisciplineFromDirectionOfTrainingView(generics.UpdateAPIView):
    """
    (PUT) Удаление дисциплины из направления подготовки
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = DirectionOfTraining.objects.all()
    serializer_class = AcademicDisciplineSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            self.get_object().disciplines.remove(AcademicDiscipline.objects.get(title=request.data["title"]))
        except AcademicDiscipline.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class GroupsView(generics.ListCreateAPIView):
    """
    (GET) Получение списка групп
    (POST) Добавление группы
    """
    # permission_classes = (IsCurator,)
    serializer_class = CreateGroupsSerializer
    queryset = Group.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = GroupsSerializer
        return super().get(request, *args, **kwargs)


class GroupDetailView(generics.RetrieveDestroyAPIView):
    """
    (GET) Получение детальной информации по группе
    (DEL) Удаление группы
    """
    # permission_classes = (IsCurator,)
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
    lookup_field = 'id'


class StudentView(generics.ListCreateAPIView):
    """
    (GET) Получение списка студентов
    (POST) Добавление студента
    """
    # permission_classes = (IsCurator,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class StudentDetailView(generics.RetrieveDestroyAPIView):
    """
    (GET) Получение детальной информации по студенту
    (DEL) Удаление студента
    """
    # permission_classes = (IsCurator,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'


class CreateReportView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        print(datetime.datetime.now().time())
        create_report()
        print(datetime.datetime.now().time())
        return Response(status=status.HTTP_204_NO_CONTENT)
