import pytest
from django.utils import timezone
from django.db.utils import IntegrityError
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
#-------------Start of user authentication module test---------
#----------------------------------------------

@pytest.mark.django_db
def test_student_custom_id_generation():
    s1 = Student.objects.create(
        full_name="John Doe",
        student_email="john@example.com",
        matric_number="A001",
        password="hashed123"
    )

    s2 = Student.objects.create(
        full_name="Jane Smith",
        student_email="jane@example.com",
        matric_number="A002",
        password="hashed456"
    )

    assert s1.student_ID == "STU001"
    assert s2.student_ID == "STU002"
    
@pytest.mark.django_db
def test_student_duplicated_email_registered():
    Student.objects.create(
        full_name="User One",
        student_email="dup@example.com",
        matric_number="A001",
        password="pass"
    )
    with pytest.raises(IntegrityError):
        Student.objects.create(
            full_name="User Two",
            student_email="dup@example.com",  
            matric_number="A002",
            password="pass"
        )
        
@pytest.mark.django_db
def test_student_duplicated_matric_registered():
    Student.objects.create(
        full_name="User One",
        student_email="john@example.com",
        matric_number="A001",
        password="pass"
    )
    with pytest.raises(IntegrityError):
        Student.objects.create(
            full_name="User Two",
            student_email="jane@example.com",
            matric_number="A001", 
            password="pass"
        )
        
@pytest.mark.django_db
def test_student_contact_number_isnull_true():
    s = Student.objects.create(
        full_name="John Doe",
        student_email="john@example.com",
        matric_number="A001",
        password="pass"
    )
    assert s.contact_number is None
    
@pytest.mark.django_db
def test_student_created_at_timestamp():
    s = Student.objects.create(
        full_name="John Doe",
        student_email="john@example.com",
        matric_number="A001",
        password="pass"
    )
    assert s.created_at is not None
    assert timezone.now() >= s.created_at
    
@pytest.mark.django_db
def test_student_invalid_email_format():
    student = Student(
        full_name="Invalid User",
        student_email="not-an-email",
        matric_number="A003",
        password="pass"
    )

    with pytest.raises(Exception):
        student.full_clean()
        
@pytest.mark.django_db
def test_instructor_custom_id_generation():
    ins1 = Instructor.objects.create(
        full_name="Mr. Alan",
        instructor_email="alan@example.com",
        password="pass"
    )
    ins2 = Instructor.objects.create(
        full_name="Ms. Bella",
        instructor_email="bella@example.com",
        password="pass"
    )
    assert ins1.instructor_ID == "INS001"
    assert ins2.instructor_ID == "INS002"
    
@pytest.mark.django_db
def test_instructor_duplicated_email_registered():
    Instructor.objects.create(
        full_name="Teacher One",
        instructor_email="dup@example.com",
        password="pass"
    )
    with pytest.raises(IntegrityError):
        Instructor.objects.create(
            full_name="Teacher Two",
            instructor_email="dup@example.com", 
            password="pass"
        )
        
@pytest.mark.django_db
def test_instructor_contact_number_isnull_true():
    ins = Instructor.objects.create(
        full_name="Mr. Alan",
        instructor_email="alan@example.com",
        password="pass"
    )
    assert ins.contact_number is None

@pytest.mark.django_db
def test_instructor_department_isnull_true():
    ins = Instructor.objects.create(
        full_name="Mr. Alan",
        instructor_email="alan@example.com",
        password="pass"
    )
    assert ins.department is None
    
@pytest.mark.django_db
def test_instructor_invalid_email_format():
    instructor = Instructor(
        full_name="Invalid Teacher",
        instructor_email="not-an-email",
        password="pass"
    )

    with pytest.raises(Exception):
        instructor.full_clean()

#----------------------------------------------
#-------------end of user authentication module test---------
#----------------------------------------------


#----------------------------------------------
#-------------Start of exam module test---------
#----------------------------------------------

