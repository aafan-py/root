from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('myProfile/', views.my_profile, name='myProfile'),
    path('updateProfile/', views.update_profile, name='updateProfile'),
    path('changePassword/', views.change_password, name='changePassword'),
    path('forgotPassword/', views.forgot_password, name='forgotPassword'),
    path('resetPasswordValidate/<uidb64>/<token>/', views.reset_password_validate, name='resetPasswordValidate'),
    path('resetPassword/', views.reset_password, name='resetPassword'),
]
