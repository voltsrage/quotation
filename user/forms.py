from django import forms
from .models import User

class UserForm(forms.ModelForm):
		email =  forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Please enter your email address'}))
		name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Please enter your full name'}))
		username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Please enter your username'}))
		password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Please enter your password'}))
		confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Please confirm your password'}))
		class Meta:
				model = User
				fields = ['email','name','username','password','confirm_password','role']


		def clean(self):
				cleaned_data = super(UserForm,self).clean()
				password = cleaned_data.get('password')
				confirm_password = cleaned_data.get('confirm_password')

				if password != confirm_password:
					raise forms.ValidationError(
						"Password does not match!"
					)