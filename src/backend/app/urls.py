from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    
    #Exam Module
    path("instructor/exams/", views.exam_list, name="instructor_exam_list"),
    path("instructor/exams/create/", views.exam_create, name="instructor_exam_create"),
    path("instructor/exams/<str:exam_id>/", views.exam_detail, name="instructor_exam_detail"),
    path("instructor/exams/<str:exam_id>/edit/", views.exam_update, name="instructor_exam_update"),
    path("instructor/exams/<str:exam_id>/delete/", views.exam_delete, name="instructor_exam_delete"),
    path("instructor/exams/<str:exam_id>/questions/add/", views.question_create, name="instructor_question_create"),
    path("instructor/exams/<str:exam_id>/questions/<int:question_id>/delete/", views.question_delete, name="instructor_question_delete"),
    path("instructor/questions/<int:question_id>/choices/add/", views.choice_add, name="instructor_choice_add"),
    path("student/exams/available/", views.available_exams, name="student_available_exams"),
    path("student/exams/<str:exam_id>/take/", views.take_exam, name="student_take_exam"),
    path("student/attempts/<str:attempt_id>/result/", views.exam_result, name="student_exam_result"),
    
]