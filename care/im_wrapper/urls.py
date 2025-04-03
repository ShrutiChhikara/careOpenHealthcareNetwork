from django.urls import path
from .views import PatientRecordsView, NotificationView, TemplateNotificationView

urlpatterns = [
    path('patient-records/<str:phone_number>/', PatientRecordsView.as_view(), name='patient-records'),
    path('send-notification/', NotificationView.as_view(), name='send-notification'),
    path('send-template-notification/', TemplateNotificationView.as_view(), name='send-template-notification'),
]
