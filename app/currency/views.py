from django.shortcuts import render

from currency.models import Rate, ContactUs


def rate_list(request):
    rates = Rate.objects.all()
    context = {
        'title': 'Rates list',
        'rates': rates,
    }

    return render(request, 'rate_list.html', context)


def contact_us_list(request):
    contacts = ContactUs.objects.all()
    context = {
        'title': 'Contacts List',
        'contacts': contacts,
    }

    return render(request, 'contact_us.html', context)
