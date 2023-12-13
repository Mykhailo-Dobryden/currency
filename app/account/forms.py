from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserSignUpForm(forms.ModelForm):
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ['email',
                  'password1',
                  'password2',
                  'first_name',
                  'last_name',
                  ]

        labels = {
            'email': _('Email'),
            'password1': _('Password'),
            'password2': _('Confirm password'),
            'first_name': _('First name'),
            'last_name': _('Last name'),
        }

    def clean(self):
        cleaned_data: dict = super().clean()

        if not self.errors:
            validate_password(cleaned_data['password1'])

            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError(_('Passwords do not match!'))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.save()

        self._send_activation_email()
        return user

    def _send_activation_email(self):
        activation_path = reverse('account:activate', args=(self.instance.username,))
        subject = 'Thank you for registering to our site!'
        body = f"""
        Please, click on the link below to verify your account:
        {settings.HTTP_METHOD}://{settings.DOMAIN}{activation_path}
        """

        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.instance.email],
            fail_silently=False,
        )
