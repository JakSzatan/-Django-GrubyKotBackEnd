from django.db import models
from django.contrib.auth.models import User



class Apointment(models.Model):

    class Appointment_types(models.TextChoices):
        CONSULTATION = 'Konsultacja'
        TATTOOING = "Sesja"
        TOUCHUP = "Poprawki"

    tattoo_artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tattoo_artist")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client")
    dateStart = models.DateTimeField()
    dateEnd = models.DateTimeField()
    type = models.CharField(choices=Appointment_types.choices,max_length=255)