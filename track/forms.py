from django import forms
from .models import Condition, SymptomLog, MedicationLog, LabResult

class SymptomLogForm(forms.ModelForm):
    class Meta:
        model = SymptomLog
        fields = ['symptom_type', 'severity', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type' : 'date'}),
            'notes' : forms.Textarea(attrs={'cols': 80}),
        }

class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = ['condition_type', 'date_of_diagnosis', 'current_medication', 'current_dosage']
        widgets = {'date_of_diagnosis': forms.DateInput(attrs={'type': 'date'})}

class MedicationLogForm(forms.ModelForm):
    class Meta:
        model = MedicationLog
        fields = ['date_taken', 'time_taken', 'taken_with_food', 'minutes_from_coffee_or_calcium']
        widgets = {
            'date_taken': forms.DateInput(attrs={'type' : 'date'}),
            'time_taken': forms.TimeInput(attrs={'type' : 'time'}),
        }

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ['date_drawn', 'test_type', 'value', 'reference_range_low', 'reference_range_high']
        widgets = {
            'date_drawn': forms.DateInput(attrs={'type' : 'date'})
        }