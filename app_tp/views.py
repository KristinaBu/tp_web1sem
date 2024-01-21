from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from .models import Tag, Question, Profile, Answer
import math

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User



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
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                next_url = request.POST.get('next', 'index')
                if not next_url:
                    next_url = 'index'
                return redirect(next_url)

            else:
                error_message = 'Неверный логин или пароль'

    return render(request, 'login.html',
                  {'form': form, 'popular_tags': popular_tags, 'error_message': error_message, 'username': username})

@csrf_exempt
def signup(request):
    popular_tags = Tag.objects.all()
    error_message = ''
    username = ''
    email = ''

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            user.save()
            # профиль для нового пользователя
            profile = Profile(user=user, nickname=form.cleaned_data['nickname'])
            profile.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            auth_login(request, user)
            return redirect('index')

    else:
        form = RegistrationForm()

    return render(request,'signup.html', {'popular_tags' : popular_tags, 'error_message': error_message, 'form': form})



def logout(request):
    auth_logout(request)
    next_page = request.META.get('HTTP_REFERER', 'index')
    return HttpResponseRedirect(next_page)

@login_required
def edit_profile(request):
    popular_tags = Tag.objects.all()
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'popular_tags' : popular_tags, 'form': form})