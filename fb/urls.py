from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('about/', views.About.as_view(), name='about'),
    path('contact/', views.Contact.as_view(), name='contact'),

    path('mypost/', views.MyPostListView.as_view(), name='mypost_list'),
    path('mypost/detail/<int:pk>/', views.MyPostDetailView.as_view(), name='mypost_detail'),
    path('mypost/update/<int:pk>/', views.MyPostUpdateView.as_view(success_url='/fb/mypost/'), name='mypost_update'),
    path('mypost/delete/<int:pk>/', views.MyPostDeleteView.as_view(success_url='/fb/mypost/'), name='mypost_delete'),
    path('mypost/create/', views.MyPostCreateView.as_view(success_url='/fb/mypost/'), name='mypost_create'),
     path('mypost/like/<int:pk>/', views.postLike, name='like'),
     path('mypost/comment/<int:pk>/', views.postComment, name='comment'),
     path('mypost/viewcomment/<int:pk>/', views.viewcomments, name='view_comment'),
    path('mypost/unlike/<int:pk>/', views.postUnlike, name='unlike'),

    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile_list'),
    path('myprofile/detail/<int:pk>/', views.MyProfileDetailView.as_view(), name='myprofile_detail'),
    path('myprofile/update/<int:pk>/',views.MyProfileUpdateView.as_view(success_url='/fb/myprofile/'), name='myprofile_update'),
    path('myprofile/follow/<int:pk>/', views.follow, name='follow'),
    path('myprofile/unfollow/<int:pk>/', views.unfollow, name='unfollow'),
    path('', RedirectView.as_view(url='home/')),
]
