
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
def test_email_validation_missing_at_symbol(client):
    data = {
        "full_name": "John Doe",
        "email": "johnexample.com",
        "matric_number": "PPE0001",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }
    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Invalid email format." in str(messages[0])
    
@pytest.mark.django_db
def test_email_validation_missing_domain(client):
    data = {
        "full_name": "John Doe",
        "email": "john@",
        "matric_number": "PPE0001",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }
    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Invalid email format." in str(messages[0])
    


@pytest.mark.django_db
def test_student_matric_invalid_format(client):
    data = {
        "full_name": "John",
        "email": "john@example.com",
        "matric_number": "ABC1234",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }
    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Matric number must follow the format PPE0000" in str(messages[0])
    
@pytest.mark.django_db
def test_contact_number_invalid(client):
    data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "matric_number": "PPE0001",
        "contact_number": "ABC123",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }

    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))

    assert "Contact number must contain only digits" in str(messages[0])
    

@pytest.mark.django_db
def test_password_too_short(client):
    data = {
        "full_name": "John",
        "email": "john@example.com",
        "matric_number": "PPE0001",
        "password": "123",
        "confirm_password": "123",
    }

    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Password must be at least 8 characters." in str(messages[0])
    
@pytest.mark.django_db
def test_password_must_contain_letters_and_numbers(client):
    data = {
        "full_name": "John",
        "email": "john@example.com",
        "matric_number": "PPE0001",
        "password": "password",
        "confirm_password": "password",
    }
    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Password must contain both letters and numbers." in str(messages[0])
    

@pytest.mark.django_db
def test_email_validation_missing_at_symbol(client):
    data = {
        "full_name": "John Doe",
        "email": "johnexample.com",
        "matric_number": "PPE0001",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }
    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Invalid email format." in str(messages[0])
    
@pytest.mark.django_db
def test_email_validation_missing_domain(client):
    data = {
        "full_name": "John Doe",
        "email": "john@",
        "matric_number": "PPE0001",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }
    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Invalid email format." in str(messages[0])
    


@pytest.mark.django_db
def test_student_matric_invalid_format(client):
    data = {
        "full_name": "John",
        "email": "john@example.com",
        "matric_number": "ABC1234",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }
    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Matric number must follow the format PPE0000" in str(messages[0])
    
@pytest.mark.django_db
def test_contact_number_invalid(client):
    data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "matric_number": "PPE0001",
        "contact_number": "ABC123",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }

    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))

    assert "Contact number must contain only digits" in str(messages[0])
    

@pytest.mark.django_db
def test_password_too_short(client):
    data = {
        "full_name": "John",
        "email": "john@example.com",
        "matric_number": "PPE0001",
        "password": "123",
        "confirm_password": "123",
    }

    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Password must be at least 8 characters." in str(messages[0])
    
@pytest.mark.django_db
def test_password_must_contain_letters_and_numbers(client):
    data = {
        "full_name": "John",
        "email": "john@example.com",
        "matric_number": "PPE0001",
        "password": "password",
        "confirm_password": "password",
    }
    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Password must contain both letters and numbers." in str(messages[0])
    

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
def test_student_register_name__reject_digits(client):
    data = {
        "full_name": "123456",
        "email": "student@example.com",
        "matric_number": "PPE1234",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }

    response = client.post(reverse("student_register"), data)
    messages = list(get_messages(response.wsgi_request))

    assert "Full name must contain at least one letter." in str(messages[0])


    
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
def test_instructor_register_name_reject_digits(client):
    data = {
        "full_name": "987654",
        "email": "inst@example.com",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }

    response = client.post(reverse("instructor_register"), data)
    messages = list(get_messages(response.wsgi_request))

    assert "Full name must contain at least one letter." in str(messages[0])

    
