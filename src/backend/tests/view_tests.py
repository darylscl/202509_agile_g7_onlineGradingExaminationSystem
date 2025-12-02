
from datetime import timedelta
from django.utils import timezone
from django.contrib.messages import get_messages
from app.views import *
import pytest
from app.models import Exam, ExamQuestion, Choice, ExamAttempt, Answer
from django.urls import reverse
from django.core.validators import validate_email

# User Module test
@pytest.mark.django_db
def test_student_register_success(client):
    data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "matric_number": "PPE0001",
        "contact_number": "0123456789",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }

    response = client.post(reverse("student_register"), data)

    assert response.status_code == 302
    assert response.url == reverse("universal_login")   

    student = Student.objects.first()
    assert student is not None
    assert student.student_email == "john@example.com"

    
@pytest.mark.django_db
def test_student_register_missing_fields(client):
    data = {
        "full_name": "",
        "email": "valid@example.com",
        "matric_number": "",
        "password": "",
        "confirm_password": "",
    }

    response = client.post(reverse("student_register"), data)
    assert response.status_code == 200

    messages = list(get_messages(response.wsgi_request))
    assert "All required fields must be filled." in str(messages[0])
    
@pytest.mark.django_db
def test_student_register_invalid_email(client):
    data = {
        "full_name": "John",
        "email": "not-an-email",
        "matric_number": "PPE0001",
        "password": "pass",
        "confirm_password": "pass",
    }

    response = client.post(reverse("student_register"), data)
    
    assert response.status_code == 200  

    messages = list(get_messages(response.wsgi_request))
    assert "Invalid email format." in str(messages[0])

    

@pytest.mark.django_db
def test_student_register_password_mismatch(client):
    data = {
        "full_name": "John",
        "email": "john@example.com",
        "matric_number": "PPE0001",
        "password": "pass1",
        "confirm_password": "pass2",
    }

    response = client.post(reverse("student_register"), data)
    
    assert response.status_code == 200  

    messages = list(get_messages(response.wsgi_request))
    assert "Passwords do not match." in str(messages[0])
    
    
@pytest.mark.django_db
def test_student_register_duplicate_email(client):
    Student.objects.create(
        full_name="User",
        student_email="john@example.com",
        matric_number="PPE0001",
        password="pass"
    )

    data = {
        "full_name": "Another User",
        "email": "john@example.com",
        "matric_number": "PPE0002",
        "password": "pass",
        "confirm_password": "pass",
    }

    response = client.post(reverse("student_register"), data)

    assert response.status_code == 200  

    messages = list(get_messages(response.wsgi_request))
    assert "Email is already registered." in str(messages[0])

    
@pytest.mark.django_db
def test_student_register_duplicate_matric(client):
    Student.objects.create(
        full_name="User",
        student_email="john@example.com",
        matric_number="PPE0001",
        password="pass"
    )

    data = {
        "full_name": "Another",
        "email": "another@example.com",
        "matric_number": "PPE0001",
        "password": "pass",
        "confirm_password": "pass",
    }

    response = client.post(reverse("student_register"), data)
    
    assert response.status_code == 200  

    messages = list(get_messages(response.wsgi_request))
    assert "Matric number already existed." in str(messages[0])

    
@pytest.mark.django_db
def test_instructor_register_success(client):
    data = {
        "full_name": "Mr Alan",
        "email": "alan@example.com",
        "contact_number": "0122222222",
        "department": "IT",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }

    response = client.post(reverse("instructor_register"), data)

    assert response.status_code == 302
    assert response.url == reverse("universal_login")

    instructor = Instructor.objects.first()
    assert instructor is not None
    assert instructor.instructor_email == "alan@example.com"
    
@pytest.mark.django_db
def test_instructor_register_missing_fields(client):
    data = {
        "full_name": "",
        "email": "",
        "password": "",
        "confirm_password": "",
    }

    response = client.post(reverse("instructor_register"), data)
    
    assert response.status_code == 200  

    messages = list(get_messages(response.wsgi_request))
    assert "All required fields must be filled." in str(messages[0])


@pytest.mark.django_db
def test_instructor_register_invalid_email(client):
    data = {
        "full_name": "Alan",
        "email": "bad-email",
        "password": "pass",
        "confirm_password": "pass",
    }

    response = client.post(reverse("instructor_register"), data)

    assert response.status_code == 200 

    messages = list(get_messages(response.wsgi_request))
    assert "Invalid email format." in str(messages[0])

@pytest.mark.django_db
def test_instructor_register_password_mismatch(client):
    data = {
        "full_name": "Alan",
        "email": "alan@example.com",
        "password": "pass1",
        "confirm_password": "pass2",
    }

    response = client.post(reverse("instructor_register"), data)
    
    assert response.status_code == 200  
    messages = list(get_messages(response.wsgi_request))
    assert "Passwords do not match." in str(messages[0])

