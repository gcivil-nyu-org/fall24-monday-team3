from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import your custom user model if you have one

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # If you're using a custom user model
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
