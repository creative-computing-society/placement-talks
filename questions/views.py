from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Question

# Create your views here.

def index(request):
    return render(request, 'questions/index.html')

@login_required(login_url='/admin/login')
def moderator(request):
    questions = Question.objects.all()
    return render(request, 'questions/moderator.html', {
        'questions': questions,
    })

def display(request):
    questions = Question.objects.filter(isAccepted=True).all()
    return render(request, 'questions/display_new.html', {
        'questions': questions,
    })
