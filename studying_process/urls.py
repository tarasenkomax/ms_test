from django.urls import path

from studying_process.views import AcademicDisciplineView, AcademicDisciplineDetailView, DirectionOfTrainingView, \
    DirectionOfTrainingDetailView, DeleteDisciplineFromDirectionOfTrainingView

app_name = "studying_process"

urlpatterns = [
    path('academic_disciplines/', AcademicDisciplineView.as_view(), name='academic_disciplines_list'),
    path('academic_disciplines/<int:id>/', AcademicDisciplineDetailView.as_view(), name='academic_discipline_detail'),
    path('direction_of_training/', DirectionOfTrainingView.as_view(), name='direction_of_training_list'),
    path('direction_of_training/<int:id>/', DirectionOfTrainingDetailView.as_view(),
         name='direction_of_training_detail'),
    path('direction_of_training/<int:id>/delete_discipline', DeleteDisciplineFromDirectionOfTrainingView.as_view(),
         name='del_discipline_from_direction_of_training'),

]
