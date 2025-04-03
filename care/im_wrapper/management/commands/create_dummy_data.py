from django.core.management.base import BaseCommand
from im_wrapper.models import Patient, Medication, Procedure, Schedule
from datetime import date, timedelta

class Command(BaseCommand):
    help = "Create dummy data for testing"

    def handle(self, *args, **kwargs):
        # Create a dummy patient
        patient, created = Patient.objects.get_or_create(
            name="John Doe",
            phone_number="1234567890",
            email="john.doe@example.com",
            date_of_birth=date(1990, 1, 1)
        )

        # Create dummy medications
        Medication.objects.get_or_create(
            patient=patient,
            name="Paracetamol",
            dosage="500mg",
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() + timedelta(days=10)
        )
        Medication.objects.get_or_create(
            patient=patient,
            name="Ibuprofen",
            dosage="200mg",
            start_date=date.today() - timedelta(days=5),
            end_date=date.today() + timedelta(days=5)
        )

        # Create dummy procedures
        Procedure.objects.get_or_create(
            patient=patient,
            name="X-Ray",
            date=date.today() - timedelta(days=7)
        )
        Procedure.objects.get_or_create(
            patient=patient,
            name="Blood Test",
            date=date.today() - timedelta(days=3)
        )

        # Create dummy schedules
        Schedule.objects.get_or_create(
            patient=patient,
            description="Follow-up appointment",
            date=date.today() + timedelta(days=7)
        )
        Schedule.objects.get_or_create(
            patient=patient,
            description="Consultation with specialist",
            date=date.today() + timedelta(days=14)
        )

        self.stdout.write(self.style.SUCCESS("Dummy data created successfully!"))
