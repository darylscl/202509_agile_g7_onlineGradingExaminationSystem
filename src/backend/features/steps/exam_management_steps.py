from behave import given, when, then
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from app.models import *
from datetime import timedelta, datetime

# Exam management scenario 1
@given('an instructor exists with multiple exams')
def step_impl(context):
    context.client = Client()
    context.user = User.objects.create(username="teacher")
    context.client.force_login(context.user)
    
    Exam.objects.create(
        title="Exam 1",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=context.user
    )
    
    Exam.objects.create(
        title="Exam 2",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=context.user
    )
    
@when('the instructor opens the exam list page')
def step_impl(ctx):
    ctx.response = ctx.client.get("/instructor/exams/")
    
@then('all the exams should be visible on the page')
def step_impl(ctx):
    assert b"Exam 1" in ctx.response.content
    assert b"Exam 2" in ctx.response.content
    
# Exam management scenario 2
@given('an instructor exists with at least 1 created exam')
def step_impl(ctx):
    ctx.client = Client()
    ctx.user = User.objects.create(username="teacher")
    ctx.client.force_login(ctx.user)
    
    ctx.exam = Exam.objects.create(
        title="Original Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=ctx.user
    )
    
@when('the instructor updates the exam details such as title')
def step_impl(ctx):
    ctx.response = ctx.client.post(
         f"/instructor/exams/{ctx.exam.exam_id}/edit/",
        {
            "title": "Updated Exam Title",
            "description": "desc",
            "start_time": ctx.exam.start_time,
            "end_time": ctx.exam.end_time
        }
    )
    
@then('this exam should be saved with the new title')
def step_impl(ctx):
    ctx.exam.refresh_from_db()
    assert ctx.exam.title == "Updated Exam Title"
    
# exam management scenario 3
@given('an instructor exists with 1 exam to delete')
def step_impl(ctx):
    ctx.client = Client()
    ctx.user = User.objects.create(username="teacher")
    ctx.client.force_login(ctx.user)
    
    ctx.exam = Exam.objects.create(
        title="Test delete Exam",
        description="desc",
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        created_by=ctx.user
    )
    
@when('the instructor deletes the exam')
def step_impl(ctx):
    ctx.response = ctx.client.post(
        f"/instructor/exams/{ctx.exam.exam_id}/delete/"  # must match url
    )
    
@then('the exam should be removed from the system')
def step_impl(ctx):
    assert Exam.objects.filter(exam_id=ctx.exam.exam_id).exists() is False # False not exist