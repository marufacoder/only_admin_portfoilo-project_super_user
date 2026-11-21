from django.contrib import admin
from .models import *
class AttachmentInline(admin.TabularInline):
 model=PortfolioFile; extra=1
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
 list_display=("title","user","is_published"); search_fields=("title","technology_used"); inlines=[AttachmentInline]
for m in (Profile,Skill,PortfolioFile,Experience,Education): admin.site.register(m)
