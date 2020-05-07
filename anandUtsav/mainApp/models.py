from django.db import models
from django.conf import settings
# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='images')
    file_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
