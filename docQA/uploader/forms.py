from django import forms
from .models import UploadedDocument

class DocumentForm(forms.ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ('file',)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        # Validate file type
        if not file.name.endswith(('.xlsx', '.xls')):
            raise forms.ValidationError('Only Excel files are allowed!')
        return file
