from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Video,PDFDocument
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .forms import VideoForm, PDFForm, VideoAvailabilityForm
from django.contrib.admin.views.decorators import staff_member_required


User = get_user_model()

def about(request):
    return render(request, 'about.html')

def home(request):
    message = request.session.pop('message', None)  # Retrieve and remove the message from session
    context = {'message': message}
    return render(request, 'home.html', context)

def video_list(request):
    videos = Video.objects.all()
    videos = Video.objects.all()

    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        video = get_object_or_404(Video, id=video_id)
        form = VideoAvailabilityForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video-list')
    if len(videos) == 0:
        message = "There are no videos"
        return render(request, 'video_list.html', {'videos': videos,'message':message})
    return render(request, 'video_list.html', {'videos': videos})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password, or user doesnt exist'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    

@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')


@staff_member_required
def create_student(request):
    if request.method == 'POST' and request.user.is_staff:
        login = request.POST.get('login')
        password = request.POST.get('password')

        user = User.objects.create_user(username=login,email=None, password=password,subpassword = password)
        user.save()
        
        message = f"Login: {login}\nPassword: {password}\nUser created successfully"
        request.session['message'] = message  # Store the message in session
        return redirect('home')  # Redirect to the home page
    else:
        alert = "You don't have access to this feature"
        context = {'alert': alert}
        return render(request, 'create_user.html', context)


@staff_member_required
def show_users(request):
    q = request.GET.get('q', '')
    
    users = User.objects.filter(
        Q(username__icontains=q) | Q(email__icontains=q)
    )
    
    context = {'users': users}
    return render(request, 'show_users.html', context)

@staff_member_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.cleaned_data['video_file']
            
            
            form.save()
            return redirect('video-list')
    else:
        form = VideoForm()
    context = {'form': form}
    return render(request, 'video_form.html', context)

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf-list')
    else:
        form = PDFForm()
    return render(request,'upload_pdf.html',{'form':form})

def pdf_list(request):
    pdfs = PDFDocument.objects.all()
    return render(request, 'pdf_list.html', {'pdfs': pdfs})