from django import forms
from accounts.models import Account


class RegistrationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    is_reseller = forms.BooleanField(required=False)

    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))

    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))

    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={
        'class' : 'form-control',
        'placeholder' : 'Create Password',
    }))

    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={
        'class' : 'form-control',
        'placeholder' : 'Confirm Password',
    }))

    class Meta:
        model = Account
        fields = ('email', 'username')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Account.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_normalized = Account.objects.normalize_email(email)
        if Account.objects.filter(email=email_normalized).exists():
            raise forms.ValidationError("Email already exists.")
        return email_normalized

    def clean_confirm_password(self):
        # Check that the two password entries match
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords didn't match")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_reseller = self.cleaned_data['is_reseller']
        if commit:
            user.save()
            # Associate user with the reseller if applicable
            if self.cleaned_data['reseller']:
                reseller = self.cleaned_data['reseller']
                reseller.users.add(user)
            self.save_m2m()
        return user
    

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'first_name', 'last_name', 'phone_number', 'company_name', 'gst_number', 'address',
            'city', 'state', 'country', 'pincode',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your company name',
            }),
            'gst_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your GST number',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your city',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your state',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your country',
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your pincode',
            }),
        }