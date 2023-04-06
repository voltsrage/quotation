"""
URL mappings for the user API
"""

from django.urls import path

from user import views

app_name='user'

urlpatterns = [
	path('create/',views.CreateUserView.as_view(), name='create'),
	path('token/',views.CreateTokenView.as_view(), name='token'),
	path('profile/',views.ManageUserView.as_view(), name='profile'),
  path('register/',views.registerUser, name='registerUser'),
  path('login/',views.loginUser, name='loginUser'),
  path('logout/',views.logoutUser, name='logoutUser'),
  path('activate/<uidb64>/<token>',views.activate, name='activateUser'),
  path('forgot_password/',views.forgot_password, name='forgot_password'),
  path('reset_password_validate/<uidb64>/<token>',views.reset_password_validate, name='reset_password_validate'),
  path('reset_password/',views.reset_password, name='reset_password'),
]