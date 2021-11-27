from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    GENDER_UNKNOWN = 0
    GENDER_FEMALE = 1
    GENDER_MALE = 2
    GENDER = (
        (GENDER_FEMALE, 'Женский'),
        (GENDER_MALE, 'Мужской'),
        (GENDER_UNKNOWN, 'Не определён'),
    )

    # Базовая информация
    email = models.EmailField('Email', blank=False, null=True, unique=True)
    password = models.CharField(_('password'), max_length=128, default=None, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=255, blank=False, null=True)
    first_name = models.CharField('Имя', max_length=255, blank=False, null=True)
    avatar = models.ImageField('Фотография', upload_to='avatars', default='static/default_avatar.png')
    gender = models.PositiveIntegerField(choices=GENDER, default=GENDER_UNKNOWN, verbose_name='Пол')

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