@pytest.mark.django_db
def test_instructor_register_duplicate_email(client):
    Instructor.objects.create(
        full_name="Alan",
        instructor_email="alan@example.com",
        password="pass"
    )

    data = {
        "full_name": "New",
        "email": "alan@example.com", 
        "password": "pass",
        "confirm_password": "pass",
    }

    response = client.post(reverse("instructor_register"), data)
    assert response.status_code == 200 

    messages = list(get_messages(response.wsgi_request))
    assert "Email already registered." in str(messages[0])



# Exam module test
@pytest.mark.django_db
def test_exam_can_be_created_with_user():
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass"
    )

    exam = Exam.objects.create(
        title="Sample Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor
    )

    assert exam.exam_id.startswith("EX-")
    assert exam.title == "Sample Exam"

   
# ID auto increment 
@pytest.mark.django_db
def test_exam_id_increments():
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass"
    )

    e1 = Exam.objects.create(
        title="Exam1",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor
    )

    e2 = Exam.objects.create(
        title="Exam2",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor
    )

    assert e1.exam_id == "EX-001"
    assert e2.exam_id == "EX-002"

    
#Question creation  
@pytest.mark.django_db
def test_text_question_creation():
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass"
    )

    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor
    )

    question = ExamQuestion.objects.create(
        exam=exam,
        question_text="What is 2+2?",
        question_type="TEXT",
    )

    assert question.question_type == "TEXT"



# MCQ question creation
@pytest.mark.django_db
def test_mcq_with_choices():
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass"
    )

    exam = Exam.objects.create(
        title="Exam",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="Test",
        question_type="MCQ",
    )

    Choice.objects.create(choice_id=q, choice_text="A", is_correct=False)
    Choice.objects.create(choice_id=q, choice_text="B", is_correct=True)

    assert q.choices.count() == 2



# unique constraint test
@pytest.mark.django_db
def test_answer_unique_per_attempt():
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass"
    )

    student = Student.objects.create(
        full_name="Student",
        student_email="stu@example.com",
        matric_number="A001",
        password="pass"
    )

    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="Test",
        question_type="TEXT"
    )

    attempt = ExamAttempt.objects.create(exam=exam, student=student)

    Answer.objects.create(attempt=attempt, question=q, text_answer="A")

    with pytest.raises(Exception):
        Answer.objects.create(attempt=attempt, question=q, text_answer="B")

        
        
# Exam is open logic
@pytest.mark.django_db
def test_exam_is_open_true():
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now() - timedelta(minutes=1),
        end_time=timezone.now() + timedelta(minutes=1),
        created_by=instructor
    )

    assert exam.is_open is True
    
