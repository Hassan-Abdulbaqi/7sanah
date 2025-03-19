from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Khatmah, Participant, JuzAssignment, HijriMonth, HijriEvent, AstronomicalEvent
from .serializers import (
    KhatmahSerializer, KhatmahListSerializer, ParticipantSerializer, JuzAssignmentSerializer,
    HijriMonthDetailSerializer, HijriMonthListSerializer, HijriEventSerializer, AstronomicalEventSerializer
)
import requests
from django.shortcuts import render
import math

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

# Hijri Calendar ViewSets
class HijriMonthPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 12

class HijriMonthViewSet(viewsets.ModelViewSet):
    queryset = HijriMonth.objects.all()
    pagination_class = HijriMonthPagination
    
    def get_serializer_class(self):
        if self.action == 'list':
            return HijriMonthListSerializer
        return HijriMonthDetailSerializer
    
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
    Calculate Qibla direction based on latitude and longitude coordinates
    
    The Qibla direction is calculated using the formula:
    qibla = atan2(sin(lon_k - lon_p), cos(lat_p) * tan(lat_k) - sin(lat_p) * cos(lon_k - lon_p))
    
    Where:
    - lat_k, lon_k are the coordinates of Kaaba (21.4225, 39.8262)
    - lat_p, lon_p are the coordinates of the given point
    """
    try:
        # Convert string parameters to float
        lat_p = float(latitude)
        lon_p = float(longitude)
        
        # Coordinates of Kaaba in Mecca
        lat_k = 21.4225  # latitude of Kaaba
        lon_k = 39.8262  # longitude of Kaaba
        
        # Convert to radians
        lat_p_rad = math.radians(lat_p)
        lon_p_rad = math.radians(lon_p)
        lat_k_rad = math.radians(lat_k)
        lon_k_rad = math.radians(lon_k)
        
        # Calculate the Qibla direction
        y = math.sin(lon_k_rad - lon_p_rad)
        x = math.cos(lat_p_rad) * math.tan(lat_k_rad) - math.sin(lat_p_rad) * math.cos(lon_k_rad - lon_p_rad)
        qibla_rad = math.atan2(y, x)
        
        # Convert to degrees and normalize to 0-360
        qibla_deg = math.degrees(qibla_rad)
        qibla_deg = (qibla_deg + 360) % 360
        
        return Response({
            "code": 200,
            "status": "OK",
            "data": {
                "latitude": lat_p,
                "longitude": lon_p,
                "direction": qibla_deg
            }
        })
    except ValueError:
        return Response({
            "code": 400,
            "status": "Bad Request",
            "data": "Invalid latitude or longitude values. Please provide valid numeric coordinates."
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "code": 500,
            "status": "Internal Server Error",
            "data": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
