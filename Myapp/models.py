from django.db import models
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericRelation
from autoslug import AutoSlugField


# Create your models here.
class UserProfile(models.Model):
    face_id = models.OneToOneField(User, on_delete=models.CASCADE)
 
    address = models.CharField(max_length = 100)
   
    phone = models.CharField(max_length =  11)
  
  
    image=models.ImageField(upload_to='profile_image')
    

    def __str__(self) -> str:
        return f'{self.face_id}'
    
class Course(models.Model):
    course_title = models.CharField(max_length=50)
    course_code = models.CharField(max_length=20)
    course_unit = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.course_title}'
    
class Registration(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course)

    def __str__(self) -> str:
        return f'{self.username}'
