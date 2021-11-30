from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.safestring import mark_safe

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
    email = models.EmailField('Email', unique=True)
    password = models.CharField(_('password'), max_length=128)
    last_name = models.CharField('Фамилия', max_length=128)
    first_name = models.CharField('Имя', max_length=128)
    avatar = models.ImageField('Фотография', upload_to='avatars', default='static/default_avatar.png')
    gender = models.PositiveIntegerField(choices=GENDER, default=GENDER_UNKNOWN, verbose_name='Пол')
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    latitude = models.DecimalField(_('latitude'), max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(_('longitude'), max_digits=22, decimal_places=16, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    indexes = [
        models.Index(fields=['longitude']),
        models.Index(fields=['latitude'])
    ]
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return str(self.email)

    @property
    def is_staff(self):
        return self.is_superuser

    def get_avatar(self):
        if self.avatar.name == self._meta.get_field('avatar').get_default():
            return '/' + self.avatar.name
        return self.avatar.url

    def avatar_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())


class UserFollowing(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    subscribers = models.ManyToManyField(UserProfile, related_name='subscribers')
    created = models.DateTimeField(auto_now_add=True)