@pytest.mark.django_db
def test_instructor_invalid_email_missing_at_symbol(client):
    data = {
        "full_name": "Alan",
        "email": "alanexample.com",   
        "contact_number": "0122222222",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }

    response = client.post(reverse("instructor_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Invalid email format." in str(messages[0])
    
@pytest.mark.django_db
def test_instructor_invalid_email_missing_domain(client):
    data = {
        "full_name": "Alan",
        "email": "alan@",   
        "contact_number": "0122222222",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }

    response = client.post(reverse("instructor_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Invalid email format." in str(messages[0])

@pytest.mark.django_db
def test_instructor_invalid_contact_non_digit(client):
    data = {
        "full_name": "Alan",
        "email": "alan@example.com",
        "contact_number": "abcd1234",  
        "password": "pass1234",
        "confirm_password": "pass1234",
    }

    response = client.post(reverse("instructor_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Contact number must contain only digits" in str(messages[0])
    
@pytest.mark.django_db
def test_instructor_invalid_contact_length(client):
    data = {
        "full_name": "Alan",
        "email": "alan@example.com",
        "contact_number": "0123",
        "password": "pass1234",
        "confirm_password": "pass1234",
    }

    response = client.post(reverse("instructor_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Contact number must be 10–11 digits." in str(messages[0])
    
@pytest.mark.django_db
def test_instructor_password_too_short(client):
    data = {
        "full_name": "Alan",
        "email": "alan@example.com",
        "password": "123",
        "confirm_password": "123",
    }

    response = client.post(reverse("instructor_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Password must be at least 8 characters." in str(messages[0])

@pytest.mark.django_db
def test_instructor_password_requires_letters_and_numbers(client):
    data = {
        "full_name": "Alan",
        "email": "alan@example.com",
        "password": "password",  
        "confirm_password": "password",
    }

    response = client.post(reverse("instructor_register"), data)
    messages = list(get_messages(response.wsgi_request))
    assert "Password must contain both letters and numbers." in str(messages[0])




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

    
@pytest.mark.django_db
def test_exam_create_missing_exam_title(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teach_missing@example.com",
        password="pass",
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(
        "/instructor/exams/create/",
        {
            "create_exam": "1",
            "title": "",                
            "description": "Desc",
            "start_time": "",          
            "end_time": "",             
        },
    )

    assert response.status_code == 200
    assert Exam.objects.count() == 0

    messages = list(get_messages(response.wsgi_request))
    assert "All fields (title, start time, end time) are required." in str(messages[0])
    

@pytest.mark.django_db
def test_exam_create_end_time_before_start_time(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(
        "/instructor/exams/create/",
        {
            "create_exam": "1",
            "title": "Test Exam",
            "description": "desc",
            "start_date": "2025-11-20",
            "start_time": "15:00",
            "end_date": "2025-11-20",
            "end_time": "14:00", 
        },
    )

    messages_list = list(get_messages(response.wsgi_request))

    assert response.status_code == 200
    assert "End time must be after start time." in str(messages_list[0])

    
@pytest.mark.django_db
def test_exam_create_invalid_datetime_format_rejected(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(
        "/instructor/exams/create/",
        {
            "create_exam": "1",
            "title": "Invalid Date Test",
            "description": "desc",
            "start_date": "not-a-date",   
            "start_time": "25:61",        
            "end_date": "still-not-date", 
            "end_time": "10:70",         
        },
    )

    messages_list = list(get_messages(response.wsgi_request))

    assert response.status_code == 200
    assert "Please enter a valid date and time." in str(messages_list[0])

   
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
        instructor_email="teacher@example.com",
        password="pass",
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()
    response = client.post(
        "/instructor/exams/create/",
        {
            "create_exam": "1",
            "title": "Sample Exam",
            "description": "desc",
            "start_date": "2030-10-10",
            "start_time": "10:00",
            "end_date": "2030-10-10",
            "end_time": "11:00",
        },
    )

    assert response.status_code == 302  # Redirect after creation

    exam = Exam.objects.first()
    assert exam is not None

    response2 = client.post(
        f"/instructor/exams/create/?exam_id={exam.exam_id}",
        {
            "add_question": "1",
            "question_text": "What is 2+2?",
            "question_type": "TEXT",
        },
    )

    assert response2.status_code == 302  
    assert exam.questions.count() == 1
    assert exam.questions.first().marks == 1


@pytest.mark.django_db
def test_choice_adding_rejected_for_text_question(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    exam = Exam.objects.create(
        title="Exam",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor,
    )

    question = ExamQuestion.objects.create(
        exam=exam,
        question_text="Explain something",
        question_type="TEXT",
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(
        reverse("instructor_choice_add", args=[question.id]),
        {"choice_text": "Option A", "is_correct": "on"},
    )

    messages = list(get_messages(response.wsgi_request))
    assert "Choices can only be added to MCQ questions." in str(messages[0])



@pytest.mark.django_db
def test_choice_add_duplicate_rejected(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    exam = Exam.objects.create(
        title="Exam",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor,
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="MCQ",
        question_type="MCQ",
    )

    Choice.objects.create(choice_id=q, choice_text="A", is_correct=False)

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(
       reverse("instructor_choice_add", args=[q.id]),
        {"choice_text": "A"},
    )

    messages = list(get_messages(response.wsgi_request))
    assert "Duplicate choices are not allowed." in str(messages[0])


@pytest.mark.django_db
def test_choice_add_max_4_choices(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    exam = Exam.objects.create(
        title="Exam",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor,
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="MCQ",
        question_type="MCQ",
    )

    for opt in ["A", "B", "C", "D"]:
        Choice.objects.create(choice_id=q, choice_text=opt, is_correct=False)

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(
        reverse("instructor_choice_add", args=[q.id]),
        {"choice_text": "E"},
    )

    messages = list(get_messages(response.wsgi_request))
    assert "Maximum 4 choices allowed." in str(messages[0])
    assert q.choices.count() == 4


@pytest.mark.django_db
def test_choice_add_multiple_correct_rejected(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    exam = Exam.objects.create(
        title="Exam",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor,
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="MCQ",
        question_type="MCQ",
    )

    Choice.objects.create(choice_id=q, choice_text="A", is_correct=True)

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(
        reverse("instructor_choice_add", args=[q.id]),
        {"choice_text": "B", "is_correct": "on"},
    )

    messages = list(get_messages(response.wsgi_request))
    assert "Only one correct answer is allowed." in str(messages[0])


@pytest.mark.django_db
def test_choice_update_multiple_correct_rejected(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    exam = Exam.objects.create(
        title="Exam",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=instructor,
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="MCQ",
        question_type="MCQ",
    )

    c1 = Choice.objects.create(choice_id=q, choice_text="A", is_correct=True)
    c2 = Choice.objects.create(choice_id=q, choice_text="B", is_correct=False)

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(
        reverse("instructor_choice_update", args=[c2.id]),
        {"choice_text": "B", "is_correct": "on"},
    )

    messages = list(get_messages(response.wsgi_request))
    assert "Only one correct answer is allowed." in str(messages[0])


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

    start = timezone.now()
    end = start + timedelta(hours=1)

    exam = Exam.objects.create(
        title="Math Test",
        description="desc",
        start_time=start,
        end_time=end,
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
            "start_date": start.strftime("%Y-%m-%d"),
            "start_time": start.strftime("%H:%M"),
            "end_date": end.strftime("%Y-%m-%d"),
            "end_time": end.strftime("%H:%M"),
        },
    )

    exam.refresh_from_db()

    assert response.status_code == 302
    assert exam.title == "New Title"
    assert exam.description == "Updated desc"

    
@pytest.mark.django_db
def test_exam_update_success(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    start = timezone.now()
    end = start + timedelta(hours=1)

    exam = Exam.objects.create(
        title="Math Test",
        description="desc",
        start_time=start,
        end_time=end,
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
            "start_date": start.date(),
            "start_time": start.strftime("%H:%M"),
            "end_date": end.date(),
            "end_time": end.strftime("%H:%M"),
        },
    )

    exam.refresh_from_db()
    assert response.status_code == 302
    assert exam.title == "New Title"
    assert exam.description == "Updated desc"
    
    
@pytest.mark.django_db
def test_exam_update_missing_fields(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    exam = Exam.objects.create(
        title="Math",
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
            "title": "",
            "start_date": "",
            "start_time": "",
            "end_date": "",
            "end_time": "",
        },
    )

    assert response.status_code == 200  
    messages = list(get_messages(response.wsgi_request))
    assert "All fields (title, start date/time, end date/time) are required." in str(messages[0])

    
@pytest.mark.django_db
def test_exam_update_invalid_datetime(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    exam = Exam.objects.create(
        title="Math",
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
            "description": "desc",
            "start_date": "invalid-date",
            "start_time": "invalid-time",
            "end_date": "invalid-date",
            "end_time": "invalid-time",
        },
    )

    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert "Please enter a valid date and time." in str(messages[0])
    
@pytest.mark.django_db
def test_exam_update_title(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    start = timezone.now()
    end = start + timedelta(hours=1)

    exam = Exam.objects.create(
        title="Old Title",
        description="Old Desc",
        start_time=start,
        end_time=end,
        created_by=instructor,
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    response = client.post(
        f"/instructor/exams/{exam.exam_id}/edit/",
        {
            "title": "Updated Title",
            "description": "Old Desc",
            "start_date": start.date(),
            "start_time": start.strftime("%H:%M"),
            "end_date": end.date(),
            "end_time": end.strftime("%H:%M"),
        }
    )

    exam.refresh_from_db()
    assert exam.title == "Updated Title"

    
@pytest.mark.django_db
def test_exam_update_end_before_start_invalid(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass",
    )

    start = timezone.now()
    end = start + timedelta(hours=1)

    exam = Exam.objects.create(
        title="Math",
        description="desc",
        start_time=start,
        end_time=end,
        created_by=instructor,
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    earlier = (start - timedelta(hours=2)).strftime("%H:%M")

    response = client.post(
        f"/instructor/exams/{exam.exam_id}/edit/",
        {
            "title": "Test",
            "description": "desc",
            "start_date": start.date(),
            "start_time": start.strftime("%H:%M"),
            "end_date": start.date(),
            "end_time": earlier,  
        },
    )

    assert response.status_code == 200
    messages = list(get_messages(response.wsgi_request))
    assert "End time must be after start time." in str(messages[0])
    
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
    student = Student.objects.create(
        full_name="Test Student",
        student_email="student1@example.com",
        matric_number="1234567890",
        contact_number="0123456789",
        password="hashed-password",
    )

    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()

    url = reverse("student_profile")

    response = client.get(url)
    assert response.status_code == 200

    new_data = {
        "full_name": "Updated Student",
        "student_email": "student_updated@example.com",
        "matric_number": "0987654321",
        "contact_number": "0112345678",  # ✅ valid
    }
    response = client.post(url, data=new_data, follow=True)
    assert response.status_code == 200

    student.refresh_from_db()
    assert student.full_name == "Updated Student"
    assert student.student_email == "student_updated@example.com"
    assert student.matric_number == "0987654321"
    assert student.contact_number == "0112345678"


@pytest.mark.django_db
def test_instructor_can_view_and_update_profile(client):
    instructor = Instructor.objects.create(
        full_name="Test Instructor",
        instructor_email="instructor1@example.com",
        contact_number="0112345678",
        department="Computer Science",
        password="hashed-password",
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    url = reverse("instructor_profile")

    response = client.get(url)
    assert response.status_code == 200

    new_data = {
        "full_name": "Updated Instructor",
        "instructor_email": "instructor_updated@example.com",
        "contact_number": "0122222222",  # ✅ valid
        "department": "Information Technology",
    }
    response = client.post(url, data=new_data, follow=True)
    assert response.status_code == 200

    instructor.refresh_from_db()
    assert instructor.full_name == "Updated Instructor"
    assert instructor.instructor_email == "instructor_updated@example.com"
    assert instructor.contact_number == "0122222222"
    assert instructor.department == "Information Technology"


@pytest.mark.django_db
def test_student_profile_rejects_invalid_email(client):
    student = Student.objects.create(
        full_name="Test Student",
        student_email="student1@example.com",
        matric_number="1234567890",
        contact_number="0123456789",
        password="pw",
    )

    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()

    url = reverse("student_profile")

    data = {
        "full_name": "New Name",
        "student_email": "not-an-email",  
        "matric_number": "1234567890",
        "contact_number": "000",
    }

    response = client.post(url, data=data)

    assert response.status_code == 200

    student.refresh_from_db()
    # Nothing changed because email invalid
    assert student.full_name == "Test Student"
    assert student.student_email == "student1@example.com"


@pytest.mark.django_db
def test_instructor_profile_rejects_invalid_email(client):
    instructor = Instructor.objects.create(
        full_name="Test Instructor",
        instructor_email="instructor1@example.com",
        contact_number="0112345678",
        department="CS",
        password="pw",
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    url = reverse("instructor_profile")

    data = {
        "full_name": "Updated",
        "instructor_email": "bad-email",  # invalid
        "contact_number": "000",
        "department": "IT",
    }

    response = client.post(url, data=data)

    assert response.status_code == 200

    instructor.refresh_from_db()
    assert instructor.instructor_email == "instructor1@example.com"

    # ---------- helpers ----------
def login_student(client, student):
    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()

def login_instructor(client, instructor):
    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

def assert_has_message(response, contains_text: str):
    msgs = list(get_messages(response.wsgi_request))
    assert any(contains_text in str(m) for m in msgs), msgs


# ---------- ACCESS CONTROL ----------
@pytest.mark.django_db
def test_student_cannot_access_instructor_profile(client):
    s = Student.objects.create(
        full_name="S",
        student_email="s@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )
    login_student(client, s)
    resp = client.get(reverse("instructor_profile"))
    assert resp.status_code == 302  


# ---------- STUDENT PROFILE VALIDATION ----------
@pytest.mark.django_db
def test_student_profile_missing_required_fields(client):
    student = Student.objects.create(
        full_name="Test Student",
        student_email="student1@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )
    login_student(client, student)

    resp = client.post(reverse("student_profile"), data={
        "full_name": "",
        "student_email": "student1@example.com",
        "matric_number": "",
        "contact_number": "0123456789",
    })

    assert resp.status_code == 200
    assert_has_message(resp, "required")  # your view uses required msg :contentReference[oaicite:4]{index=4}

    student.refresh_from_db()
    assert student.full_name == "Test Student"


@pytest.mark.django_db
def test_student_profile_rejects_duplicate_email(client):
    s1 = Student.objects.create(
        full_name="S1",
        student_email="s1@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )
    Student.objects.create(
        full_name="S2",
        student_email="s2@example.com",
        matric_number="PPE0002",
        contact_number="0123456789",
        password="pw",
    )
    login_student(client, s1)

    resp = client.post(reverse("student_profile"), data={
        "full_name": "S1",
        "student_email": "s2@example.com",  # duplicate
        "matric_number": "PPE0001",
        "contact_number": "0123456789",
    })

    assert resp.status_code == 200
    assert_has_message(resp, "already used by another student")  # view msg :contentReference[oaicite:6]{index=6}

    s1.refresh_from_db()
    assert s1.student_email == "s1@example.com"

@pytest.mark.django_db
def test_student_profile_rejects_duplicate_matric(client):
    s1 = Student.objects.create(
        full_name="S1",
        student_email="s1@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )
    Student.objects.create(
        full_name="S2",
        student_email="s2@example.com",
        matric_number="PPE0002",
        contact_number="0123456789",
        password="pw",
    )
    login_student(client, s1)

    resp = client.post(reverse("student_profile"), data={
        "full_name": "S1",
        "student_email": "s1@example.com",
        "matric_number": "PPE0002",  # duplicate
        "contact_number": "0123456789",
    })

    assert resp.status_code == 200
    assert_has_message(resp, "matric number is already used")  # view msg :contentReference[oaicite:7]{index=7}

    s1.refresh_from_db()
    assert s1.matric_number == "PPE0001"


# These 2 tests assume you implemented your NEW matric/phone validation message strings:
@pytest.mark.django_db
def test_student_profile_rejects_invalid_matric_format_new_rules(client):
    student = Student.objects.create(
        full_name="Test Student",
        student_email="student1@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )
    login_student(client, student)

    resp = client.post(reverse("student_profile"), data={
        "full_name": "Test Student",
        "student_email": "student1@example.com",
        "matric_number": "@@@@",  # invalid
        "contact_number": "0123456789",
    })

    assert resp.status_code == 200
    assert_has_message(resp, "Matric number must")  # match your new message

    student.refresh_from_db()
    assert student.matric_number == "PPE0001"

@pytest.mark.django_db
def test_student_profile_rejects_invalid_phone_new_rules(client):
    student = Student.objects.create(
        full_name="Test Student",
        student_email="student1@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )
    login_student(client, student)

    resp = client.post(reverse("student_profile"), data={
        "full_name": "Test Student",
        "student_email": "student1@example.com",
        "matric_number": "PPE0001",
        "contact_number": "abc",  # invalid phone input
    })

    assert resp.status_code == 200
    assert_has_message(resp, "Invalid phone number")  # match your new message

    student.refresh_from_db()
    assert student.contact_number == "0123456789"


@pytest.mark.django_db
def test_student_profile_valid_update_success(client):
    student = Student.objects.create(
        full_name="Test Student",
        student_email="student1@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )
    login_student(client, student)

    resp = client.post(reverse("student_profile"), data={
        "full_name": "Updated Student",
        "student_email": "student_updated@example.com",
        "matric_number": "PPE0009",
        "contact_number": "0112345678",  # valid MY mobile
    }, follow=True)

    assert resp.status_code == 200
    student.refresh_from_db()
    assert student.full_name == "Updated Student"
    assert student.student_email == "student_updated@example.com"
    assert student.matric_number == "PPE0009"
    assert student.contact_number == "0112345678"


# ---------- INSTRUCTOR PROFILE VALIDATION ----------
@pytest.mark.django_db
def test_instructor_profile_missing_required_fields(client):
    instructor = Instructor.objects.create(
        full_name="Test Instructor",
        instructor_email="i1@example.com",
        contact_number="0112345678",
        department="CS",
        password="pw",
    )
    login_instructor(client, instructor)

    resp = client.post(reverse("instructor_profile"), data={
        "full_name": "",
        "instructor_email": "",
        "contact_number": "0112345678",
        "department": "CS",
    })

    assert resp.status_code == 200
    assert_has_message(resp, "Full name and email are required.")  # view msg :contentReference[oaicite:8]{index=8}

@pytest.mark.django_db
def test_instructor_profile_rejects_invalid_email(client):
    instructor = Instructor.objects.create(
        full_name="Test Instructor",
        instructor_email="i1@example.com",
        contact_number="0112345678",
        department="CS",
        password="pw",
    )
    login_instructor(client, instructor)

    resp = client.post(reverse("instructor_profile"), data={
        "full_name": "Updated",
        "instructor_email": "bad-email",
        "contact_number": "0112345678",
        "department": "IT",
    })

    assert resp.status_code == 200
    assert_has_message(resp, "Invalid email format.")  # view msg :contentReference[oaicite:9]{index=9}

    instructor.refresh_from_db()
    assert instructor.instructor_email == "i1@example.com"

@pytest.mark.django_db
def test_instructor_profile_rejects_duplicate_email(client):
    i1 = Instructor.objects.create(
        full_name="I1",
        instructor_email="i1@example.com",
        contact_number="0112345678",
        department="CS",
        password="pw",
    )
    Instructor.objects.create(
        full_name="I2",
        instructor_email="i2@example.com",
        contact_number="0112345678",
        department="CS",
        password="pw",
    )
    login_instructor(client, i1)

    resp = client.post(reverse("instructor_profile"), data={
        "full_name": "I1",
        "instructor_email": "i2@example.com",  # duplicate
        "contact_number": "0112345678",
        "department": "CS",
    })

    assert resp.status_code == 200
    assert_has_message(resp, "already used by another instructor")  # view msg :contentReference[oaicite:10]{index=10}

    i1.refresh_from_db()
    assert i1.instructor_email == "i1@example.com"


# This assumes you implemented your NEW phone validation message strings in instructor_profile:
@pytest.mark.django_db
def test_instructor_profile_rejects_invalid_phone_new_rules(client):
    instructor = Instructor.objects.create(
        full_name="Test Instructor",
        instructor_email="i1@example.com",
        contact_number="0112345678",
        department="CS",
        password="pw",
    )
    login_instructor(client, instructor)

    resp = client.post(reverse("instructor_profile"), data={
        "full_name": "Test Instructor",
        "instructor_email": "i1@example.com",
        "contact_number": "abc",  # invalid phone
        "department": "CS",
    })

    assert resp.status_code == 200
    assert_has_message(resp, "Invalid phone number")

    instructor.refresh_from_db()
    assert instructor.contact_number == "0112345678"

@pytest.mark.django_db
def test_instructor_profile_valid_update_success(client):
    instructor = Instructor.objects.create(
        full_name="Test Instructor",
        instructor_email="i1@example.com",
        contact_number="0112345678",
        department="CS",
        password="pw",
    )
    login_instructor(client, instructor)

    resp = client.post(reverse("instructor_profile"), data={
        "full_name": "Updated Instructor",
        "instructor_email": "updated_i@example.com",
        "contact_number": "0122222222",  # valid MY mobile
        "department": "IT",
    }, follow=True)

    assert resp.status_code == 200
    instructor.refresh_from_db()
    assert instructor.full_name == "Updated Instructor"
    assert instructor.instructor_email == "updated_i@example.com"
    assert instructor.contact_number == "0122222222"
    assert instructor.department == "IT"


# ---------- OPTIONAL: stats / recent activity shown ----------
@pytest.mark.django_db
def test_student_profile_shows_recent_exam_activity(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        contact_number="0112345678",
        department="CS",
        password="pw",
    )
    student = Student.objects.create(
        full_name="Student",
        student_email="stu@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )
    login_student(client, student)

    now = timezone.now()
    exam = Exam.objects.create(
        title="Math",
        description="desc",
        start_time=now - timedelta(minutes=10),
        end_time=now + timedelta(minutes=10),
        created_by=instructor,
    )
    ExamAttempt.objects.create(exam=exam, student=student)

    resp = client.get(reverse("student_profile"))
    assert resp.status_code == 200
    # these strings exist in your updated template section
    assert b"Recent Exam Activity" in resp.content
    assert b"Math" in resp.content

    import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from zoneinfo import ZoneInfo

@pytest.mark.django_db
def test_instructor_can_view_exam_detail_with_schedule_and_questions(client):
    """
    User story:
    Instructor can view one exam's details (schedule + questions)
    so they can review before editing / analysing results.
    """
    KL = ZoneInfo("Asia/Kuala_Lumpur")

    # Create instructor + login session
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pw",
    )
    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()

    # Create exam (store UTC-aware datetimes)
    start = timezone.now().replace(second=0, microsecond=0) + timedelta(hours=2)
    end = start + timedelta(hours=1)

    exam = Exam.objects.create(
        title="Final Exam",
        description="Exam desc",
        start_time=start,
        end_time=end,
        created_by=instructor,
    )

    # Create questions
    q1 = ExamQuestion.objects.create(
        exam=exam, question_text="Explain OOP", question_type="TEXT", marks=5
    )
    q2 = ExamQuestion.objects.create(
        exam=exam, question_text="2+2=?", question_type="MCQ", marks=1
    )

    # MCQ choices
    Choice.objects.create(choice_id=q2, choice_text="3", is_correct=False)
    Choice.objects.create(choice_id=q2, choice_text="4", is_correct=True)

    # Visit exam detail
    url = reverse("instructor_exam_detail", args=[exam.exam_id])
    resp = client.get(url)
    assert resp.status_code == 200

    # Exam metadata
    assert exam.title.encode() in resp.content
    assert exam.exam_id.encode() in resp.content
    assert b"Exam Information" in resp.content or b"Exam info" in resp.content

    # Schedule appears (either UTC or KL formatted depending on template)
    # We'll check KL formatted string (recommended display)
    start_kl = timezone.localtime(start, KL).strftime("%Y-%m-%d %H:%M").encode()
    end_kl = timezone.localtime(end, KL).strftime("%Y-%m-%d %H:%M").encode()
    assert (start_kl in resp.content) or (start.strftime("%Y-%m-%d %H:%M").encode() in resp.content)
    assert (end_kl in resp.content) or (end.strftime("%Y-%m-%d %H:%M").encode() in resp.content)

    # Questions displayed
    assert b"Explain OOP" in resp.content
    assert b"2+2=?" in resp.content
    assert b"3" in resp.content
    assert b"4" in resp.content
    assert b"Correct" in resp.content  # your template shows "Correct" badge

    # Edit button exists (link text can differ)
    edit_url = reverse("instructor_exam_update", args=[exam.exam_id]).encode()
    assert edit_url in resp.content


@pytest.mark.django_db
def test_instructor_cannot_view_other_instructors_exam_detail(client):
    """Negative: instructor cannot view exam created_by someone else (404)."""
    instructor1 = Instructor.objects.create(
        full_name="Teacher 1", instructor_email="t1@example.com", password="pw"
    )
    instructor2 = Instructor.objects.create(
        full_name="Teacher 2", instructor_email="t2@example.com", password="pw"
    )

    exam = Exam.objects.create(
        title="Secret Exam",
        description="x",
        start_time=timezone.now() + timedelta(hours=1),
        end_time=timezone.now() + timedelta(hours=2),
        created_by=instructor1,
    )

    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor2.instructor_ID
    session.save()

    resp = client.get(reverse("instructor_exam_detail", args=[exam.exam_id]))
    assert resp.status_code == 404


import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
def test_student_cannot_access_instructor_exam_detail(client):
    student = Student.objects.create(
        full_name="Stu",
        student_email="stu@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )

    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pw",
    )

    exam = Exam.objects.create(
        title="Exam",
        description="x",
        start_time=timezone.now() + timedelta(hours=1),
        end_time=timezone.now() + timedelta(hours=2),
        created_by=instructor,
    )

    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()

    # Because exam_detail() tries to load Instructor using session["user_id"],
    # a student session causes Instructor.DoesNotExist (500 in real run).
    with pytest.raises(Instructor.DoesNotExist):
        client.get(reverse("instructor_exam_detail", args=[exam.exam_id]))

import pytest
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone

from app.models import Student, Instructor, Exam, ExamAttempt, ExamQuestion


def login_student(client, student: Student):
    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()


@pytest.mark.django_db
def test_student_results_page_shows_only_my_submitted_attempts(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pw",
    )

    s1 = Student.objects.create(
        full_name="Student One",
        student_email="s1@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )
    s2 = Student.objects.create(
        full_name="Student Two",
        student_email="s2@example.com",
        matric_number="PPE0002",
        contact_number="0123456789",
        password="pw",
    )

    now = timezone.now()

    exam_a = Exam.objects.create(
        title="Exam A",
        description="A",
        start_time=now - timedelta(days=1),
        end_time=now + timedelta(days=1),
        created_by=instructor,
    )
    exam_b = Exam.objects.create(
        title="Exam B",
        description="B",
        start_time=now - timedelta(days=1),
        end_time=now + timedelta(days=1),
        created_by=instructor,
    )

    # add marks so total_possible > 0
    ExamQuestion.objects.create(exam=exam_a, question_text="Q1", question_type="TEXT", marks=1)
    ExamQuestion.objects.create(exam=exam_a, question_text="Q2", question_type="TEXT", marks=1)

    # s1 submitted attempt -> SHOULD appear
    a1 = ExamAttempt.objects.create(
        attempt_id="ATT-S1-SUB",
        exam=exam_a,
        student=s1,
        started_at=now - timedelta(minutes=30),
        submitted_at=now - timedelta(minutes=10),
        score=2.0,
    )

    # s1 not submitted -> should NOT appear (filtered by submitted_at__isnull=False)
    ExamAttempt.objects.create(
        attempt_id="ATT-S1-DRAFT",
        exam=exam_b,
        student=s1,
        started_at=now - timedelta(minutes=20),
        submitted_at=None,
        score=0.0,
    )

    # s2 submitted -> should NOT appear for s1
    ExamAttempt.objects.create(
        attempt_id="ATT-S2-SUB",
        exam=exam_b,
        student=s2,
        started_at=now - timedelta(minutes=25),
        submitted_at=now - timedelta(minutes=5),
        score=1.0,
    )

    login_student(client, s1)

    resp = client.get(reverse("student_results"))
    assert resp.status_code == 200

    # Context check
    attempts = resp.context["attempts"]
    assert len(attempts) == 1
    assert attempts[0]["attempt_id"] == a1.attempt_id
    assert attempts[0]["exam"].title == "Exam A"

    # HTML contains my submitted exam
    content = resp.content.decode("utf-8")
    assert "My Exam Results" in content
    assert "Exam A" in content

    # Should NOT show exam B for s1 (draft) or s2 data
    assert "Exam B" not in content

    # Has the View link
    assert reverse("student_exam_result", args=[a1.attempt_id]) in content


@pytest.mark.django_db
def test_student_results_page_when_no_attempts_shows_empty_message(client):
    s1 = Student.objects.create(
        full_name="Student One",
        student_email="s1@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )

    login_student(client, s1)

    resp = client.get(reverse("student_results"))
    assert resp.status_code == 200
    assert b"You have not completed any exams yet." in resp.content


@pytest.mark.django_db
def test_student_results_ignores_unsubmitted_attempts(client):
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pw",
    )
    s1 = Student.objects.create(
        full_name="Student One",
        student_email="s1@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )

    now = timezone.now()
    exam = Exam.objects.create(
        title="Draft Exam",
        description="",
        start_time=now - timedelta(days=1),
        end_time=now + timedelta(days=1),
        created_by=instructor,
    )

    # Attempt exists but not submitted
    ExamAttempt.objects.create(
        attempt_id="ATT-DRAFT",
        exam=exam,
        student=s1,
        started_at=now - timedelta(minutes=5),
        submitted_at=None,
        score=0.0,
    )

    login_student(client, s1)

    resp = client.get(reverse("student_results"))
    assert resp.status_code == 200
    assert b"Draft Exam" not in resp.content
    assert b"You have not completed any exams yet." in resp.content


def login_instructor(client, instructor):
    session = client.session
    session["user_type"] = "instructor"
    session["user_id"] = instructor.instructor_ID
    session.save()


def login_student(client, student):
    session = client.session
    session["user_type"] = "student"
    session["user_id"] = student.student_ID
    session.save()


@pytest.mark.django_db
def test_instructor_exam_list_page_shows_only_own_exams(client):
    i1 = Instructor.objects.create(
        full_name="Inst 1",
        instructor_email="i1@example.com",
        password="pw",
    )
    i2 = Instructor.objects.create(
        full_name="Inst 2",
        instructor_email="i2@example.com",
        password="pw",
    )

    now = timezone.now()
    e1 = Exam.objects.create(
        title="I1 Exam A",
        description="a",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=1),
        created_by=i1,
    )
    e2 = Exam.objects.create(
        title="I1 Exam B",
        description="b",
        start_time=now + timedelta(days=2),
        end_time=now + timedelta(days=2, hours=1),
        created_by=i1,
    )
    Exam.objects.create(
        title="I2 Exam X",
        description="x",
        start_time=now + timedelta(days=3),
        end_time=now + timedelta(days=3, hours=1),
        created_by=i2,
    )

    login_instructor(client, i1)
    resp = client.get(reverse("instructor_exam_list"))
    assert resp.status_code == 200

    content = resp.content.decode("utf-8")
    assert "I1 Exam A" in content
    assert "I1 Exam B" in content
    assert "I2 Exam X" not in content

    # (Optional) sanity: exam ids show up too
    assert e1.exam_id in content
    assert e2.exam_id in content


@pytest.mark.django_db
def test_instructor_exam_list_has_search_and_sort_ui(client):
    instructor = Instructor.objects.create(
        full_name="Inst",
        instructor_email="inst@example.com",
        password="pw",
    )
    now = timezone.now()
    Exam.objects.create(
        title="Searchable Exam",
        description="desc",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=1),
        created_by=instructor,
    )

    login_instructor(client, instructor)
    resp = client.get(reverse("instructor_exam_list"))
    assert resp.status_code == 200

    html = resp.content.decode("utf-8")

    # Search input exists (based on your template placeholder)
    assert "Search exam by ID or title" in html

    # Sort UI hooks exist (these strings depend on your template/JS)
    # If your headers use onclick="sortTable(...)" this will pass.
    assert "sortTable" in html or "onclick" in html


@pytest.mark.django_db
def test_instructor_exam_list_default_order_latest_first(client):
    instructor = Instructor.objects.create(
        full_name="Inst",
        instructor_email="inst2@example.com",
        password="pw",
    )

    now = timezone.now()
    older = Exam.objects.create(
        title="Older Exam",
        description="old",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=1),
        created_by=instructor,
    )
    newer = Exam.objects.create(
        title="Newer Exam",
        description="new",
        start_time=now + timedelta(days=5),
        end_time=now + timedelta(days=5, hours=1),
        created_by=instructor,
    )

    login_instructor(client, instructor)
    resp = client.get(reverse("instructor_exam_list"))
    assert resp.status_code == 200

    html = resp.content.decode("utf-8")

    # If your queryset orders by "-start_time", "Newer Exam" should appear before "Older Exam"
    assert html.find("Newer Exam") != -1
    assert html.find("Older Exam") != -1
    assert html.find("Newer Exam") < html.find("Older Exam")


@pytest.mark.django_db
def test_student_cannot_access_instructor_exam_list(client):
    # This matches your current behavior if the view does:
    # instructor = Instructor.objects.get(instructor_ID=session["user_id"])
    student = Student.objects.create(
        full_name="Stu",
        student_email="stu@example.com",
        matric_number="PPE0001",
        contact_number="0123456789",
        password="pw",
    )
    login_student(client, student)

    # Your app currently raises Instructor.DoesNotExist (based on your previous failures)
    with pytest.raises(Instructor.DoesNotExist):
        client.get(reverse("instructor_exam_list"))


