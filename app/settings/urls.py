from django.contrib import admin
from django.urls import include, path

from currency.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('django.contrib.auth.urls')),
    path('auth/', include('account.urls')),

    path('', IndexView.as_view(), name='index'),

    path('currency/', include('currency.urls')),

    path("__debug__/", include("debug_toolbar.urls"))
]