# -----Exam models / id generation-------
@pytest.mark.django_db
def test_exam_custom_id_generated():
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")

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
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")

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
    instructor = Instructor.objects.create(
        full_name="Teacher",
        instructor_email="teacher@example.com",
        password="pass"
    )

    student = Student.objects.create(
        full_name="Student",
        student_email="stud@example.com",
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

    attempt = ExamAttempt.objects.create(exam=exam, student=student)

    assert attempt.attempt_id.startswith("ATT-")
    assert len(attempt.attempt_id) == 10

    
@pytest.mark.django_db
def test_exam_str():
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")
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
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")
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
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")
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
    student = Student.objects.create(
        full_name="Stu",
        student_email="stu@example.com",
        matric_number="A001",
        password="pass"
    )

    teacher = Instructor.objects.create(
        full_name="Teach",
        instructor_email="teach@example.com",
        password="pass"
    )

    exam = Exam.objects.create(
        title="Sample Exam",
        description="Test exam",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=teacher,
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="What is 2+2?",
        question_type="TEXT",
        order_no=1,
    )

    attempt = ExamAttempt.objects.create(exam=exam, student=student)

    Answer.objects.create(
        attempt=attempt,
        question=q,
        text_answer="Ans1"
    )

    with pytest.raises(Exception):
        Answer.objects.create(
            attempt=attempt,
            question=q,
            text_answer="Ans2"
        )


#----- Date logic tests----

@pytest.mark.django_db
def test_exam_is_open_true():
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")
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
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")
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
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")
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
    student = Student.objects.create(
        full_name="Stu",
        student_email="stu@example.com",
        matric_number="A001",
        password="pass"
    )

    teacher = Instructor.objects.create(
        full_name="Teach",
        instructor_email="teach@example.com",
        password="pass"
    )

    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=teacher
    )

    question = ExamQuestion.objects.create(
        exam=exam,
        question_text="Test question",
        question_type="TEXT"
    )

    attempt = ExamAttempt.objects.create(exam=exam, student=student)

    answer = Answer.objects.create(
        attempt=attempt,
        question=question,
        text_answer="Some answer"   
    )

    s = str(answer)
    assert "Answer for" in s
    assert "Attempt" in s

    
@pytest.mark.django_db
def test_choice_str():
    teacher = Instructor.objects.create(
        full_name="Teach",
        instructor_email="teach@example.com",
        password="pass"
    )

    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=teacher
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="Hello",
        question_type="MCQ"
    )

    c = Choice.objects.create(
        choice_id=q,
        choice_text="Hello",
        is_correct=False
    )

    assert "Choice for" in str(c)
    

@pytest.mark.django_db
def test_question_order_default():
    teacher = Instructor.objects.create(
        full_name="Teach",
        instructor_email="teach@example.com",
        password="pass"
    )

    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=teacher
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="Hello",
        question_type="TEXT"
    )

    assert q.order_no == 1

    
    
# --- Required fields test ---
@pytest.mark.django_db
def test_exam_requires_title():
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")

    with pytest.raises(Exception):
        Exam.objects.create(
            title=None,
            description="desc",
            start_time=timezone.now(),
            end_time=timezone.now(),
            created_by=user
        )
        
@pytest.mark.django_db
def test_exam_requires_start_time():
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")

    with pytest.raises(Exception):
        Exam.objects.create(
            title="Exam",
            description="desc",
            start_time=None,   
            end_time=timezone.now(),
            created_by=user
        )
        
@pytest.mark.django_db
def test_exam_requires_end_time():
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")

    with pytest.raises(Exception):
        Exam.objects.create(
            title="Exam",
            description="desc",
            start_time=timezone.now(),
            end_time=None,    
            created_by=user
        )
        
        
@pytest.mark.django_db
def test_exam_end_time_before_start_invalid():
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")

    exam = Exam(
        title="Exam",
        description="desc",
        start_time=timezone.now() + timedelta(hours=1),
        end_time=timezone.now(),  
        created_by=user
    )

    with pytest.raises(Exception):
        exam.full_clean()
        
@pytest.mark.django_db
def test_question_without_exam_invalid():
    with pytest.raises(Exception):
        ExamQuestion.objects.create(
            exam=None,  
            question_text="Invalid",
            question_type="TEXT",
        )
        
@pytest.mark.django_db
def test_mcq_without_choices_invalid():
    user = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")
    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=user
    )

    q = ExamQuestion.objects.create(
        exam=exam,
        question_text="MCQ no choices",
        question_type="MCQ"
    )

    assert q.choices.count() == 0
    
@pytest.mark.django_db
def test_answer_requires_some_response():
    user = student = Student.objects.create(full_name="Stu",student_email="stu@example.com",matric_number="A123",password="pass")

    teacher = Instructor.objects.create(full_name="Test Teacher",instructor_email="t@example.com",password="pass")

    exam = Exam.objects.create(
        title="Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=teacher
    )

    question = ExamQuestion.objects.create(
        exam=exam,
        question_text="Q1",
        question_type="TEXT"
    )

    attempt = ExamAttempt.objects.create(exam=exam, student=user)

    answer = Answer(
        attempt=attempt,
        question=question,
        text_answer=""     
    )

    with pytest.raises(Exception):
        answer.full_clean()

#----------------------------------------------
#-------------End  of exam module test---------
#----------------------------------------------

