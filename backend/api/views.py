from django.http import JsonResponse
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Khatmah, Participant, JuzAssignment, SurahAssignment, HijriMonth, HijriEvent, AstronomicalEvent
from .serializers import (
    KhatmahSerializer, KhatmahListSerializer, ParticipantSerializer, JuzAssignmentSerializer,
    SurahAssignmentSerializer, HijriMonthDetailSerializer, HijriMonthListSerializer, 
    HijriEventSerializer, AstronomicalEventSerializer
)
import requests
from django.shortcuts import render
import math
import uuid
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings
from django.core.cache import cache


def home(request):
    return JsonResponse({"message": "Welcome to Quran Khatmah API!"})

def calendar_dashboard(request):
    """
    Render the Hijri Calendar Dashboard page that showcases all calendar endpoints
    """
    return render(request, 'api/calendar_dashboard.html')

@api_view(['GET'])
def test_api_view(request):
    """
    Test API view that returns data about the Hijri calendar
    """
    try:
        # Get the Muharram month
        muharram = HijriMonth.objects.filter(name_en='Muharram').first()
        
        if not muharram:
            return Response({'error': 'Muharram month not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get events for Muharram
        events = HijriEvent.objects.filter(month=muharram)
        events_data = HijriEventSerializer(events, many=True).data
        
        # Get astronomical events for Muharram
        astro_events = AstronomicalEvent.objects.filter(month=muharram)
        astro_events_data = AstronomicalEventSerializer(astro_events, many=True).data
        
        # Return the data
        return Response({
            'month': {
                'id': str(muharram.id),
                'name_ar': muharram.name_ar,
                'name_en': muharram.name_en,
                'number': muharram.number,
                'year': muharram.year,
                'gregorian_start': muharram.gregorian_start,
                'gregorian_end': muharram.gregorian_end,
                'moon_sighting_data': muharram.moon_sighting_data,
                'calendar_data': muharram.calendar_data
            },
            'events': events_data,
            'astronomical_events': astro_events_data
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        api_url = f"https://api.alquran.cloud/v1/juz/{juz_number}/quran-uthmani"
        
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
        formatted_text = juz_number
        
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

@api_view(['GET'])
def get_surah_text(request, surah_number):
    """
    Fetch the text content for a specific Surah from the Quran API
    """
    if surah_number < 1 or surah_number > 114:
        return Response({'error': 'Invalid Surah number. Must be between 1 and 114.'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Fetch Arabic text from the Quran API
        api_url = f"https://api.alquran.cloud/v1/surah/{surah_number}/quran-uthmani"
        
        # Add proper headers to the request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # Check if the response is valid
        if response.status_code != 200:
            return Response(
                {'error': f'Failed to fetch Surah text from Quran API: {response.status_code}', 'details': response.text[:200]},
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
        surah_name = data['data']['name']
        
        # Format the response
        formatted_text = f"## {surah_name}\n\n"
        
        # Add each ayah to the formatted text
        for ayah in ayahs:
            formatted_text += f"{ayah['text']} ({ayah['numberInSurah']})\n\n"
        
        return Response({
            'surah_number': surah_number,
            'surah_name': surah_name,
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
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class KhatmahViewSet(viewsets.ModelViewSet):
    """
    Khatmah API endpoints.
    
    Authentication & Authorization:
    - Creating a khatmah generates a unique creator_token which is returned in the response
    - For secure ownership verification, provide this creator_token:
      - In query parameters for GET, DELETE requests: ?creator_token=xxx
      - In request body for PUT, PATCH, POST requests: {"creator_token": "xxx"}
    - The token is only returned when requesting a khatmah with a valid creator_token
    - The creator_token provides permanent ownership rights, even across different devices
    
    File Upload:
    - Images can be uploaded using multipart/form-data
    - Supported formats: jpg, jpeg, png, gif
    - Maximum file size: 5MB
    """
    queryset = Khatmah.objects.all()
    pagination_class = KhatmahPagination
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return KhatmahListSerializer
        return KhatmahSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def validate_uuid(self, uuid_string):
        """Helper method to validate UUID format"""
        try:
            uuid_obj = uuid.UUID(str(uuid_string))
            return True
        except (ValueError, TypeError, AttributeError):
            return False
    
    def get_queryset(self):
        queryset = Khatmah.objects.all()
        
        # Check if is_private filter is in the request
        is_private = self.request.query_params.get('is_private', None)
        if is_private is not None:
            # Only accept valid boolean string values
            if is_private.lower() in ('true', 'false'):
                # Convert string to boolean ('false' -> False, 'true' -> True)
                is_private_bool = is_private.lower() == 'true'
                queryset = queryset.filter(is_private=is_private_bool)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Validate the creator_token if provided (must be a valid UUID)
        creator_token_from_request = request.data.get('creator_token')
        if creator_token_from_request:
            try:
                # Verify it's a valid UUID format
                uuid_obj = uuid.UUID(str(creator_token_from_request))
            except (ValueError, TypeError, AttributeError):
                return Response(
                    {'error': 'Invalid creator_token format. Must be a valid UUID.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Validate image file if provided
        image_file = request.FILES.get('image')
        if image_file:
            # Check file size (5MB limit)
            if image_file.size > 5 * 1024 * 1024:
                return Response(
                    {'error': 'Image file size must be less than 5MB.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check file type
            valid_types = ['image/jpeg', 'image/png', 'image/gif']
            if not any(image_file.content_type.startswith(t) for t in valid_types):
                return Response(
                    {'error': 'Invalid image format. Supported formats: jpg, jpeg, png, gif'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Remove creator_token from the request data before creating the instance
        mutable_data = request.data.copy()
        if 'creator_token' in mutable_data:
            del mutable_data['creator_token']
        request._full_data = mutable_data
        
        # Create the khatmah
        response = super().create(request, *args, **kwargs)
        
        # Add the creator_token to the response
        khatmah_id = response.data['id']
        khatmah = Khatmah.objects.get(id=khatmah_id)
        
        # Set flag for serializer that will add creator_token to response
        request.creator_token_matched = True
        
        return response
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        khatmah = self.get_object()
        name = request.data.get('name')
        creator_token = request.data.get('creator_token')
        
        # If name is not required and not provided, use "Anonymous Reader"
        if not khatmah.require_name and (not name or not name.strip()):
            name = "قارء مجهول"
        # If name is required but not provided, return error
        elif khatmah.require_name and (not name or not name.strip()):
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        participant = Participant.objects.create(name=name, khatmah=khatmah)
        
        # Check if this participant should be the creator based on the creator_token
        if creator_token and str(khatmah.creator_token) == str(creator_token) and not khatmah.creator:
            khatmah.creator = participant
            khatmah.save()
        
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        khatmah = self.get_object()
        
        # Validate the creator_token if provided (must be a valid UUID)
        creator_token = request.data.get('creator_token')
        if creator_token:
            try:
                # Verify it's a valid UUID format
                uuid_obj = uuid.UUID(str(creator_token))
            except (ValueError, TypeError, AttributeError):
                return Response(
                    {'error': 'Invalid creator_token format. Must be a valid UUID.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Validate image file if provided
        image_file = request.FILES.get('image')
        if image_file:
            # Check file size (5MB limit)
            if image_file.size > 5 * 1024 * 1024:
                return Response(
                    {'error': 'Image file size must be less than 5MB.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check file type
            valid_types = ['image/jpeg', 'image/png', 'image/gif']
            if not any(image_file.content_type.startswith(t) for t in valid_types):
                return Response(
                    {'error': 'Invalid image format. Supported formats: jpg, jpeg, png, gif'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Remove creator_token from the request data before updating
        mutable_data = request.data.copy()
        if 'creator_token' in mutable_data:
            del mutable_data['creator_token']
        request._full_data = mutable_data
        
        # Check authentication
        if creator_token and str(khatmah.creator_token) == str(creator_token):
            # Set flag for serializer that will add creator_token to response
            request.creator_token_matched = True
            return super().update(request, *args, **kwargs)
        
        # Otherwise, check participant ID authentication
        participant_id = request.data.get('participant_id')
        if not participant_id:
            # Check if there's a creator set on the khatmah
            if khatmah.creator:
                return Response(
                    {'error': 'You are not authorized to edit this khatmah. Must provide participant_id or creator_token.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            # For backward compatibility, allow edits if no creator is set
            return super().update(request, *args, **kwargs)
            
        # Verify the participant is the creator
        if not khatmah.creator or str(khatmah.creator.id) != participant_id:
            return Response(
                {'error': 'You are not authorized to edit this khatmah'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        return super().update(request, *args, **kwargs)
        
    def destroy(self, request, *args, **kwargs):
        khatmah = self.get_object()
        
        # Validate the creator_token if provided (must be a valid UUID)
        creator_token = request.query_params.get('creator_token')
        if creator_token:
            try:
                # Verify it's a valid UUID format
                uuid_obj = uuid.UUID(str(creator_token))
            except (ValueError, TypeError, AttributeError):
                return Response(
                    {'error': 'Invalid creator_token format. Must be a valid UUID.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Check token validity
            if str(khatmah.creator_token) == str(creator_token):
                return super().destroy(request, *args, **kwargs)
        
        # Otherwise check participant ID authentication
        participant_id = request.query_params.get('participant_id')
        if not participant_id:
            # Check if there's a creator set on the khatmah
            if khatmah.creator:
                return Response(
                    {'error': 'You are not authorized to delete this khatmah. Must provide participant_id or creator_token.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            # For backward compatibility, allow deletion if no creator is set
            return super().destroy(request, *args, **kwargs)
            
        # Verify the participant is the creator
        if not khatmah.creator or str(khatmah.creator.id) != participant_id:
            return Response(
                {'error': 'You are not authorized to delete this khatmah'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        khatmah = self.get_object()
        
        # Validate the creator_token if provided (must be a valid UUID)
        creator_token = request.query_params.get('creator_token')
        if creator_token:
            try:
                # Verify it's a valid UUID format
                uuid_obj = uuid.UUID(str(creator_token))
                
                # If valid, check if it matches
                if str(khatmah.creator_token) == str(creator_token):
                    # The serializer will see this match and include creator_token in response
                    request.creator_token_matched = True
            except (ValueError, TypeError, AttributeError):
                # Don't return an error for GET requests, just don't authenticate
                pass
        
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def remove_participant(self, request, pk=None):
        """
        Remove a participant from a khatmah.
        This will also remove all their assignments and progress.
        Only the khatmah creator can remove participants.
        """
        khatmah = self.get_object()
        participant_id = request.data.get('participant_id')
        creator_token = request.data.get('creator_token')

        # Validate participant_id
        if not participant_id:
            return Response(
                {'error': 'Participant ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify it's a valid UUID format
            uuid_obj = uuid.UUID(str(participant_id))
        except (ValueError, TypeError, AttributeError):
            return Response(
                {'error': 'Invalid participant ID format. Must be a valid UUID.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify authorization
        is_authorized = False
        if creator_token:
            try:
                uuid_obj = uuid.UUID(str(creator_token))
                is_authorized = str(khatmah.creator_token) == str(creator_token)
            except (ValueError, TypeError, AttributeError):
                return Response(
                    {'error': 'Invalid creator_token format. Must be a valid UUID.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif request.data.get('requester_participant_id'):
            # Alternative auth method using participant ID
            requester_id = request.data.get('requester_participant_id')
            is_authorized = khatmah.creator and str(khatmah.creator.id) == str(requester_id)

        if not is_authorized:
            return Response(
                {'error': 'You are not authorized to remove participants from this khatmah'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if participant exists and is not the creator
        try:
            participant = Participant.objects.get(id=participant_id, khatmah=khatmah)
            
            # Don't allow removing the creator
            if khatmah.creator and participant.id == khatmah.creator.id:
                return Response(
                    {'error': 'Cannot remove the khatmah creator'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Delete the participant (this will cascade delete their assignments due to FK)
            participant.delete()
            
            # Refresh khatmah data
            serializer = self.get_serializer(khatmah)
            return Response(serializer.data)
            
        except Participant.DoesNotExist:
            return Response(
                {'error': 'Participant not found in this khatmah'},
                status=status.HTTP_404_NOT_FOUND
            )

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class JuzAssignmentViewSet(viewsets.ModelViewSet):
    queryset = JuzAssignment.objects.all()
    serializer_class = JuzAssignmentSerializer
    
    def create(self, request, *args, **kwargs):
        # Validate the input data
        khatmah_id = request.data.get('khatmah')
        juz_number = request.data.get('juz_number')
        participant_id = request.data.get('participant')
        
        # Validate UUID fields
        if not khatmah_id or not participant_id:
            return Response(
                {'error': 'Khatmah ID and participant ID are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            uuid.UUID(str(khatmah_id))
            uuid.UUID(str(participant_id))
        except (ValueError, TypeError, AttributeError):
            return Response(
                {'error': 'Invalid UUID format for khatmah ID or participant ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate juz_number is within range
        try:
            juz_number = int(juz_number)
            if juz_number < 1 or juz_number > 30:
                return Response(
                    {'error': 'Juz number must be between 1 and 30'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid juz number format'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Check if the juz is already assigned in this khatmah
        if JuzAssignment.objects.filter(khatmah_id=khatmah_id, juz_number=juz_number).exists():
            return Response(
                {'error': f'Juz {juz_number} is already assigned in this khatmah'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        # Validate UUID
        try:
            uuid.UUID(str(pk))
        except (ValueError, TypeError, AttributeError):
            return Response(
                {'error': 'Invalid assignment ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        assignment = self.get_object()
        assignment.completed = not assignment.completed
        assignment.save()
        serializer = self.get_serializer(assignment)
        return Response(serializer.data)

class SurahAssignmentViewSet(viewsets.ModelViewSet):
    queryset = SurahAssignment.objects.all()
    serializer_class = SurahAssignmentSerializer
    
    def create(self, request, *args, **kwargs):
        # Validate the input data
        khatmah_id = request.data.get('khatmah')
        surah_number = request.data.get('surah_number')
        participant_id = request.data.get('participant')
        
        # Validate UUID fields
        if not khatmah_id or not participant_id:
            return Response(
                {'error': 'Khatmah ID and participant ID are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            uuid.UUID(str(khatmah_id))
            uuid.UUID(str(participant_id))
        except (ValueError, TypeError, AttributeError):
            return Response(
                {'error': 'Invalid UUID format for khatmah ID or participant ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate surah_number is within range
        try:
            surah_number = int(surah_number)
            if surah_number < 1 or surah_number > 114:
                return Response(
                    {'error': 'Surah number must be between 1 and 114'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid surah number format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the surah is already assigned in this khatmah
        if SurahAssignment.objects.filter(khatmah_id=khatmah_id, surah_number=surah_number).exists():
            return Response(
                {'error': f'Surah {surah_number} is already assigned in this khatmah'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        # Validate UUID
        try:
            uuid.UUID(str(pk))
        except (ValueError, TypeError, AttributeError):
            return Response(
                {'error': 'Invalid assignment ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        assignment = self.get_object()
        assignment.completed = not assignment.completed
        assignment.save()
        serializer = self.get_serializer(assignment)
        return Response(serializer.data)

# Hijri Calendar ViewSets
class HijriMonthPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 12


class HijriMonthViewSet(viewsets.ModelViewSet):
    queryset = HijriMonth.objects.all()
    pagination_class = HijriMonthPagination
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']  # Only allow GET requests

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HijriMonthDetailSerializer
        return HijriMonthListSerializer

    @action(detail=False, methods=['get'])
    def by_number(self, request):
        """Get a Hijri month by its number and year"""
        number = request.query_params.get('number')
        year = request.query_params.get('year')
        
        if not number or not year:
            return Response({'error': 'Both month number and year are required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            number = int(number)
            year = int(year)
            
            if number < 1 or number > 12:
                return Response({'error': 'Month number must be between 1 and 12'}, 
                               status=status.HTTP_400_BAD_REQUEST)
            
            try:
                month = HijriMonth.objects.get(number=number, year=year)
                serializer = HijriMonthDetailSerializer(month)
                return Response(serializer.data)
            except HijriMonth.DoesNotExist:
                return Response({'error': f'No Hijri month found with number {number} and year {year}'}, 
                               status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'error': 'Month number and year must be integers'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get the current Hijri month based on today's date"""
        try:
            # Get today's date
            from datetime import date
            today = date.today()
            
            # Find the Hijri month that contains today's date
            current_month = HijriMonth.objects.filter(
                gregorian_start__lte=today,
                gregorian_end__gte=today
            ).first()
            
            # If no month contains today's date (might happen if data is incomplete)
            if not current_month:
                # Try to find the closest month
                future_months = HijriMonth.objects.filter(
                    gregorian_start__gt=today
                ).order_by('gregorian_start')
                
                past_months = HijriMonth.objects.filter(
                    gregorian_end__lt=today
                ).order_by('-gregorian_end')
                
                if future_months.exists() and past_months.exists():
                    # Calculate which is closer - the most recent past month or the nearest future month
                    future_month = future_months.first()
                    past_month = past_months.first()
                    
                    days_to_future = (future_month.gregorian_start - today).days
                    days_from_past = (today - past_month.gregorian_end).days
                    
                    current_month = future_month if days_to_future < days_from_past else past_month
                elif future_months.exists():
                    current_month = future_months.first()
                elif past_months.exists():
                    current_month = past_months.first()
                else:
                    return Response({'error': 'No Hijri months found in the database'}, 
                                  status=status.HTTP_404_NOT_FOUND)
            
            serializer = HijriMonthDetailSerializer(current_month)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def by_name(self, request):
        """Get a Hijri month by its name and year"""
        name = request.query_params.get('name')
        year = request.query_params.get('year')
        
        if not name:
            return Response({'error': 'Month name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Try to find by Arabic name first
            queryset = HijriMonth.objects.filter(name_ar__icontains=name)
            
            # If not found, try English name
            if not queryset.exists():
                queryset = HijriMonth.objects.filter(name_en__icontains=name)
            
            # Filter by year if provided
            if year:
                queryset = queryset.filter(year=year)
            
            # Get the first match
            if not queryset.exists():
                return Response({'error': f'No Hijri month found with name: {name}'}, 
                               status=status.HTTP_404_NOT_FOUND)
            
            month = queryset.first()
            serializer = HijriMonthDetailSerializer(month)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HijriEventViewSet(viewsets.ModelViewSet):
    queryset = HijriEvent.objects.all()
    serializer_class = HijriEventSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']  # Only allow GET requests

    @action(detail=False, methods=['get'])
    def by_month(self, request):
        """Get events for a specific Hijri month"""
        month_id = request.query_params.get('month_id')
        month_number = request.query_params.get('month_number')
        year = request.query_params.get('year')
        
        if month_id:
            queryset = HijriEvent.objects.filter(month_id=month_id)
        elif month_number and year:
            try:
                month = HijriMonth.objects.get(number=month_number, year=year)
                queryset = HijriEvent.objects.filter(month=month)
            except HijriMonth.DoesNotExist:
                return Response({'error': f'No Hijri month found with number {month_number} and year {year}'}, 
                               status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Either month_id or both month_number and year are required'}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        serializer = HijriEventSerializer(queryset, many=True)
        return Response(serializer.data)

class AstronomicalEventViewSet(viewsets.ModelViewSet):
    queryset = AstronomicalEvent.objects.all()
    serializer_class = AstronomicalEventSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get']  # Only allow GET requests

    @action(detail=False, methods=['get'])
    def by_month(self, request):
        """Get astronomical events for a specific Hijri month"""
        month_id = request.query_params.get('month_id')
        
        if not month_id:
            return Response({'error': 'month_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = AstronomicalEvent.objects.filter(month_id=month_id)
        serializer = AstronomicalEventSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_hijri_calendar(request):
    """
    Get Hijri calendar data for a specific month or the current month
    """
    month_name = request.query_params.get('month')
    month_number = request.query_params.get('month_number')
    year = request.query_params.get('year')
    gregorian_date = request.query_params.get('gregorian_date')
    
    try:
        # If gregorian_date is provided, find the Hijri month containing this date
        if gregorian_date:
            try:
                # Parse the date string (format: YYYY-MM-DD)
                from datetime import datetime
                date_obj = datetime.strptime(gregorian_date, '%Y-%m-%d').date()
                
                # Find the Hijri month that contains this Gregorian date
                month = HijriMonth.objects.filter(
                    gregorian_start__lte=date_obj,
                    gregorian_end__gte=date_obj
                ).first()
                
                if not month:
                    # If no exact match, get the closest month
                    future_months = HijriMonth.objects.filter(
                        gregorian_start__gt=date_obj
                    ).order_by('gregorian_start')
                    
                    past_months = HijriMonth.objects.filter(
                        gregorian_end__lt=date_obj
                    ).order_by('-gregorian_end')
                    
                    if future_months.exists() and past_months.exists():
                        # Calculate which is closer
                        future_month = future_months.first()
                        past_month = past_months.first()
                        
                        days_to_future = (future_month.gregorian_start - date_obj).days
                        days_from_past = (date_obj - past_month.gregorian_end).days
                        
                        month = future_month if days_to_future < days_from_past else past_month
                    elif future_months.exists():
                        month = future_months.first()
                    elif past_months.exists():
                        month = past_months.first()
                    else:
                        return Response({'error': 'No Hijri months found in the database'}, 
                                      status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        # If month_number and year are provided, get that specific month by number
        elif month_number and year:
            try:
                month_number = int(month_number)
                year = int(year)
                
                if month_number < 1 or month_number > 12:
                    return Response({'error': 'Month number must be between 1 and 12'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
                
                month = HijriMonth.objects.filter(number=month_number, year=year).first()
                
                if not month:
                    return Response({'error': f'No Hijri month found with number: {month_number} and year: {year}'}, 
                                  status=status.HTTP_404_NOT_FOUND)
            except ValueError:
                return Response({'error': 'Month number and year must be integers'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        # If month name and year are provided, get that specific month by name
        elif month_name and year:
            # Try to find by English name first (case insensitive)
            month = HijriMonth.objects.filter(name_en__iexact=month_name, year=year).first()
            
            # If not found, try Arabic name
            if not month:
                month = HijriMonth.objects.filter(name_ar__iexact=month_name, year=year).first()
                
            if not month:
                return Response({'error': f'No Hijri month found with name: {month_name} and year: {year}'}, 
                              status=status.HTTP_404_NOT_FOUND)
        else:
            # Get the current month based on today's date
            from datetime import date
            today = date.today()
            
            # Find the Hijri month that contains today's date
            month = HijriMonth.objects.filter(
                gregorian_start__lte=today,
                gregorian_end__gte=today
            ).first()
            
            # If no month contains today's date (might happen if data is incomplete)
            if not month:
                # Try to find the closest month
                future_months = HijriMonth.objects.filter(
                    gregorian_start__gt=today
                ).order_by('gregorian_start')
                
                past_months = HijriMonth.objects.filter(
                    gregorian_end__lt=today
                ).order_by('-gregorian_end')
                
                if future_months.exists() and past_months.exists():
                    # Calculate which is closer
                    future_month = future_months.first()
                    past_month = past_months.first()
                    
                    days_to_future = (future_month.gregorian_start - today).days
                    days_from_past = (today - past_month.gregorian_end).days
                    
                    month = future_month if days_to_future < days_from_past else past_month
                elif future_months.exists():
                    month = future_months.first()
                elif past_months.exists():
                    month = past_months.first()
                else:
                    return Response({'error': 'No Hijri months found in the database'}, 
                                  status=status.HTTP_404_NOT_FOUND)
        
        # Get events for this month
        events = HijriEvent.objects.filter(month=month)
        events_data = HijriEventSerializer(events, many=True).data
        
        # Get astronomical events for this month
        astro_events = AstronomicalEvent.objects.filter(month=month)
        astro_events_data = AstronomicalEventSerializer(astro_events, many=True).data
        
        # Format the calendar data
        calendar_data = []
        if month.calendar_data and 'gregorian_dates' in month.calendar_data:
            for date_mapping in month.calendar_data['gregorian_dates']:
                hijri_day = date_mapping['hijri']
                gregorian_date = date_mapping['gregorian']
                
                # Find events for this day
                day_events = [event for event in events_data if event['day'] == hijri_day]
                
                # Find astronomical events for this day (comparing gregorian date)
                day_astro_events = [
                    event for event in astro_events_data 
                    if event['date'] == gregorian_date
                ]
                
                calendar_data.append({
                    'hijri_day': hijri_day,
                    'gregorian_date': gregorian_date,
                    'events': day_events,
                    'astronomical_events': day_astro_events
                })
        
        # Return the data
        return Response({
            'month': {
                'id': str(month.id),
                'name_ar': month.name_ar,
                'name_en': month.name_en,
                'number': month.number,
                'year': month.year,
                'gregorian_start': month.gregorian_start,
                'gregorian_end': month.gregorian_end,
                'moon_sighting_data': month.moon_sighting_data
            },
            'calendar': calendar_data,
            'events': events_data,
            'astronomical_events': astro_events_data
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_qibla_direction(request, latitude, longitude):
    """
    Calculate Qibla direction (angle from North) for a given location
    Kaaba coordinates: 21.422487, 39.826206
    """
    try:
        # Convert string coordinates to float
        lat = float(latitude)
        lng = float(longitude)
        
        # Mecca coordinates
        mecca_lat = 21.422487
        mecca_lng = 39.826206
        
        # Convert to radians
        lat_rad = math.radians(lat)
        lng_rad = math.radians(lng)
        mecca_lat_rad = math.radians(mecca_lat)
        mecca_lng_rad = math.radians(mecca_lng)
        
        # Calculate qibla direction
        y = math.sin(mecca_lng_rad - lng_rad)
        x = math.cos(lat_rad) * math.tan(mecca_lat_rad) - math.sin(lat_rad) * math.cos(mecca_lng_rad - lng_rad)
        qibla = math.atan2(y, x)
        qibla = math.degrees(qibla)
        
        # Convert to 0-360 range
        if qibla < 0:
            qibla += 360
            
        return JsonResponse({
            'direction': round(qibla, 2),
            'from_coordinates': f"{lat}, {lng}",
            'to_coordinates': f"{mecca_lat}, {mecca_lng}"
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def compass_view(request):
    """
    Render the compass page
    """
    return render(request, 'api/compass.html')
