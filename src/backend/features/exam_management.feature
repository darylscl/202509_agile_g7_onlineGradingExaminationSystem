Feature: Instructor exam management
    As an Instructor, I want to view the list of exams that I created, 
    including exam ID, title, schedule, total number of questions, 
    and be able to edit the details of the exam or delete any created exams, 
    so that I can update mistakes or remove the exam

    Scenario: Instructor views the list of created exams
        Given an instructor exists with multiple exams 
        When the instructor opens the exam list page
        Then all the exams should be visible on the page

    Scenario: Instructor edits an existing exam
        Given an instructor exists with at least 1 created exam
        When the instructor updates the exam details such as title
        Then this exam should be saved with the new title

    Scenario: Instructor deletes an existing exam
        Given an instructor exists with 1 exam to delete
        When the instructor deletes the exam
        Then the exam should be removed from the system
