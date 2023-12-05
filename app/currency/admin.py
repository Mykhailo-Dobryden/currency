from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilterBuilder

from currency.models import Rate, Source, ContactUs


@admin.register(Rate)
class RateAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'buy',
        'sell',
        'source',
        'currency_type',
        'created',
    )

    list_filter = (
        'currency_type',
        ('created', DateRangeFilterBuilder()),
        'source',
    )

    search_fields = (
        'buy',
        'sell',
        'source',
    )

    readonly_fields = (
        'buy',
        'sell',
    )


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'source_url',
        'created',
    )

    list_filter = (
        'name',
    )

    search_fields = (
        'name',
        'source_url',
    )


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    verbose_name = 'Contact Us'

    list_display = (
        'id',
        'created',
        'name',
        'email_from',
        'subject',
        'body',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
