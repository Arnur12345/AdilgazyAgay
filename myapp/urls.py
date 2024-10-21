from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login,name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('create_user/',views.create_student,name='create-user'),
    path('show-users/',views.show_users,name="show-users"),
    path('create-video/',views.upload_video,name='create-video'),
    path('videos/',views.video_list,name="video-list"),
    path('upload_pdf/',views.upload_pdf,name="upload-pdf"),
    path('pdfs/', views.pdf_list, name='pdf-list'),
    path('about/',views.about, name='about'),
]
