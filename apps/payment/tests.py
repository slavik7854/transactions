import json

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Account, Payment


class PaymentTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create(username='admin', email='admin@mailinator.com', password='1')
        self.test_user = User.objects.create(username='test', email='test@mailinator.com', password='1')
        self.first_account = Account.objects.create(
            user=self.admin_user,
            balance=1000,
            currency='USD'
        )
        self.second_account = Account.objects.create(
            user=self.admin_user,
            balance=1000,
            currency='EUR'
        )
        self.third_account = Account.objects.create(
            user=self.test_user,
            balance=1000,
            currency='GBP'
        )
        self.fourth_account = Account.objects.create(
            user=self.test_user,
            balance=1000,
            currency='USD'
        )

    def test_transfer(self):
        '''
        Check currency of accounts
        '''
        account_to = self.fourth_account
        self.assertIn(account_to.currency, self.admin_user.account_set.all().values_list('currency', flat=True))
        account_to_failed = self.third_account
        self.assertNotIn(account_to_failed.currency, self.admin_user.account_set.all().values_list(
            'currency', flat=True))

    def test_get_payments(self):
        '''
        'payments' entry check
        '''
        response = self.client.get('/api/')
        self.assertIn('payments', response.data)

    def test_balance_change(self):
        '''
        Transfer from first account to fourth account
        '''
        amount = 100
        Payment.objects.create(
            account=self.first_account,
            amount=amount,
            to_account=self.third_account,
            direction='Outgoing'
        )
        Payment.objects.create(
            account=self.third_account,
            amount=amount,
            from_account=self.first_account,
            direction='Incoming'
        )
        self.first_account.balance -= amount
        self.third_account.balance += amount

        self.assertEqual(self.first_account.balance, 900)
        self.assertEqual(self.third_account.balance, 1100)
