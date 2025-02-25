from django.db import models

from users.models import User

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

