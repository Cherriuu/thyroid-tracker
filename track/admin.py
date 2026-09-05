from django.contrib import admin
from .models import Condition, SymptomLog, MedicationLog, LabResult

# Register your models here.
admin.site.register(Condition)
admin.site.register(SymptomLog)
admin.site.register(MedicationLog)
admin.site.register(LabResult)
