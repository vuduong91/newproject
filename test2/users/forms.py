from .models import CustomUser
from django import forms
from .models import Product, OrderDetail, User,Order
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        fields = ('email',)
class LoginForm(forms.Form):
    email = forms.CharField(label='Email Address', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class OrderAcceptForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['cost', 'quanity', 'product', 'order']

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','password']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user']

class UpdateForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['order','cost', 'quanity', 'product']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name','email','password','phone','address']