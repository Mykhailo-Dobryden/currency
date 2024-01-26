from django.core.cache import cache

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer

from django_filters.rest_framework import DjangoFilterBackend

from currency.choices import CurrencyTypeChoices
from currency.constants import LATEST_RATES_CACHE_KEY
from currency.api.throttling import RateThrottle, SourceThrottle
from currency.api.paginators import RatePagination
from currency.api.serializers import RateSerializer, SourceSerializer, ContactUsSerializer
from currency.filters import RateFilter, ContactUsFilter
from currency.models import Rate, Source, ContactUs


class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all().order_by('-created')
    serializer_class = RateSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, YAMLRenderer, XMLRenderer)
    pagination_class = RatePagination
    filterset_class = RateFilter
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    ordering_fields = ('buy', 'sell', 'created')
    throttle_classes = (RateThrottle,)
    permission_classes = (AllowAny,)

    @action(methods=('GET',), detail=False, serializer_class=RateSerializer)
    def latest(self, request, *args, **kwargs):
        cached_data = cache.get(LATEST_RATES_CACHE_KEY)
        if cached_data is not None:
            return Response(cached_data)

        sources = Source.objects.all()

        latest_rates = []
        for source in sources:
            for currency in CurrencyTypeChoices:
                rate = Rate.objects.filter(source=source, currency_type=currency).order_by('-created').first()

                if rate is not None:
                    latest_rates.append(RateSerializer(instance=rate).data)

        cache.set(LATEST_RATES_CACHE_KEY, latest_rates, 60 * 60 * 24 * 7)  # 1 week

        return Response(latest_rates)


class ContactUsViewSet(ModelViewSet):
    queryset = ContactUs.objects.all().order_by('-created')
    serializer_class = ContactUsSerializer
    renderer_classes = (JSONRenderer, YAMLRenderer, XMLRenderer, BrowsableAPIRenderer,)
    filterset_class = ContactUsFilter
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    ordering_fields = ('name', 'email_from', 'subject')
    search_fields = ('name', 'email_from', 'subject', 'body')


class SourceViewSet(ModelViewSet):
    queryset = Source.objects.all().order_by('-created')
    serializer_class = SourceSerializer
    renderer_classes = (JSONRenderer, YAMLRenderer, XMLRenderer, BrowsableAPIRenderer)
    throttle_classes = (SourceThrottle,)
