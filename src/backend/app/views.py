from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User #default django admin user for now, waiting for user
from .models import *

#To see different page for different user roles
# Login to django admin first
# Instructor: Username: instructor Password: 1234

# Helper function
def homepage(request):
    return render(request, "base.html")

def is_instructor(user):
    return user.is_staff  # treat staff as instructor currently

def get_default_user():
    from django.contrib.auth.models import User
    return User.objects.first()

# User viewset


# Exam Module Viewset
# User not yet implemented
# the url need to change

# @login_required
# @user_passes_test(is_instructor)
def exam_list(request):
    user = get_default_user()
    exams = Exam.objects.filter(created_by=user).order_by("-created_at")
    return render(request, "app/instructor/exam_list.html", {"exams": exams})
 # url need to change later when frontend comes in


# @login_required
# @user_passes_test(is_instructor)
def exam_create(request):
    user = get_default_user()
    exam = None
    exam_id = request.GET.get("exam_id")

    if exam_id:
        exam = Exam.objects.filter(exam_id=exam_id, created_by=user).first()

    # CREATE EXAM
    if request.method == "POST" and "create_exam" in request.POST:
        exam = Exam.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            start_time=request.POST.get("start_time"),
            end_time=request.POST.get("end_time"),
            created_by=user,
        )
        return redirect(f"/instructor/exams/create/?exam_id={exam.exam_id}")

    # ADD QUESTION
    if request.method == "POST" and "add_question" in request.POST:
        exam = Exam.objects.get(exam_id=exam_id, created_by=user)

        question = ExamQuestion.objects.create(
            exam=exam,
            question_text=request.POST.get("question_text"),
            question_type=request.POST.get("question_type"),
        )

        # MCQ Choices
        if question.question_type == "MCQ":
            choices = request.POST.getlist("choice_text")
            correct = request.POST.get("correct_choice")
            for idx, text in enumerate(choices):
                Choice.objects.create(
                    choice_id=question,
                    choice_text=text,
                    is_correct=(str(idx) == correct),
                )

        return redirect(f"/instructor/exams/create/?exam_id={exam.exam_id}")

    questions = exam.questions.all() if exam else []
    return render(request, "app/instructor/exam_form.html", {"exam": exam, "questions": questions})




# @login_required
# @user_passes_test(is_instructor)
def exam_detail(request, exam_id):
    user = get_default_user()
    exam = get_object_or_404(Exam, exam_id=exam_id, created_by=user)
    questions = exam.questions.prefetch_related("choices").order_by("order_no")

    return render(request, "app/instructor/exam_detail.html", {
        "exam": exam, "questions": questions
    })


# @login_required
# @user_passes_test(is_instructor)
def exam_update(request, exam_id):
    user = get_default_user()
    exam = get_object_or_404(Exam, exam_id=exam_id, created_by=user)

    if request.method == "POST":
        exam.title = request.POST.get("title", exam.title)
        exam.description = request.POST.get("description", exam.description)
        exam.start_time = request.POST.get("start_time", exam.start_time)
        exam.end_time = request.POST.get("end_time", exam.end_time)
        exam.save()
        return redirect("instructor_exam_detail", exam_id=exam.exam_id)

    return render(request, "app/instructor/exam_edit.html", {"exam": exam})




# @login_required
# @user_passes_test(is_instructor)
def exam_delete(request, exam_id):
    user = get_default_user()
    exam = get_object_or_404(Exam, exam_id=exam_id, created_by=user)
    exam.delete()
    return redirect("instructor_exam_list")




# @login_required
# @user_passes_test(is_instructor)
def question_create(request, exam_id):
    user = get_default_user()
    exam = get_object_or_404(Exam, exam_id=exam_id, created_by=user)

    if request.method == "POST":
        ExamQuestion.objects.create(
            exam=exam,
            question_text=request.POST.get("question_text"),
            question_type=request.POST.get("question_type"),
            order_no=request.POST.get("order_no") or 1,
        )
        return redirect("instructor_exam_detail", exam_id=exam.exam_id)

    return render(request, "app/instructor/question_form.html", {"exam": exam})


