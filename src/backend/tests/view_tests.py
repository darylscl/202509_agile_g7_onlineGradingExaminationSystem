
from datetime import timedelta
from django.utils import timezone
from app.views import *
from django.contrib.auth.models import User
import pytest

# TDD test need to let user to know where is the failed test and what is the failed test. A summary like that


# Exam module test
@pytest.mark.django_db
def test_exam_can_be_created_with_user():
    user = User.objects.create(username="teacher", is_staff=True)

    exam = Exam.objects.create(
        title="Sample Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )

    assert exam.exam_id.startswith("EX-")
    assert exam.title == "Sample Exam"
   
# ID auto increment 
@pytest.mark.django_db
def test_exam_id_increments():
    user = User.objects.create(username="teacher", is_staff=True)
    
    e1 = Exam.objects.create(
        title="Exam1",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )
    e2 = Exam.objects.create(
        title="Exam2",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )

    assert e1.exam_id == "EX-001"
    assert e2.exam_id == "EX-002"
    
#Question creation  
@pytest.mark.django_db
def test_text_question_creation():
    user = User.objects.create(username="teacher", is_staff=True)

    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
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
    user = User.objects.create(username="teacher", is_staff=True)
    exam = Exam.objects.create(
        title="Exam",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
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
    user = User.objects.create(username="teacher", is_staff=True)
    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )
    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="Test",
        question_type="TEXT"
    )
    attempt = ExamAttempt.objects.create(exam=exam, student=user)  

    Answer.objects.create(attempt=attempt, question=q, text_answer="A")

    with pytest.raises(Exception):
        Answer.objects.create(attempt=attempt, question=q, text_answer="B")
        
        
# Exam is open logic
@pytest.mark.django_db
def test_exam_is_open_true():
    user = User.objects.create(username="teacher", is_staff=True)

    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now() - timedelta(minutes=1),
        end_time=timezone.now() + timedelta(minutes=1),
        created_by=user
    )

    assert exam.is_open is True
    
# Builder test
@pytest.mark.django_db
def test_exam_create_and_add_question(client):
    user = User.objects.create(username="teacher", is_staff=True)
    client.force_login(user)

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
    user = User.objects.create(username="teacher", is_staff=True)
    
    exam1 = Exam.objects.create(
        title="Math Test",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )
    ExamQuestion.objects.create(exam=exam1, question_text="Q1", question_type="TEXT")
    ExamQuestion.objects.create(exam=exam1, question_text="Q2", question_type="MCQ")

    exam2 = Exam.objects.create(
        title="Science Test",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )
    ExamQuestion.objects.create(exam=exam2, question_text="Q1", question_type="TEXT")

    client.force_login(user)
    response = client.get("/instructor/exams/")

    assert response.status_code == 200
    assert b"Math Test" in response.content
    assert b"Science Test" in response.content
    assert exam1.exam_id.encode() in response.content
    assert exam2.exam_id.encode() in response.content
    assert str(exam1.start_time.date()).encode() in response.content
    assert str(exam1.end_time.date()).encode() in response.content
    assert b"2 Questions" in response.content   
    assert b"1 Question" in response.content    

    
# test edit exam
@pytest.mark.django_db
def test_exam_update_view(client):
    user = User.objects.create(username="teacher", is_staff=True)
    
    # create sample
    exam = Exam.objects.create(
        title="Math Test",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )
    
    # call the sample and perform updates
    client.force_login(user)
    response = client.post(f"/instructor/exams/{exam.exam_id}/edit/", {
        "title": "New Title",
        "description": "Updated desc",
        "start_time": exam.start_time,
        "end_time": exam.end_time,
    })
    
    exam.refresh_from_db()
    assert exam.title == "New Title"
    assert response.status_code == 302
    
# test delete exam
@pytest.mark.django_db
def test_exam_delete_view(client):
    user = User.objects.create(username="teacher", is_staff=True)
    
    # create sample
    exam = Exam.objects.create(
        title="Math Test",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )
    
    client.force_login(user)
    response = client.post(f"/instructor/exams/{exam.exam_id}/delete/")
    assert response.status_code == 302
    assert Exam.objects.filter(exam_id=exam.exam_id).exists() is False

# test Student takes the online exam during the valid schedule
@pytest.mark.django_db
def test_student_takes_exam_during_valid_schedule(client):
    # teacher (exam owner)
    teacher = User.objects.create(username="teacher")

    # student
    student = User.objects.create_user(username="student", password="pass")

    # exam is open now
    now = timezone.now()
    exam = Exam.objects.create(
        title="Sample Exam",
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
    wrong = Choice.objects.create(choice_id=q1, choice_text="3", is_correct=False)
    correct = Choice.objects.create(choice_id=q1, choice_text="4", is_correct=True)

    # TEXT question
    q2 = ExamQuestion.objects.create(
        exam=exam,
        question_text="Explain your answer",
        question_type="TEXT",
        order_no=2,
    )

    # student logs in
    client.force_login(student)

    # GET – student can access the exam page while it's open
    response = client.get(f"/student/exams/{exam.exam_id}/take/")
    assert response.status_code == 200
    assert b"2 + 2" in response.content  # question shown

    # POST – student submits answers
    post_data = {
        f"q_{q1.id}": str(correct.id),                  # MCQ answer
        f"q_{q2.id}": "Because 2+2=4, obviously.",      # TEXT answer
    }
    response = client.post(f"/student/exams/{exam.exam_id}/take/", data=post_data)

    # should redirect to exam result page
    assert response.status_code == 302

    # attempt created and marked as submitted
    attempt = ExamAttempt.objects.get(exam=exam, student=student)
    assert attempt.submitted is True
    assert attempt.score == 1  # 1 MCQ question, answered correctly

    # MCQ answer saved and marked
    a1 = Answer.objects.get(attempt=attempt, question=q1)
    assert a1.selected_choice == correct
    assert a1.marks == 1

    # TEXT answer saved
    a2 = Answer.objects.get(attempt=attempt, question=q2)
    assert a2.text_answer == "Because 2+2=4, obviously."

@pytest.mark.django_db
def test_student_sees_only_currently_available_exams(client):
    # create a student user & log in
    student = User.objects.create_user(username="student1", password="pass")
    client.force_login(student)

    # teacher (creator) - adjust if your Exam model doesn't need this
    teacher = User.objects.create(username="teacher1")

    now = timezone.now()

    # exam that already ended
    past_exam = Exam.objects.create(
        title="Past Exam",
        description="Already finished",
        start_time=now - timedelta(days=2),
        end_time=now - timedelta(days=1),
        created_by=teacher,
    )

    # exam that hasn't started yet
    future_exam = Exam.objects.create(
        title="Future Exam",
        description="Not started yet",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=2),
        created_by=teacher,
    )

    # exam that is currently available (start <= now <= end)
    current_exam = Exam.objects.create(
        title="Current Exam",
        description="Happening now",
        start_time=now - timedelta(hours=1),
        end_time=now + timedelta(hours=1),
        created_by=teacher,
    )

    # call the view
    response = client.get("/student/exams/available/")

    assert response.status_code == 200

    content = response.content

    # current exam should be visible
    assert b"Current Exam" in content

    # past and future exams should NOT appear
    assert b"Past Exam" not in content
    assert b"Future Exam" not in content