from django import forms
from .models import *

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate

from django.conf import settings










class StudentsSearchForm(forms.ModelForm):
	
	StudentName = forms.CharField(
		required=False,
	#label=False,
		widget=forms.TextInput(attrs={'id' :'StudentName', 'placeholder' : 'Enter Student Name'})

	)
	export_to_CSV = forms.BooleanField(required=False)
	#start_date = forms.DateTimeField(required=False)
	#end_date = forms.DateTimeField(required=False)


	class Meta:
		model = Students
		fields =['Class', 'StudentName']



class ReceiveStudentFeeeForm(forms.ModelForm):
	# is_received = forms.BooleanField(
	# 	required=True,
	# #label=False,
		

	# )
	ReceivedAmount = forms.IntegerField(
		required=True,
	)
	
	

	class Meta:
		model = Students
		fields =['ReceivedAmount','ReceivedBy']





class StudentCreateForm(forms.ModelForm):
	


	class Meta:
		model = Students
		fields =[
			
			'Class', 
			'StudentName', 
			'ParentNumber', 
			'StudentImage',
			'Gender',
			'StudentLocation'

			
			#'time_stamp',
			#'last_updated'


			]

	def clean_Class(self):
		Class = self.cleaned_data.get('Class')
		if not Class:
			raise forms.ValidationError('Please enter Student class')
		#for instance in Stock.objects.all():
			#if instance.category == category:
				#raise forms.ValidationError(category + 'is already created')

		return Class
	def clean_StudentName(self):
		StudentName = self.cleaned_data.get('StudentName')
		if not StudentName:
			raise forms.ValidationError('Please enter Student Name')
		#for instance in Stock.objects.all():
			#if instance.item_name == item_name:
				#raise forms.ValidationError(item_name + ' is already created')
		return StudentName