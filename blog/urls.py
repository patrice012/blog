
from django.urls import path

from blog import  views 


app_name = 'blog'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('create/', views.CreatePost.as_view(), name='create'),
    path('blog/', views.post_list, name='post_list'),
    path('about/', views.about, name='about'),
    path('posts/tags/<str:tag>', views.post_by_tag, name='post_by_tag'),
    path('update/<slug:slug>/<int:id>/', views.UpdatePost.as_view(), name='update_post'),
    path('delete/<slug:slug>/<int:id>/', views.delete_post, name='delete_post'),
    path('<slug:slug>/<int:id>/', views.post_detail, name = 'post_detail'),

    path('search/', views.search_view, name='search_view'),
    path('subscribe/', views.subscription, name='subscription')
]