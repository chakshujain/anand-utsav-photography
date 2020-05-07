from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *

# Create your views here.


def uploadImage(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            for field in request.FILES.keys():
                for formfile in request.FILES.getlist(field):
                    img = Image(image=formfile)
                    img.save()
            return redirect('success')
    else:
        form = UploadFileForm()
    return render(request, 'upload-image.html', {'form': form})


def success(request):
    return HttpResponse('successfully uploaded')


def displayImages(request):
    if request.method == 'GET':
        images = Image.objects.all()
        return render(request, 'display-images.html', {'images': images})
