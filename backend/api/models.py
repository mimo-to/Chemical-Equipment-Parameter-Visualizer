from django.db import models

class EquipmentDataset(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    type_distribution = models.JSONField()
    csv_data = models.TextField()
