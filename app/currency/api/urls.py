from rest_framework import routers

from currency.api.views import RateViewSet, SourceViewSet, ContactUsViewSet

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'rates', RateViewSet, basename='rate')
router.register(r'contact-us', ContactUsViewSet, basename='contact-us')
router.register(r'sources', SourceViewSet, basename='source')

app_name = 'currency_api'

urlpatterns = [
    # path('rates/', RateListAPIView.as_view(), name='rate-list'),
    # path('rates/<int:pk>/', RateDetailsAPIView.as_view(), name='rate-details'),
    # path('sources/', SourceListAPIView.as_view(), name='source'),
    ] + router.urls
