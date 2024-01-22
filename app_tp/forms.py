from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, Question, Tag, Answer

# образец:
class QuestionForm(forms.ModelForm):
    tags = forms.CharField()
    # тип для поля формы
    title = forms.CharField(widget=forms.Textarea)
    text = forms.CharField(widget=forms.Textarea)

    # доп параметры для класса
    class Meta:
        # модель, кот. использует эта форма
        model = Question
        # поля модели, которые включены в форму
        fields = ['title', 'text', 'tags']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if Question.objects.filter(title=title).exists():
            raise ValidationError("Заголовок title уже существует")
        if title and title.strip() == '':
            raise ValidationError("Заголовок title не может состоять только из пробелов")
        if title and len(title.strip()) < 10:
            raise ValidationError("Длина заголовка должна быть более 10 символов")

        if text and text.strip() == '':
            raise ValidationError("Текст text не может состоять только из пробелов")
        if text and len(text.strip()) < 20:
            raise ValidationError("Длина текста должна быть более 20 символов")


    def clean_tags(self):
        tags = self.cleaned_data.get('tags')

        if tags:
            # по запятым и без пробелов
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip() != '']

            # проверка на количество тегов
            if len(tag_list) > 3:
                raise ValidationError("Вы не можете создать более трех тегов за один вопрос")

            # создание списка для объектов Tag
            tag_objs = []
            for tag in tag_list:
                # существует тег или нет
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                tag_objs.append(tag_obj)
            return tag_objs

    def save(self, commit=True):
        # commit=False, чтобы предотвратить автоматическое сохранение
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # теги для объекта модели
            instance.tags.set(self.cleaned_data.get('tags'))
        return instance


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'nickname']

    def clean(self):
        #проверка

        cleaned_data = super().clean()
        nickname = cleaned_data.get('nickname')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        email = cleaned_data.get('email')

        # уникальность
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        # ошибка ввода
        if username.strip() == '':
            raise ValidationError("Имя пользователя не может состоять только из пробелов")
        if password != password_repeat:
            raise ValidationError("Пароли не совпадают")
        if nickname.strip() == '':
            raise ValidationError("Никнейм не может состоять только из пробелов")
        if '@' not in email:
            raise ValidationError("Email должен содержать символ @")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        # проверка уникальности почты
        if User.objects.filter(email=email).exclude(username=self.instance.user.username).exists():
            raise ValidationError("Пользователь с таким email уже существует")

        return cleaned_data


class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Answer
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text and not text.strip():
            raise ValidationError("Текст ответа не может состоять только из пробелов")

        if text and len(text.strip()) < 15:
            raise ValidationError("Длина ответа должна быть более 15 символов")
        return text
