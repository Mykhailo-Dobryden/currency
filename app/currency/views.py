from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from currency.models import Rate, ContactUs, Source
from currency.forms import SourceCreateForm


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


def source_create(request):
    if request.method == 'POST':
        form = SourceCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')
    else:
        form = SourceCreateForm()

    context = {
        'title': 'Source create',
        'form': form,
    }

    return render(request, 'source_create.html', context)


def source_update(request, pk):
    source = get_object_or_404(Source, id=pk)

    if request.method == 'POST':
        form = SourceCreateForm(request.POST, instance=source)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/source/list/')

    elif request.method == 'GET':
        form = SourceCreateForm(instance=source)

    context = {
        'title': 'Source Update',
        'form': form,
    }

    return render(request, 'source_update.html', context)


def source_delete(request, pk):
    source = get_object_or_404(Source, id=pk)

    if request.method == 'GET':
        context = {
            'title': 'Source Delete',
            'source': source,
        }
        return render(request, 'source_delete.html', context)

    elif request.method == 'POST':
        source.delete()
        return HttpResponseRedirect('/source/list/')


def source_list(request):
    sources = Source.objects.all()
    context = {
        'title': 'Source list',
        'sources': sources,
    }

    return render(request, 'source_list.html', context)


def source_detail(request, pk):
    source = get_object_or_404(Source, id=pk)
    context = {
        'title': 'Source detail',
        'source': source,
    }

    return render(request, 'source_detail.html', context)
