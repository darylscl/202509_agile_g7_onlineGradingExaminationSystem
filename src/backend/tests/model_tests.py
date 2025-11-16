import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from app.models import *

# Models test is a type of unit test
# Models test include:
# test fields behaviour
# test methods / properties
# test on custom function 
# test on foreign key and models relationship
# test on constraint 



#----------------------------------------------
#-------------Start of exam module test---------
#----------------------------------------------

# -----Exam models / id generation-------
@pytest.mark.django_db
def test_exam_custom_id_generated():
    user = User.objects.create(username="teacher")

    exam = Exam.objects.create(
        title="Sample Exam",
        description="Test",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user,
    )

    assert exam.exam_id.startswith("EX-")
    assert len(exam.exam_id) == 6
    
@pytest.mark.django_db
def test_exam_id_increments():
    user = User.objects.create(username="teacher")

    exam1 = Exam.objects.create(
        title="Exam 1",
        description="Desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )

    exam2 = Exam.objects.create(
        title="Exam 2",
        description="Desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )

    assert exam1.exam_id == "EX-001"
    assert exam2.exam_id == "EX-002"
    
@pytest.mark.django_db
def test_attempt_custom_id_generated():
    user = User.objects.create(username="student")
    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )

    attempt = ExamAttempt.objects.create(exam=exam, student=user)

    assert attempt.attempt_id.startswith("ATT-")
    assert len(attempt.attempt_id) == 10
    
@pytest.mark.django_db
def test_exam_str():
    user = User.objects.create(username="teacher")
    exam = Exam.objects.create(
        title="My Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )
    assert str(exam) == f"{exam.exam_id} - {exam.title}"
    
    
# ----ExamQuestion Choice models----

@pytest.mark.django_db
def test_question_str():
    user = User.objects.create(username="teacher")
    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="Hello world",
        question_type="MCQ",
        order_no=3
    )

    assert str(q) == "Q3: Hello world"
    
@pytest.mark.django_db
def test_choice_creation():
    user = User.objects.create(username="teacher")
    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="Hello",
        question_type="MCQ"
    )

    c = Choice.objects.create(
        choice_id=q,
        choice_text="4",
        is_correct=True
    )

    assert q.choices.count() == 1
    assert c.is_correct is True
    
# -----Answer models -----
@pytest.mark.django_db
def test_answer_unique_constraint():
    user = User.objects.create(username="student")
    exam = Exam.objects.create(...)
    q = ExamQuestion.objects.create(...)
    attempt = ExamAttempt.objects.create(exam=exam, student=user)

    Answer.objects.create(attempt=attempt, question=q, text_answer="Ans1")

    with pytest.raises(Exception):
        Answer.objects.create(attempt=attempt, question=q, text_answer="Ans2")

#----- Date logic tests----

@pytest.mark.django_db
def test_exam_is_open_true():
    user = User.objects.create(username="teacher")
    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now() - timedelta(minutes=5),
        end_time=timezone.now() + timedelta(minutes=5),
        created_by=user
    )
    assert exam.is_open is True


@pytest.mark.django_db
def test_exam_is_open_false_before_start():
    user = User.objects.create(username="teacher")
    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now() + timedelta(minutes=5),
        end_time=timezone.now() + timedelta(minutes=10),
        created_by=user
    )
    assert exam.is_open is False


@pytest.mark.django_db
def test_exam_is_open_false_after_end():
    user = User.objects.create(username="teacher")
    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now() - timedelta(minutes=10),
        end_time=timezone.now() - timedelta(minutes=5),
        created_by=user
    )
    assert exam.is_open is False
    
    
# ---Str methods tests----

@pytest.mark.django_db
def test_answer_str():
    user = User.objects.create(username="student")
    exam = Exam.objects.create(...)
    question = ExamQuestion.objects.create(...)
    attempt = ExamAttempt.objects.create(exam=exam, student=user)

    answer = Answer.objects.create(attempt=attempt, question=question)
    s = str(answer)

    assert "Answer for" in s
    assert "Attempt" in s
    
    
@pytest.mark.django_db
def test_answer_str():
    user = User.objects.create(username="student")
    exam = Exam.objects.create(...)
    question = ExamQuestion.objects.create(...)
    attempt = ExamAttempt.objects.create(exam=exam, student=user)

    answer = Answer.objects.create(attempt=attempt, question=question)
    s = str(answer)

    assert "Answer for" in s
    assert "Attempt" in s
    
    
@pytest.mark.django_db
def test_choice_str():
    user = User.objects.create(username="teacher")
    exam = Exam.objects.create(...)
    q = ExamQuestion.objects.create(...)
    c = Choice.objects.create(choice_id=q, choice_text="Hello", is_correct=False)

    assert "Choice for" in str(c)
    
@pytest.mark.django_db
def test_question_order_default():
    user = User.objects.create(username="teacher")
    exam = Exam.objects.create(...)
    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="Hello",
        question_type="TEXT"
    )
    assert q.order_no == 1
    
    
# --- Required fields test ---
@pytest.mark.django_db
def test_exam_requires_title():
    user = User.objects.create(username="teacher")

    with pytest.raises(Exception):
        Exam.objects.create(
            title=None,
            description="desc",
            start_time=timezone.now(),
            end_time=timezone.now(),
            created_by=user
        )

#----------------------------------------------
#-------------End  of exam module test---------
#----------------------------------------------

