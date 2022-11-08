from rest_framework import serializers

from studying_process.models import AcademicDiscipline, DirectionOfTraining, Group, Student


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


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate(self, data):
        group = data.get('group')
        count_students_in_group = group.get_students_count()
        if count_students_in_group >= group.max_length:
            raise serializers.ValidationError(
                detail={'group': f'Максимальное количество студентов в группе:{group.max_length}'})
        return data


class GroupsSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True)

    class Meta:
        model = Group
        fields = ['id', 'title', 'max_length', 'direction', 'students']


class CreateGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['title', 'direction']


class CheckTaskStatusSerializer(serializers.Serializer):
    task_id = serializers.CharField()

    class Meta:
        fields = ['task_id', ]
