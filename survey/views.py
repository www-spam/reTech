from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from .models import Choice, Question

# Create your views here.
def survey(request):
    if check(request) == 'login':
        latest_question_list = Question.objects.order_by('pub_data')[:5]
        template = loader.get_template('survey.html')
        context = {
            'latest_question_list': latest_question_list,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, "챗봇을 이용하시려면 로그인이 필요해요.")
        return redirect('/polls/login')
    

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})

def results(question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('/survey/survey')
    

def login_check(request):
    if check(request) == 'login':
        return 'login'
    else:
        messages.error(request, "만족도 조사를 위해 로그인 해주세요.")
        return 'logout'

def check(request):
    user_session = request.session.get('user_session', '')
    if user_session == '':
        return 'logout'
    else:
        return 'login'