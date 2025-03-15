from rest_framework import serializers
from .models import Khatmah, Participant, JuzAssignment

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