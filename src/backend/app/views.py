from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import *
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from django.contrib import messages
import re
from django.utils.dateparse import parse_datetime

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d).{8,}$"
CONTACT_REGEX = r"^\d{10,11}$"
MATRIC_REGEX = r"^PPE\d{4}$"

#todo list:
# Update marks not able to save error


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

        context = {
            "full_name": full_name,
            "email": email,
            "matric": matric,
            "contact": contact,
        }

        if not full_name or not email or not matric or not password:
            messages.error(request, "All required fields must be filled.")
            return render(request, "app/student/register.html", context)
        
        if not re.search(r"[A-Za-z]", full_name):
            messages.error(request, "Full name must contain at least one letter.")
            return render(request, "app/student/register.html", context)


        if len(full_name) < 3:
            messages.error(request, "Full name must be at least 3 characters.")
            return render(request, "app/student/register.html", context)

        if not re.match(EMAIL_REGEX, email):
            messages.error(request, "Invalid email format.")
            return render(request, "app/student/register.html", context)

        if not re.match(MATRIC_REGEX, matric):
            messages.error(request, "Matric number must follow the format PPE0000 (e.g., PPE1234).")
            return render(request, "app/student/register.html", context)

        if contact and not contact.isdigit():
            messages.error(request, "Contact number must contain only digits.")
            return render(request, "app/student/register.html", context)

        if contact and not (10 <= len(contact) <= 11):
            messages.error(request, "Contact number must be 10–11 digits.")
            return render(request, "app/student/register.html", context)

        if Student.objects.filter(student_email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "app/student/register.html", context)

        if Student.objects.filter(matric_number=matric).exists():
            messages.error(request, "Matric number already existed.")
            return render(request, "app/student/register.html", context)

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "app/student/register.html", context)

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "app/student/register.html", context)

        if password.isalpha() or password.isdigit():
            messages.error(request, "Password must contain both letters and numbers.")
            return render(request, "app/student/register.html", context)

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



def student_profile(request):
    student_id = request.session.get("user_id")
    student = get_object_or_404(Student, student_ID=student_id)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("student_email")
        matric = request.POST.get("matric_number")
        contact = request.POST.get("contact_number")

        # simple validation
        if not full_name or not email or not matric:
            messages.error(request, "Full name, email and matric number are required.")
            return render(request, "app/student/profile.html", {"student": student})

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return render(request, "app/student/profile.html", {"student": student})

        if Student.objects.filter(student_email=email).exclude(student_ID=student.student_ID).exists():
            messages.error(request, "This email is already used by another student.")
            return render(request, "app/student/profile.html", {"student": student})

        if Student.objects.filter(matric_number=matric).exclude(student_ID=student.student_ID).exists():
            messages.error(request, "This matric number is already used by another student.")
            return render(request, "app/student/profile.html", {"student": student})

        student.full_name = full_name
        student.student_email = email
        student.matric_number = matric
        student.contact_number = contact
        student.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("student_profile")

    return render(request, "app/student/profile.html", {"student": student})


@instructor_required
def instructor_profile(request):
    instructor_id = request.session.get("user_id")
    instructor = get_object_or_404(Instructor, instructor_ID=instructor_id)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("instructor_email")
        contact = request.POST.get("contact_number")
        department = request.POST.get("department")

        if not full_name or not email:
            messages.error(request, "Full name and email are required.")
            return render(request, "app/instructor/profile.html", {"instructor": instructor})

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return render(request, "app/instructor/profile.html", {"instructor": instructor})

        if Instructor.objects.filter(instructor_email=email).exclude(instructor_ID=instructor.instructor_ID).exists():
            messages.error(request, "This email is already used by another instructor.")
            return render(request, "app/instructor/profile.html", {"instructor": instructor})

        instructor.full_name = full_name
        instructor.instructor_email = email
        instructor.contact_number = contact
        instructor.department = department
        instructor.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("instructor_profile")

    return render(request, "app/instructor/profile.html", {"instructor": instructor})



