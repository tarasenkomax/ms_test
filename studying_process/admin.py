from django.contrib import admin

from studying_process.models import Student, Group, AcademicDiscipline, DirectionOfTraining, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_curator")
    list_filter = ("is_curator",)


class StudentAdmin(admin.ModelAdmin):
    """ Студент """
    list_display = ("id", "name", "surname", "gender", "group")
    list_display_links = ("id", "name", "surname", "gender", "group")
    list_filter = ("gender", "group")


class GroupAdmin(admin.ModelAdmin):
    """ Учебная группа """
    list_display = ("id", "title", "max_length", "direction")
    list_display_links = ("id", "title", "max_length", "direction")
    list_filter = ("direction",)


class AcademicDisciplineAdmin(admin.ModelAdmin):
    """ Учебная дисциплина """
    list_display = ("id", "title")
    list_display_links = ("id", "title")


class DirectionOfTrainingAdmin(admin.ModelAdmin):
    """ Направление подготовки """
    list_display = ("id", "title", "curator")
    list_display_links = ("id", "title", "curator")
    filter_horizontal = ('disciplines',)
    list_filter = ("curator",)


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(AcademicDiscipline, AcademicDisciplineAdmin)
admin.site.register(DirectionOfTraining, DirectionOfTrainingAdmin)
admin.site.register(Profile, ProfileAdmin)
