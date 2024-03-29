
from django.shortcuts import render, redirect
from django.http import HttpResponse
from main import models
from django.utils  import timezone

def create_result(id):
    quiz_taker = models.QuizTaker.objects.get(id=id)
    correct = 0
    incorrect = 0
    for object in models.Answer.objects.filter(taker=quiz_taker):
        if object.is_correct:
            correct +=1
        else:
            incorrect +=1

    models.Result.objects.create(
        taker=quiz_taker,
        correct_answers=correct,
        incorrect_answers=incorrect
    )

def quiz_detail(request, code):
    quiz = models.Quiz.objects.get(code=code)
    quiz_taker = models.QuizTaker.objects.filter(quiz=quiz).first()
    
    # Check if quiz_taker is None before using it
    if not quiz_taker:
        return HttpResponse("Quiz taker not found")
    
    result = models.Result.objects.filter(taker=quiz_taker).first()
    questions = models.Question.objects.filter(
        quiz=quiz
    )
    now = timezone.now()
    
    if quiz.start_time and now < quiz.start_time:
        return HttpResponse("Quiz hali boshlanmagan")
    elif quiz.end_time and now > quiz.end_time:
        return HttpResponse("Quiz tugagan")
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'result': result
    }
    return render(request, 'front/quiz-detail.html', context)



def create_answers(request, code):
    quiz = models.Quiz.objects.get(code=code)
    full_name = request.POST['full_name']
    phone = request.POST['phone']
    email = request.POST.get('email')
    quiz_taker = models.QuizTaker.objects.create(
        full_name=full_name,
        phone=phone,
        email=email,
        quiz=quiz
    )
    for key, value in request.POST.items():
        if key.isdigit():
            models.Answer.objects.create(
                taker=quiz_taker,
                question_id=int(key),
                answer_id=int(value)
            )
    create_result(quiz_taker.id)
    return redirect('dash:result_detail', id=quiz_taker.id)
