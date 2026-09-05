from django.urls import path
from . import views

app_name = 'track'

urlpatterns = [
    path('', views.home , name='home'),
    path('setup/', views.setup_condition, name='setup_condition'),
    path('symptoms/', views.symptom_list, name='symptom_list'),
    path('symptoms/add', views.add_symptom, name='add_symptom'),
    path('symptoms/<int:symptom_id>/edit/', views.edit_symptom, name='edit_symptom'),
    path('symptoms/<int:symptom_id>/delete/', views.delete_symptom, name='delete_symptom'),
    path('medications/', views.medication_list, name='medication_list'),
    path('medications/add/', views.add_medication, name='add_medication'),
    path('medications/<int:medication_id>/edit/', views.edit_medication, name='edit_medication'),
    path('medications/<int:medication_id>/delete/', views.delete_medication, name='delete_medication'),
    path('labs/', views.lab_list, name='lab_list'),
    path('labs/add', views.add_lab, name='add_lab'),
    path('labs/<int:lab_id>/edit/', views.edit_lab, name='edit_lab'),
    path('labs/<int:lab_id>/delete/', views.delete_lab, name='delete_lab'),
]