from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone


TYPE_OPTIONS = (
    ('credit','Credit'),
    ('debit','Debit'),
)

PAYMENT_OPTIONS = (
    ('credit card','Credit Card'),
    ('debit card','Debit Card'),
    ('check','Check'),
    ('cash','Cash'),
    ('income','Income'),
)

CATEGORY_OPTIONS = (
    ('hou','Housing'),
    ('car','Car'),
    ('gro','Groceries'),
    ('res','Restaurants'),
    ('gas','Gas'),
    ('util','Utilities'),
    ('ent','Entertainment'),
    ('sho','Shopping'),
    ('sub','Subscriptions'),
    ('sav','Savings'),
    ('debt','Debt'),
    ('cha','Charity'),
    ('misc','Miscellaneous'),
    ('pay','Paycheck'),
)

# Create your models here.
class Transaction(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    transaction_type = models.CharField(max_length=255, choices=TYPE_OPTIONS)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    transaction_category = models.CharField(max_length=255, choices=CATEGORY_OPTIONS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_transaction = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_OPTIONS)

    def __str__(self):
        return f'{self.name} - {self.amount}'

    def get_absolute_url(self):
        return reverse('adad-home')
    

    class Meta:
        ordering = ['-date_of_transaction']
