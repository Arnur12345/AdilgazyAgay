from django.db import models
from django.contrib.auth.models import User, AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=200, null=True,unique=True)
    subpassword = models.TextField(null=True)
    email = models.EmailField(unique=True, null=True)

    
    USERNAME_FIELD = 'username'

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='video/%y')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class PDFDocument(models.Model):    
    pdf_file = models.FileField(upload_to='pdf')

    def __str__(self):
        return self.pdf_file.name