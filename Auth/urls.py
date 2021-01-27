from django.urls import path
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('', views.home,name='home'),
    path('profile/', views.userSettings, name='profile'),
    path('activity/', views.userInfo, name='activity'),
    path('product/', views.product, name='product'),
    #******************Authentication**************************
    path('login/', views.userLogin, name='login'),
    path('register/', views.userRegister, name='register'),
    path('logout/', views.userLogout, name='logout'),

    #************Forgot password***************************
    path('reset_password/', authViews.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', authViews.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', authViews.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_done.html"), name="password_reset_complete"),

    #**************Email confirmation*************************
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    #**************Change Password*****************************
    path('password_change/', authViews.PasswordChangeView.as_view(
        template_name="accounts/password_change.html"), name="password_change"),
    path('password_change_done/', authViews.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"), name="password_change_done"),

    #**********************************************
    
]
