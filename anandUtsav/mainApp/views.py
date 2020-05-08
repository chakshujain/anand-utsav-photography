from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .forms import *
from .models import Image
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import user_passes_test, login_required
from .utils import resizeImage
# Create your views here.

def isSuperUser(user):
    return user.is_superuser

def home(request):
    return render(request, 'home.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print("logged in")
            if(user.is_superuser):
                return redirect('/new-user')
            else:
                usr = User.objects.get(id=user.id)
                return redirect('/images')
        return render(request, 'login.html', {'error': "Invalid Username or password"})
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
@user_passes_test(isSuperUser, login_url="/login")
def createNewUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        checked = 'superuser' in request.POST
        user = User.objects.create_user(
            username=username, password=password)
        if(checked):
            user.is_superuser = True
        else:
            user.is_superuser = False
        user.save()
        return redirect('/new-user')
    else:
        users = User.objects.all()
        return render(request, 'new-user.html', {'users': users})


@login_required(login_url='/login')
@user_passes_test(isSuperUser, login_url="/login")
def uploadImage(request, userId):
    user = User.objects.get(id=userId)
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for field in request.FILES.keys():
                for formfile in request.FILES.getlist(field):
                    print("formfie", formfile)
                    
                    img = Image(file_name=formfile.name,
                                image=formfile, user=user, className="")
                    img.save()
            form = UploadFileForm()
            return render(request, 'upload-image.html', {'user': user, 'form': form})

    form = UploadFileForm()
    if request.method == "GET":
        return render(request, 'upload-image.html', {'user': user, 'form': form})
    
    
    


@login_required(login_url='/login')
def displayImages(request):
    images = Image.objects.filter(user=request.user).order_by('id')
    
    if request.method == 'POST':
        for image in images:
            try:
                image.className = str(request.GET[str(image.id)]) 
            except Exception as e:
                print("Exception in displayImages", e)
                image.className = ""
            finally:
                image.save() 
    
    return render(request, 'display-images.html', {'images': images})