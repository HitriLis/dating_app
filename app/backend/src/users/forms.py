from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name',  'email', 'password')  
        
    def save(self, commit=True):
        print(self.__dict__)
        user = super().save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user
class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = User
        fields = ('name',  'email', 'password')  
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

