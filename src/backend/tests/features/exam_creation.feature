Feature: Exam Creation

Scenario: Teacher creates an exam
GIven a Teacher exist 
When a teacher creates a an exam titled "Test Exam"
Then the exam should be save with an xam ID
