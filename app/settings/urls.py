from django.contrib import admin
from django.urls import include, path
from currency.views import IndexView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('account.urls')),

    path('', IndexView.as_view(), name='index'),

    path('currency/', include('currency.urls')),

    path('currency/api/', include('currency.api.urls')),
    path('api/account/', include('account.api.urls')),

    path("__debug__/", include("debug_toolbar.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
