from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, name, email, role, gender, maritalStatus, location, phone, phoneVisibility, password=None):
        if not email:
            raise ValueError("Users must have an email address!")
        user = self.model(
            name = name,
            email = self.normalize_email(email),
            role = role,
            gender = gender,
            maritalStatus = maritalStatus,
            location = location,
            phone = phone,
            phoneVisibility = phoneVisibility,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, name, email, role, gender, maritalStatus, location, phone, phoneVisibility):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            name = name,
            role = role,
            gender = gender,
            maritalStatus = maritalStatus,
            location = location,
            phone = phone,
            phoneVisibility = phoneVisibility,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):

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

    id = models.AutoField(primary_key=True)
    username = None

    name = models.CharField(max_length=200)
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    role = models.CharField(choices=role_choices, max_length=100)
    gender = models.CharField(choices=gender_choices, max_length=250)
    maritalStatus = models.CharField(choices=maritalStatus_choices, max_length=100)
    location = models.CharField(max_length=100, unique=False)
    phone = models.CharField(max_length=100, unique=True)
    phoneVisibility = models.CharField(max_length=100, choices=phoneVisibility_choices, default='Private')
    isAuthenticated = models.BooleanField(default=False, blank=True)

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role', 'gender', 'maritalStatus', 'location', 'phone']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class BasicInformation(models.Model):

    branch_choices = (
        ('Computer Sci. & Engg.', 'Computer Sci. & Engg.'),
        ('Mechanical Engg.', 'Mechanical Engg.'),
        ('Architectural Asst.', 'Architectural Asst.'),
        ('Civil Engg.', 'Civil Engg.'),
        ('Electrical Engg.', 'Electrical Engg.'),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.CharField(max_length=100, default='Diploma')
    branch = models.CharField(choices=branch_choices, max_length=250)
    joiningYear = models.CharField(max_length=100)
    passingYear = models.CharField(max_length=100)
    rollNo = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.course

class FacultyInformation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    jobTitle = models.CharField(max_length=100)
    Department = models.CharField(max_length=250)
    joinYear = models.CharField(max_length=100)
    leftYear = models.CharField(max_length=100)

    def __str__(self):
        return self.jobTitle

class AboutMe(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField(max_length=5000)

    def __str__(self):
        return f"{self.user.name} - {self.user.email} - {self.user.role}"

class Education(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    instituteName = models.CharField(max_length=500)
    joinYear = models.CharField(max_length=100)
    passYear = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.instituteName

class SocialMedia(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    facebook = models.CharField(max_length=500, default='', blank=True)
    instagram = models.CharField(max_length=100, default='', blank=True)
    linkedin = models.CharField(max_length=100, default='', blank=True)
    twitter = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.user.email}"

class WorkExperience(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    workTitle = models.CharField(max_length=500)
    companyName = models.CharField(max_length=500)
    workIndustry = models.CharField(max_length=500)
    achievements = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.user.email}"

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class JobOpening(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    jobTitle = models.CharField(max_length=100)
    companyName = models.CharField(max_length=250)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=500)
    description = models.TextField()
    applyLink = models.CharField(max_length=500)
    postedOn = models.DateField()

    def __str__(self):
        return self.jobTitle
