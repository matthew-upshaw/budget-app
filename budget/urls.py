from django.urls import path

from . import views

urlpatterns = [
    path('chart/filter-options/', views.get_filter_options, name='chart-filter-options'),
    path('chart/expenses/<int:year>/', views.get_expense_chart, name='chart-expenses'),
    path('chart/expenses/<int:year>/<int:month>/', views.get_expense_month_chart, name='chart-expenses-by-month'),
    path('chart/expenses/<int:year>/<str:category>/', views.get_expense_category_chart, name='chart-expenses-by-category'),
]

urlpatterns += [
    path('transaction/<str:username>/list-all/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transaction/add/', views.TransactionCreateView.as_view(), name='add-transaction'),
    path('transaction/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('transaction/<int:pk>/update', views.TransactionUpdateView.as_view(),name='transaction-update'),
    path('transaction/<int:pk>/delete/', views.TransactionDeleteView.as_view(),name='transaction-delete'),
]