from django.db import models
from django.contrib.auth.models import User, AbstractUser
    
from datetime import datetime, timedelta

class User(AbstractUser):
    username = models.CharField(max_length=200, null=True,unique=True)
    subpassword = models.TextField(null=True)
    email = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=100)
    
    USERNAME_FIELD = 'username'

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='video/%y')
    is_available = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos', default=None, null = True)


    def __str__(self):
        return self.title

class PDFDocument(models.Model):    
    pdf_file = models.FileField(upload_to='pdf')

    def __str__(self):
        return self.pdf_file.name

class UserCourseAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='accesses')
    expiration_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
       
class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:20]}'