from django import forms

from .models import Analysis


class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = (
            'image_path',
        )
        widgets = {
            'image_path': forms.TextInput(attrs={
                'placeholder': ' /image/sample.jpg',
            }),
        }
