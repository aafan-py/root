from django.urls import path
from . import views

urlpatterns = [
    path('campaign/',views.create_whtsapp_campaign,name='whtsappCampaign'),
    path('report/',views.whtsapp_report,name='whtsappReport'),
]