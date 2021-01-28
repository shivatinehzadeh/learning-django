from django.forms import ModelForm
from .models import Suggestion,Reserve,Book
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class suggestionForm(ModelForm):
    name=forms.CharField(label= 'نام',label_suffix='')
    email=forms.EmailField(label='ایمیل')
    description=forms.CharField(widget=forms.Textarea(),label='توضیحات')
    class Meta:
        model = Suggestion
        fields=['name','email','description']


class RegisterForm(UserCreationForm):
    # username=forms.CharField(label="نام کاربری")

    password1 = forms.CharField(
        label=("رمز عبور"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=""
    )
    phone=forms.IntegerField(label='شماره تلفن' , label_suffix="")
    class Meta:
     model=User
     fields=['username','email','password1','password2','phone']


class LoginForm(AuthenticationForm):
    password = forms.CharField(
        label=("رمز عبور"),
        strip=False,
        widget=forms.PasswordInput(),
        help_text=""
    )
    class Meta:
        model=User

class quantityForm(ModelForm):
    class Meta:
        model=Reserve
        fields=['quantity',]
        widgets={
            'quantity':forms.NumberInput(attrs={'style':'width:40px'})
        }



