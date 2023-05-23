from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import login as loginUser, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import Http404

# Create your views here.

# Home
def home(request):

    if(request.method == "POST"):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, phone=phone, message=message, date=datetime.today())
        contact.save()
        messages.success(request, f'Thanks {name} for your feedback!')

        return redirect('/')

    return render(request, "home.html")

# Authentication
def signup(request):

    context = {}

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            phoneVisibility = form.cleaned_data.get('phoneVisibility')

            messages.success(request, "Your account has been created successfully!")

            # Email
            subject = 'TPC Alumni Association'
            html_message = render_to_string('registration_email.html', {'email': email, 'password': password, 'phoneVisibility': phoneVisibility})
            plain_message = strip_tags(html_message)
            from_email = 'harmanbatheja15@gmail.com'
            to_email = email
            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

            return redirect('/login/')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, "signup.html", context)

def login(request):

    context = {}

    basicInformation = BasicInformation.objects.filter(id=request.user.id).exists()
    facultyInformation = FacultyInformation.objects.filter(id=request.user.id).exists()

    user = request.user
    if user.is_authenticated:
        if user.role == 'Alumni' or user.role == 'Student':
            if basicInformation:
                return redirect("/profile/")
            else:
                return redirect("/addBasicInformation/")
        
        if user.role == 'Faculty':
            if facultyInformation:
                return redirect("/profile/")
            else:
                return redirect('/addFacultyInformation/')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            messages.success(request, "You are logged in successfully!")

            if user:
                loginUser(request, user)
                if user.role == 'Alumni' or user.role == 'Student':
                    if basicInformation:
                        return redirect("/profile/")
                    else:
                        return redirect("/addBasicInformation/")

                if user.role == 'Faculty':
                    if facultyInformation:
                        return redirect("/profile/")
                    else:
                        return redirect("/addFacultyInformation/")

    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form

    return render(request, "login.html", context)

def signout(request):
    logout(request)
    return redirect('/')

# Basic Information
def addBasicInformation(request):
    context = {}

    if request.method == 'POST':
        form = AddBasicInformationForm(request.POST)
        if form.is_valid():
            basicInfoForm = form.save(commit=False)
            basicInfoForm.user = request.user
            basicInfoForm.save()
            messages.success(request, "Information has been added successfully!")
            return redirect("/profile/")
    else:
        form = AddBasicInformationForm()
    context['addBasicInformation_form'] = form

    basicInformation = BasicInformation.objects.filter(user=request.user).exists()
    if basicInformation:
        return redirect('/profile/')

    if request.user.role == 'Faculty':
        return redirect('/profile/')

    return render(request, "addBasicInformation.html", context)

@login_required(login_url='login')
def editBasicInformation(request, basicInfo_id):

    try:
        basicInformation = get_object_or_404(BasicInformation, id=basicInfo_id)
    except Http404:
        return redirect('/profile/')
        
    editBasicInfo_form = EditBasicInformationForm(request.POST or None, instance=basicInformation)

    if editBasicInfo_form.is_valid():
        basicInformation = editBasicInfo_form.save(commit=False)
        basicInformation.user = request.user
        basicInformation.save()
        messages.success(request, 'Education Updated successfully!')
        return redirect('/profile/')

    if basicInformation.user != request.user:
        return redirect('/profile/')

    context = {
        'basicInformation': basicInformation,
        'editBasicInfo_form': editBasicInfo_form
    }

    return render(request, 'editBasicInformation.html', context)

# Faculty Information
def addFacultyInformation(request):
    context = {}

    if request.method == 'POST':
        form = AddFacultyInformationForm(request.POST)
        if form.is_valid():
            facultyInfoForm = form.save(commit=False)
            facultyInfoForm.user = request.user
            facultyInfoForm.save()
            messages.success(request, "Information has been added successfully!")
            return redirect("/profile/")
    else:
        form = AddFacultyInformationForm()
    context['addFacultyInformation_form'] = form

    facultyInformation = FacultyInformation.objects.filter(user=request.user).exists()
    if facultyInformation:
        return redirect('/profile/')

    if request.user.role == 'Alumni' or request.user.role == 'Student':
        return redirect('/profile/')

    return render(request, "addFacultyInformation.html", context)

@login_required(login_url='login')
def editFacultyInformation(request, facultyInfo_id):

    try:
        facultyInformation = get_object_or_404(FacultyInformation, id=facultyInfo_id)
    except Http404:
        return redirect('/profile/')

    editFacultyInfo_form = EditFacultyInformationForm(request.POST or None, instance=facultyInformation)

    if editFacultyInfo_form.is_valid():
        facultyInformation = editFacultyInfo_form.save(commit=False)
        facultyInformation.user = request.user
        facultyInformation.save()
        messages.success(request, 'Updated successfully!')
        return redirect('/profile/')

    if facultyInformation.user != request.user:
        return redirect('/profile/')

    context = {
        'facultyInformation': facultyInformation,
        'editFacultyInfo_form': editFacultyInfo_form
    }

    return render(request, 'editFacultyInformation.html', context)

