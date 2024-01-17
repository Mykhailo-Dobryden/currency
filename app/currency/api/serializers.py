from rest_framework import serializers

from currency.models import Rate, Source, ContactUs

from django.conf import settings
from django.core.mail import send_mail


class RateSerializer(serializers.ModelSerializer):
    currency_type = serializers.CharField(source='get_currency_type_display')

    class Meta:
        model = Rate
        fields = ('id', 'created', 'currency_type', 'sell', 'buy', 'source')


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('id', 'name', 'source_url', 'code_name')


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('id', 'name', 'email_from', 'subject', 'body')

    def _send_mail(self):
        subject = 'New Contact Us Message'
        body = f"""
                        Name: {self.validated_data['name']}
                        Email: {self.validated_data['email_from']}
                        Subject: {self.validated_data['subject']}
                        Message: {self.validated_data['body']}
                        """
        # body = "Saved in serializer"
        send_mail(
            subject=subject,
            message=body,
            from_email=self.validated_data['email_from'],
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

    def save(self, **kwargs):
        self._send_mail()
        return super().save(**kwargs)  # TODO: ask about this a teacher
