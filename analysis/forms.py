from django import forms
import datetime
from django.core.files.storage import default_storage


class ImagePathForm(forms.Form):

    image_path = forms.fields.ChoiceField(
        choices=(),
        required=True,
        widget=forms.widgets.Select,
    )


class UploadImageForm(forms.Form):
    file = forms.ImageField()

    def save(self):
        now_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        upload_file = self.files['file']
        file_name = default_storage.save(
            now_date + '_' + upload_file.name, upload_file)
        return default_storage.url(file_name)
