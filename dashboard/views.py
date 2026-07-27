from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from contacts.models import Contact
# Create your views here.


@login_required(login_url="accounts:login")
def home_view(requests):
    
    return render(requests, "home.html", {
        'total_user': User.objects.count(),
        'total_contacts':Contact.objects.count()
    })


def sobre_view(requests):
    return render(requests, "sobre.html", {})
