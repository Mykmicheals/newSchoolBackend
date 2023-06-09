from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

CLASSROOM_CHOICES = (
    ('1', 'JSS1'),
    ('2', 'JSS2'),
    ('3', 'JSS3'),
    ('4', 'SSS1'),
    ('5', 'SSS2'),
    ('6', 'SSS3'),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    middle_name = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profile_pictures', blank=True)

    last_name = models.CharField(max_length=20, blank=True)
    is_teacher = models.BooleanField(default=False, blank=True)
    is_student = models.BooleanField(default=False, blank=True)
    is_principal = models.BooleanField(default=False, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    classroom = models.ForeignKey(
        'app.ClassRoom', on_delete=models.CASCADE,null=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
