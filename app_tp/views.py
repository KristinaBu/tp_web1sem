from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Tag, Question, Profile, Answer
import math



def paginate(objects, request, per_page=10):
    page_number_str = request.GET.get('page', '1')
    if not page_number_str.isdigit() or int(page_number_str) <= 0:
        page_number = 1
    else:
        page_number = int(page_number_str)
    if page_number > math.ceil(len(objects)/per_page):
        page_number = math.ceil(len(objects)/per_page)
    paginator = Paginator(objects, per_page)

    return paginator.get_page(page_number)


def index(request):
    questions = Question.objects.get_questions_ordered_by_date()
    popular_tags = Tag.objects.all()
    return render(request,'index.html',
                  {'questions' : paginate(questions, request, 5),
                   'popular_tags' : popular_tags})

def hot(request):
    hot_questions = Question.objects.get_questions_ordered_by_rating()
    popular_tags = Tag.objects.all()
    return render(request,'index.html',
                  {'questions' : paginate(hot_questions, request, 5),
                                                'popular_tags' : popular_tags})

def tag(request, tag_id):
    popular_tags = Tag.objects.all()
    tag_item = Tag.objects.get(id=tag_id)
    return render(request,'tag.html', {'tag' : tag_item,
                                       'questions' : paginate(Question.objects.get_questions_by_tag(tag_item.id), request, 5),
                                       'popular_tags' : popular_tags})



def question(request, question_id):
    #questions = Question.objects.get_questions_ordered_by_date()
    #question_item = questions[question_id]
    popular_tags = Tag.objects.all()
    question_item = Question.objects.get(id=question_id)
    return render(request,'question.html', {'question' : question_item, 'popular_tags' : popular_tags,
                                            'answers' : paginate(Answer.objects.get_answers_by_question(question_item.id), request, 5)})



def ask(request):
    popular_tags = Tag.objects.all()
    return render(request,'ask.html', {'popular_tags' : popular_tags})


def login(request):
    popular_tags = Tag.objects.all()
    return render(request,'login.html', {'popular_tags' : popular_tags})


def signup(request):
    popular_tags = Tag.objects.all()
    return render(request,'signup.html', {'popular_tags' : popular_tags})




