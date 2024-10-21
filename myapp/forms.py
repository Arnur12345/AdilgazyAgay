from django.forms import ModelForm
from .models import Video, PDFDocument

from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'is_available']
        widgets = {
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class VideoAvailabilityForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['is_available']


class PDFForm(ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['pdf_file']