from django.urls import path
from . import views

urlpatterns = [
    path('manageUsers/', views.manage_users, name='manageUsers'),
    path('loginAsUser/<int:user_id>', views.login_as_user, name='loginAsUser'),
    path('updateUserStatus/<int:user_id>', views.update_user_status, name='updateUserStatus'),
    path('transactionHistory/', views.transaction_history, name='transactionHistory'),
    path('creditDebit/', views.credit_debit, name='creditDebit'),
]