# Builder test
@pytest.mark.django_db
def test_exam_create_and_add_question(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teach@example.com",
        password="pass"
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post("/instructor/exams/create/", {
        "create_exam": "1",
        "title": "Exam",
        "description": "Desc",
        "start_time": "2025-11-20T12:00",
        "end_time": "2025-11-20T13:00",
    })

    assert response.status_code == 302
    exam = Exam.objects.first()
    assert exam is not None

    response = client.post(f"/instructor/exams/create/?exam_id={exam.exam_id}", {
        "add_question": "1",
        "question_text": "Test Question",
        "question_type": "TEXT"
    })

    assert exam.questions.count() == 1



# test listing exam view
@pytest.mark.django_db
def test_exam_list_view(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teach@example.com",
        password="pass"
    )

    exam1 = Exam.objects.create(
        title="Math Test",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor,
    )
    ExamQuestion.objects.create(exam=exam1, question_text="Q1", question_type="TEXT")
    ExamQuestion.objects.create(exam=exam1, question_text="Q2", question_type="MCQ")

    exam2 = Exam.objects.create(
        title="Science Test",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor,
    )
    ExamQuestion.objects.create(exam=exam2, question_text="Q1", question_type="TEXT")

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.get("/instructor/exams/")
    assert response.status_code == 200

    content = response.content
    assert b"Math Test" in content
    assert b"Science Test" in content
    assert b"2 Questions" in content
    assert b"1 Question" in content
  

    
# test edit exam
@pytest.mark.django_db
def test_exam_update_view(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    exam = Exam.objects.create(
        title="Math Test",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor,
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(
        f"/instructor/exams/{exam.exam_id}/edit/",
        {
            "title": "New Title",
            "description": "Updated desc",
            "start_time": exam.start_time,
            "end_time": exam.end_time,
        },
    )

    exam.refresh_from_db()
    assert response.status_code == 302
    assert exam.title == "New Title"
    
# test delete exam
@pytest.mark.django_db
def test_exam_delete_view(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )
    
    exam = Exam.objects.create(
        title="Math Test",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(f"/instructor/exams/{exam.exam_id}/delete/")

    assert response.status_code == 302
    assert not Exam.objects.filter(exam_id=exam.exam_id).exists()

@pytest.mark.django_db
def test_student_takes_exam_during_valid_schedule(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    student = Student.objects.create(
        full_name="Student",
        student_email="student@example.com",
        matric_number="A001",
        password="pass",
    )

    now = timezone.now()
    exam = Exam.objects.create(
        title="Sample Exam",
        description="desc",
        start_time=now - timedelta(minutes=10),
        end_time=now + timedelta(minutes=50),
        created_by=instructor,
    )

    # MCQ question
    q1 = ExamQuestion.objects.create(
        exam=exam,
        question_text="2 + 2 = ?",
        question_type="MCQ",
        order_no=1,
    )
    wrong = Choice.objects.create(choice_id=q1, choice_text="3", is_correct=False)
    correct = Choice.objects.create(choice_id=q1, choice_text="4", is_correct=True)

    # TEXT question
    q2 = ExamQuestion.objects.create(
        exam=exam,
        question_text="Explain your answer",
        question_type="TEXT",
        order_no=2,
    )

    # ⭐ SESSION-BASED LOGIN (CUSTOM AUTH)
    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()

    # Step 1: Load exam page
    response = client.get(f"/student/exams/{exam.exam_id}/take/")
    assert response.status_code == 200
    assert b"2 + 2" in response.content

    # Step 2: Submit exam
    post_data = {
        f"q_{q1.id}": str(correct.id),
        f"q_{q2.id}": "Because 2+2=4, obviously.",
    }
    response = client.post(f"/student/exams/{exam.exam_id}/take/", data=post_data)

    assert response.status_code == 302

    # Check attempt
    attempt = ExamAttempt.objects.get(exam=exam, student=student)

    # Check that attempt is marked submitted
    assert attempt.submitted_at is not None

    # Check MCQ answer
    a1 = Answer.objects.get(attempt=attempt, question=q1)
    assert a1.selected_choice == correct
    assert a1.marks == 1

    # Check TEXT answer
    a2 = Answer.objects.get(attempt=attempt, question=q2)
    assert a2.text_answer == "Because 2+2=4, obviously."

@pytest.mark.django_db
def test_student_sees_only_currently_available_exams(client):
    teacher = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    student = Student.objects.create(
        full_name="Student",
        student_email="student@example.com",
        matric_number="A100",
        password="pass",
    )

    now = timezone.now()

    # past exam (should NOT appear)
    Exam.objects.create(
        title="Past Exam",
        description="Already finished",
        start_time=now - timedelta(days=2),
        end_time=now - timedelta(days=1),
        created_by=teacher,
    )

    # future exam (should NOT appear)
    Exam.objects.create(
        title="Future Exam",
        description="Not started yet",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=2),
        created_by=teacher,
    )

    # current exam (should appear)
    Exam.objects.create(
        title="Current Exam",
        description="Happening now",
        start_time=now - timedelta(hours=1),
        end_time=now + timedelta(hours=1),
        created_by=teacher,
    )

    # ⭐ SESSION-BASED LOGIN (CUSTOM AUTH)
    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()

    # call the view
    response = client.get("/student/exams/available/")
    assert response.status_code == 200

    content = response.content

    assert b"Current Exam" in content
    assert b"Past Exam" not in content
    assert b"Future Exam" not in content

@pytest.mark.django_db
def test_student_submit_exam_for_processing(client):
    teacher = Instructor.objects.create(
        full_name="Teacher OEGS5",
        instructor_email="teacher_oegs5@example.com",
        password="pass",
    )
    student = Student.objects.create(
        full_name="Student OEGS5",
        student_email="student_oegs5@example.com",
        matric_number="A200",
        password="pass",
    )

    now = timezone.now()

    # exam currently available
    exam = Exam.objects.create(
        title="Processing Test Exam",
        description="For OEGS-5",
        start_time=now - timedelta(minutes=10),
        end_time=now + timedelta(minutes=50),
        created_by=teacher,
    )

    # MCQ question
    q1 = ExamQuestion.objects.create(
        exam=exam,
        question_text="2 + 3 = ?",
        question_type="MCQ",
        order_no=1,
    )
    wrong = Choice.objects.create(choice_id=q1, choice_text="4", is_correct=False)
    correct = Choice.objects.create(choice_id=q1, choice_text="5", is_correct=True)

    # TEXT question
    q2 = ExamQuestion.objects.create(
        exam=exam,
        question_text="Explain your calculation.",
        question_type="TEXT",
        order_no=2,
    )

    # ⭐ Session-based login instead of force_login
    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()

    # submit exam
    post_data = {
        f"q_{q1.id}": str(correct.id),
        f"q_{q2.id}": "Because 2 + 3 = 5.",
    }
    response = client.post(f"/student/exams/{exam.exam_id}/take/", data=post_data)

    # attempt created
    attempt = ExamAttempt.objects.get(exam=exam, student=student)

    # redirect to result page
    expected_url = reverse("student_exam_result", kwargs={"attempt_id": attempt.attempt_id})
    assert response.status_code == 302
    assert response["Location"] == expected_url

    # MCQ answer
    a1 = Answer.objects.get(attempt=attempt, question=q1)
    assert a1.selected_choice == correct
    assert a1.marks == 1

    # TEXT answer
    a2 = Answer.objects.get(attempt=attempt, question=q2)
    assert a2.text_answer == "Because 2 + 3 = 5."


@pytest.mark.django_db
def test_student_can_resume_ongoing_exam_attempt(client):
    teacher = Instructor.objects.create(
        full_name="Teacher Resume",
        instructor_email="teacher_resume@example.com",
        password="pass",
    )
    student = Student.objects.create(
        full_name="Student Resume",
        student_email="student_resume@example.com",
        matric_number="A300",
        password="pass",
    )

    now = timezone.now()

    exam = Exam.objects.create(
        title="Resume Exam",
        description="desc",
        start_time=now - timedelta(minutes=10),
        end_time=now + timedelta(minutes=50),
        created_by=teacher,
    )

    # MCQ question
    q1 = ExamQuestion.objects.create(
        exam=exam,
        question_text="2 + 2 = ?",
        question_type="MCQ",
        order_no=1,
    )
    Choice.objects.create(choice_id=q1, choice_text="3", is_correct=False)
    Choice.objects.create(choice_id=q1, choice_text="4", is_correct=True)

    # create an existing attempt (not submitted)
    attempt = ExamAttempt.objects.create(exam=exam, student=student)
    assert attempt.submitted_at is None
    assert ExamAttempt.objects.filter(exam=exam, student=student).count() == 1

    # ⭐ session-based login (no force_login)
    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()

    # student revisits the take exam page
    response = client.get(f"/student/exams/{exam.exam_id}/take/")
    assert response.status_code == 200
    assert b"2 + 2" in response.content

    # ensure NO new attempt is created
    assert ExamAttempt.objects.filter(exam=exam, student=student).count() == 1


@pytest.mark.django_db
def test_student_can_view_and_update_profile(client):
    # Create a student in DB
    student = Student.objects.create(
        full_name="Test Student",
        student_email="student1@example.com",
        matric_number="1234567890",
        contact_number="0123456789",
        password="hashed-password",
    )

    # Simulate "logged in" student via session
    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()

    url = reverse("student_profile")

    # VIEW: student can see their profile page
    response = client.get(url)
    assert response.status_code == 200
    assert b"Student Profile" in response.content
    assert student.full_name.encode() in response.content
    assert student.student_email.encode() in response.content

    # UPDATE: student submits new profile data
    new_data = {
        "full_name": "Updated Student",
        "student_email": "student_updated@example.com",
        "matric_number": "0987654321",
        "contact_number": "9999999999",
    }
    response = client.post(url, data=new_data, follow=True)

    # Should render OK (either after redirect or directly)
    assert response.status_code == 200

    # Data should be updated in DB
    student.refresh_from_db()
    assert student.full_name == "Updated Student"
    assert student.student_email == "student_updated@example.com"
    assert student.matric_number == "0987654321"
    assert student.contact_number == "9999999999"

@pytest.mark.django_db
def test_instructor_can_view_and_update_profile(client):
    # Create an instructor in DB
    instructor = Instructor.objects.create(
        full_name="Test Instructor",
        instructor_email="instructor1@example.com",
        contact_number="0112345678",
        department="Computer Science",
        password="hashed-password",
    )

    # Simulate "logged in" instructor via session
    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    url = reverse("instructor_profile")

    # VIEW: instructor can see their profile page
    response = client.get(url)
    assert response.status_code == 200
    assert b"Instructor Profile" in response.content
    assert instructor.full_name.encode() in response.content
    assert instructor.instructor_email.encode() in response.content

    # UPDATE: instructor submits new profile data
    new_data = {
        "full_name": "Updated Instructor",
        "instructor_email": "instructor_updated@example.com",
        "contact_number": "0222222222",
        "department": "Information Technology",
    }
    response = client.post(url, data=new_data, follow=True)

    assert response.status_code == 200

    # Data should be updated in DB
    instructor.refresh_from_db()
    assert instructor.full_name == "Updated Instructor"
    assert instructor.instructor_email == "instructor_updated@example.com"
    assert instructor.contact_number == "0222222222"
    assert instructor.department == "Information Technology"
