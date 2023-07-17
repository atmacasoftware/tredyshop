from django.shortcuts import render, redirect
from customer.models import Subscription

# Create your views here.

def comingsoon(request):

    if 'subscriptionBtn' in request.POST:
        email = request.POST.get('email')
        ip = request.META.get('REMOTE_ADDR')

        if email != '':
            Subscription.objects.create(email=email, ip=ip)
            return redirect('comingsoon')

    return render(request,'waitingdeploy/coming_soon.html')