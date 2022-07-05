import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager as CustomUserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user with only required fields for the system. 
    This model supports django default authentication system.
    Email is taken as a username field and email and password are required fields.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    is_admin = models.BooleanField(
        _('Admin status'),
        default=False,
        help_text=_(
            'Designates that this user has all staffs permissions without '
            'explicitly assigning them.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email' # making email field as a username

    objects = CustomUserManager() # assigning custom User manager

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.is_admin = self.is_admin or self.is_superuser
        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def is_staff(self):
        """Overriding staff permission with admin permission (for Django Admin)"""
        return self.is_admin

