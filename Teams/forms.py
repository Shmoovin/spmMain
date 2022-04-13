from django import forms

'''This file contains all of the forms for the group app'''

'''This class defines the fields for the JoinGroup form'''
class JoinGroup(forms.Form):
    name = forms.CharField(label='Team Name', max_length=100)
    pswd = forms.CharField(label='Team Password', max_length=15)



