from django.contrib.auth.models import User
from django.db import models


class Student(models.Model):
    """ Студент"""
    STUDENT_GENDER = (
        ('man', 'Мужской'),
        ('women', 'Женский')
    )
    name = models.CharField(max_length=32, verbose_name="Имя")
    surname = models.CharField(max_length=32, verbose_name="Фамилия")
    gender = models.CharField(max_length=16, choices=STUDENT_GENDER, verbose_name='Пол')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name='Учебная группа')

    def __str__(self):
        return f"{self.surname} {self.name}"

    class Meta:
        verbose_name_plural = "Студенты"
        verbose_name = "Студент"


class Group(models.Model):
    """ Учебная группа """
    title = models.CharField(max_length=32, verbose_name="Название группы")
    max_length = models.PositiveIntegerField(default=20, verbose_name='Максимальная длина группы')
    direction = models.ForeignKey('DirectionOfTraining', on_delete=models.CASCADE,
                                  verbose_name='Направление подготовки')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Учебные группы"
        verbose_name = "Учебная группа"


class AcademicDiscipline(models.Model):
    """ Учебная дисциплина """
    title = models.CharField(max_length=32, verbose_name="Название дисциплины")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Учебные дисциплины"
        verbose_name = "Учебная дисциплина"


class DirectionOfTraining(models.Model):
    """ Направление подготовки """
    title = models.CharField(max_length=32, verbose_name="Название направления")
    disciplines = models.ManyToManyField('AcademicDiscipline', related_name="disciplines", verbose_name="Дисциплины")
    curator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Куратор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Направления подготовки"
        verbose_name = "Направление подготовки"
