from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


STATUS_CHOICES= [
    ('research', 'Research'),
    ('professor', 'Professor'),
    ('student', 'Student'),
]

TOPIC_CHOICES = [
    ('medicine', 'Medcine'),
    ('informatics', 'Informatics' ),
    ('biology', 'Biology'),
    ('cybersecurity', 'Cybersecurityt'),
    ('robotics', 'Robotics')
]

SUBTOPIC_CHOICES = [
    ('ai', 'Artificial Intelligence'),
    ('genetics', 'Genetics'),
    ('cybersecurity', 'CyberSecurity'),
    ('robotics', 'Robotics'),
]


class SingupForm(forms.Form):
    name = forms.CharField(label='First Name', max_length=100)
    surname = forms.CharField(label='Surname', max_length=100)
    username = forms.CharField(label='Nickname (unique)', max_length=100)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    company = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField(required=False)
    topics = forms.MultipleChoiceField(choices=TOPIC_CHOICES, widget=forms.CheckboxSelectMultiple)
    subtopics = forms.MultipleChoiceField(choices=SUBTOPIC_CHOICES, widget=forms.CheckboxSelectMultiple)

class ArticleUploadForm(forms.Form):
    title = forms.CharField(max_length=255)
    abstract = forms.CharField(widget=forms.Textarea)
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(help_text="Comma-separated tags (e.g., AI, Robotics, Research)")

