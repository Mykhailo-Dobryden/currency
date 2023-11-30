"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from currency.views import (
    RateListView, RateCreateView, RateUpdateView, RateDeleteView,
    RateDetailsView, SourceListView, SourceCreateView, SourceUpdateView,
    SourceDeleteView, SourceDetailsView, ContactUsListView, ContactUsCreateView,
    ContactUsUpdateView, ContactUsDeleteView, ContactUsDetailsView)


app_name = 'currency'

urlpatterns = [
    path('rate-list/', RateListView.as_view(), name='rate-list'),
    path('rate-create/', RateCreateView.as_view(), name='rate-create'),
    path('rate-update/<int:pk>/', RateUpdateView.as_view(), name='rate-update'),
    path('rate-delete/<int:pk>/', RateDeleteView.as_view(), name='rate-delete'),
    path('rate-details/<int:pk>/', RateDetailsView.as_view(), name='rate-details'),

    path('contact-us-list/', ContactUsListView.as_view(), name='contactus-list'),
    path('contact-us-create/', ContactUsCreateView.as_view(), name='contactus-create'),
    path('contact-us-update/<int:pk>/', ContactUsUpdateView.as_view(), name='contactus-update'),
    path('contact-us-delete/<int:pk>/', ContactUsDeleteView.as_view(), name='contactus-delete'),
    path('contact-us-details/<int:pk>/', ContactUsDetailsView.as_view(), name='contactus-details'),


    path('source-create/', SourceCreateView.as_view(), name='source-create'),
    path('source-list/', SourceListView.as_view(), name='source-list'),
    path('source-update/<int:pk>/', SourceUpdateView.as_view(), name='source-update'),
    path('source-delete/<int:pk>/', SourceDeleteView.as_view(), name='source-delete'),
    path('source-details/<int:pk>/', SourceDetailsView.as_view(), name='source-details'),
]
