from django.db import models
from django.conf import settings
from .utils import resizeImage
# Create your models here.

class Image(models.Model):
    def save(self, *args, **kwargs):
        super().save()
        self.width, self.height = resizeImage(self.image.path)
        super().save()

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='images')
    file_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    className = models.CharField(max_length=50, blank=True)
    width = models.CharField(max_length=5, blank=True)
    height = models.CharField(max_length=5, blank=True)


class BlogPost(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100)
    published_date = models.DateField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content_des = models.CharField(max_length=500)
    content_main = models.TextField(max_length=5000)
            

class Gallery(models.Model):
    image = models.ImageField(upload_to = 'media/')
    text = models.TextField(null=True, blank=True)
    