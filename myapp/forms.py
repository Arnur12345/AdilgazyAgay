from django.forms import ModelForm
from .models import Video, PDFDocument, UserCourseAccess, Comment, Course

from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']
        widgets = {
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course description',
                'rows': 4
            }),
        }

class VideoAvailabilityForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['is_available']


class PDFForm(ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['pdf_file']

class AccessForm(ModelForm):
    class Meta:
        model = UserCourseAccess
        fields = ['user','course','expiration_date']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'comment-textarea',
                'placeholder': 'Add a comment...',
                'rows': 3
            }),
        }