"""
Views from the user API
"""
from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.urls import resolve
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from user.serializers import AuthTokenSerializer, UserSerializer
from user.forms import UserForm
from .models import User
from .utils import send_verification_email
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

class HttpResponseNoContent(HttpResponse):
    status_code = 204

def loginUser(request):
	if request.user.is_authenticated:
		messages.warning(request, 'You are already logged in!')
		return HttpResponseNoContent()
	elif request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']

		user = auth.authenticate(email=email, password=password)

		if user is not None:
			auth.login(request,user)
			messages.success(request,'You are now logged in')
			return redirect('quotation:list')
		else:
			messages.error(request,'Invalid login credentials')
			return redirect('user:loginUser')
	context ={
	}
	return render(request,'user/login.html',context=context)

@login_required(login_url='user:loginUser')
def logoutUser(request):
	auth.logout(request)
	messages.info(request,'You are logged out.')
	return redirect('user:loginUser')

def registerUser(request):
	if request.user.is_authenticated:
		messages.warning(request, 'You are already logged in!')
	elif request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			user = form.save(commit=False)
			user.set_password(password)
			user.email = email
			user.save()
			send_verification_email(request,user)
			messages.success(request,"Your account has been registerd successfully!")
			return redirect('user:loginUser')
	else:
		form = UserForm()
	context ={
		'form':form
	}
	return render(request,'user/register.html',context=context)

def activate(request,uidb64,token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = User._default_manager.get(pk=uid)
	except(TypeError,ValueError,OverflowError,User.DoesNotExist):
		user = None

	if user is not None and default_token_generator.check_token(token):
		user.is_active = True
		user.save()
		messages.success(request,'Congratulations Your account is activated.')
		return redirect('user:loginUser')
	else:
		messages.error(request,'Invalid activation link')
		return redirect('user:loginUser')


def forgot_password(request):
	return render(request,'user/forgot_password.html')

def reset_password_validate(request,uidb64,token):
	return

def reset_password(request):
	return render(request,'user/reset_password.html')

class CreateUserView(generics.CreateAPIView):
	"""Create a new user in the system"""

	serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
	"""Create a new auth token for user"""

	serializer_class = AuthTokenSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
	"""Manage the authenticated user."""

	serializer_class = UserSerializer
	authentication_classes = [authentication.TokenAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		""""Retrieve and return the authenticated user."""
		return self.request.user