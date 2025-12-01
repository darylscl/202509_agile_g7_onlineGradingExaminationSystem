from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import uuid

#Helper function
def generate_student_id():
    last = Student.objects.order_by("-student_ID").first()
    if not last:
        return "STU001"
    
    last_id = int(last.student_ID.replace("STU", ""))
    new_id = last_id + 1
    return "STU" + str(new_id).zfill(3)

def generate_instructor_id():
    last = Instructor.objects.order_by("-instructor_ID").first()
    if not last:
        return "INS001"
    
    last_id = int(last.instructor_ID.replace("INS", ""))
    new_id = last_id + 1
    return "INS" + str(new_id).zfill(3)


# User models
class Student(models.Model):
    student_ID = models.CharField(max_length=10, primary_key=True, editable=False)
    full_name =  models.CharField(max_length=255)
    student_email =  models.EmailField(unique=True)
    matric_number = models.CharField(max_length=50, unique=True) #exam number
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default="student")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        validate_email(self.student_email)
        if not self.student_ID:
            self.student_ID = generate_student_id()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.student_ID} - {self.full_name}"
    
class Instructor(models.Model):
    instructor_ID =  models.CharField(max_length=10, primary_key=True, editable=False)
    full_name = models.CharField(max_length=255)
    instructor_email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default="instructor")
    
    def save(self, *args, **kwargs):
        validate_email(self.instructor_email)
        if not self.instructor_ID:
            self.instructor_ID = generate_instructor_id()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.instructor_ID} - {self.full_name}"
    

# Examination models

class Exam(models.Model):
    exam_id = models.CharField(max_length=20, unique=True, editable=False) # custom exam id
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("End time must be after start time.")
    
    # custom exam id
    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.exam_id:  
            last_exam = Exam.objects.order_by('-id').first()
            if last_exam:
                last_number = int(last_exam.exam_id.split('-')[1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.exam_id = f"EX-{new_number:03d}"   # EX-001
        super().save(*args, **kwargs)
    
    @property
    def is_open(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time
    
    def __str__(self):
        return f"{self.exam_id} - {self.title}"
    
class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=[
        ("MCQ", "Multiple Choice"),
        ("TEXT", "Short Answer"),
    ])
    order_no = models.PositiveIntegerField(default=1)
    marks = models.FloatField(default=1)  # <-- Add this line

    def __str__(self):
        return f"Q{self.order_no}: {self.question_text[:30]}"
    
class Choice(models.Model):   # for mcq only
    choice_id = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)  # set which ans is correct for auto grading (mcq)
    
    def __str__(self):
        return f"Choice for Q{self.choice_id.id}: {self.choice_text}"
    
    
class ExamAttempt(models.Model):
    attempt_id = models.CharField(max_length=20, unique=True, editable=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    
    #custom id 
    def save(self, *args, **kwargs):
        if not self.attempt_id:
            self.attempt_id = f"ATT-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def submitted(self):
        return self.submitted_at is not None
    
    def __str__(self):
        return f"{self.attempt_id} ({self.student})"
    
    
    
class Answer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    
    selected_choice = models.ForeignKey(Choice, null=True, blank=True, on_delete=models.SET_NULL)
    text_answer = models.TextField(blank=True)
    
    marks = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ('attempt', 'question')
        
    def clean(self):
        if self.question and self.question.question_type == "MCQ":
            if not self.selected_choice:
                raise ValidationError("MCQ answers must have a selected choice.")

        if self.question and self.question.question_type == "TEXT":
            if not self.text_answer or not self.text_answer.strip():
                raise ValidationError("Text answers cannot be empty.")
            
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Answer for {self.question.id} by Attempt {self.attempt.attempt_id}"
    


# Reporting models
