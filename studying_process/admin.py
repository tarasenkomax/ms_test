from django.contrib import admin

from studying_process.models import Student, Group, AcademicDiscipline, DirectionOfTraining


class StudentAdmin(admin.ModelAdmin):
    """ Студент """
    list_display = ("id", "name", "surname")
    list_display_links = ("id", "name", "surname")


class GroupAdmin(admin.ModelAdmin):
    """ Учебная группа """
    list_display = ("id", "title", "max_length")
    list_display_links = ("id", "title", "max_length")


class AcademicDisciplineAdmin(admin.ModelAdmin):
    """ Учебная дисциплина """
    list_display = ("id", "title")
    list_display_links = ("id", "title")


class DirectionOfTrainingAdmin(admin.ModelAdmin):
    """ Направление подготовки """
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    filter_horizontal = ('disciplines',)


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(AcademicDiscipline, AcademicDisciplineAdmin)
admin.site.register(DirectionOfTraining, DirectionOfTrainingAdmin)
