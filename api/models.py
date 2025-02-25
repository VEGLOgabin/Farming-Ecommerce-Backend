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

class Category(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):  # Renamed for consistency
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Out of Stock', 'Out of Stock'),
        ('Discontinued', 'Discontinued'),
        ('Backorder', 'Backorder'),
        ('Preorder', 'Preorder'),
        ('Hidden', 'Hidden'),
        ('Archived', 'Archived'),
        ('On Sale', 'On Sale'),
        ('Pending Approval', 'Pending Approval'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantity = models.PositiveIntegerField()  # Enforce non-negative values
    prod_unit = models.CharField(max_length=15)
    money_unit = models.CharField(max_length=15)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="products")
    image = models.ImageField(upload_to='produits/', blank=False, null=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-added_at', 'title')
        db_table = 'Product'


        
# Paiement model
class Pay(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='payment_history')
    amount = models.FloatField()
    money_unit = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=50, choices=[('Mobile Money', 'Mobile Money'), ('Especes', 'Especes')])
    status = models.CharField(max_length=50, default='pending')


    def paiement_en_attente(self):
        self.status = 'Pending'
        self.save()

    def effectuer_paiement(self):
        self.status = 'Paid'
        self.save()

    def rembourser(self):
        self.status = 'Refunded'
        self.save()

    class Meta:
        db_table = 'Payment'

# Messagerie model
class ContactUS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='text_admin')
    content = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ContactUS'

# Feedback model
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='feedbacks')
    rate = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Feedback'