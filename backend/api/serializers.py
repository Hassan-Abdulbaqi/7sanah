from rest_framework import serializers
from .models import Khatmah, Participant, JuzAssignment, HijriMonth, HijriEvent, AstronomicalEvent

class JuzAssignmentSerializer(serializers.ModelSerializer):
    participant_name = serializers.CharField(source='participant.name', read_only=True)
    
    class Meta:
        model = JuzAssignment
        fields = ['id', 'juz_number', 'participant', 'participant_name', 'khatmah', 'created_at', 'completed']
        read_only_fields = ['id', 'created_at']

class ParticipantSerializer(serializers.ModelSerializer):
    assignments = JuzAssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Participant
        fields = ['id', 'name', 'khatmah', 'created_at', 'assignments']
        read_only_fields = ['id', 'created_at']

class KhatmahSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    assignments = JuzAssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Khatmah
        fields = ['id', 'name', 'created_at', 'is_private', 'require_name', 'end_date', 'image_url', 'participants', 'assignments']
        read_only_fields = ['id', 'created_at']

class KhatmahListSerializer(serializers.ModelSerializer):
    participant_count = serializers.SerializerMethodField()
    completed_juz_count = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    
    class Meta:
        model = Khatmah
        fields = ['id', 'name', 'created_at', 'is_private', 'require_name', 'end_date', 'image_url', 'participant_count', 'completed_juz_count', 'participants']
    
    def get_participant_count(self, obj):
        return obj.participants.count()
    
    def get_completed_juz_count(self, obj):
        return obj.assignments.filter(completed=True).count()
        
    def get_participants(self, obj):
        return [{'id': p.id, 'name': p.name} for p in obj.participants.all()]

# Hijri Calendar Serializers
class AstronomicalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomicalEvent
        fields = ['id', 'title_ar', 'title_en', 'date', 'time', 'month', 'description_ar', 'description_en']
        read_only_fields = ['id']

class HijriEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HijriEvent
        fields = ['id', 'title_ar', 'title_en', 'description_ar', 'description_en', 'day', 'month', 
                 'year_of_event', 'is_holiday', 'event_type']
        read_only_fields = ['id']

class HijriMonthDetailSerializer(serializers.ModelSerializer):
    events = HijriEventSerializer(many=True, read_only=True)
    astronomical_events = AstronomicalEventSerializer(many=True, read_only=True)
    
    class Meta:
        model = HijriMonth
        fields = ['id', 'name_ar', 'name_en', 'number', 'year', 'gregorian_start', 'gregorian_end', 
                 'moon_sighting_data', 'calendar_data', 'events', 'astronomical_events']
        read_only_fields = ['id']

class HijriMonthListSerializer(serializers.ModelSerializer):
    event_count = serializers.SerializerMethodField()
    
    class Meta:
        model = HijriMonth
        fields = ['id', 'name_ar', 'name_en', 'number', 'year', 'gregorian_start', 'gregorian_end', 'event_count']
        read_only_fields = ['id']
    
    def get_event_count(self, obj):
        return obj.events.count() 