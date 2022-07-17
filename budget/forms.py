from django.forms import ModelForm
from django.forms.widgets import DateInput
from . models import (
    Transaction,
)

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        exclude = ['id','owner']

        labels = {
            'name':'Name',
            'description':'Description',
            'transaction_type':'Credit or Debit',
            'amount':'Amount',
            'date_of_transaction':'Date',
            'transaction_category':'Category',
            'payment_method':'Payment Method',
        }

        widgets = {
            'date_of_transaction':DateInput(attrs={'type':'date'})
        }
