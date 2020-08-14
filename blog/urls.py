from django.urls import path
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', views.home, name = 'home'),

    path('news/', PostListView.as_view(template_name = 'blog/news.html',
    							  context_object_name = 'posts', 
    							  ordering = '-date_posted'),  name = 'news'),
    path('news/<int:pk>/', PostDetailView.as_view(), name = 'news-detail'),
    path('news/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
	path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]
