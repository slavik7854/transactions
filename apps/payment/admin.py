from django.contrib import admin

from .models import Payment, Account


admin.site.register(Account)
admin.site.register(Payment)
