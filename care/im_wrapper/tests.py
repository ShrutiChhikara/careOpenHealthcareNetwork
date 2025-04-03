from django.test import TestCase
from .models import Patient, Medication, Procedure, Schedule
from whatsapp_bot.bot import WhatsAppBot
from unittest.mock import patch

class IMWrapperTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            name="John Doe",
            phone_number="1234567890",
            email="john@example.com",
            date_of_birth="1990-01-01"
        )
        Medication.objects.create(
            patient=self.patient,
            name="Paracetamol",
            dosage="500mg",
            start_date="2023-01-01",
            end_date="2023-01-10"
        )
        Procedure.objects.create(
            patient=self.patient,
            name="X-Ray",
            date="2023-01-05"
        )
        Schedule.objects.create(
            patient=self.patient,
            description="Follow-up appointment",
            date="2023-01-15"
        )

    def test_patient_records(self):
        response = self.client.get(f"/im_wrapper/patient-records/{self.patient.phone_number}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("patient", response.json())

    @patch("twilio.rest.Client.messages.create")
    def test_send_notification(self, mock_twilio_send_message):
        mock_twilio_send_message.return_value = type("Message", (object,), {"sid": "12345", "status": "sent"})
        response = self.client.post("/im_wrapper/send-notification/", {
            "recipient_number": "1234567890",
            "message": "Test message"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "Message sent successfully."})

    @patch("twilio.rest.Client.messages.create")
    def test_send_template_notification(self, mock_twilio_send_message):
        mock_twilio_send_message.return_value = type("Message", (object,), {"sid": "12345", "status": "sent"})
        response = self.client.post("/im_wrapper/send-template-notification/", {
            "recipient_number": "1234567890",
            "content_sid": "HXb5b62575e6e4ff6129ad7c8efe1f983e",
            "content_variables": '{"1":"12/1","2":"3pm"}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": "Template message sent successfully."})
