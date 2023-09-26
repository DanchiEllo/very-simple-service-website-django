from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.template.backends.dummy import Template
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from worker.models import CustomUser, GENDERS


class UserAuthorizationForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=100, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = CustomUser.objects.filter(username=username)

        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password1')
        if not password:
            raise ValidationError("Введите пароль")

        return password

    def authorization(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            print("Всё чётко")
        else:
            raise ValidationError("Данные не совпадают")

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        html =  Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))

@csrf_exempt
class UserRegistrationForm(forms.Form):
    username = forms.CharField(label="Логин", min_length=5, max_length= 100, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'a'}))
    first_name = forms.CharField(label="Имя", min_length=4, max_length=150, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'a'}))
    last_name = forms.CharField(label="Фамилия", min_length=4, max_length=150, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'a'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'a'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'a'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'a'}))
    gender = forms.ChoiceField(choices=GENDERS, required=True, label='Пол')
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs= {'onchange': 'loadFile(event)'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label='Роль', empty_label='Выберите группу')

    def clean_group(self):
        group = self.cleaned_data['group']
        return group

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data['profile_picture']
        return profile_picture

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        return gender

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = CustomUser.objects.filter(username=username)
        if r.count():
            raise ValidationError("Этот логин уже занят")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].lower()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].lower()
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = CustomUser.objects.filter(email=email)
        if r.count():
            raise ValidationError("Эта почта уже используется")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")

        return password2

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.gender = self.cleaned_data['gender']
        user.profile_picture = self.cleaned_data['profile_picture']
        user.group = self.cleaned_data['group']
        Group.objects.get(name=user.group).user_set.add(user)

        user.save()
        return user

    # first_name = forms.CharField(label='Your name', max_length=100)
    # second_name = forms.CharField(label='Your second name', max_length=100)
    # email = forms.EmailField(label='Email')
    # password = forms.CharField(label='Password', widget=forms.PasswordInput())
    # re_password = forms.CharField(label='Password', widget=forms.PasswordInput())