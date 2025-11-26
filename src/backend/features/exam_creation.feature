Feature: Create Exam Creation functionality for Instructor
    As an Instructor, I want to create exam questions with either type, 
    MCQ with 4 choices for the question or TEXT question, 
    so that I can let students take the exam 

    Scenario: Instructor create a new exam
        Given a logged-in Instructor exists
        When the Instructor opens the exam creation page
        And fills in the exam form with valid data
        And submits the exam form
        Then a new exam should be created
        And the teacher is redirect to the question filling page

    Scenario: Instructor adds a TEXT question to the exam
        Given an existing exam created by the Instructor
        When the teacher submits a Text question
        Then the TEXT question should be saved under that exam

    Scenario: Instructor adds a MCQ question with choices to the exam
        Given an existing exam created by the Instructor
        When the Instructor submits and MCQ question with 4 choices
        And selects one correct choices
        Then the MCQ question and its choices should be saved