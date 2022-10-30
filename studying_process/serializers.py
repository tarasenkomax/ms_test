from rest_framework import serializers

from studying_process.models import AcademicDiscipline, DirectionOfTraining


class AcademicDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicDiscipline
        fields = ['id', 'title']


class DirectionOfTrainingSerializer(serializers.ModelSerializer):
    disciplines = AcademicDisciplineSerializer(read_only=True, many=True)

    class Meta:
        model = DirectionOfTraining
        fields = ['id', 'title', 'curator', 'disciplines']


class CreateDirectionOfTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectionOfTraining
        fields = ['id', 'title', 'curator']
