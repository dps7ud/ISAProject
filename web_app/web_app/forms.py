from django import forms

class SignUpForm(forms.Form):
	username = forms.CharField(label='Username', max_length=100)
	fname = forms.CharField(label='First name', max_length=100)
	lname = forms.CharField(label='Last name', max_length=100)
	location = forms.CharField(label='Location', max_length=100)
	email = forms.CharField(label='Email', max_length=100)
	bio = forms.CharField(label='Bio', max_length=100)
	pw = forms.CharField(label='Password', max_length=100)

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=100)
	pw = forms.CharField(label='Password', max_length=100)

class CreateListingForm(forms.Form):
	title = forms.CharField(label='Title', max_length=200)
	description = forms.CharField(label='description', max_length=200)
	location = forms.CharField(label='location', max_length=200)
	status = forms.CharField(label='Status', max_length=25)
	remote = forms.CharField(label='remote', max_length=25)
	time = forms.CharField(label='time', max_length=200)
	pricing_type = forms.CharField(label='pricing_type', max_length=25)
	pricing_info = forms.FloatField(label='pricing_info')
