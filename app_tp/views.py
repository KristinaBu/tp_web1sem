from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Tag, Question, Profile, Answer
import math

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.decorators import login_required



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
                  {'questions' : paginate(hot_questions, request, 2),
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


@login_required
def ask(request):
    popular_tags = Tag.objects.all()
    return render(request,'ask.html', {'popular_tags' : popular_tags})


@csrf_exempt
def login(request):
    popular_tags = Tag.objects.all()
    error_message = ''
    username = ''

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            next_url = request.POST.get('next', 'index')  # Get the next parameter
            if not next_url:  # If next_url is empty
                next_url = 'index'  # Set a default URL
            return redirect(next_url)  # Redirect to the next page or index

        else:
            error_message = 'Неверный логин или пароль'

    return render(request, 'login.html',
                  {'popular_tags': popular_tags, 'error_message': error_message, 'username': username})


def signup(request):
    popular_tags = Tag.objects.all()
    error_message = ''
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')

        if User.objects.filter(username=username).exists():
            error_message = 'Пользователь с таким именем уже существует'
        elif User.objects.filter(email=email).exists():
            error_message = 'Этот адрес электронной почты уже зарегистрирован'
        elif password != password_repeat:
            error_message = 'Пароли не совпадают'
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = Profile(user=user, user_login=username)
            profile.save()
            auth_login(request, user)
            return redirect('index')

    return render(request,'signup.html', {'popular_tags' : popular_tags, 'error_message': error_message})


def logout(request):
    auth_logout(request)
    next_page = request.META.get('HTTP_REFERER', 'index')
    return HttpResponseRedirect(next_page)