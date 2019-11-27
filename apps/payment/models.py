from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


CURRENCY_USD = 'USD'
CURRENCY_EUR = 'EUR'
CURRENCY_GBP = 'GBP'
CURRENCY_RUB = 'RUB'
CURRENCY_UAH = 'UAH'

CURRENCY_CHOICES = (
    (CURRENCY_USD, 'USD'),
    (CURRENCY_EUR, 'EUR'),
    (CURRENCY_GBP, 'GBP'),
    (CURRENCY_RUB, 'RUB'),
    (CURRENCY_UAH, 'UAH'),
)


DIRECTION_OUTGOING = 'Outgoing'
DIRECTION_INCOMING = 'Incoming'

DIRECTION_CHOICES = (
    (DIRECTION_OUTGOING, 'Outgoing'),
    (DIRECTION_INCOMING, 'Incoming'),
)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default=CURRENCY_USD)

    def __str__(self):
        return f'{self.user.username}-{self.currency}'

    class Meta:
        ordering = ['user']


class Payment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    to_account = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='to_account', null=True)
    from_account = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='from_account', null=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default=DIRECTION_OUTGOING)

    def __str__(self):
        return f'#{self.pk}: {self.amount} - {self.direction}'
