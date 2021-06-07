
from django.urls import path
from blog.views import detail_view,PostListView,TagHomeView,CatListView,SearchResultsView,contact


urlpatterns = [
    path('',PostListView.as_view(),name='home'),
    path('<slug:post>/',detail_view,name='detail'),
    path('category/<category>/', CatListView.as_view(), name='category'),
    path('post/tags/<slug:tag_slug>/',TagHomeView.as_view(),name = 'posts_by_tag'),
    path('post/search/',SearchResultsView.as_view(),name='search_results'),
    path('post/contact/',contact,name='contact'),
]
