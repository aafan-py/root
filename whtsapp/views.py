# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# from .forms import WhtsappCampaignForm

# from whtsapp.models import WhtsappCampaign

# from django.http import HttpResponseRedirect
# from django.urls import reverse

# from .forms import WhtsappCampaignForm
# from .models import WhtsappCampaign

# from django.utils import timezone


# @login_required(login_url='login')
# def create_whtsapp_campaign(request):
#     if request.method == 'POST':
#         form = WhtsappCampaignForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = request.user # or set the user to a specific user object
#             numbers = form.cleaned_data['numbers']
#             message = form.cleaned_data['message']
#             image1 = form.cleaned_data['image1']
#             image2 = form.cleaned_data['image2']
#             image3 = form.cleaned_data['image3']
#             image4 = form.cleaned_data['image4']
#             video = form.cleaned_data['video']
#             pdf = form.cleaned_data['pdf']
            
#             whtsapp_campaign = WhtsappCampaign(
#                 user=user, numbers=numbers, 
#                 message=message, image1=image1, 
#                 image2=image2, image3=image3, image4=image4, 
#                 video=video, pdf=pdf,
#                 created_at=timezone.now(),
#                 )
#             whtsapp_campaign.save()
#             messages.success(request, 'Campaign Submitted Successfully!')
#             return HttpResponseRedirect(reverse('whtsappCampaign'))
        
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{error}")
#             return HttpResponseRedirect(reverse('whtsappCampaign'))

#     else:
#         form = WhtsappCampaignForm()

#     context = {
#         'form': form
#         }
    
#     return render(request, 'whtsapp/create_whtsapp_campaign.html', context)




from decimal import Decimal
from django.db import transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from accounts.models import Account
from .models import WhtsappCampaign
from .forms import WhtsappCampaignForm

@login_required(login_url='login')
@transaction.atomic
def create_whtsapp_campaign(request):
    if request.method == 'POST':
        form = WhtsappCampaignForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user # or set the user to a specific user object
            numbers = form.cleaned_data['numbers']
            message = form.cleaned_data['message']
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']
            image3 = form.cleaned_data['image3']
            image4 = form.cleaned_data['image4']
            video = form.cleaned_data['video']
            pdf = form.cleaned_data['pdf']
            
            service_name = 'WAPP' # Replace this with the actual service name from the form data
            print(f'Service Name = {service_name}')

            service_rate = user.servicerate_set.get(service__service=service_name).rate 
            print(f'Service Rate = {service_rate}')

            total_cost = len(numbers.split('\n')) * Decimal(service_rate)
            print(f'Total Cost = {total_cost}')

            # Update the account's wallet_balance
            user.wallet_balance -= total_cost
            user.save()

            whtsapp_campaign = WhtsappCampaign(
                user=user, numbers=numbers, 
                message=message, image1=image1, 
                image2=image2, image3=image3, image4=image4, 
                video=video, pdf=pdf,
                created_at=timezone.now(),
                )
            whtsapp_campaign.save()
            messages.success(request, 'Campaign Submitted Successfully!')
            return HttpResponseRedirect(reverse('whtsappCampaign'))
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
            return HttpResponseRedirect(reverse('whtsappCampaign'))

    else:
        form = WhtsappCampaignForm()

    context = {
        'form': form
        }
    
    return render(request, 'whtsapp/create_whtsapp_campaign.html', context)



def whtsapp_report(request):
    user_id =  request.user.id
    reports = WhtsappCampaign.objects.filter(user=user_id).order_by('-created_at')
    
    context = {
        'reports': reports
        }
    return render(request, 'whtsapp/whtsapp_report.html', context)