from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

GENDER_CATEGORY = (
    ('U', 'Undefined'),
    ('F', 'Female'),
    ('M', 'Male')
)


class CustomUserManager(BaseUserManager):

    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('name'), max_length=128)
    surname = models.CharField(_('name'), max_length=128)
    email = models.EmailField(_('email'), unique=True)
    avatar = models.ImageField()
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    gender = models.CharField(choices=GENDER_CATEGORY, max_length=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return str(self.email)

    @property
    def is_staff(self):
        return self.is_superuser