# @login_required
# @user_passes_test(is_instructor)
def question_update(request, question_id):
    question = get_object_or_404(ExamQuestion, id=question_id)
    exam = question.exam

    if request.method == "POST":
        old_type = question.question_type
        new_type = request.POST.get("question_type")

        question.question_text = request.POST.get("question_text")
        question.question_type = new_type
        question.save()

        if old_type == "TEXT" and new_type == "MCQ":
            question.choices.all().delete()

            choices = [
                request.POST.get("choice_text_0"),
                request.POST.get("choice_text_1"),
                request.POST.get("choice_text_2"),
                request.POST.get("choice_text_3"),
            ]
            correct = int(request.POST.get("correct_choice", 0))

            for i, text in enumerate(choices):
                Choice.objects.create(
                    choice_id=question,
                    choice_text=text,
                    is_correct=(i == correct),
                )

        elif old_type == "MCQ" and new_type == "TEXT":
            question.choices.all().delete()

        elif new_type == "MCQ":
            choices_qs = list(question.choices.all())

            for i, choice in enumerate(choices_qs):
                choice.choice_text = request.POST.get(f"choice_text_{i}")
                choice.is_correct = (str(i) == request.POST.get("correct_choice"))
                choice.save()

        return redirect("instructor_exam_detail", exam_id=exam.exam_id)

    return render(
        request,
        "app/instructor/question_form.html",
        {"question": question}
    )




# @login_required
# @user_passes_test(is_instructor)
def question_delete(request, exam_id, question_id):
    user = get_default_user()
    exam = get_object_or_404(Exam, exam_id=exam_id, created_by=user)
    question = get_object_or_404(ExamQuestion, id=question_id, exam=exam)

    question.delete()
    return redirect("instructor_exam_detail", exam_id=exam.exam_id)



# @login_required
# @user_passes_test(is_instructor)
def choice_add(request, question_id):
    question = get_object_or_404(ExamQuestion, id=question_id)

    if request.method == "POST":
        Choice.objects.create(
            choice_id=question,
            choice_text=request.POST.get("choice_text"),
            is_correct=bool(request.POST.get("is_correct")),
        )
        return redirect("instructor_exam_detail", exam_id=question.exam.exam_id)

    return render(request, "app/instructor/choice_form.html", {"question": question})


# @login_required
# @user_passes_test(is_instructor)
def choice_update(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)

    if request.method == "POST":
        choice.choice_text = request.POST.get("choice_text")
        choice.is_correct = bool(request.POST.get("is_correct"))
        choice.save()

        return redirect("instructor_exam_detail", exam_id=choice.choice_id.exam.exam_id)

    return render(request, "app/instructor/choice_form.html", {"choice": choice})


#@login_required
def available_exams(request):
    now = timezone.now()
    exams = Exam.objects.filter(start_time__lte=now, end_time__gte=now)
    return render(request, "app/student/available_exams.html", {"exams": exams})


#@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    
    if not exam.is_open:
        return render(request, "app/student/exam_closed.html", {"exam": exam})
    
    attempt, created = ExamAttempt.objects.get_or_create(
        exam=exam,
        student=request.user,
        defaults={},
    )
    
    if attempt.submitted:
        return render(request, "app/student/exam_done.html", {
            "exam": exam,
            "attempt": attempt
        })

    
    questions = exam.questions.all().order_by("order_no")
    
    if request.method == "POST":
        total_score = 0
        max_score = 0
        
        for q in questions:
            field_name = f"q_{q.id}"
            
            if q.question_type == "MCQ":
                choice_id = request.POST.get(field_name)
                if choice_id:
                    selected_choice = Choice.objects.filter(id=choice_id, choice_id=q).first()
                else:
                    selected_choice = None
                    
                answer, _ = Answer.objects.get_or_create(
                    attempt=attempt,
                    question=q,
                    defaults={"selected_choice": selected_choice},
                )
                answer.selected_choice = selected_choice
                answer.text_answer = ""
                
                if selected_choice and selected_choice.is_correct:
                    answer.marks = 1
                    total_score += 1
                else:
                    answer.marks = 0
                answer.save()
                max_score += 1
                
            else:
                text_value = request.POST.get(field_name, "")
                answer, _ = Answer.objects.get_or_create(
                    attempt=attempt,
                    question=q,
                    defaults={"text_answer": text_value},
                )
                answer.text_answer = text_value
                answer.marks = answer.marks or 0
                answer.selected_choice = None
                answer.save()
                
        attempt.submitted_at = timezone.now()
        attempt.score = total_score if max_score == 0 else total_score
        attempt.save()
        return redirect("student_exam_result", attempt_id=attempt.attempt_id)
    
    return render(
        request,
        "app/student/take_exam.html",
        {"exam": exam, "questions": questions, "attempt": attempt},
    )


#@login_required
def exam_result(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, attempt_id=attempt_id, student=request.user)
    answers = attempt.answers.select_related("question", "selected_choice")
    return render(
        request,
        "app/student/exam_result.html",
        {"attempt": attempt, "answers": answers},
    )