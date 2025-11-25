from behave import given, when, then
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from app.models import *
from datetime import timedelta, datetime


# Exam creation: Scenario 1
@given("a logged-in Instructor exists")
def step_impl(context):
    context.teacher = User.objects.create_user(username="teacher", password="pass123")
    context.client = Client()


@when("the Instructor opens the exam creation page")
def step_impl(context):
    context.response = context.client.get("/instructor/exams/create/")


@when("fills in the exam form with valid data")
def step_impl(context):
    context.exam_data = {
        "create_exam": "1",
        "title": "BMSE3333 Agile Developement",
        "description": "Chapter 5",
        "start_time": "2025-11-25T10:00",
        "end_time": "2025-11-25T11:00",
    }


@when("submits the exam form")
def step_impl(context):
    context.response = context.client.post(
        "/instructor/exams/create/", context.exam_data
    )
    context.exam = Exam.objects.first()


@then("a new exam should be created")
def step_impl(context):
    assert context.exam is not None
    assert context.exam.title == "BMSE3333 Agile Developement"


@then("the teacher is redirect to the question filling page")
def step_impl(context):
    assert context.response.status_code == 302
    assert f"?exam_id={context.exam.exam_id}" in context.response.url


# Exam creation: Scenario 2


@given("an existing exam created by the Instructor")
def step_impl(context):
    context.teacher = User.objects.create_user(username="teacher2", password="pass123")
    context.client = Client()
    context.exam = Exam.objects.create(
        title="Math Test",
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
        created_by=context.teacher,
    )


@when("the teacher submits a Text question")
def step_impl(context):
    data = {
        "add_question": "1",
        "question_text": "Explain what is Agile Programming",
        "question_type": "TEXT",
    }
    context.client.post(
        f"/instructor/exams/create/?exam_id={context.exam.exam_id}", data
    )


@then("the TEXT question should be saved under that exam")
def step_impl(context):
    assert context.exam.questions.count() == 1
    q = context.exam.questions.first()
    assert q.question_type == "TEXT"
    

# Exam creation: Scenario 3 

# basic test
@when('the Instructor submits and MCQ question with 4 choices')
def step_impl(context):
    data = {
        "add_question": "1",
        "question_text": "What is 2+2?",
        "question_type": "MCQ",
        "choice_text": ["1", "2", "3", "4"],
        "correct_choice": "3"
    }
    context.client.post(f"/instructor/exams/create/?exam_id={context.exam.exam_id}", data)
    
@when('selects one correct choices')
def step_impl(context):
    pass

@then('the MCQ question and its choices should be saved')
def step_impl(context):
    q = context.exam.questions.first()
    assert q.question_type == "MCQ"
    assert q.choices.count() == 4
    correct = q.choices.filter(is_correct=True).first()
    assert correct.choice_text == "4"
