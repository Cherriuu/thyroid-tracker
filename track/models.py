from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.
class Condition(models.Model):
    CONDITION_CHOICES = [
        ('hypo', 'Hypothyroidism'),
        ('hyper', 'Hyperthyroidism'),
        ('hashimotos', "Hashimoto's"),
        ('other', 'Other'),
    ]
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    condition_type = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    date_of_diagnosis = models.DateField()
    current_medication = models.CharField(max_length=100)
    current_dosage = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.get_condition_type_display()} - {self.current_medication}"

class SymptomLog(models.Model):
    SYMPTOM_CHOICES = [
        ('fatigue', 'Fatigue'),
        ('weight_change', 'Weight Change'),
        ('cold_sensitivity', 'Cold Sensitivity'),
        ('mood_changes', 'Mood Changes'),
        ('hair_thinning', 'Hair Thinning'),
        ('heart_palpitations', 'Heart Palpitations'),
        ('brain_fog', 'Brain Fog'),
        ('joint_pain', 'Joint pain'),
    ]
    owner = models.ForeignKey(Condition, on_delete=models.CASCADE)

    date_logged = models.DateField(auto_now_add=True)
    symptom_type = models.CharField(max_length=30, choices=SYMPTOM_CHOICES)
    severity = models.IntegerField(choices=[(i, i) for i in range (1,6)])
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.get_symptom_type_display()} ({self.severity} / 5)"
    
class MedicationLog(models.Model):
    date_taken = models.DateField()
    time_taken = models.TimeField()
    taken_with_food = models.BooleanField(default=False)
    minutes_from_coffee_or_calcium = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    owner = models.ForeignKey(Condition, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} {self.time_taken}" 

class LabResult(models.Model):
    TEST_CHOICES = [
        ('tsh', 'TSH'),
        ('free_t3', 'Free T3'),
        ('free_t4', 'Free T4'),
    ]

    date_drawn = models.DateField()
    test_type = models.CharField(max_length=10, choices=TEST_CHOICES)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    reference_range_low = models.DecimalField(max_digits=6, decimal_places=2)
    reference_range_high = models.DecimalField(max_digits=6, decimal_places=2)

    owner = models.ForeignKey(Condition, on_delete=models.CASCADE)

    def normalized_score(self):
        range_span = self.reference_range_high - self.reference_range_low

        if range_span == 0:
            return None
        return round(((self.value - self.reference_range_low) / range_span) * 100, 1)

    def __str__(self):
        return f"{self.date_drawn} - {self.get_test_type_display()}: {self.value}"