from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import login
from django.contrib import messages

from accounts.models import Account
from .models import Wallet
from .forms import CreditDebitForm

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


@login_required(login_url="login")
def manage_users(request):
    # Retrieve the reseller object from the session data
    reseller = request.user
    if not reseller.is_reseller:
        return HttpResponseForbidden()

    # Retrieve the list of users associated with the reseller
    # users = Account.objects.filter(reseller=reseller).order_by('-date_joined')
    if request.user.is_superuser:
        users = Account.objects.all().order_by('-date_joined')
    elif request.user.is_reseller:
        users = Account.objects.filter(reseller=request.user).order_by('-date_joined')
    else:
        users = Account.objects.filter(id=request.user.id).order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        users = users.filter(
            Q(id__icontains=search_query)|
            Q(username__icontains=search_query)
            )

    # Pagination logic
    page_number = request.GET.get('page_number', 1)
    users_per_page = 5
    paginator = Paginator(users, users_per_page)
    try:
        users = paginator.page(page_number)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    # Construct the context dictionary and render the template
    context = {
        'reseller': reseller, 
        'users': users
        }
    return render(request, 'usermanagement/manage_users.html', context)


@login_required(login_url="signin")
def login_as_user(request, user_id):
    # Retrieve the target user object with the given ID
    user = Account.objects.get(id=user_id)

    # Check if the logged-in account is authorized to access the target user account
    if not is_authorized(request.user, user):
        messages.warning(request, "Invalid user access")
        return redirect("manage_users")

    # Log in the reseller as the selected user
    login(request, user)

    # Redirect to the user dashboard
    return redirect('index')


def is_authorized(request_account, target_account):
    # Check if the request account is the target account or a parent account of the target account
    if request_account == target_account:
        return True
    elif target_account.reseller is None:
        return False
    else:
        return is_authorized(request_account, target_account.reseller)
    

def transaction_history(request):
    user_id = request.user.id
    try:
        user = get_object_or_404(Account, id=user_id)
    except Account.DoesNotExist:
        messages.error(request, "Invalid user ID")
        return redirect(reverse("manage_users"))

    credits_debits = Wallet.objects.filter(user=user).order_by('-created_at')
    form = CreditDebitForm(reseller=user.reseller)

    context = {
        'user': user, 
        'credits_debits': credits_debits, 
        'form': form
        }
    return render(request, 'usermanagement/transaction_history.html', context)



@login_required(login_url="signin")
def credit_debit(request):
    reseller_id = request.user.id
    try:
        reseller = Account.objects.get(id=reseller_id)
    except Account.DoesNotExist:
        messages.error(request, "Invalid reseller ID")
        return redirect(reverse("manageUsers"))

    if not reseller.is_active:
        messages.error(request, "Reseller is inactive")
        return redirect(reverse("manageUsers"))

    users = Account.objects.filter(reseller=reseller_id)

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        try:
            user = Account.objects.get(id=user_id, reseller=reseller_id)
        except Account.DoesNotExist:
            messages.error(request, "Invalid user ID")
            return redirect(reverse("manageUsers"))

        if not user.is_active:
            messages.error(request, "User is inactive")
            return redirect(reverse("manageUsers"))

        form = CreditDebitForm(reseller=reseller, data=request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]
            remark = form.cleaned_data["remark"]
            transaction_type = form.cleaned_data["transaction_type"]

            wallet_credits = Wallet.objects.filter(user=user).order_by('-created_at')
            wallet_balance = wallet_credits.first().wallet_balance if wallet_credits else 0

            if transaction_type == 'credit':
                if amount > reseller.wallet_balance:
                    messages.error(request, "Your account doesn't have sufficient balance to perform credit.")
                    return redirect(reverse('creditDebit'))

                updated_wallet_balance = wallet_balance + amount

                wallet_credit = Wallet.objects.create(
                    user=user,
                    created_at=timezone.now(),
                    wallet_balance=updated_wallet_balance,
                    amount=amount,
                    transaction_type=transaction_type,
                    credit_on=timezone.now(),
                    remark=remark
                )
                wallet_credit.save()

                reseller.wallet_balance -= amount
                reseller.save()

                messages.success(
                    request, f"Wallet of {user} is credited with INR {amount}")
                return redirect(reverse('manageUsers'))

            elif transaction_type == 'debit':
                if amount <= 0:
                    messages.error(request, "Amount must be greater than 0.")
                    return redirect(reverse('creditDebit'))

                if amount > wallet_balance:
                    messages.error(request, 'User does not have sufficient balance to perform debit.')
                    return redirect(reverse('creditDebit'))

                wallet_credit = Wallet.objects.create(
                    user=user,
                    created_at=timezone.now(),
                    wallet_balance=wallet_balance - amount,
                    amount=amount,
                    transaction_type=transaction_type,
                    debit_on=timezone.now(),
                    remark=remark
                )
                wallet_credit.save()

                reseller.wallet_balance += amount
                reseller.save()

                user.wallet_balance = wallet_balance - amount
                user.save()

                messages.warning(
                    request, f"Wallet of {user} is debited with INR {amount}")
                return redirect(reverse('manageUsers'))

            else:
                messages.error(request, "Invalid request")
                return redirect(reverse('creditDebit'))

        else:
            messages.error(request, "Form is invalid.")
            return redirect(reverse('creditDebit'))

    else:
        form = CreditDebitForm(reseller=reseller)

    context = {
        "users": users,
        "form": form,
        "reseller": reseller,
    }
    return render(request, "usermanagement/credit_debit.html", context)


def update_user_status(request, user_id):
    if request.method == 'POST':
        user = Account.objects.get(id=user_id)
        user.is_active = not user.is_active  # toggle the status
        user.save()
    return redirect('manageUsers')