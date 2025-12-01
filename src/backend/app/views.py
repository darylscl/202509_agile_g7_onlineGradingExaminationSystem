from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import *


#Session login
def student_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            student = Student.objects.get(student_email=email)
        except Student.DoesNotExist:
            messages.error(request, "No user found with this email")
            return render(request, "login.html", {})
        
        if not check_password(password, student.password):
            messages.error(request, "Invalid password")
            return render(request, "login.html", {})
        
        request.session["user_type"] = "student"
        request.session["user_id"] = student.student_ID
        return redirect("homepage")
    
    return render(request, "app/login.html", {"user_type": "student"})

def instructor_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            instructor = Instructor.objects.get(instructor_email=email)
        except Instructor.DoesNotExist:
            messages.error(request, "No user found with this email")
            return render(request, "login.html", {})

        if not check_password(password, instructor.password):
            messages.error(request, "Invalid password.")
            return render(request, "login.html", {})

        request.session["user_type"] = "instructor"
        request.session["user_id"] = instructor.instructor_ID 
        return redirect("homepage")

    return render(request, "app/login.html", {"user_type": "instructor"})

def universal_login(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if Student.objects.filter(student_email=email).exists():
            return student_login(request)

        if Instructor.objects.filter(instructor_email=email).exists():
            return instructor_login(request)

        messages.error(request, "No account found with this email.")
        return redirect("universal_login")

    return render(request, "login.html")


def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get("user_type") != "student":
            return redirect("student_login")
        return view_func(request, *args, **kwargs)
    return wrapper

def instructor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get("user_type") != "instructor":
            return redirect("instructor_login")
        return view_func(request, *args, **kwargs)
    return wrapper


#To see different page for different user roles
# Login to django admin first
# Instructor: Username: instructor Password: 1234

# Helper function
def homepage(request):
    user_type = request.session.get("user_type")
    
    if not user_type:
        return render(request, "home_public.html")

    if user_type == "instructor":
        return render(request, "app/instructor/dashboard.html")

    return render(request, "app/student/dashboard.html")


def is_instructor(user):
    return   # treat staff as instructor currently


def custom_logout(request):
    request.session.flush()
    return redirect("homepage")

def signup_role_select(request):
    return render(request, "signup.html")



# User viewset
def student_register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        matric = request.POST.get("matric_number")
        contact = request.POST.get("contact_number")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")
        
        #validation
        if not full_name or not email or not matric or not password:
            messages.error(request, "All required fields must be filled.")
            return redirect("student_register")
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect("student_register")
        
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("student_register")
        
        if Student.objects.filter(student_email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("student_register")
        
        if Student.objects.filter(matric_number=matric).exists():
            messages.error(request, "Matric number already existed.")
            return redirect("student_register")
        
        Student.objects.create(
            full_name=full_name,
            student_email=email,
            matric_number=matric,
            contact_number=contact,
            password=make_password(password),  
        )
        
        messages.success(request, "Registration successful. Please log in.")
        return redirect("universal_login")
    
    return render(request, "app/student/register.html")

def instructor_register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        contact = request.POST.get("contact_number")
        department = request.POST.get("department")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")
        
        #validation
        if not full_name or not email or not password:
            messages.error(request, "All required fields must be filled.")
            return redirect("instructor_register")
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return redirect("instructor_register")
        
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("instructor_register")
        
        if Instructor.objects.filter(instructor_email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("instructor_register")
        
        Instructor.objects.create(
            full_name=full_name,
            instructor_email=email,
            contact_number=contact,
            department=department,
            password=make_password(password),  
        )
        
        messages.success(request, "Instructor account created. Please log in.")
        return redirect("universal_login")
    
    return render(request, "app/instructor/register.html")

# Exam Module Viewset
def available_exams(request):
    now = timezone.now()
    exams = Exam.objects.filter(start_time__lte=now, end_time__gte=now)
    from .models import ExamAttempt
    student_id = request.session.get("user_id")
    student = Student.objects.get(student_ID=student_id)
    attempts = ExamAttempt.objects.filter(student=student, submitted_at__isnull=False)
    done_exam_ids = set(attempt.exam_id for attempt in attempts)
    return render(request, "app/student/available_exams.html", {
        "exams": exams,
        "now": now,
        "done_exam_ids": done_exam_ids,
    })


def exam_submissions(request, exam_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    attempts = ExamAttempt.objects.filter(exam=exam, submitted_at__isnull=False).select_related('student').order_by('-submitted_at')
    return render(request, "app/instructor/exam_submissions.html", {
        "exam": exam,
        "attempts": attempts,
    })

def view_submission(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, attempt_id=attempt_id)
    answers = attempt.answers.select_related("question", "selected_choice")
    # Calculate totals for template
    total_possible = sum([a.question.marks or 0 for a in answers])
    total_awarded = sum([a.marks or 0 for a in answers])
    if request.method == "POST":
        # Example: update marks for each answer
        for answer in answers:
            mark = request.POST.get(f"mark_{answer.id}")
            if mark is not None:
                answer.marks = float(mark)
                answer.save()
        # Optionally, update total score
        attempt.score = sum(a.marks or 0 for a in answers)
        attempt.save()
    return render(request, "app/instructor/view_submission.html", {
        "attempt": attempt,
        "answers": answers,
        "total_possible": total_possible,
        "total_awarded": total_awarded,
    })

def exam_list(request):
    instructor_id = request.session.get("user_id")
    instructor = Instructor.objects.get(instructor_ID=instructor_id)
    exams = Exam.objects.filter(created_by=instructor).order_by("-created_at")
    return render(request, "app/instructor/exam_list.html", {"exams": exams})
 # url need to change later when frontend comes in


def exam_create(request):
    instructor_id = request.session.get("user_id")
    instructor = Instructor.objects.get(instructor_ID=instructor_id)
    exam = None
    exam_id = request.GET.get("exam_id")

    if exam_id:
        exam = Exam.objects.filter(exam_id=exam_id, created_by=instructor).first()

    # CREATE EXAM
    if request.method == "POST" and "create_exam" in request.POST:
        exam = Exam.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            start_time=request.POST.get("start_time"),
            end_time=request.POST.get("end_time"),
            created_by=instructor,
        )
        return redirect(f"/instructor/exams/create/?exam_id={exam.exam_id}")

    # ADD QUESTION
    if request.method == "POST" and "add_question" in request.POST:
        exam = Exam.objects.get(exam_id=exam_id, created_by=instructor)

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




def exam_detail(request, exam_id):
    instructor_id = request.session.get("user_id")
    instructor = Instructor.objects.get(instructor_ID=instructor_id)
    user = instructor
    exam = get_object_or_404(Exam, exam_id=exam_id, created_by=user)
    questions = exam.questions.prefetch_related("choices").order_by("order_no")

    return render(request, "app/instructor/exam_detail.html", {
        "exam": exam, "questions": questions
    })


def exam_update(request, exam_id):
    instructor_id = request.session.get("user_id")
    instructor = Instructor.objects.get(instructor_ID=instructor_id)
    user = instructor
    exam = get_object_or_404(Exam, exam_id=exam_id, created_by=user)

    if request.method == "POST":
        exam.title = request.POST.get("title", exam.title)
        exam.description = request.POST.get("description", exam.description)
        exam.start_time = request.POST.get("start_time", exam.start_time)
        exam.end_time = request.POST.get("end_time", exam.end_time)
        exam.save()
        return redirect("instructor_exam_detail", exam_id=exam.exam_id)

    return render(request, "app/instructor/exam_edit.html", {"exam": exam})




def exam_delete(request, exam_id):
    instructor_id = request.session.get("user_id")
    instructor = Instructor.objects.get(instructor_ID=instructor_id)
    user = instructor
    exam = get_object_or_404(Exam, exam_id=exam_id, created_by=user)
    exam.delete()
    return redirect("instructor_exam_list")




def question_create(request, exam_id):
    instructor_id = request.session.get("user_id")
    instructor = Instructor.objects.get(instructor_ID=instructor_id)
    user = instructor
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


def question_update(request, question_id):
    question = get_object_or_404(ExamQuestion, id=question_id)
    exam = question.exam

    if request.method == "POST":
        old_type = question.question_type
        new_type = request.POST.get("question_type")

        question.question_text = request.POST.get("question_text")
        question.question_type = new_type
        marks_value = request.POST.get("marks")
        if marks_value is not None:
            try:
                question.marks = float(marks_value)
            except ValueError:
                question.marks = 1  # fallback/default
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




def question_delete(request, exam_id, question_id):
    instructor_id = request.session.get("user_id")
    instructor = Instructor.objects.get(instructor_ID=instructor_id)
    user = instructor
    exam = get_object_or_404(Exam, exam_id=exam_id, created_by=user)
    question = get_object_or_404(ExamQuestion, id=question_id, exam=exam)

    question.delete()
    return redirect("instructor_exam_detail", exam_id=exam.exam_id)



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


def choice_update(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)

    if request.method == "POST":
        choice.choice_text = request.POST.get("choice_text")
        choice.is_correct = bool(request.POST.get("is_correct"))
        choice.save()

        return redirect("instructor_exam_detail", exam_id=choice.choice_id.exam.exam_id)

    return render(request, "app/instructor/choice_form.html", {"choice": choice})


def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    
    if not exam.is_open:
        return render(request, "app/student/exam_closed.html", {"exam": exam})
    
    student_id = request.session.get("user_id")
    student = Student.objects.get(student_ID=student_id)
    attempt, created = ExamAttempt.objects.get_or_create(exam=exam,student=student)
    
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

def student_results(request):
    """
    Display a list of all completed exam attempts for the logged-in student.
    """
    student_id = request.session.get("user_id")
    student = Student.objects.get(student_ID=student_id)
    attempts = ExamAttempt.objects.filter(student=student, submitted_at__isnull=False).select_related("exam").order_by("-submitted_at")
    # Prepare extra info for each attempt: total_possible and grade
    attempt_list = []
    for attempt in attempts:
        answers = attempt.answers.select_related("question", "selected_choice")
        total_possible = sum([a.question.marks or 0 for a in answers])
        total_awarded = sum([a.marks or 0 for a in answers])
        if total_possible > 0:
            percent = total_awarded / total_possible
            if percent >= 0.9:
                grade = "A"
            elif percent >= 0.8:
                grade = "B"
            elif percent >= 0.7:
                grade = "C"
            elif percent >= 0.6:
                grade = "D"
            else:
                grade = "F"
            status = "Pass" if percent >= 0.5 else "Fail"
        else:
            grade = "N/A"
            status = "N/A"
        attempt_list.append({
            "exam": attempt.exam,
            "score": attempt.score,
            "submitted_at": attempt.submitted_at,
            "attempt_id": attempt.attempt_id,
            "total_possible": total_possible,
            "grade": grade,
            "status": status,
        })
    return render(request, "app/student/results.html", {"attempts": attempt_list})

def exam_result(request, attempt_id):
    student_id = request.session.get("user_id")
    student = Student.objects.get(student_ID=student_id)
    attempt = get_object_or_404(ExamAttempt, attempt_id=attempt_id, student=student)
    answers = attempt.answers.select_related("question", "selected_choice")
    # Calculate total possible marks
    total_possible = sum([a.question.marks for a in answers])
    # Calculate total awarded marks
    total_awarded = sum([a.marks for a in answers if a.marks is not None])
    # Grade calculation (example: A/B/C/D/F)
    if total_possible > 0:
        percent = total_awarded / total_possible
        if percent >= 0.9:
            grade = "A"
        elif percent >= 0.8:
            grade = "B"
        elif percent >= 0.7:
            grade = "C"
        elif percent >= 0.6:
            grade = "D"
        else:
            grade = "F"
    else:
        grade = "N/A"
    return render(
        request,
        "app/student/exam_result.html",
        {"attempt": attempt, "answers": answers, "total_possible": total_possible, "total_awarded": total_awarded, "grade": grade},
    )

