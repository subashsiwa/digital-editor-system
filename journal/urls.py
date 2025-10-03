from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),  # или auth_views.LogoutView.as_view()
    path('dashboard/', views.dashboard, name='dashboard'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articles/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('articles/<int:article_id>/status/<str:new_status>/', views.change_article_status, name='change_article_status'),
    path('articles/<int:article_id>/comment/', views.add_comment, name='add_comment'),
]