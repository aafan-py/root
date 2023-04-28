from django import forms
from accounts.models import Account
from .models import Wallet

class CreditDebitForm(forms.Form):
    user_id = forms.IntegerField()
    transaction_type = forms.ChoiceField(choices=Wallet.TRANSACTION_TYPE_CHOICES)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    remark = forms.CharField(max_length=100, required=False)

    def __init__(self, reseller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id'].queryset = Account.objects.filter(reseller=reseller)

    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        try:
            user = Account.objects.get(id=user_id)
        except Account.DoesNotExist:
            raise forms.ValidationError("Invalid user ID")
        return user_id