from django.urls import path
from blogs import views


app_name = 'blogs'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='home'),
    path('post_create/', views.BlogCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/detail/', views.BlogDetailView.as_view(), name='detail'),
    path('post/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='update'),
    path('post/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='delete'),
    path('my-blogs/', views.BlogSortMyBlogsView.as_view(), name='my-blogs')
]
