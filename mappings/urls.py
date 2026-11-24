from django.urls import path
from .views import (
    MappingListCreateView,
    PatientMappingListView,
    MappingDeleteView
)

urlpatterns = [
    path('', MappingListCreateView.as_view(), name='mapping-list-create'),
    path('<int:pk>/', MappingDeleteView.as_view(), name='mapping-delete'),
    path('<int:patient_id>/', PatientMappingListView.as_view(), name='patient-doctors'),
]