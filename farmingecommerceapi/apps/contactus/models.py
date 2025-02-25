from django.db import models
from users.models import User

# ContactUS model
class ContactUS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='text_admin')
    content = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ContactUS'
