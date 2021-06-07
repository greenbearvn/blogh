from django.shortcuts import render , redirect, reverse,get_object_or_404,HttpResponseRedirect
from django.views.generic import ListView, DetailView,TemplateView
from .models import Post,  Category
from django.db.models import Q
from taggit.models import Tag 
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import datetime
import random


class PostListView(ListView):
    model = Post
    template_name = 'main/home.html'
    context_object_name = 'posts'
    ordering = ['-id']


    def get_context_data(self, **kwargs):
        period = timezone.now() - datetime.timedelta(days=7)
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update({
        'most_view7day':Post.objects.filter(date__gte=period).order_by('-post_views'),
        'recent_post':random.sample(list(Post.objects.all()),2),# random goi y post
        'random_post':random.sample(list(Post.objects.all()),1)[0],
        'categories':Category.objects.all()[:5],# hiên thi danh muc
        'most_tags':Post.tags.most_common()[:10]# hiên thi cac tag nhieu luot truy cap
        })
        return context


def detail_view(request,  post ):
    
    post = get_object_or_404(Post, slug=post,status='published')
    

    post_related = post.tags.similar_objects()
    next_post = Post.objects.filter(slug__gt=post).order_by('id').first()
    previous_post = Post.objects.filter(slug__lt=post).order_by('id').last()
    
    
    post_object=Post.objects.get(id=post.id)
    post_object.post_views=post_object.post_views+1
    post_object.save()
    
        
    return render(request, 'main/detail.html', {
        'object':post,
        "post_related":post_related,
        "next_post":next_post,
        "previous_post":previous_post
    })

class Contact(TemplateView):
    template_name = 'main/contact.html'

class SearchResultsView(ListView):
    model = Post
    template_name = 'main/search_results.html'
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) |  Q(body__icontains=query)  
        )
        
        return object_list


class TagMiXin(object):
        def get_context_data(self,**kwargs):
            context = super(TagMiXin,self).get_context_data(**kwargs)
            context['tags'] = Tag.objects.all()
            return context
        

class TagHomeView(TagMiXin,ListView):
    model = Post
    template_name = 'main/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__slug = self.kwargs.get('tag_slug'))[:3]

class CatListView(ListView):
    template_name = 'main/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published'),
            'count': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published').count()
        }
        return content

def error_404_view(request, exception):
    return render(request,'main/404.html')

def contact(request):
    
    if request.method == 'POST':
        
        message = request.POST['message']

        send_mail('Contact form', 
        
        message,
        settings.EMAIL_HOST_USER,
        ['hungvu2352002@gmail.com'],
        fail_silently=False
        )
       
    return render(request,"main/contact.html",{ })