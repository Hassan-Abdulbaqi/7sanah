from django.db import models
import uuid

# Create your models here.

class Khatmah(models.Model):
    JUZ_TYPE = 'juz'
    SURAH_TYPE = 'surah'
    KHATMAH_TYPES = [
        (JUZ_TYPE, 'Juz Based'),
        (SURAH_TYPE, 'Surah Based'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    require_name = models.BooleanField(default=True)
    end_date = models.DateField(null=True, blank=True)
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    khatmah_type = models.CharField(max_length=10, choices=KHATMAH_TYPES, default=JUZ_TYPE)
    creator = models.ForeignKey('Participant', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_khatmahs')
    creator_token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    
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

class SurahAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    surah_number = models.IntegerField()
    participant = models.ForeignKey(Participant, related_name='surah_assignments', on_delete=models.CASCADE)
    khatmah = models.ForeignKey(Khatmah, related_name='surah_assignments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('surah_number', 'khatmah')
    
    def __str__(self):
        return f"Surah {self.surah_number} assigned to {self.participant.name} in {self.khatmah.name}"

# Hijri Calendar Models
class HijriMonth(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_ar = models.CharField(max_length=50)  # Arabic name
    name_en = models.CharField(max_length=50)  # English name
    number = models.IntegerField()  # Month number (1-12)
    year = models.IntegerField()  # Hijri year
    gregorian_start = models.DateField()  # Gregorian date when this Hijri month starts
    gregorian_end = models.DateField()  # Gregorian date when this Hijri month ends
    moon_sighting_data = models.JSONField(null=True, blank=True)  # Data about moon sighting
    calendar_data = models.JSONField(null=True, blank=True)  # Calendar mapping between Hijri and Gregorian
    
    class Meta:
        unique_together = ('number', 'year')
        ordering = ['year', 'number']
    
    def __str__(self):
        return f"{self.name_ar} ({self.name_en}) - {self.year}H"

class HijriEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_ar = models.CharField(max_length=255)  # Arabic title
    title_en = models.CharField(max_length=255, null=True, blank=True)  # English title (optional)
    description_ar = models.TextField(null=True, blank=True)  # Arabic description
    description_en = models.TextField(null=True, blank=True)  # English description
    day = models.IntegerField()  # Day of the month
    month = models.ForeignKey(HijriMonth, related_name='events', on_delete=models.CASCADE)
    year_of_event = models.IntegerField(null=True, blank=True)  # Original Hijri year when event occurred
    is_holiday = models.BooleanField(default=False)  # Whether this is a holiday/special day
    event_type = models.CharField(max_length=50, null=True, blank=True)  # Type of event (historical, religious, etc.)
    
    class Meta:
        ordering = ['month__number', 'day']
    
    def __str__(self):
        return f"{self.title_ar} - {self.day} {self.month.name_ar}"

class AstronomicalEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title_ar = models.CharField(max_length=255)  # Arabic title
    title_en = models.CharField(max_length=255, null=True, blank=True)  # English title
    date = models.DateField()  # Gregorian date
    time = models.TimeField()  # Time of event
    month = models.ForeignKey(HijriMonth, related_name='astronomical_events', on_delete=models.CASCADE)
    description_ar = models.TextField(null=True, blank=True)  # Arabic description
    description_en = models.TextField(null=True, blank=True)  # English description
    
    def __str__(self):
        return f"{self.title_ar} - {self.date}"
