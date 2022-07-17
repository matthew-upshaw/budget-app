import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth, Round
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Transaction, CATEGORY_OPTIONS

from .forms import TransactionForm

from utils.charts import (
    get_year_dict, 
    get_category_dict, generate_color_palette, 
    MONTHS, 
    MONTH_DICT,
    color_primary, 
    color_success, 
    color_danger, 
) 

CATEGORY_DICT = dict(CATEGORY_OPTIONS)

# Create your views here.
class TransactionCreateView(LoginRequiredMixin,CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/transaction-create.html'

    def form_valid(self,form,*args,**kwargs):
        form.instance.owner = self.request.user
        return super().form_valid(form,*args,**kwargs)

class TransactionListView(LoginRequiredMixin,ListView):
    model = Transaction
    template_name = 'budget/transaction-list.html'
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Transaction.objects.filter(owner=user).order_by('-date_of_transaction')

class TransactionDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Transaction
    template_name = 'budget/transaction-detail.html'

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.owner:
            return True
        return False

class TransactionUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'budget/transaction-update.html'

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.owner:
            return True
        return False

class TransactionDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Transaction
    success_url = '/'

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.owner:
            return True
        return False

@login_required
def transaction_list_view(request):
    username = request.user.username
    transactions_list = Transaction.objects.filter(owner__username=username).order_by('-date_of_transaction')
    page = request.GET.get('page',1)
    paginator = Paginator(transactions_list,10)

    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    context = {
        'transactions':transactions,
    }

    return render(request,'budget/transaction-list.html',context=context)

@login_required
def home(request):
    username = request.user.username
    today = datetime.date.today()
    expense_list = Transaction.objects.filter(owner__username=username,transaction_type='debit').order_by('-date_of_transaction')
    payment_list = Transaction.objects.filter(owner__username=username,transaction_type='credit').order_by('-date_of_transaction')
    total_expenses = Transaction.objects.filter(owner__username=username,transaction_type='debit',date_of_transaction__month=today.month).aggregate(total_amount=Round(Sum('amount')))
    total_payments = Transaction.objects.filter(owner__username=username,transaction_type='credit',date_of_transaction__month=today.month).aggregate(total_amount=Round(Sum('amount')))

    context = {
        'expense_list':expense_list,
        'payment_list':payment_list,
        'recent_expense_list':expense_list[:5],
        'total_expenses':total_expenses,
        'total_payments':total_payments,
    }

    return render(request,'budget/budget-home.html',context=context)

@login_required
def get_filter_options(request):
    username = request.user.username
    grouped_transactions = Transaction.objects.filter(owner__username=username).annotate(year=ExtractYear('date_of_transaction')).values('year').order_by('-year').distinct()
    options = [transaction['year'] for transaction in grouped_transactions]

    return JsonResponse({
        'year_options':options,
        'month_options':list(MONTH_DICT.keys()),
        'category_options':list(CATEGORY_DICT.keys())[:-1],
    })

@login_required
def get_expense_chart(request, year):
    username = request.user.username
    expenses = Transaction.objects.filter(owner__username=username).filter(date_of_transaction__year=year).filter(transaction_type='debit')
    grouped_expenses = expenses.annotate(month=ExtractMonth('date_of_transaction'))\
        .values('month').annotate(average=Sum('amount')).values('month','average').order_by('month')

    expenses_dict = get_year_dict()

    for group in grouped_expenses:
        expenses_dict[MONTHS[group['month']-1]] = round(group['average'],2)

    return JsonResponse({
        'title': f'Expenses in {year}',
        'data':{
            'labels':list(expenses_dict.keys()),
            'datasets':[{
                'label':'Amount ($)',
                'backgroundColor':color_primary,
                'borderColor':color_primary,
                'data':list(expenses_dict.values()),
            }]
        },
    })

@login_required
def get_expense_month_chart(request, year, month):
    username = request.user.username
    expenses = Transaction.objects.filter(owner__username=username, date_of_transaction__year=year, date_of_transaction__month=month, transaction_type='debit')
    grouped_expenses = expenses.values('transaction_category').annotate(average=Sum('amount'))\
        .values('transaction_category','average').order_by('transaction_category')

    expenses_dict = get_category_dict()

    for group in grouped_expenses:
        expenses_dict[group['transaction_category']] = round(group['average'],2)

    return JsonResponse({
        'title': f'Expenses in {MONTH_DICT[month]} {year}',
        'data':{
            'labels':[pair[1] for pair in CATEGORY_OPTIONS][:-1],
            'datasets':[{
                'label':'Amount ($)',
                'backgroundColor':color_primary,
                'borderColor':color_primary,
                'data':list(expenses_dict.values()),
            }]
        },
    })

@login_required
def get_expense_category_chart(request, year, category):
    username = request.user.username
    expenses = Transaction.objects.filter(owner__username=username, date_of_transaction__year=year,transaction_category=category)
    grouped_expenses = expenses.annotate(month=ExtractMonth('date_of_transaction'))\
        .values('month').annotate(average=Sum('amount')).values('month','average').order_by('month')

    expenses_dict = get_year_dict()

    for group in grouped_expenses:
        expenses_dict[MONTHS[group['month']-1]] = round(group['average'],2)

    return JsonResponse({
        'title': f'Expenses in {year} for {CATEGORY_DICT[category]}',
        'data':{
            'labels':list(expenses_dict.keys()),
            'datasets':[{
                'label':'Amount ($)',
                'backgroundColor':color_primary,
                'borderColor':color_primary,
                'data':list(expenses_dict.values()),
            }]
        },
    })

@login_required
def statistics_view(request):
    return render(request, 'budget/userview.html', {})

    