# Profile
@login_required(login_url='login')
def profile(request):
    context = {}

    if request.method == 'POST':
        form = AddEducationForm(request.POST)
        if form.is_valid():
            eduForm = form.save(commit=False)
            eduForm.user = request.user
            eduForm.email = request.user.email
            eduForm.save()

            messages.success(request, "Education added successfully!")
            return redirect('/profile/')
        else:
            context['addEducation_form'] = form
    else:
        form = AddEducationForm()
        context['addEducation_form'] = form

    aboutMe = AboutMe.objects.filter(user=request.user)
    basicInformation = BasicInformation.objects.filter(user=request.user)
    facultyInformation = FacultyInformation.objects.filter(user=request.user)
    educationDetails = Education.objects.filter(user=request.user).order_by('-joinYear')
    socialAccounts = SocialMedia.objects.filter(user=request.user)
    workExperiences = WorkExperience.objects.filter(user=request.user).order_by('-id')
    jobOpenings = JobOpening.objects.filter(user=request.user).order_by('-postedOn')

    basicInfo = BasicInformation.objects.filter(user=request.user).exists()
    aboutDescription = AboutMe.objects.filter(user=request.user).exists()
    socialProfiles = SocialMedia.objects.filter(user=request.user).exists()

    context = {
        'aboutMe': aboutMe,
        'basicInformation': basicInformation,
        'basicInfo': basicInfo,
        'facultyInformation': facultyInformation,
        'educationDetails': educationDetails,
        'socialAccounts': socialAccounts,
        'addEducation_form': form,
        'aboutDescription': aboutDescription,
        'socialProfiles': socialProfiles,
        'workExperiences': workExperiences,
        'jobOpenings': jobOpenings,
    }
    return render(request, "profile.html", context)

@login_required(login_url='login')
def editProfile(request):
    
    basicInformation = BasicInformation.objects.filter(user=request.user).exists()
    facultyInformation = FacultyInformation.objects.filter(user=request.user).exists()

    if request.user.role == 'Alumni' or request.user.role == 'Student':
        if basicInformation:
            basicInfo = BasicInformation.objects.get(user=request.user)
    elif request.user.role == 'Faculty':
        if facultyInformation:
            facultyInfo = FacultyInformation.objects.get(user=request.user)
    
    user = request.user
    current_role = user.role

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "Your account has been updated!")
            
            new_role = user.role
            try:
                if current_role == 'Alumni' and new_role == 'Student':
                    pass
                elif current_role == 'Alumni' and new_role == 'Faculty':
                    alumni_data = BasicInformation.objects.get(user=user)
                    alumni_data.delete()
                elif current_role == 'Student' and new_role == 'Alumni':
                    pass
                elif current_role == 'Student' and new_role == 'Faculty':
                    student_data = BasicInformation.objects.get(user=user)
                    student_data.delete()
                elif current_role == 'Faculty' and new_role == 'Student':
                    faculty_data = FacultyInformation.objects.get(user=user)
                    faculty_data.delete()
                elif current_role == 'Faculty' and new_role == 'Alumni':
                    faculty_data = FacultyInformation.objects.get(user=user)
                    faculty_data.delete()
            except:
                BasicInformation.DoesNotExist()
                FacultyInformation.DoesNotExist()

            if request.user.role == 'Alumni' or request.user.role == 'Student':
                if basicInformation:
                    return redirect('/editBasicInformation/' + str(basicInfo.id) + '/')
                else:
                    return redirect('/addBasicInformation/')
            
            if request.user.role == 'Faculty':
                if facultyInformation:
                    return redirect('/editFacultyInformation/' + str(facultyInfo.id) + '/')
                else:
                    return redirect('/addFacultyInformation/')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }

    return render(request, 'editProfile.html', context)

# About Me
@login_required(login_url='login')
def addAboutMe(request):

    context = {}

    if request.method == 'POST':
        form = AddAboutMeForm(request.POST)
        if form.is_valid():
            aboutForm = form.save(commit=False)
            aboutForm.user = request.user
            aboutForm.save()
            return redirect('/profile/')
        else:
            context['addAboutMe_form'] = form
    else:
        form = AddAboutMeForm()
        context['addAboutMe_form'] = form

    return render(request, "addAboutMe.html", context)

