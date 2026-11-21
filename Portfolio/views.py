from pathlib import Path
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.http import Http404,FileResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
def owner(): return User.objects.filter(is_staff=True).order_by("id").first()
def ctx():
 u=owner()
 if not u:return {"profile":None,"skills":[],"projects":[],"experiences":[],"education_list":[]}
 return {"profile":Profile.objects.filter(user=u).first(),"skills":Skill.objects.filter(user=u),"projects":Project.objects.filter(user=u,is_published=True),"experiences":Experience.objects.filter(user=u),"education_list":Education.objects.filter(user=u),"counts":[("Skills",Skill.objects.filter(user=u).count()),("Projects",Project.objects.filter(user=u).count()),("Experience",Experience.objects.filter(user=u).count())]}
def home(request): return render(request,"Portfolio/home.html",ctx())
def about(request): return render(request,"Portfolio/about.html",ctx())
def skills(request): return render(request,"Portfolio/skills.html",ctx())
def projects(request): return render(request,"Portfolio/projects.html",ctx())
def experience(request): return render(request,"Portfolio/experience.html",ctx())
def education(request): return render(request,"Portfolio/education.html",ctx())
def resume(request): return render(request,"Portfolio/resume.html",ctx())
def register_view(request):
 f=RegistrationForm(request.POST or None)
 if request.method=="POST" and f.is_valid(): f.save(); messages.success(request,"Account created. Please log in."); return redirect("login")
 return render(request,"Portfolio/auth_form.html",{"form":f,"title":"Create account"})
def login_view(request):
 f=LoginForm(request.POST or None)
 if request.method=="POST" and f.is_valid():
  ident=f.cleaned_data["username_or_email"]
  u=User.objects.filter(email__iexact=ident).first() if "@" in ident else User.objects.filter(username__iexact=ident).first()
  user=authenticate(request,username=u.username,password=f.cleaned_data["password"]) if u else None
  if user: login(request,user); return redirect("dashboard" if user.is_staff else "home")
  f.add_error(None,"Invalid username/email or password.")
 return render(request,"Portfolio/auth_form.html",{"form":f,"title":"Login"})
@login_required
def logout_view(request):
 if request.method=="POST": logout(request)
 return redirect("home")
staff=user_passes_test(lambda u:u.is_authenticated and u.is_staff,login_url="login")
@staff
def dashboard(request):
 u=request.user
 return render(request,"Portfolio/dashboard.html",{"profile":Profile.objects.filter(user=u).first(),"skills":Skill.objects.filter(user=u),"projects":Project.objects.filter(user=u),"experiences":Experience.objects.filter(user=u),"education_list":Education.objects.filter(user=u),"counts":[("Skills",Skill.objects.filter(user=u).count()),("Projects",Project.objects.filter(user=u).count()),("Experience",Experience.objects.filter(user=u).count())]})
@staff
def profile_edit(request):
 obj=Profile.objects.filter(user=request.user).first(); f=ProfileForm(request.POST or None,request.FILES or None,instance=obj)
 if request.method=="POST" and f.is_valid(): x=f.save(commit=False);x.user=request.user;x.save();messages.success(request,"Profile saved.");return redirect("dashboard")
 return render(request,"Portfolio/form_page.html",{"form":f,"title":"Edit profile"})
def owned(model,u,pk): return get_object_or_404(model,pk=pk,user=u)
def form_view(request,cls,model,pk=None,title="Manage information"):
 obj=owned(model,request.user,pk) if pk else None; f=cls(request.POST or None,request.FILES or None,instance=obj)
 if request.method=="POST" and f.is_valid(): x=f.save(commit=False);x.user=request.user;x.save();messages.success(request,"Saved successfully.");return redirect("dashboard")
 return render(request,"Portfolio/form_page.html",{"form":f,"title":title})
@staff
def skill_add(r): return form_view(r,SkillForm,Skill,title="Add skill")
@staff
def skill_edit(r,pk): return form_view(r,SkillForm,Skill,pk,"Edit skill")
@staff
def project_add(r): return form_view(r,ProjectForm,Project,title="Add project")
@staff
def project_edit(r,pk): return form_view(r,ProjectForm,Project,pk,"Edit project")
@staff
def experience_add(r): return form_view(r,ExperienceForm,Experience,title="Add experience")
@staff
def experience_edit(r,pk): return form_view(r,ExperienceForm,Experience,pk,"Edit experience")
@staff
def education_add(r): return form_view(r,EducationForm,Education,title="Add education")
@staff
def education_edit(r,pk): return form_view(r,EducationForm,Education,pk,"Edit education")
def delete_view(r,model,pk):
 if r.method=="POST": owned(model,r.user,pk).delete();messages.success(r,"Deleted.")
 return redirect("dashboard")
@staff
def skill_delete(r,pk): return delete_view(r,Skill,pk)
@staff
def project_delete(r,pk): return delete_view(r,Project,pk)
@staff
def experience_delete(r,pk): return delete_view(r,Experience,pk)
@staff
def education_delete(r,pk): return delete_view(r,Education,pk)
@staff
def file_add(r,pk):
 p=owned(Project,r.user,pk);f=PortfolioFileForm(r.POST or None,r.FILES or None)
 if r.method=="POST" and f.is_valid():x=f.save(commit=False);x.project=p;x.save();messages.success(r,"File uploaded.");return redirect("dashboard")
 return render(r,"Portfolio/form_page.html",{"form":f,"title":"Upload project attachment","help_text":"Any extension is accepted; multiple files can be uploaded one by one."})
@staff
def file_delete(r,pk):
 f=get_object_or_404(PortfolioFile,pk=pk,project__user=r.user)
 if r.method=="POST":f.delete()
 return redirect("dashboard")

def download_file(request,pk):
 item=get_object_or_404(PortfolioFile,pk=pk,project__is_published=True)
 if not item.uploaded_file: raise Http404
 response=FileResponse(item.uploaded_file.open("rb"),as_attachment=True,filename=Path(item.uploaded_file.name).name)
 response["X-Content-Type-Options"]="nosniff"
 return response
