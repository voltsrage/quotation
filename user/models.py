import os
# Create your models here.
import uuid

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
	"""Manager for users"""

	def create_user(self,email,username=None, password=None, **extra_fields):
		"""Create, save and return a new user."""
		if not email:
			raise ValueError('User must have an email address.')
		if not username:
			raise ValueError('User must have an username.')
		user = self.model(email=self.normalize_email(email), **extra_fields)
		#hashes password

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,email,username, password):
		"""Create, save and return a new superuser."""
		user = self.create_user(email,username, password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser,PermissionsMixin):
	"""User in the system"""
	ADMIN = 1
	SHRIMP = 2
	SALMON = 3
	SCALLOP = 4
	HALIBUT = 5
	GUEST = 6

	ROLE_CHOICE = (
		(ADMIN,'Admin'),
		(SHRIMP,'Shrimp'),
		(SALMON,'Salmon'),
		(SCALLOP,'Scallop'),
		(HALIBUT,'Halibut'),
		(GUEST,'Guest'),
	)

	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255, unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_superadmin = models.BooleanField(default=False)
	role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True, null=True)

	date_joined = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True,blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date= models.DateTimeField(auto_now=True)

	objects = UserManager()
	#since default username is username
	#To use email instead, you have to set it here
	USERNAME_FIELD = 'email'

	def __str__(self):
		return self.email

	def has_perrm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label) :
		return True