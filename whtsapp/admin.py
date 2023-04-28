from django.contrib import admin
from .models import WhtsappCampaign
from django.db.models import Q


@admin.register(WhtsappCampaign)
class WhtsappCampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_display_links = ('user',)
    readonly_fields = ('created_at',)
    search_fields = ('user',)
    ordering = ()

    search_fields = ['user__username']
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(Q(user__id=search_term_as_int))
        except ValueError:
            pass
        return queryset, use_distinct