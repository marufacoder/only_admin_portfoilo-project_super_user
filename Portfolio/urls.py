from django.urls import path
from . import views as v
urlpatterns=[
 path("",v.home,name="home"),path("about/",v.about,name="about"),path("skills/",v.skills,name="skills"),path("projects/",v.projects,name="projects"),path("experience/",v.experience,name="experience"),path("education/",v.education,name="education"),path("resume/",v.resume,name="resume"),path("file/<int:pk>/download/",v.download_file,name="download_file"),
 path("register/",v.register_view,name="register"),path("login/",v.login_view,name="login"),path("logout/",v.logout_view,name="logout"),path("dashboard/",v.dashboard,name="dashboard"),path("dashboard/profile/",v.profile_edit,name="profile_edit"),
 path("dashboard/skill/add/",v.skill_add,name="skill_add"),path("dashboard/skill/<int:pk>/edit/",v.skill_edit,name="skill_edit"),path("dashboard/skill/<int:pk>/delete/",v.skill_delete,name="skill_delete"),
 path("dashboard/project/add/",v.project_add,name="project_add"),path("dashboard/project/<int:pk>/edit/",v.project_edit,name="project_edit"),path("dashboard/project/<int:pk>/delete/",v.project_delete,name="project_delete"),path("dashboard/project/<int:pk>/file/add/",v.file_add,name="file_add"),path("dashboard/file/<int:pk>/delete/",v.file_delete,name="file_delete"),
 path("dashboard/experience/add/",v.experience_add,name="experience_add"),path("dashboard/experience/<int:pk>/edit/",v.experience_edit,name="experience_edit"),path("dashboard/experience/<int:pk>/delete/",v.experience_delete,name="experience_delete"),
 path("dashboard/education/add/",v.education_add,name="education_add"),path("dashboard/education/<int:pk>/edit/",v.education_edit,name="education_edit"),path("dashboard/education/<int:pk>/delete/",v.education_delete,name="education_delete")]
