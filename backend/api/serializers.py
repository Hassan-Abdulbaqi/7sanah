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
    image_url = serializers.SerializerMethodField()
    creator_token = serializers.SerializerMethodField()
    
    class Meta:
        model = Khatmah
        fields = ['id', 'name', 'created_at', 'is_private', 'require_name', 'end_date', 'image', 'image_url',
                 'khatmah_type', 'participants', 'assignments', 'surah_assignments', 'creator_id',
                 'completed_juz_count', 'completed_surah_count', 'creator_token']
        read_only_fields = ['id', 'created_at', 'creator_id', 'creator_token']
    
    def get_completed_juz_count(self, obj):
        return obj.assignments.filter(completed=True).count()
    
    def get_completed_surah_count(self, obj):
        return obj.surah_assignments.filter(completed=True).count()
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return obj.image_url
    
    def get_creator_token(self, obj):
        request = self.context.get('request')
        if not request:
            return None
            
        if request.method == 'POST':
            return str(obj.creator_token)
            
        creator_token = request.query_params.get('creator_token') or request.data.get('creator_token')
        if creator_token and str(creator_token) == str(obj.creator_token):
            return str(obj.creator_token)
            
        return None

class KhatmahListSerializer(serializers.ModelSerializer):
    participant_count = serializers.SerializerMethodField()
    completed_count = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    completed_juz_count = serializers.SerializerMethodField()
    completed_surah_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Khatmah
        fields = ['id', 'name', 'created_at', 'is_private', 'require_name', 'end_date', 'image', 'image_url',
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
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return obj.image_url  # Return the legacy image_url if no uploaded image
        
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