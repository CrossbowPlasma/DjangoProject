from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('changepassword/', views.change_password, name='change_password'),
    path('switchuser/', views.switch_user, name='switch_user'),
    path('restoreuser/<str:uname>/<str:upass>', views.restore_user, name='restore_user'),
     path('logout-and-redirect/<str:redirect_url>/', views.logout_and_redirect, name='logout_and_redirect'),
]