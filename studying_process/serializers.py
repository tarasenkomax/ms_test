from rest_framework import serializers

from studying_process.models import AcademicDiscipline


class AcademicDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicDiscipline
        fields = ['id', 'title']
