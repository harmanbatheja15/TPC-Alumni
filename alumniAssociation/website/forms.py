from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import *

# Authentication Forms
class RegistrationForm(UserCreationForm):

    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    role_choices = (
        ('Alumni', 'Alumni'),
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
    )

    maritalStatus_choices = (
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried'),
        ('Other', 'Other'),
    )

    phoneVisibility_choices = (
        ('Private', 'Private'),
        ('Public', 'Public'),
    )

    name = forms.CharField(label="Full Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=100, help_text="Required, Enter a valid email address!", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label="Role", choices=role_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label="Gender", choices=gender_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    maritalStatus = forms.ChoiceField(label="Marital Status", choices=maritalStatus_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.CharField(label="Current Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Phone Number (enter country code)", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'eg. +919999999999'}))
    phoneVisibility = forms.ChoiceField(label="Phone Number Visibility", choices=phoneVisibility_choices, widget=forms.RadioSelect())

    class Meta:
        model = Account
        fields = ('name', 'email', 'password1', 'password2', 'role', 'gender', 'maritalStatus', 'location', 'phone', 'phoneVisibility')

class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login")

class UserUpdateForm(forms.ModelForm):

    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    role_choices = (
        ('Alumni', 'Alumni'),
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
    )

    maritalStatus_choices = (
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried'),
        ('Other', 'Other'),
    )

    phoneVisibility_choices = (
        ('Private', 'Private'),
        ('Public', 'Public'),
    )

    name = forms.CharField(label="Full Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=100, help_text="Required, Enter a valid email address!", widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label="Role", choices=role_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label="Gender", choices=gender_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    maritalStatus = forms.ChoiceField(label="Marital Status", choices=maritalStatus_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.CharField(label="Current Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Phone Number (enter country code)", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'eg. +919999999999'}))
    phoneVisibility = forms.ChoiceField(label="Phone Number Visibility", choices=phoneVisibility_choices, widget=forms.RadioSelect())
    
    class Meta:
        model = Account
        fields = ['name', 'email', 'role', 'gender', 'maritalStatus', 'location', 'phone', 'phoneVisibility']

# Basic Information Forms
class AddBasicInformationForm(forms.ModelForm):

    branch_choices = (
        ('Computer Sci. & Engg.', 'Computer Sci. & Engg.'),
        ('Mechanical Engg.', 'Mechanical Engg.'),
        ('Architectural Asst.', 'Architectural Asst.'),
        ('Civil Engg.', 'Civil Engg.'),
        ('Electrical Engg.', 'Electrical Engg.'),
    )

    course = forms.CharField(label="Course", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': 'Diploma'}))
    branch = forms.ChoiceField(label="Branch", choices=branch_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    joiningYear = forms.CharField(label="Year of joining", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    passingYear = forms.CharField(label="Year of passing", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    rollNo = forms.CharField(label="Roll No", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = BasicInformation
        fields = ('course', 'branch', 'joiningYear', 'passingYear', 'rollNo')

class EditBasicInformationForm(forms.ModelForm):

    branch_choices = (
        ('Computer Sci. & Engg.', 'Computer Sci. & Engg.'),
        ('Mechanical Engg.', 'Mechanical Engg.'),
        ('Architectural Asst.', 'Architectural Asst.'),
        ('Civil Engg.', 'Civil Engg.'),
        ('Electrical Engg.', 'Electrical Engg.'),
    )

    course = forms.CharField(label="Course", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': 'Diploma'}))
    branch = forms.ChoiceField(label="Branch", choices=branch_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    joiningYear = forms.CharField(label="Year of joining", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    passingYear = forms.CharField(label="Year of passing", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    rollNo = forms.CharField(label="Roll No", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = BasicInformation
        fields = ('course', 'branch', 'joiningYear', 'passingYear', 'rollNo')

# Faculty Information Forms
class AddFacultyInformationForm(forms.ModelForm):

    jobTitle = forms.CharField(label="Job Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    Department = forms.CharField(label="Department", widget=forms.TextInput(attrs={'class': 'form-control'}))
    joinYear = forms.CharField(label="Joined In", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    leftYear = forms.CharField(label="Left In", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = FacultyInformation
        fields = ('jobTitle', 'Department', 'joinYear', 'leftYear')

class EditFacultyInformationForm(forms.ModelForm):

    jobTitle = forms.CharField(label="Course", widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'value': 'Diploma'}))
    Department = forms.CharField(label="Department", widget=forms.TextInput(attrs={'class': 'form-control'}))
    joinYear = forms.CharField(label="Joined In", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    leftYear = forms.CharField(label="Left In", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = FacultyInformation
        fields = ('jobTitle', 'Department', 'joinYear', 'leftYear')

# About Me Forms
class AddAboutMeForm(forms.ModelForm):

    description = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))

    class Meta:
        model = AboutMe
        fields = ('description', )

class EditAboutMeForm(forms.ModelForm):

    description = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))

    class Meta:
        model = AboutMe
        fields = ('description', )

# Education Forms
class AddEducationForm(forms.ModelForm):

    instituteName = forms.CharField(label="Institute Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    joinYear = forms.CharField(label="Year of joining", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    passYear = forms.CharField(label="Year of passing", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    degree = forms.CharField(label="Degree", widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.CharField(label="Department", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Education
        fields = ('instituteName', 'joinYear', 'passYear', 'degree', 'department')

class EditEducationForm(forms.ModelForm):

    instituteName = forms.CharField(label="Institute Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    joinYear = forms.CharField(label="Year of joining", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    passYear = forms.CharField(label="Year of passing", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    degree = forms.CharField(label="Degree", widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.CharField(label="Department", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Education
        fields = ('instituteName', 'joinYear', 'passYear', 'degree', 'department')

# Social Accounts Forms
class AddSocialAccountsForm(forms.ModelForm):

    facebook = forms.CharField(label="Facebook Username", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    instagram = forms.CharField(label="Instagram Username", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    linkedin = forms.CharField(label="Linkedin Username", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    twitter = forms.CharField(label="Twitter Username", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = SocialMedia
        fields = ('facebook', 'instagram', 'linkedin', 'twitter')

class EditSocialAccountsForm(forms.ModelForm):

    facebook = forms.CharField(label="Facebook Username", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    instagram = forms.CharField(label="Instagram Username", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    linkedin = forms.CharField(label="Linkedin Username", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    twitter = forms.CharField(label="Twitter Username", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = SocialMedia
        fields = ('facebook', 'instagram', 'linkedin', 'twitter')

# Work Experience Forms
class AddWorkExperienceForm(forms.ModelForm):

    workTitle = forms.CharField(label="Work Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    companyName = forms.CharField(label="Company Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    workIndustry = forms.CharField(label="Work Industry", widget=forms.TextInput(attrs={'class': 'form-control'}))
    achievements = forms.CharField(label="Achievements", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = WorkExperience
        fields = ('workTitle', 'companyName', 'workIndustry', 'achievements')

class EditWorkExperienceForm(forms.ModelForm):

    workTitle = forms.CharField(label="Work Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    companyName = forms.CharField(label="Company Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    workIndustry = forms.CharField(label="Work Industry", widget=forms.TextInput(attrs={'class': 'form-control'}))
    achievements = forms.CharField(label="Achievements", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = WorkExperience
        fields = ('workTitle', 'companyName', 'workIndustry', 'achievements')

# Job Opening Forms
class AddJobOpeningForm(forms.ModelForm):

    jobTitle = forms.CharField(label="Job Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    companyName = forms.CharField(label="Company Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label="Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    skills = forms.CharField(label="Skills", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))
    applyLink = forms.CharField(label="Apply Link", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = JobOpening
        fields = ('jobTitle', 'companyName', 'location', 'skills', 'description', 'applyLink')
