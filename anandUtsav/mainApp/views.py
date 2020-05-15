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
    return render(request, 'index.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print("logged in")
            return redirect('/services')

        return render(request, 'services.html', {'error': "Invalid Username or password"})
    return render(request, 'services.html')


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
    
    return redirect('/services')
        


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
    

def superUserServices(request):
    context = {'servicesClass' : 'active'}
    users = User.objects.all()
    return render(request, 'new-user.html', {'users': users})


def endUserServices(request):
    context = {'servicesClass' : 'active'}
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

    rows = []
    row = []
    for i in range(0, len(images)):
        if (i+1) % 3 == 0:
            rows.append(row)
            row = []
        row.append(images[i])
    
    if len(row):
        rows.append(row)

         
    return render(request, 'display-images.html', {'row': rows})


def services(request):
    if request.user.is_superuser:
        return superUserServices(request)
    if request.user.is_authenticated:
        return endUserServices(request)

    context = {'servicesClass' : 'active'}
    return render(request, 'services.html', context)






def about(request):
    context = {'aboutClass' : 'active'}
    return render(request, 'about.html', context)

def contact(request):
    context = {'contactClass' : 'active'}
    return render(request, 'contact.html', context)

def blog(request):
    context = {'blogClass' : 'active'}
    return render(request, 'blog.html', context)

def gallery(request):
    context = {'galleryClass' : 'active'}
    return render(request, 'gallery.html', context)


