from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html')


def loginUser(request):
    if request.method == 'POST':
        print("inside post")
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print("logged in")
            if(user.is_superuser):
                return redirect('/new-user')
            elif(user.is_superuser == False):
                usr = User.objects.get(id=user.id)
                return render(request, 'upload-image.html', {'mainuser': request.user, 'user': usr})
        else:
            return render(request, 'login.html', {'error': "Invalid Username or password"})
    return render(request, 'login.html')


@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def createNewUser(request):
    if(request.user.is_superuser):
        if request.method == 'POST':
            print(request.POST)
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
            userquerry = User.objects.all()
            return render(request, 'new-user.html', {'users': userquerry})
    else:
        return render(request, 'new-user.html', {'premissionError': 'PermissionError'})
    return render(request, 'new-user.html')


@login_required(login_url='/login')
def uploadImage(request, userid):
    usr = User.objects.get(id=userid)
    if(request.user.is_superuser):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            print(request.FILES)
            if form.is_valid():
                for field in request.FILES.keys():
                    for formfile in request.FILES.getlist(field):
                        img = Image(file_name=formfile.name,
                                    image=formfile, user=usr)
                        img.save()
                form = UploadFileForm()
                return render(request, 'upload-image.html', {'user': usr, 'form': form, 'mainuser': request.user})
        else:
            form = UploadFileForm()
            return render(request, 'upload-image.html', {'user': usr, 'form': form, 'mainuser': request.user})
    else:
        return render(request, 'upload-image.html', {'user': usr, 'mainuser': request.user})
    return render(request, 'upload-image.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')


@login_required(login_url='/login')
def displayImages(request):
    if request.method == 'GET':
        images = Image.objects.all()
        return render(request, 'display-images.html', {'images': images})