@login_required(login_url='login')
def editAboutMe(request, about_id):

    try:
        about = get_object_or_404(AboutMe, id=about_id)
    except Http404:
        return redirect('/profile/')

    editAboutMe_form = EditAboutMeForm(request.POST or None, instance=about)

    if editAboutMe_form.is_valid():
        aboutMe = editAboutMe_form.save(commit=False)
        aboutMe.user = request.user
        aboutMe.save()
        messages.success(request, 'About Me Updated successfully!')
        return redirect('/profile/')
    
    if about.user != request.user:
        return redirect('/profile/')

    context = {
        'about': about,
        'editAboutMe_form': editAboutMe_form
    }

    return render(request, "editAboutMe.html", context)

# Alumni Directory
@login_required(login_url='login')
def alumniDirectory(request):

    allAlumnis = Account.objects.prefetch_related('basicinformation_set', 'facultyinformation_set').order_by('-date_joined')[:8]
    alumni_search = BasicInformation.objects.values_list('joiningYear', flat=True).distinct()
    joiningYear = request.GET.get('joiningYear')
    alumnis = BasicInformation.objects.filter(joiningYear__iexact=joiningYear)
    faculties = FacultyInformation.objects.filter(joinYear__iexact=joiningYear)

    name = request.GET.get('name')
    if name is not None:
        nameAlumnis = BasicInformation.objects.filter(user__name__icontains=name)
        nameFaculties = FacultyInformation.objects.filter(user__name__icontains=name)
    else:
        nameAlumnis = BasicInformation.objects.none()
        nameFaculties = FacultyInformation.objects.none()

    if 'joiningYear' in request.GET:
        joiningYear = request.GET['joiningYear']
        if joiningYear:
            alumnis = alumnis.filter(joiningYear__iexact=joiningYear)
            faculties = faculties.filter(joinYear__iexact=joiningYear)

    if 'name' in request.GET:
        name = request.GET['name']
        if name:
            nameAlumnis = nameAlumnis.filter(user__name__icontains=name)
            nameFaculties = nameFaculties.filter(user__name__icontains=name)

    context = {
        'allAlumnis': allAlumnis,
        'alumnis': alumnis,
        'faculties': faculties,
        'alumni_search': alumni_search,
        'nameAlumnis': nameAlumnis,
        'nameFaculties': nameFaculties,
    }

    return render(request, "alumniDirectory.html", context)

@login_required(login_url='login')
def userDetail(request, name):
    user = Account.objects.get(name=name)
    educationDetails = Education.objects.filter(id=user.id).order_by('-joinYear')
    aboutMe = AboutMe.objects.filter(user=user)
    workExperiences = WorkExperience.objects.filter(user=user).order_by('-id')
    socialAccounts = SocialMedia.objects.filter(user=user)
    basicInformation = BasicInformation.objects.filter(user=user)
    facultyInformation = FacultyInformation.objects.filter(user=user)
    
    ctx = {
        'user': user,
        'aboutMe': aboutMe,
        'educationDetails': educationDetails,
        'workExperiences': workExperiences,
        'socialAccounts': socialAccounts,
        'basicInformation': basicInformation,
        'facultyInformation': facultyInformation,
    }
    return render(request, 'userDetail.html', ctx)

# Social Media
@login_required(login_url='login')
def addSocialMedia(request):

    context = {}

    if request.method == 'POST':
        form = AddSocialAccountsForm(request.POST)
        if form.is_valid():
            socialMediaForm = form.save(commit=False)
            socialMediaForm.user = request.user
            socialMediaForm.save()

            messages.success(request, "Education added successfully!")
            return redirect('/profile/')
        else:
            context['addSocialAccounts_form'] = form
    else:
        form = AddSocialAccountsForm()
        context['addSocialAccounts_form'] = form

    socialProfiles = SocialMedia.objects.filter(user=request.user).exists()
    if socialProfiles:
        return redirect('/profile/')

    return render(request, "addSocialMedia.html", context)

@login_required(login_url='login')
def editSocialMedia(request, socialMedia_id):

    try:
        socialMedia = get_object_or_404(SocialMedia, id=socialMedia_id)
    except Http404:
        return redirect('/profile/')

    editSocialMedia_form = EditSocialAccountsForm(request.POST or None, instance=socialMedia)

    if editSocialMedia_form.is_valid():
        social = editSocialMedia_form.save(commit=False)
        social.user = request.user
        social.save()
        messages.success(request, 'Social Media Updated successfully!')
        return redirect('/profile/')

    socialAccounts = SocialMedia.objects.filter(user=request.user)
    basicInformation = BasicInformation.objects.filter(user=request.user)

    socialProfiles = SocialMedia.objects.get(id=socialMedia_id)
    if socialProfiles.user != request.user:
        return redirect('/profile/')

    context = {
        'socialMedia': socialMedia,
        'socialAccounts': socialAccounts,
        'editSocialMedia_form': editSocialMedia_form,
        'basicInformation': basicInformation,
    }

    return render(request, 'editSocialMedia.html', context)

