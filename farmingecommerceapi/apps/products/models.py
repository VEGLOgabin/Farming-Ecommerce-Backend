from django.db import models
from users.models import User

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    image = models.ImageField(upload_to='produits/', blank=False, null=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-added_at', 'title')
        db_table = 'Product'



# Feedback model
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feedbacks')
    rate = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Feedback'