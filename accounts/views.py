from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

# Used in forgot password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMessage

from accounts.models import Account
from accounts.forms import RegistrationForm, AccountUpdateForm


@login_required(login_url='login')
def index(request):
    context = {
        "site" : "Dashboard - Marketing Solution",
    }
    return render(request, 'index.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            is_reseller = form.cleaned_data.get('is_reseller')

            if request.user.is_authenticated and request.user.is_reseller:
                # If the logged-in user is a reseller, create a user under the reseller's account
                reseller = request.user
                user = form.save(commit=False)
                user.set_password(password)
                user.is_reseller = is_reseller
                user.reseller = reseller
                user.save()
                form.save_m2m()
                if is_reseller:
                    messages.success(request, 'Reseller created successfully!')
                else:
                    messages.success(request, 'User created successfully!')
                return redirect('manageUsers')

            else:
                # If the user is not a reseller or not logged in, create a new superuser
                user = Account.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_reseller=is_reseller,
                )
                user.save()
                if is_reseller:
                    messages.success(request, 'Reseller created successfully!')
                else:
                    messages.success(request, 'User created successfully!')
                return render(request, 'accounts/login.html')

        context = {
            'form': form,
        }
        
        print(form.errors)
        return render(request, 'accounts/register.html', context)

    else:
        form = RegistrationForm()

    context = {
        'form': form,
        "site": "Register - Best Marketing Agency",
        }
    return render(request, 'accounts/register.html', context)


def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Check if user exists and is active
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            messages.error(request, 'Invalid login credentials')
            return render(request, 'accounts/login.html')

        if not user.is_active:
            messages.error(request, 'Your account is inactive.')
            return render(request, 'accounts/login.html')

        # Authenticate user
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid login credentials')
            return render(request, 'accounts/login.html')
    else:
        context = {
            "site": "Login - Best Marketing Agency",
            }
        return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def signout(request):
    auth.logout(request)
    messages.success(request=request, message='Logged out')
    return redirect('login')


@login_required
def my_profile(request):
    try:
        userprofile = Account.objects.get(email=request.user.email)
    except Account.DoesNotExist:
        userprofile = None

    # if userprofile is None:
    #     userprofile = Account.objects.create(email=request.user.email)

    if request.method == 'POST':
        form = AccountUpdateForm(
            request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save()
            return redirect('myProfile')
    else:
        form = AccountUpdateForm(instance=userprofile)

    context = {
        'form': form, 
        'userprofile': userprofile,
        "site": "My Profile",
        }
    return render(request, 'accounts/my_profile.html', context)


@login_required
def update_profile(request):
    user_profile = request.user
    if request.method == 'POST':
        form = AccountUpdateForm(
            request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request=request, message='Profile updated!')
            return redirect('myProfile')
        else:
            messages.error(request=request, message='Something went wrong!')
    else:
        form = AccountUpdateForm(instance=user_profile)

    context = {
        'form': form,
        "site": "Update Profile",
        }

    return render(request, 'accounts/update_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # check if the current password is correct
        if request.user.check_password(password):
            # check if the new password matches the confirm password
            if new_password == confirm_password:
                # set the new password
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Your password was successfully updated!')
                return redirect('login')
            else:
                messages.error(request, 'New passwords do not match.')
                return redirect('myProfile')
        else:
            messages.error(request, 'Your current password was entered incorrectly.')
            return redirect('myProfile')
    return render(request, 'accounts/my_profile.html')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()
            messages.success(request, 'Password reset email has been sent to your registered email address')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')
        
    context = {
        "site": "Forgot Password",
        }
    return render(request, 'accounts/forgot_password.html', context)


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please enter your new password")
        return redirect('resetPassword')
    else:
        messages.error(request, "This link has been expired")
        return redirect('login')


def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully")
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')
            
    else:
        context = {
            "site": "Login - Best Marketing Agency",
        }
        return render(request, "accounts/reset_password.html", context)

