from django.urls import path
from . import views

urlpatterns = [
    # General
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # User Management
    path('create-user/', views.create_user, name='create-user'),
    path('show-users/', views.show_users, name='show-users'),

    # Courses
    path('courses/', views.course_list, name='course-list'),
    path('courses/create/', views.create_course, name='create-course'),
    path('courses/<int:course_id>/', views.course_detail, name='course-detail'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit-course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete-course'),

    # Videos
    path('courses/<int:course_id>/videos/', views.video_list, name='video-list'),
    path('courses/<int:course_id>/videos/add/', views.add_video, name='add-video'),
    path('courses/<int:course_id>/add-video/', views.add_video, name='add-video'),
    path('courses/<int:course_id>/videos/<int:video_id>/edit/', views.edit_video, name='edit-video'),
    path('courses/<int:course_id>/videos/<int:video_id>/delete/', views.delete_video, name='delete-video'),
    path('courses/<int:course_id>/videos/<int:video_id>/', views.video_detail, name='video-detail'),





    path('courses/<int:course_id>/grant-access/', views.grant_course_access, name='grant-course-access'),

    # PDFs
    path('pdfs/', views.pdf_list, name='pdf-list'),
    path('upload-pdf/', views.upload_pdf, name='upload-pdf'),
]
