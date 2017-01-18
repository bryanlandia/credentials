"""
Django forms for the credentials
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from credentials.apps.credentials.models import Signatory


class SignatoryModelForm(forms.ModelForm):
    """Signatory form with updated model fields."""
    title = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Signatory
        fields = '__all__'


class ProgramCertificateAdminForm(forms.ModelForm):
    def clean_program_uuid(self):
        site = self.cleaned_data['site']
        program_uuid = self.cleaned_data['program_uuid']
        program = site.siteconfiguration.get_program(program_uuid, ignore_cache=True)

        for organization in program['authoring_organizations']:
            if not organization['certificate_logo_image_url']:
                raise ValidationError(
                    _('All authoring organizations of the program MUST have a certificate image defined!'))

        return program_uuid
