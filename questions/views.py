from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Question

# Create your views here.

def index(request):
    return render(request, 'questions/index.html')

@staff_member_required
def moderator(request):
    questions = Question.objects.all()
    return render(request, 'questions/moderator.html', {
        'questions': questions,
    })

def display(request):
    questions = Question.objects.filter(isAccepted=True).all()
    return render(request, 'questions/display.html', {
        'questions': questions,
    })
