from rest_framework import serializers
from .models import PatientDoctorMapping


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_patient(self, value):
        request = self.context['request']

        if value.user != request.user:
            raise serializers.ValidationError(
                "You can only assign doctors to your own patients."
            )

        return value

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')

        if PatientDoctorMapping.objects.filter(
            patient=patient,
            doctor=doctor
        ).exists():
            raise serializers.ValidationError(
                "This doctor is already assigned to this patient."
            )

        return attrs