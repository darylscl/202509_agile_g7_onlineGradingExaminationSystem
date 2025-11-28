from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',redirect_authenticated_user=True), name='login'),
    path("logout/", views.custom_logout, name="logout"),

    
    #Exam Module
    path("instructor/exams/", views.exam_list, name="instructor_exam_list"),
    path("instructor/exams/create/", views.exam_create, name="instructor_exam_create"),
    path("instructor/exams/<str:exam_id>/", views.exam_detail, name="instructor_exam_detail"),
    path("instructor/questions/<int:question_id>/edit/",views.question_update,name="instructor_question_update"),
    path("instructor/choices/<int:choice_id>/edit/",views.choice_update,name="instructor_choice_update"),
    path("instructor/exams/<str:exam_id>/edit/", views.exam_update, name="instructor_exam_update"),
    path("instructor/exams/<str:exam_id>/delete/", views.exam_delete, name="instructor_exam_delete"),
    path("instructor/exams/<str:exam_id>/questions/add/", views.question_create, name="instructor_question_create"),
    path("instructor/exams/<str:exam_id>/questions/<int:question_id>/delete/", views.question_delete, name="instructor_question_delete"),
    path("instructor/questions/<int:question_id>/choices/add/", views.choice_add, name="instructor_choice_add"),
    path("student/exams/available/", views.available_exams, name="student_available_exams"),
    path("student/exams/<str:exam_id>/take/", views.take_exam, name="student_take_exam"),
    path("student/attempts/<str:attempt_id>/result/", views.exam_result, name="student_exam_result"),
    
]