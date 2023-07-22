from django import forms
from .models import Report

# Model Form | Very similar to model serializer
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('name', 'remarks')


