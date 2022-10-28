from django.urls import path

from studying_process.views import AcademicDisciplineView, AcademicDisciplineDetailView

app_name = "studying_process"

urlpatterns = [
    path('academic_disciplines/', AcademicDisciplineView.as_view(), name='academic_disciplines_list'),
    path('academic_disciplines/<int:id>/', AcademicDisciplineDetailView.as_view(), name='academic_discipline_detail'),
    # path('<int:id>/', PictureDetailView.as_view(), name='picture_detail'),
    # path('<int:id>/resize', ResizePictureView.as_view(), name='picture_resize'),

]