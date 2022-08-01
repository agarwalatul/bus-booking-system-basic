from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserTitles(models.TextChoices):
    MR = 'MR', _('MR')
    MS = 'MS', _('MS')
    MRS = 'MRS', _('MRS')


class UserGender(models.TextChoices):
    MALE = 'MALE', _('MALE')
    FEMALE = 'FEMALE', _('FEMALE')


class User(AbstractUser, BaseModel):
    gender = models.CharField(max_length=16, choices=UserGender.choices, default=UserGender.MALE.value)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
