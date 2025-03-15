from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Khatmah, Participant, JuzAssignment
from .serializers import KhatmahSerializer, KhatmahListSerializer, ParticipantSerializer, JuzAssignmentSerializer
import requests

def home(request):
    return JsonResponse({"message": "Welcome to Quran Khatmah API!"})

@api_view(['GET'])
def get_juz_text(request, juz_number):
    """
    Fetch the text content for a specific Juz from the Quran API
    """
    if juz_number < 1 or juz_number > 30:
        return Response({'error': 'Invalid Juz number. Must be between 1 and 30.'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Fetch Arabic text from the Quran API
        api_url = f"http://api.alquran.cloud/v1/juz/{juz_number}/quran-uthmani"
        
        # Add proper headers to the request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # Check if the response is valid
        if response.status_code != 200:
            return Response(
                {'error': f'Failed to fetch Juz text from Quran API: {response.status_code}', 'details': response.text[:200]},
                status=status.HTTP_502_BAD_GATEWAY
            )
        
        # Try to parse the JSON response
        try:
            data = response.json()
        except ValueError as e:
            return Response(
                {'error': 'Invalid JSON response from Quran API', 'details': str(e), 'response': response.text[:200]},
                status=status.HTTP_502_BAD_GATEWAY
            )
        
        # Check if the API response is valid
        if data.get('code') != 200 or 'data' not in data:
            return Response(
                {'error': 'Invalid response format from Quran API', 'response': data},
                status=status.HTTP_502_BAD_GATEWAY
            )
        
        # Extract the ayahs from the response
        ayahs = data['data']['ayahs']
        
        # Format the response
        formatted_text = f"# بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ\n\n# Juz {juz_number}\n\n"
        
        # Group ayahs by surah
        current_surah = None
        for ayah in ayahs:
            surah_name = ayah['surah']['name']
            
            # Add surah header when changing to a new surah
            if current_surah != surah_name:
                current_surah = surah_name
                formatted_text += f"\n## {surah_name}\n\n"
            
            # Add the ayah text
            formatted_text += f"{ayah['text']} ({ayah['numberInSurah']})\n\n"
        
        return Response({
            'juz_number': juz_number,
            'text': formatted_text,
            'ayahs': ayahs
        })
    except requests.exceptions.RequestException as e:
        return Response(
            {'error': f'Network error when connecting to Quran API: {str(e)}'},
            status=status.HTTP_502_BAD_GATEWAY
        )
    except Exception as e:
        return Response(
            {'error': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class KhatmahPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100

class KhatmahViewSet(viewsets.ModelViewSet):
    queryset = Khatmah.objects.all()
    pagination_class = KhatmahPagination
    
    def get_serializer_class(self):
        if self.action == 'list':
            return KhatmahListSerializer
        return KhatmahSerializer
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        khatmah = self.get_object()
        name = request.data.get('name')
        
        # If name is not required and not provided, use "Anonymous Reader"
        if not khatmah.require_name and (not name or not name.strip()):
            name = "Anonymous Reader"
        # If name is required but not provided, return error
        elif khatmah.require_name and (not name or not name.strip()):
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        participant = Participant.objects.create(name=name, khatmah=khatmah)
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class JuzAssignmentViewSet(viewsets.ModelViewSet):
    queryset = JuzAssignment.objects.all()
    serializer_class = JuzAssignmentSerializer
    
    def create(self, request, *args, **kwargs):
        # Check if the juz is already assigned in this khatmah
        khatmah_id = request.data.get('khatmah')
        juz_number = request.data.get('juz_number')
        
        if JuzAssignment.objects.filter(khatmah_id=khatmah_id, juz_number=juz_number).exists():
            return Response(
                {'error': f'Juz {juz_number} is already assigned in this khatmah'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        assignment = self.get_object()
        assignment.completed = not assignment.completed
        assignment.save()
        serializer = self.get_serializer(assignment)
        return Response(serializer.data)
