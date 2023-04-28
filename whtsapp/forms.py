from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import WhtsappCampaign

class WhtsappCampaignForm(forms.ModelForm):
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)
    image4 = forms.ImageField(required=False)
    video = forms.FileField(required=False)
    pdf = forms.FileField(required=False)

    class Meta:
        model = WhtsappCampaign
        fields = ['numbers', 'message', 'image1', 'image2', 'image3', 'image4', 'video', 'pdf']

    def clean(self):
        cleaned_data = super().clean()
        image1 = cleaned_data.get('image1')
        image2 = cleaned_data.get('image2')
        image3 = cleaned_data.get('image3')
        image4 = cleaned_data.get('image4')
        video = cleaned_data.get('video')
        pdf = cleaned_data.get('pdf')

        # Validate each image
        if image1:
            if image1.size > 250 * 1024:
                raise ValidationError(_('Image 1 file size must be under 250 KB.'))
        if image2:
            if image2.size > 250 * 1024:
                raise ValidationError(_('Image 2 file size must be under 250 KB.'))
        if image3:
            if image3.size > 250 * 1024:
                raise ValidationError(_('Image 3 file size must be under 250 KB.'))
        if image4:
            if image4.size > 250 * 1024:
                raise ValidationError(_('Image 4 file size must be under 250 KB.'))

        # Validate the video
        if video:
            if video.size > 3 * 1024 * 1024:
                raise ValidationError(_('Video file size must be under 3 MB.'))

        # Validate the PDF
        if pdf:
            if pdf.size > 1024 * 1024:
                raise ValidationError(_('PDF file size must be under 1 MB.'))

        return cleaned_data
