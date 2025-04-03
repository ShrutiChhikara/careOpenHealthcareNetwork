from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient, Medication, Procedure, Schedule
from .serializers import PatientSerializer, MedicationSerializer, ProcedureSerializer, ScheduleSerializer
from whatsapp_bot.bot import WhatsAppBot

class PatientRecordsView(APIView):
    def get(self, request, phone_number):
        try:
            patient = Patient.objects.get(phone_number=phone_number)
            medications = Medication.objects.filter(patient=patient)
            procedures = Procedure.objects.filter(patient=patient)
            schedules = Schedule.objects.filter(patient=patient)

            data = {
                "patient": PatientSerializer(patient).data,
                "medications": MedicationSerializer(medications, many=True).data,
                "procedures": ProcedureSerializer(procedures, many=True).data,
                "schedules": ScheduleSerializer(schedules, many=True).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

class NotificationView(APIView):
    def post(self, request):
        bot = WhatsAppBot()
        recipient_number = request.data.get("recipient_number")
        message = request.data.get("message")
        if not recipient_number or not message:
            return Response({"error": "Recipient number and message are required."}, status=status.HTTP_400_BAD_REQUEST)
        status_code, response = bot.send_message(recipient_number, message)
        if status_code == 200:
            return Response({"success": "Message sent successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to send message.", "details": response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TemplateNotificationView(APIView):
    def post(self, request):
        bot = WhatsAppBot()
        recipient_number = request.data.get("recipient_number")
        content_sid = request.data.get("content_sid")
        content_variables = request.data.get("content_variables")
        if not recipient_number or not content_sid or not content_variables:
            return Response({"error": "Recipient number, ContentSid, and ContentVariables are required."}, status=status.HTTP_400_BAD_REQUEST)
        status_code, response = bot.send_message_with_template(recipient_number, content_sid, content_variables)
        if status_code == 200:
            return Response({"success": "Template message sent successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to send template message.", "details": response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
