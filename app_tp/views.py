from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import math


# Create your views here.
QUETIONS = [{'id': i,
              'title': f'title {i}',
              'text': f'text {i}'} for i in range(0, 20)]
HOT_QUETIONS = [{'id': i,
              'title': f'hot title {i}',
              'text': f'text {i}'} for i in range(0, 20)]

TAGS = [{'id': i,
         'tag_name': f'bububu {i}'} for i in range(0, 3)]

AMSWERS = [{'id': i,
            'text': f'clever answer {i}'} for i in range(0, 10)]

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

    return render(request,'index.html',
                  {'questions' : paginate(QUETIONS, request, 5),
                   'tags' : TAGS})

def hot(request):
    '''один вопрос под своим id'''
    return render(request,'index.html', {'questions' : paginate(HOT_QUETIONS, request, 5),
                                                'tags' : TAGS})

def tag(request, tag_id):
    tag_item = TAGS[tag_id]
    question_item = QUETIONS[1]
    return render(request,'tag.html', {'tag' : tag_item, 'questions' : paginate(QUETIONS, request, 5),
                                              'question' : question_item,  'tags' : TAGS})


def answers(request):
    return render(request, 'question.html', {'answers' : AMSWERS,
                   'tags' : TAGS})

def question(request, question_id):
    question_item = QUETIONS[question_id]
    return render(request,'question.html', {'question' : question_item,
                                                   'tags' : TAGS,
                                                   'answers' : paginate(AMSWERS, request, 5)})



def ask(request):
    return render(request,'ask.html', {'tags' : TAGS})


def login(request):
    return render(request,'login.html', {'tags' : TAGS})


def signup(request):
    return render(request,'signup.html', {'tags' : TAGS})




