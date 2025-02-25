from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin,AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, password, email, telephone, adresse,is_active = True,  **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
            adresse=adresse,
            is_staff=False, 
            is_admin=False,
            is_active = is_active,
            **kwargs
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
        

    def create_staffuser(self, first_name, last_name,password,email, telephone, adresse, is_active = True):

        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
            adresse=adresse,
            password=password,
            is_staff=True,
            is_admin=False,
            is_active = is_active
        )
        return user
    
    def create_superuser(self, first_name, last_name, email, password, telephone, adresse, is_active = True):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
            adresse=adresse,
            password=password,
            is_staff=True,
            is_admin=True,
            is_active = is_active
        )
        return user


# Custom User model (inherits from AbstractUser)
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', "telephone", "adresse"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'user'