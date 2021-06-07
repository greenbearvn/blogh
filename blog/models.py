from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify # new
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to ='poster/')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1,related_name='posts')
    post_views=models.IntegerField(default=0,blank=True)
    slug = models.SlugField(null=False, unique=True)
    date = models.DateTimeField(auto_now_add = True)
    published = models.BooleanField(default=1)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    status = models.CharField(max_length=10, choices=options, default='published')
    tags = TaggableManager()
    
    
    
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', args=[self.slug])

    