
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientMappingListView(generics.ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']

        if not Patient.objects.filter(
            id=patient_id,
            user=self.request.user
        ).exists():
            raise ValidationError("Patient not found.")

        return PatientDoctorMapping.objects.filter(
            patient_id=patient_id,
            patient__user=self.request.user
        )


class MappingDeleteView(generics.DestroyAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__user=self.request.user
        )
