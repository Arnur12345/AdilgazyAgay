from django.contrib import admin
from .models import Video,User,PDFDocument, UserCourseAccess, Course


admin.site.register(User)
admin.site.register(Video)
admin.site.register(PDFDocument)
admin.site.register(Course)
admin.site.register(UserCourseAccess)