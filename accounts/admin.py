from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('username','last_login','date_joined','is_active','is_reseller', 'reseller_id')
    list_display_links = ('username',)
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ('is_active','is_reseller')
    fieldsets = (
        (None, {'fields': ('username','email','password', 'reseller')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'company_name', 'gst_number', 'address', 'city', 'state','country', 'pincode')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_reseller')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username','email','password', 'reseller')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'company_name', 'gst_number', 'address', 'city', 'state','country', 'pincode')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_reseller')}),
    )