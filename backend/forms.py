from .models import ChatMessage
from django import forms


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['user_message']
        widgets = {
            'user_message': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
