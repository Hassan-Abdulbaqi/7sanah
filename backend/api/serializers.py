from rest_framework import serializers
from .models import Khatmah, Participant, JuzAssignment, SurahAssignment, HijriMonth, HijriEvent, AstronomicalEvent

class JuzAssignmentSerializer(serializers.ModelSerializer):
    participant_name = serializers.CharField(source='participant.name', read_only=True)
    
    class Meta:
        model = JuzAssignment
        fields = ['id', 'juz_number', 'participant', 'participant_name', 'khatmah', 'created_at', 'completed']
        read_only_fields = ['id', 'created_at']

class SurahAssignmentSerializer(serializers.ModelSerializer):
    participant_name = serializers.CharField(source='participant.name', read_only=True)
    
    class Meta:
        model = SurahAssignment
        fields = ['id', 'surah_number', 'participant', 'participant_name', 'khatmah', 'created_at', 'completed']
        read_only_fields = ['id', 'created_at']

class ParticipantSerializer(serializers.ModelSerializer):
    assignments = JuzAssignmentSerializer(many=True, read_only=True)
    surah_assignments = SurahAssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Participant
        fields = ['id', 'name', 'khatmah', 'created_at', 'assignments', 'surah_assignments']
        read_only_fields = ['id', 'created_at']

class KhatmahSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    assignments = JuzAssignmentSerializer(many=True, read_only=True)
    surah_assignments = SurahAssignmentSerializer(many=True, read_only=True)
    creator_id = serializers.UUIDField(source='creator.id', read_only=True, allow_null=True)
    completed_juz_count = serializers.SerializerMethodField()
    completed_surah_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Khatmah
        fields = ['id', 'name', 'created_at', 'is_private', 'require_name', 'end_date', 'image_url', 
                 'khatmah_type', 'participants', 'assignments', 'surah_assignments', 'creator_id',
                 'completed_juz_count', 'completed_surah_count']
        read_only_fields = ['id', 'created_at', 'creator_id']
    
    def get_completed_juz_count(self, obj):
        return obj.assignments.filter(completed=True).count()
    
    def get_completed_surah_count(self, obj):
        return obj.surah_assignments.filter(completed=True).count()
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Include creator_token in response when:
        # 1. It's a POST response (creating a khatmah)
        # 2. The request context contains a matching creator_token in the query params or data
        request = self.context.get('request')
        
        if request:
            # For POST/PUT responses, check against saved token
            if (request.method in ['POST', 'PUT'] and 
                getattr(request, 'creator_token_matched', False)):
                ret['creator_token'] = str(instance.creator_token)
            # For GET requests, check for token in query params
            elif (request.method == 'GET' and 
                  request.query_params.get('creator_token') and 
                  str(request.query_params.get('creator_token')) == str(instance.creator_token)):
                ret['creator_token'] = str(instance.creator_token)
        
        return ret

class KhatmahListSerializer(serializers.ModelSerializer):
    participant_count = serializers.SerializerMethodField()
    completed_count = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    completed_juz_count = serializers.SerializerMethodField()
    completed_surah_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Khatmah
        fields = ['id', 'name', 'created_at', 'is_private', 'require_name', 'end_date', 'image_url', 
                 'khatmah_type', 'participant_count', 'completed_count', 'participants',
                 'completed_juz_count', 'completed_surah_count']
    
    def get_participant_count(self, obj):
        return obj.participants.count()
    
    def get_completed_count(self, obj):
        if obj.khatmah_type == Khatmah.JUZ_TYPE:
            return obj.assignments.filter(completed=True).count()
        else:  # Surah type
            return obj.surah_assignments.filter(completed=True).count()
    
    def get_completed_juz_count(self, obj):
        return obj.assignments.filter(completed=True).count()
    
    def get_completed_surah_count(self, obj):
        return obj.surah_assignments.filter(completed=True).count()
        
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