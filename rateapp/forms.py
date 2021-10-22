from django import forms
from .models import Project,Profile, Review

class NewProjectForm(forms.ModelForm):
  live_site = forms.CharField()
  class Meta:
    model = Project
    fields = ("title", "description", "img", "live_site",)
    exclude = ['publish_date']

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ['user']

class ReviewForm(forms.ModelForm):
  class Meta:
    model = Review
    exclude = ['average','project', 'user']