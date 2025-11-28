from django import template

register = template.Library()

@register.filter
def get_answer_selected(answers, question_choice):
    """
    Usage: answers|get_answer_selected:question:choice
    Returns True if the answer for the question has the selected choice.
    """
    try:
        question, choice = question_choice
        return answers.filter(question=question, selected_choice=choice).exists()
    except Exception:
        return False

@register.filter
def get_answer_text(answers, question):
    """
    Usage: answers|get_answer_text:question
    Returns the text answer for the question if it exists.
    """
    answer = answers.filter(question=question).first()
    return answer.text_answer if answer else ''


@register.filter
def sum_list(value):
    """
    Usage: some_list|sum_list
    Returns the sum of a list of numbers.
    """
    try:
        return sum(value)
    except Exception:
        return 0