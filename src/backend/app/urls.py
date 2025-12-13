from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("signup/", views.signup_role_select, name="signup_role_select"),
    path("login/", views.universal_login, name="universal_login"),
    path("logout/", views.custom_logout, name="logout"),
    path("login/", views.universal_login, name="student_login"),
    path("login/", views.universal_login, name="instructor_login"),
    path("login/", views.universal_login, name="universal_login"),
    
    
    #User module
    path("register/student/", views.student_register, name="student_register"),
    path("register/instructor/", views.instructor_register, name="instructor_register"),

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
    path("student/exams/", views.available_exams, name="student_available_exams"),
    path("student/exams/available/", views.available_exams, name="student_available_exams_alias"),
    path("student/exams/<str:exam_id>/take/", views.take_exam, name="student_take_exam"),
    path("student/attempts/<str:attempt_id>/result/", views.exam_result, name="student_exam_result"),
    path("student/results/", views.student_results, name="student_results"),
    path('instructor/exams/<str:exam_id>/submissions/', views.exam_submissions, name='instructor_exam_submissions'),
    path('instructor/exams/<str:exam_id>/grade-distribution/', views.grade_distribution, name='instructor_grade_distribution'),
    path('instructor/submission/<str:attempt_id>/', views.view_submission, name='instructor_view_submission'),
    path('instructor/student/<str:student_id>/history/', views.student_history, name='instructor_student_history'),
    path('instructor/results/', views.instructor_results, name='instructor_results'),
    path("student/profile/", views.student_profile, name="student_profile"),
    path("instructor/profile/", views.instructor_profile, name="instructor_profile"),
]