def instructor_register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        contact = request.POST.get("contact_number")
        department = request.POST.get("department")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        context = {
            "full_name": full_name,
            "email": email,
            "contact": contact,
            "department": department,
        }

        if not full_name or not email or not password:
            messages.error(request, "All required fields must be filled.")
            return render(request, "app/instructor/register.html", context)
        
        if not re.search(r"[A-Za-z]", full_name):
            messages.error(request, "Full name must contain at least one letter.")
            return render(request, "app/instructor/register.html", context)


        if len(full_name) < 3:
            messages.error(request, "Full name must be at least 3 characters.")
            return render(request, "app/instructor/register.html", context)

        if not re.match(EMAIL_REGEX, email):
            messages.error(request, "Invalid email format.")
            return render(request, "app/instructor/register.html", context)

        if contact and not contact.isdigit():
            messages.error(request, "Contact number must contain only digits.")
            return render(request, "app/instructor/register.html", context)

        if contact and not (10 <= len(contact) <= 11):
            messages.error(request, "Contact number must be 10–11 digits.")
            return render(request, "app/instructor/register.html", context)

        if Instructor.objects.filter(instructor_email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "app/instructor/register.html", context)

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "app/instructor/register.html", context)

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "app/instructor/register.html", context)

        if password.isalpha() or password.isdigit():
            messages.error(request, "Password must contain both letters and numbers.")
            return render(request, "app/instructor/register.html", context)

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

    if request.method == "POST" and "create_exam" in request.POST:
        title = (request.POST.get("title") or "").strip()
        description = request.POST.get("description") or ""
        start_date = request.POST.get("start_date") or ""
        start_time_part = request.POST.get("start_time") or ""
        end_date = request.POST.get("end_date") or ""
        end_time_part = request.POST.get("end_time") or ""
        

        if not title or not start_date or not start_time_part or not end_date or not end_time_part:
            messages.error(
                request,
                "All fields (title, start time, end time) are required.",
            )
            return render(
                request,
                "app/instructor/exam_form.html",
                {"exam": exam, "questions": exam.questions.all() if exam else []},
            )
            
        start_raw = f"{start_date} {start_time_part}"
        end_raw = f"{end_date} {end_time_part}"
        start_time = parse_datetime(start_raw)
        end_time = parse_datetime(end_raw)

        if not start_time or not end_time:
            messages.error(request, "Please enter a valid date and time.")
            return render(
                request,
                "app/instructor/exam_form.html",
                {"exam": exam, "questions": exam.questions.all() if exam else []},
            )

        if timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time)
        if timezone.is_naive(end_time):
            end_time = timezone.make_aware(end_time)
            
        if end_time <= start_time:
            messages.error(request, "End time must be after start time.")
            return render(
                request,
                "app/instructor/exam_form.html",
                {"exam": exam, "questions": exam.questions.all() if exam else []},
            )
            
        now = timezone.now()
        if start_time < now:
            messages.error(request, "Start time cannot be earlier than the current date & time.")
            return render(request, "app/instructor/exam_form.html",
                          {"exam": exam, "questions": exam.questions.all() if exam else []})

        try:
            exam = Exam.objects.create(
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
                created_by=instructor,
            )
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return render(
                request,
                "app/instructor/exam_form.html",
                {"exam": None, "questions": []},
            )

        return redirect(f"/instructor/exams/create/?exam_id={exam.exam_id}")

    if request.method == "POST" and "add_question" in request.POST:
        exam = Exam.objects.get(exam_id=exam_id, created_by=instructor)
        
        marks = request.POST.get("marks", "1")
        try:
            marks = float(marks)
        except:
            marks = 1
        question = ExamQuestion.objects.create(
            exam=exam,
            question_text=request.POST.get("question_text"),
            question_type=request.POST.get("question_type"),
            marks=marks,
        )

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
    exam = get_object_or_404(Exam, exam_id=exam_id, created_by=instructor)

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        description = request.POST.get("description") or ""

        start_date = request.POST.get("start_date") or ""
        start_time_part = request.POST.get("start_time") or ""
        end_date = request.POST.get("end_date") or ""
        end_time_part = request.POST.get("end_time") or ""

        if not title or not start_date or not start_time_part or not end_date or not end_time_part:
            messages.error(request, "All fields (title, start time, end time) are required.")
            return render(request, "app/instructor/exam_edit.html", {"exam": exam})

        start_raw = f"{start_date} {start_time_part}"
        end_raw = f"{end_date} {end_time_part}"

        start_time = parse_datetime(start_raw)
        end_time = parse_datetime(end_raw)

        if not start_time or not end_time:
            messages.error(request, "Please enter a valid date and time.")
            return render(request, "app/instructor/exam_edit.html", {"exam": exam})

        if timezone.is_naive(start_time):
            start_time = timezone.make_aware(start_time)
        if timezone.is_naive(end_time):
            end_time = timezone.make_aware(end_time)

        exam.title = title
        exam.description = description
        exam.start_time = start_time
        exam.end_time = end_time

        try:
            exam.full_clean()  
            exam.save()
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return render(request, "app/instructor/exam_edit.html", {"exam": exam})

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

    # 1️⃣ Only MCQ can have choices
    if question.question_type != "MCQ":
        messages.error(request, "Choices can only be added to MCQ questions.")
        return redirect("instructor_exam_detail", exam_id=question.exam.exam_id)

    if request.method == "POST":
        choice_text = request.POST.get("choice_text", "").strip()
        is_correct = request.POST.get("is_correct") == "on"

        if not choice_text:
            messages.error(request, "Choice text cannot be empty.")
            return render(request, "app/instructor/choice_form.html", {"question": question, "exam": question.exam,})

        if question.choices.count() >= 4:
            messages.error(request, "Maximum 4 choices allowed.")
            return redirect("instructor_exam_detail", exam_id=question.exam.exam_id)

        if question.choices.filter(choice_text__iexact=choice_text).exists():
            messages.error(request, "Duplicate choices are not allowed.")
            return redirect("instructor_exam_detail", exam_id=question.exam.exam_id)

        if is_correct and question.choices.filter(is_correct=True).exists():
            messages.error(request, "Only one correct answer is allowed.")
            return redirect("instructor_exam_detail", exam_id=question.exam.exam_id)

        Choice.objects.create(
            choice_id=question,
            choice_text=choice_text,
            is_correct=is_correct,
        )

        return redirect("instructor_exam_detail", exam_id=question.exam.exam_id)

    return render(request, "app/instructor/choice_form.html", {"question": question})


def choice_update(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    question = choice.choice_id

    if request.method == "POST":
        choice_text = request.POST.get("choice_text", "").strip()
        is_correct = request.POST.get("is_correct") == "on"

        if not choice_text:
            messages.error(request, "Choice text cannot be empty.")
            return render(
                request,
                "app/instructor/choice_form.html",
                {"choice": choice},
            )

        if question.choices.exclude(id=choice.id).filter(
            choice_text__iexact=choice_text
        ).exists():
            messages.error(request, "Duplicate choices are not allowed.")
            return redirect(
                "instructor_exam_detail",
                exam_id=question.exam.exam_id,
            )

        if is_correct and question.choices.exclude(id=choice.id).filter(is_correct=True).exists():
            messages.error(request, "Only one correct answer is allowed.")
            return redirect(
                "instructor_exam_detail",
                exam_id=question.exam.exam_id,
            )

        choice.choice_text = choice_text
        choice.is_correct = is_correct
        choice.save()

        return redirect(
            "instructor_exam_detail",
            exam_id=question.exam.exam_id,
        )

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

