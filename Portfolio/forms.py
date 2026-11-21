from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *
class CrispyMixin:
 def init_crispy(self,label="Save"):
  self.helper=FormHelper(); self.helper.form_method="post"; self.helper.add_input(Submit("submit",label,css_class="btn btn-primary"))
class RegistrationForm(UserCreationForm):
 email=forms.EmailField()
 class Meta: model=User; fields=("username","email","password1","password2")
 def __init__(self,*a,**kw):
  super().__init__(*a,**kw); self.init_crispy("Create account")
 def clean_email(self):
  v=self.cleaned_data["email"].lower()
  if User.objects.filter(email__iexact=v).exists(): raise forms.ValidationError("Email already registered.")
  return v
class LoginForm(forms.Form):
 username_or_email=forms.CharField(label="Username or Email"); password=forms.CharField(widget=forms.PasswordInput)
 def __init__(self,*a,**kw): super().__init__(*a,**kw); self.init_crispy("Login")
class ProfileForm(forms.ModelForm):
 class Meta: model=Profile; exclude=("user",)
 def __init__(self,*a,**kw): super().__init__(*a,**kw); self.init_crispy()
class SkillForm(forms.ModelForm):
 class Meta: model=Skill; exclude=("user",)
 def __init__(self,*a,**kw): super().__init__(*a,**kw); self.init_crispy()
class ProjectForm(forms.ModelForm):
 class Meta: model=Project; exclude=("user","created_at")
 def __init__(self,*a,**kw): super().__init__(*a,**kw); self.init_crispy()
class PortfolioFileForm(forms.ModelForm):
 class Meta: model=PortfolioFile; fields=("uploaded_file","display_name")
 def __init__(self,*a,**kw): super().__init__(*a,**kw); self.init_crispy("Upload file")
class ExperienceForm(forms.ModelForm):
 class Meta:
  model=Experience; exclude=("user",)
  widgets={"start_date":forms.DateInput(attrs={"type":"date"}),"end_date":forms.DateInput(attrs={"type":"date"})}
 def __init__(self,*a,**kw): super().__init__(*a,**kw); self.init_crispy()
class EducationForm(forms.ModelForm):
 class Meta: model=Education; exclude=("user",)
 def __init__(self,*a,**kw): super().__init__(*a,**kw); self.init_crispy()
