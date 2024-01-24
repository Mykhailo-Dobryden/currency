from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_yaml.renderers import YAMLRenderer

from django_filters.rest_framework import DjangoFilterBackend

from currency.api.throttling import RateThrottle, SourceThrottle
from currency.api.paginators import RatePagination
from currency.api.serializers import RateSerializer, SourceSerializer, ContactUsSerializer
from currency.filters import RateFilter, ContactUsFilter
from currency.models import Rate, Source, ContactUs


# class RateListAPIView(ListCreateAPIView):
#     queryset = Rate.objects.all().order_by('-created')
#     serializer_class = RateSerializer
#     renderer_classes = (JSONRenderer, XMLRenderer, YAMLRenderer)
#
# class RateDetailsAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Rate.objects.all().order_by('-created')
#     serializer_class = RateSerializer


class RateViewSet(ModelViewSet):
    queryset = Rate.objects.all().order_by('-created')
    serializer_class = RateSerializer
    renderer_classes = (JSONRenderer, YAMLRenderer, XMLRenderer, BrowsableAPIRenderer)
    pagination_class = RatePagination
    filterset_class = RateFilter
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    ordering_fields = ('buy', 'sell', 'created')
    throttle_classes = (RateThrottle,)


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
