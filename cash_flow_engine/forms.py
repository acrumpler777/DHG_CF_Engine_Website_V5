from django import forms

from .models import fileUpload

class fileUploadForm(forms.ModelForm):
    class Meta:
        model = fileUpload
        fields = ('filetxt', )
        # widgets = {
        #     'calculated_file': forms.HiddenInput(),
        # }