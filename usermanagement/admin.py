from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from .models import Wallet, ServiceRate, Service

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet_balance')
    list_display_links = ('user',)
    readonly_fields = ()
    search_fields = ['user__username']
    ordering = ()
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(Q(user__id=search_term_as_int))
        except ValueError:
            pass
        return queryset, use_distinct


@admin.register(Service)
class Service(admin.ModelAdmin):
    list_display = ('service',)
    list_display_links = ('service',)
    readonly_fields = ()
    search_fields = ['service']
    ordering = ()
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(Q(user__id=search_term_as_int))
        except ValueError:
            pass
        return queryset, use_distinct


@admin.register(ServiceRate)
class ServiceRate(admin.ModelAdmin):
    list_display = ('user', 'service', 'rate')
    list_display_links = ('user',)
    readonly_fields = ()
    search_fields = ['user__username']
    ordering = ()
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(Q(user__id=search_term_as_int))
        except ValueError:
            pass
        return queryset, use_distinct