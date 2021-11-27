from users.models import UserProfile
from django import forms

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name',  'email', 'password')
        
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
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'password')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

