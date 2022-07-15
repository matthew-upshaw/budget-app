from django.contrib import admin
from . import models

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date_of_transaction',
        'transaction_category',
        'amount',
        'owner',
    )

# Register your models here.
admin.site.register(models.Transaction, TransactionAdmin)
