from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import Model


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Require email!!!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('name', "admin")

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

        return self._create_user(email, password, **extra_fields)


class Scope(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    scopes = models.ManyToManyField(Scope, related_name="roles", null=True)

    def __str__(self):
        return self.name


# class Role_Scope(models.Model):
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
#     scope = models.ForeignKey(Scope, on_delete=models.CASCADE)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    default_roles = models.ManyToManyField(Role, related_name="users", null=True)
    add_scope = models.ManyToManyField(Scope, related_name="add_roles", null=True, default=None)
    except_scope = models.ManyToManyField(Scope, related_name="except_roles", null=True, default=None)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    def __str__(self):
        return self.email