# Education
@login_required(login_url='login')
def editEducation(request, edu_id):

    try:
        education = get_object_or_404(Education, id=edu_id)
    except Http404:
        return redirect('/profile/')

    editEdu_form = EditEducationForm(request.POST or None, instance=education)

    if editEdu_form.is_valid():
        education = editEdu_form.save(commit=False)
        education.user = request.user
        education.save()
        messages.success(request, 'Education Updated successfully!')
        return redirect('/profile/')

    if education.user != request.user:
        return redirect('/profile/')

    context = {
        'education': education,
        'editEdu_form': editEdu_form
    }

    return render(request, 'editEducation.html', context)

@login_required(login_url='login')
def deleteEducation(request, edu_id):

    try:
        education = get_object_or_404(Education, id=edu_id)
    except Http404:
        return redirect('/profile/')

    if education.user != request.user:
        return redirect('/profile/')

    education.delete()
    messages.success(request, 'Education deleted successfully!')
    return redirect('/profile/')

# Work Experience
@login_required(login_url='login')
def addWorkExperience(request):

    socialAccounts = SocialMedia.objects.filter(user=request.user)
    basicInformation = BasicInformation.objects.filter(user=request.user)

    context = {}

    if request.method == 'POST':
        form = AddWorkExperienceForm(request.POST)
        if form.is_valid():
            workExperienceForm = form.save(commit=False)
            workExperienceForm.user = request.user
            workExperienceForm.save()
            messages.success(request, "Work Experience added successfully!")

            return redirect('/profile/')
        else:
            context['addWorkExperience_form'] = form
    else:
        form = AddWorkExperienceForm()
        context['addWorkExperience_form'] = form

        context = {
            'addWorkExperience_form': form,
            'socialAccounts': socialAccounts,
            'basicInformation': basicInformation,
        }

    return render(request, "addWorkExperience.html", context)

@login_required(login_url='login')
def editWorkExperience(request, workExperienceId):

    try:
        work = get_object_or_404(WorkExperience, id=workExperienceId)
    except Http404:
        return redirect('/profile/')
    editWorkExperience_form = EditWorkExperienceForm(request.POST or None, instance=work)
    socialAccounts = SocialMedia.objects.filter(user=request.user)
    basicInformation = BasicInformation.objects.filter(user=request.user)

    if editWorkExperience_form.is_valid():
        workExperience = editWorkExperience_form.save(commit=False)
        workExperience.user = request.user
        workExperience.save()
        messages.success(request, 'Work Experience Updated successfully!')
        return redirect('/profile/')

    if work.user != request.user:
        return redirect('/profile/')

    context = {
        'work': work,
        'editWorkExperience_form': editWorkExperience_form,
        'socialAccounts': socialAccounts,
        'basicInformation': basicInformation,
    }

    return render(request, "editWorkExperience.html", context)

@login_required(login_url='login')
def deleteWorkExperience(request, workExperienceId):

    try:
        work = get_object_or_404(WorkExperience, id=workExperienceId)
    except Http404:
        return redirect('/profile/')

    if work.user != request.user:
        return redirect('/profile/')
    work.delete()
    messages.success(request, 'Work Experience deleted successfully!')
    return redirect('/profile/')

# Job Openings
@login_required(login_url='login')
def addJobOpenings(request):
    
    context = {}

    if request.method == 'POST':
        form = AddJobOpeningForm(request.POST)
        if form.is_valid():
            jobForm = form.save(commit=False)
            jobForm.user = request.user
            jobForm.postedOn = datetime.today()
            jobForm.save()
            messages.success(request, 'Job Opening posted successfully!')
            return redirect('/jobOpenings/')
        else:
            context['addJobOpenings_form'] = form
    else:
        form = AddJobOpeningForm()
        context['addJobOpenings_form'] = form

    if request.user.role == 'Student':
        return redirect('/profile/')

    return render(request, "addJobOpenings.html", context)

@login_required(login_url='login')
def deleteJobOpening(request, job_id):

    try:
        job = get_object_or_404(JobOpening, id=job_id)
    except Http404:
        return redirect('/profile/')

    if job.user != request.user:
        return redirect('/profile/')

    job.delete()
    
    messages.success(request, 'Job Opening deleted successfully!')
    return redirect('/profile/')

@login_required(login_url='login')
def jobOpenings(request):

    jobOpenings = JobOpening.objects.all().order_by('-postedOn')
    
    context = {
        'jobOpenings': jobOpenings
    }

    return render(request, 'jobOpenings.html', context)

@login_required(login_url='login')
def jobDetail(request, id):

    job = JobOpening.objects.filter(id=id)

    if not job:
        return redirect('/jobOpenings/')
    
    context = {
        'job': job
    }

    return render(request, 'jobDetail.html', context)

# Error 404
def error_404(request, exception):
    return render(request, 'error404.html')
