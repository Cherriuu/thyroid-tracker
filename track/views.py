from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Condition, SymptomLog, MedicationLog, LabResult
from .forms import ConditionForm, SymptomLogForm, MedicationLogForm, LabResultForm

def home(request):
    condition = None
    recent_symptoms = []
    recent_medications = []
    recent_labs = []

    if request.user.is_authenticated:
        condition = Condition.objects.filter(owner=request.user).first()
        if condition:
            recent_symptoms = SymptomLog.objects.filter(owner=condition).order_by('-date_logged')[:3]
            recent_medications = MedicationLog.objects.filter(owner=condition).order_by('-date_taken')[:3]
            recent_labs = LabResult.objects.filter(owner=condition).order_by('-date_drawn')[:3]

    context = {
        'condition': condition,
        'recent_symptoms': recent_symptoms,
        'recent_medications': recent_medications,
        'recent_labs': recent_labs,
    }
    return render(request, 'track/home.html', context)


def check_condition_owner(request, condition):
    if condition.owner != request.user:
        raise Http404

@login_required
def setup_condition(request):
    if request.method != 'POST':
        form = ConditionForm()
    else:
        form = ConditionForm(request.POST)
        if form.is_valid():
            new_condition = form.save(commit=False)
            new_condition.owner = request.user
            new_condition.save()
            return HttpResponseRedirect(reverse('track:home'))

    context = {'form': form}
    return render(request, 'track/new_condition.html', context)

@login_required
def symptom_list(request):
    condition = Condition.objects.get(owner=request.user)
    check_condition_owner(request, condition)

    symptoms = SymptomLog.objects.filter(owner=condition).order_by('-date_logged')

    context = {'condition': condition, 'symptoms': symptoms}
    return render(request, 'track/symptom_list.html', context)


@login_required
def add_symptom(request):
    condition = Condition.objects.get(owner=request.user)
    check_condition_owner(request, condition)

    if request.method != 'POST':
        form = SymptomLogForm()
    else:
        form = SymptomLogForm(request.POST)
        if form.is_valid():
            new_symptom = form.save(commit=False)
            new_symptom.owner = condition
            new_symptom.save()
            return HttpResponseRedirect(reverse('track:home'))

    context = {'condition': condition, 'form': form}
    return render(request, 'track/new_symptom.html', context)


@login_required
def edit_symptom(request, symptom_id):
    symptom = SymptomLog.objects.get(id=symptom_id)
    condition = symptom.owner
    check_condition_owner(request, condition)

    if request.method != 'POST':
        form = SymptomLogForm(instance=symptom)
    else:
        form = SymptomLogForm(instance=symptom, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('track:home'))

    context = {'symptom': symptom, 'condition': condition, 'form': form}
    return render(request, 'track/edit_symptom.html', context)


@login_required
def delete_symptom(request, symptom_id):
    symptom = SymptomLog.objects.get(id=symptom_id)
    condition = symptom.owner
    check_condition_owner(request, condition)

    if request.method == 'POST':
        symptom.delete()
        return HttpResponseRedirect(reverse('track:home'))

    context = {'symptom': symptom, 'condition': condition}
    return render(request, 'track/delete_symptom.html', context)

@login_required
def medication_list(request):
    condition = Condition.objects.get(owner=request.user)
    check_condition_owner(request, condition)

    medications = MedicationLog.objects.filter(owner=condition).order_by('-date_taken')

    context = {'condition': condition, 'medications': medications}
    return render(request, 'track/medication_list.html', context)

@login_required
def add_medication(request):
    condition = Condition.objects.get(owner=request.user)
    check_condition_owner(request, condition)

    if request.method != 'POST':
        form = MedicationLogForm()
    else:
        form = MedicationLogForm(request.POST)
        if form.is_valid():
            new_medication = form.save(commit=False)
            new_medication.owner = condition
            new_medication.save()
            return HttpResponseRedirect(reverse('track:home'))

    context = {'condition': condition, 'form': form}
    return render(request, 'track/add_medication.html', context)


@login_required
def edit_medication(request, medication_id):
    medication = MedicationLog.objects.get(id=medication_id)
    condition = medication.owner
    check_condition_owner(request, condition)

    if request.method != 'POST':
        form = MedicationLogForm(instance=medication)
    else:
        form = MedicationLogForm(instance=medication, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('track:home'))

    context = {'medication': medication, 'condition': condition, 'form': form}
    return render(request, 'track/edit_medication.html', context)

@login_required
def delete_medication(request, medication_id):
    medication = MedicationLog.objects.get(id=medication_id)
    condition = medication.owner
    check_condition_owner(request, condition)

    if request.method == 'POST':
        medication.delete()
        return HttpResponseRedirect(reverse('track:home'))

    context = {'medication': medication, 'condition': condition}
    return render(request, 'track/delete_medication.html', context)

@login_required
def lab_list(request):
    condition = Condition.objects.get(owner=request.user)
    check_condition_owner(request, condition)

    labs = LabResult.objects.filter(owner=condition).order_by('-date_drawn')

    context = {'condition': condition, 'labs': labs}
    return render(request, 'track/lab_list.html', context)


@login_required
def add_lab(request):
    condition = Condition.objects.get(owner=request.user)
    check_condition_owner(request, condition)

    if request.method != 'POST':
        form = LabResultForm()
    else:
        form = LabResultForm(data=request.POST)
        if form.is_valid():
            lab = form.save(commit=False)
            lab.owner = condition
            lab.save()
            return HttpResponseRedirect(reverse('track:home'))

    context = {'condition': condition, 'form': form}
    return render(request, 'track/add_lab.html', context)

@login_required
def edit_lab(request, lab_id):
    lab = LabResult.objects.get(id=lab_id)
    condition = lab.owner
    check_condition_owner(request, condition)

    if request.method != 'POST':
        form = LabResultForm(instance=lab)
    else:
        form = LabResultForm(instance=lab, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('track:home'))

    context = {'lab': lab, 'condition': condition, 'form': form}
    return render(request, 'track/edit_lab.html', context)

@login_required
def delete_lab(request, lab_id):
    lab = LabResult.objects.get(id=lab_id)
    condition = lab.owner
    check_condition_owner(request, condition)

    if request.method == 'POST':
        lab.delete()
        return HttpResponseRedirect(reverse('track:home'))

    context = {'lab': lab, 'condition': condition}
    return render(request, 'track/delete_lab.html', context)



