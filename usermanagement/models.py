from django.db import models
from accounts.models import Account

class Wallet(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('credit', 'Credit'),
        ('debit', 'Debit')
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True, blank=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, null=True, blank=True)
    credit_on = models.DateTimeField(null=True, blank=True)
    debit_on = models.DateTimeField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    def is_credit(self):
        return self.transaction_type == 'credit'

    def is_debit(self):
        return self.transaction_type == 'debit'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_credit():
            self.user.wallet_balance = self.wallet_balance
        else:
            self.user.wallet_balance -= self.amount
        self.user.save()


class Service(models.Model):
    service = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.service

class ServiceRate(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('user', 'service')

    def __str__(self) -> str:
        return f"User = {self.user.username} | Service = {self.service} | rate = {self.rate}"