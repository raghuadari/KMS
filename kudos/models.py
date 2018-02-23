from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm

class Release(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField('release start date')
    end_date = models.DateTimeField('release end date')
    is_current_release = models.BooleanField(default=False)
    def __str__(self):
       return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    def __str__(self):
       return self.name

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
       return self.first_name + ' ' + self.last_name

class KudoTitle(models.Model):
    kudo_title = models.CharField(max_length=20)
    def __str__(self):
       return self.kudo_title

class Kudo(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grantor')
    title = models.ForeignKey(KudoTitle, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    date = models.DateTimeField('kudo given date')
