from django.urls import path
from . import views

urlpatterns = [
    path('', views.ForumHome, name='forum'),
    path('posts/<int:pk>', views.ForumPosts, name='posts'),
    path('posts', views.ForumPostsGeneral, name='general_posts'),
    path('createpost', views.CreatePost, name='createpost'),
    path('post-detail/<int:pk>', views.PostDetail, name='post-detail'),
    path('post-change-status<int:post_id>', views.PostChangeStatus, name='change-status')
]