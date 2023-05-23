from django.contrib import admin
from .models import *

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'phoneVisibility', 'isAuthenticated')
    list_display_links = ('id', 'name')
    readonly_fields = ('id', 'date_joined', 'last_login')
    search_fields = ('name', 'location', 'role', 'phoneVisibility')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class BasicInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'branch', 'joiningYear', 'passingYear', 'rollNo')
    list_display_links = ('id', 'user')

class FacultyInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'jobTitle', 'Department', 'joinYear', 'leftYear')
    list_display_links = ('id', 'user')

class AboutMeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    search_fields = ('user', )
    list_per_page = 50

class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'instituteName', 'joinYear', 'passYear', 'degree', 'department')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'degree', 'department', 'joinYear', 'passYear')
    list_per_page = 50

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'facebook', 'instagram', 'linkedin', 'twitter')
    list_per_page = 50

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'workTitle', 'companyName', 'workIndustry')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'workTitle', 'companyName', 'workIndustry')
    list_per_page = 50

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'date')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'email', 'date')
    list_per_page = 25

class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'jobTitle', 'companyName', 'location', 'skills', 'postedOn')
    list_display_links = ('id', 'user')
    search_fields = ('id', 'user', 'jobTitle', 'companyName', 'location', 'skills', 'postedOn')
    list_per_page = 25

admin.site.register(Account, AccountAdmin)
admin.site.register(BasicInformation, BasicInformationAdmin)
admin.site.register(FacultyInformation, FacultyInformationAdmin)
admin.site.register(AboutMe, AboutMeAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(JobOpening, JobOpeningAdmin)
