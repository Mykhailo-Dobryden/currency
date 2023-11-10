from django.http.response import HttpResponse

from currency.models import Rate, ContactUs


def rate_list(request):
    results = []
    rates = Rate.objects.all()

    for rate in rates:
        results.append(
            f"ID: {rate.id}, buy: {rate.buy}, sell: {rate.sell}, type: {rate.type}, "
            f"source: {rate.source}, created: {rate.created}<br>"
        )

    return HttpResponse(str(results))


def contact_us_list(request):
    resuslts = []
    contacts = ContactUs.objects.all()

    for contact in contacts:
        resuslts.append(
            f"ID: {contact.id}, email_from: {contact.email_from}, subject: {contact.subject}, message: {contact.message}"
        )

    return HttpResponse("<br>".join(resuslts))

# def contact_us(request):
