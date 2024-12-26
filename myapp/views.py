from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib import messages
from django.utils.timezone import now
from .models import Course, Video, UserCourseAccess, PDFDocument
from .forms import CourseForm, VideoForm, AccessForm, PDFForm, CommentForm
from django.contrib.auth import get_user_model, authenticate, login, logout

User = get_user_model()

# General Views
def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})

def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')

# User Management
@user_passes_test(lambda u: u.is_staff)
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect('show-users')
    return render(request, 'create_user.html')

@user_passes_test(lambda u: u.is_staff)
def show_users(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
    return render(request, 'show_users.html', {'users': users})

# Course Views
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

@user_passes_test(lambda u: u.is_staff)
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course-list')
    else:
        form = CourseForm()
    return render(request, 'create_course.html', {'form': form})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()
    return render(request, 'course_detail.html', {'course': course, 'videos': videos})

@user_passes_test(lambda u: u.is_staff)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course-list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'edit_course.html', {'form': form, 'course': course})

@user_passes_test(lambda u: u.is_staff)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        return redirect('course-list')
    return render(request, 'delete_course.html', {'course': course})

# Video Views
def video_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()
    return render(request, 'video_list.html', {'course': course, 'videos': videos})

def add_video(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        print("Form submission received")  # Debugging step
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")  # Debugging step
            video = form.save(commit=False)
            video.course = course
            video.save()
            print("Video created:", video)  # Debugging step
            return redirect('video-list', course_id=course.id)  # Redirect to the video list of the course
        else:
            print("Form is invalid:", form.errors)  # Debugging step
    else:
        form = VideoForm()
    return render(request, 'video_form.html', {'form': form, 'course': course})

def video_detail(request, course_id, video_id):
    video = get_object_or_404(Video, id=video_id, course_id=course_id)
    comments = video.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video
            comment.save()
            return redirect('video-detail', course_id=course_id, video_id=video_id)
    else:
        form = CommentForm()
    return render(request, 'video_detail.html', {'video': video, 'comments': comments, 'form': form})

def edit_video(request, course_id, video_id):
    course = get_object_or_404(Course, id=course_id)
    video = get_object_or_404(Video, id=video_id, course=course)

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video-list', course_id=course.id)
    else:
        form = VideoForm(instance=video)

    return render(request, 'edit_video.html', {'form': form, 'course': course, 'video': video})

def delete_video(request, course_id, video_id):
    course = get_object_or_404(Course, id=course_id)
    video = get_object_or_404(Video, id=video_id, course=course)

    if request.method == 'POST':
        video.delete()
        messages.success(request, "Video deleted successfully.")
        return redirect('video-list', course_id=course.id)

    return render(request, 'delete_video.html', {'course': course, 'video': video})

# Access Management
def grant_course_access(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = AccessForm(request.POST)
        if form.is_valid():
            access = form.save(commit=False)
            access.course = course
            access.save()
            return redirect('course-list')
    else:
        form = AccessForm()
    return render(request, 'access.html', {'form': form, 'course': course})

# PDF Views
def pdf_list(request):
    pdfs = PDFDocument.objects.all()
    return render(request, 'pdf_list.html', {'pdfs': pdfs})

@user_passes_test(lambda u: u.is_staff)
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf-list')
    else:
        form = PDFForm()
    return render(request, 'upload_pdf.html', {'form': form})
