# discussions/forms.py
from django import forms
from .models import Discussion, Reply


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content', 'topic']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a descriptive title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your discussion content here...'
            }),
            'topic': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'title': 'Discussion Title',
            'content': 'Discussion Content',
            'topic': 'Select Topic'
        }
        help_texts = {
            'title': 'Keep it clear and specific',
            'content': 'Provide all relevant details for better responses',
            'topic': 'Choose the most appropriate category'
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your reply here...'
            })
        }
        labels = {
            'content': 'Your Reply'
        }