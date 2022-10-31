from django.urls import path

from studying_process.views import AcademicDisciplineView, AcademicDisciplineDetailView, DirectionOfTrainingView, \
    DirectionOfTrainingDetailView, DeleteDisciplineFromDirectionOfTrainingView, GroupsView, GroupDetailView, \
    StudentView, StudentDetailView, CreateReportView

app_name = "studying_process"

urlpatterns = [
    path('academic_disciplines/', AcademicDisciplineView.as_view(), name='academic_disciplines_list'),
    path('academic_disciplines/<int:id>/', AcademicDisciplineDetailView.as_view(), name='academic_discipline_detail'),

    path('groups/', GroupsView.as_view(), name='groups_list'),
    path('groups/<int:id>/', GroupDetailView.as_view(), name='groups_detail'),

    path('direction_of_training/', DirectionOfTrainingView.as_view(), name='direction_of_training_list'),
    path('direction_of_training/<int:id>/', DirectionOfTrainingDetailView.as_view(),
         name='direction_of_training_detail'),
    path('direction_of_training/<int:id>/delete_discipline', DeleteDisciplineFromDirectionOfTrainingView.as_view(),
         name='del_discipline_from_direction_of_training'),

    path('students/', StudentView.as_view(), name='student_list'),
    path('students/<int:id>/', StudentDetailView.as_view(), name='student_detail'),
    path('report/', CreateReportView.as_view(), name='create_report'),

]
