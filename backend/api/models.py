from django.db import models
import uuid

# Create your models here.

class Khatmah(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    require_name = models.BooleanField(default=True)
    end_date = models.DateField(null=True, blank=True)
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    khatmah = models.ForeignKey(Khatmah, related_name='participants', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} in {self.khatmah.name}"

class JuzAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    juz_number = models.IntegerField()
    participant = models.ForeignKey(Participant, related_name='assignments', on_delete=models.CASCADE)
    khatmah = models.ForeignKey(Khatmah, related_name='assignments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('juz_number', 'khatmah')
    
    def __str__(self):
        return f"Juz {self.juz_number} assigned to {self.participant.name} in {self.khatmah.name}"
