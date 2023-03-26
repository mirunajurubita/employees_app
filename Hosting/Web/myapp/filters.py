import django_filters
from django_filters import DateFilter
from.models import *
from django import forms

class TaskFilterForm(forms.Form):
    COLUMN_CHOICES = [
        ('started_at__date', 'Started at'),
        ('deadline__date', 'Deadline'),
        ('closed_at__date', 'Completed at'),
    ]
    column = forms.ChoiceField(choices=COLUMN_CHOICES)
    value = forms.CharField()

class ClosedTaskFilterForm(forms.Form):
    COLUMN_CHOICES = [
        ('started_at__date', 'Started at'),
        ('deadline__date', 'Deadline'),
        ('closed_at__date', 'Completed at'),
    ]
    column = forms.ChoiceField(choices=COLUMN_CHOICES)
    value = forms.CharField()

class EmployeeReporsFilterForm(forms.Form):
    COLUMN_CHOICES = [
        ('current_date__date', 'Date'),
        ('type', 'Type'),
    ]
    column = forms.ChoiceField(choices=COLUMN_CHOICES)
    value = forms.CharField()

