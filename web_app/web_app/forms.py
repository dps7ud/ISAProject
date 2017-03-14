from django import forms

class SignUpForm(forms.Form):
	first_name = forms.CharField(label='First name', max_length=100)
	last_name = forms.CharField(label='Last name', max_length=100)
	location = forms.CharField(label='Location', max_length=100)
	email = forms.CharField(label='Email', max_length=100)
	bio = forms.CharField(label='Bio', max_length=100)
	pw = forms.CharField(label='Password', max_length=100)
