from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (
    BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email,  username, password=None,**extra_fields):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('acivation_status', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError((
                'Super user must have is_staff'
            ))

        return self.create_user(email,username,password,**extra_fields)

    
class User(AbstractUser):
    phone=models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    acivation_status=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email



class Category(models.Model):
    name=models.CharField(max_length=100)
    type=models.CharField(max_length=10)


class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    discription=models.CharField(max_length=150)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.CharField(max_length=100)
    bank_name=models.CharField(max_length=100)
    account_number=models.CharField(max_length=10,)
    branch=models.CharField(max_length=100)
    ifsc=models.CharField(max_length=8) 


class UserProduct(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
