from django.db import models
from django.contrib.auth.models import User

class EquipmentDataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)
    filename = models.CharField(max_length=255, db_index=True)
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    type_distribution = models.JSONField()
    csv_data = models.TextField()

    class Meta:
        ordering = ['-uploaded_at']
