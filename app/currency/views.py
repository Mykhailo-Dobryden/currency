from datetime import datetime, timedelta
import re

from django.urls import reverse_lazy
from django.views.generic import (CreateView, UpdateView,
                                  DeleteView, DetailView, TemplateView)

from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from currency.filters import RateFilter, ContactUsFilter, SourceFilter
from currency.models import Rate, ContactUs, Source
from currency.forms import (SourceCreateForm,
                            RateCreateForm,
                            ContactUsCreateForm)
from currency.tasks import send_email_in_background


class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {'title': 'Home'}


class RateListView(FilterView):
    paginate_by = 50
    queryset = Rate.objects.all().select_related('source')
    template_name = 'rate_list.html'
    extra_context = {'title': 'Rate List'}
    filterset_class = RateFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        query_parameters = self.request.GET.urlencode()
        # context['filter_params'] = '&'.join(
        #     f'{key}={value}' for key, value in self.request.GET.items()
        #     if key != 'page'
        # )

        context['filter_params'] = re.sub(r'page=\d+', '', query_parameters).lstrip('&')
        return context


class RateCreateView(CreateView):
    form_class = RateCreateForm
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'rate_create.html'
    extra_context = {'title': 'Rate Create'}


class RateUpdateView(UserPassesTestMixin, UpdateView):
    model = Rate
    form_class = RateCreateForm
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'rate_update.html'
    extra_context = {'title': 'Rate Update'}

    def test_func(self):
        return self.request.user.is_superuser


class RateDeleteView(UserPassesTestMixin, DeleteView):
    model = Rate
    success_url = reverse_lazy('currency:rate-list')
    template_name = 'rate_delete.html'
    extra_context = {'title': 'Rate Delete'}

    def test_func(self):
        return self.request.user.is_superuser


class RateDetailsView(LoginRequiredMixin, DetailView):
    model = Rate
    template_name = 'rate_details.html'
    extra_context = {'title': 'Rate Details'}


class ContactUsListView(FilterView):
    paginate_by = 3
    queryset = ContactUs.objects.all()
    template_name = 'contact_us_list.html'
    extra_context = {'title': 'Contact Us List'}
    filterset_class = ContactUsFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        query_parameters = self.request.GET.urlencode()
        context['filter_params'] = re.sub(r'page=\d+', '', query_parameters).lstrip('&')
        return context


class ContactUsCreateView(CreateView):
    form_class = ContactUsCreateForm
    success_url = reverse_lazy('currency:contactus-list')
    template_name = 'contact_us_create.html'
    extra_context = {'title': 'Contact Us Create'}

    def _send_email(self):
        subject = 'New Contact Us Message'
        body = f"""
                Name: {self.object.name}
                Email: {self.object.email_from}
                Subject: {self.object.subject}
                Body: {self.object.body}
                """

        eta = datetime.now() + timedelta(seconds=10)
        send_email_in_background.apply_async(
            kwargs={
                'subject': subject,
                'body': body,
            },
            eta=eta
        )

    def form_valid(self, form):
        redirect = super().form_valid(form)

        self._send_email()

        return redirect


class ContactUsUpdateView(UserPassesTestMixin, UpdateView):
    model = ContactUs
    form_class = ContactUsCreateForm
    success_url = reverse_lazy('currency:contactus-list')
    template_name = 'contact_us_update.html'
    extra_context = {'title': 'Contact Us Update'}

    def test_func(self):
        return self.request.user.is_superuser


class ContactUsDeleteView(UserPassesTestMixin, DeleteView):
    model = ContactUs
    success_url = reverse_lazy('currency:contactus-list')
    template_name = 'contact_us_delete.html'
    context_object_name = 'contact'
    extra_context = {'title': 'Contact Us Delete'}

    def test_func(self):
        return self.request.user.is_superuser


class ContactUsDetailsView(LoginRequiredMixin, DetailView):
    model = ContactUs
    template_name = 'contact_us_details.html'
    context_object_name = 'contact'
    extra_context = {'title': 'Contact Us Details'}


class SourceListView(FilterView):
    paginate_by = 2
    queryset = Source.objects.all()
    template_name = 'source_list.html'
    extra_context = {'title': 'Source list'}
    filterset_class = SourceFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        query_parameters = self.request.GET.urlencode()
        context['filter_params'] = re.sub(r'page=\d+', '', query_parameters).lstrip('&')
        return context


class SourceCreateView(CreateView):
    form_class = SourceCreateForm
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_create.html'
    extra_context = {'title': 'Source create'}


class SourceUpdateView(UpdateView):
    model = Source
    form_class = SourceCreateForm
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_update.html'
    extra_context = {'title': 'Source update'}


class SourceDeleteView(DeleteView):
    model = Source
    success_url = reverse_lazy('currency:source-list')
    template_name = 'source_delete.html'
    extra_context = {'title': 'Source Delete'}


class SourceDetailsView(DetailView):
    model = Source
    template_name = 'source_details.html'
    extra_context = {'title': 'Source Details'}
