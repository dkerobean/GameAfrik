from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager, PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    name = models.CharField(_('name'), max_length=150, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    USER_ROLES = [
        ('user', 'User'),
        ('host', 'Host')
    ]

    USER_SKILLS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                related_name='profile')
    username = models.CharField(_('username'), max_length=100)
    role = models.CharField(_('role'), max_length=50, choices=USER_ROLES,
                            default="user")
    avatar = models.ImageField(_('avatar'), upload_to='user_profiles',
                               blank=True, null=True,
                               default='user_profile/avatar.svg')
    bio = models.TextField(_('bio'), null=True, blank=True)
    location = models.CharField(_('location'), max_length=100,
                                null=True, blank=True)
    skill_level = models.CharField(_('skill level'), max_length=20,
                                   choices=USER_SKILLS, default='beginner')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4,
                            unique=True, editable=False)

    def __str__(self):
        return self.username


class Clips(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='games')
    description = models.TextField()
    clips = models.ForeignKey(Clips, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    GAME_STATUS = [
        ('open', 'Open'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed')
    ]
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='tournaments')
    game_type = models.CharField(max_length=100)
    game_mode = models.CharField(max_length=100)
    game_format = models.CharField(max_length=100)
    entry_fee = models.IntegerField()
    prize_pool = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    bracket = models.CharField(max_length=50, null=True, blank=True)
    participants = models.ManyToManyField(Profile,
                                          related_name='tournaments_participated') # noqa
    host = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             related_name='hosted_tournaments')
    status = models.CharField(choices=GAME_STATUS, max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    rules = models.TextField()

    def __str__(self):
        return self.name
