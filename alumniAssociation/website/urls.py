from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # Home url
    path('', views.home, name="home"),
    # Authentication urls
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('signout/', views.signout, name="signout"),
    # Profile urls
    path('profile/', views.profile, name="profile"),
    path('editProfile/', views.editProfile, name="editProfile"),
    # Basic Information urls
    path('addBasicInformation/', views.addBasicInformation, name="addBasicInformation"),
    path('editBasicInformation/<int:basicInfo_id>/', views.editBasicInformation, name="editBasicInformation"),
    # Faculty Information urls
    path('addFacultyInformation/', views.addFacultyInformation, name="addFacultyInformation"),
    path('editFacultyInformation/<int:facultyInfo_id>/', views.editFacultyInformation, name="editFacultyInformation"),
    # Alumni Directory urls
    path('alumniDirectory/', views.alumniDirectory, name="alumniDirectory"),
    path('user/detail/<str:name>/', views.userDetail, name='userDetail'),
    # Social Media urls
    path('addSocialMedia/', views.addSocialMedia, name="addSocialMedia"),
    path('editSocialMedia/<int:socialMedia_id>/', views.editSocialMedia, name="editSocialMedia"),
    # Education urls
    path('editEducation/<int:edu_id>/', views.editEducation, name="editEducation"),
    path('deleteEducation/<int:edu_id>/', views.deleteEducation, name="deleteEducation"),
    # About Me urls
    path('addAboutMe/', views.addAboutMe, name="addAboutMe"),
    path('editAboutMe/<int:about_id>/', views.editAboutMe, name="editAboutMe"),
    # Work Experience urls
    path('addWorkExperience/', views.addWorkExperience, name="addWorkExperience"),
    path('editWorkExperience/<int:workExperienceId>/', views.editWorkExperience, name="editWorkExperience"),
    path('deleteWorkExperience/<int:workExperienceId>/', views.deleteWorkExperience, name="deleteWorkExperience"),
    # Job Openings urls
    path('addJobOpenings/', views.addJobOpenings, name="addJobOpenings"),
    path('deleteJobOpening/<int:job_id>/', views.deleteJobOpening, name="deleteJobOpening"),
    path('jobOpenings/', views.jobOpenings, name="jobOpenings"),
    path('jobDetail/<int:id>/', views.jobDetail, name="jobDetail"),
    # Password change urls
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password/password_change_done.html'), name='password_change_done'),
    # Password reset urls
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html', html_email_template_name='password/password_reset_email.html', subject_template_name='password/password_reset_subject.txt'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
]
