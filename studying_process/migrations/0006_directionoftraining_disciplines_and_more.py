# Generated by Django 4.1.2 on 2022-10-28 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studying_process', '0005_academicdiscipline_directionoftraining'),
    ]

    operations = [
        migrations.AddField(
            model_name='directionoftraining',
            name='disciplines',
            field=models.ManyToManyField(related_name='disciplines', to='studying_process.academicdiscipline', verbose_name='Дисциплины'),
        ),
        migrations.AddField(
            model_name='directionoftraining',
            name='groups',
            field=models.ManyToManyField(related_name='groups', to='studying_process.group', verbose_name='Группы'),
        ),
    ]