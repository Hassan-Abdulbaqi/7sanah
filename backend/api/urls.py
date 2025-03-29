from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (
    home, get_juz_text, get_surah_text, KhatmahViewSet, ParticipantViewSet, JuzAssignmentViewSet,
    SurahAssignmentViewSet, HijriMonthViewSet, HijriEventViewSet, AstronomicalEventViewSet, 
    test_api_view, get_hijri_calendar, calendar_dashboard, get_qibla_direction, compass_view
)

router = DefaultRouter()
router.register(r'khatmahs', KhatmahViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'assignments', JuzAssignmentViewSet)
router.register(r'surah-assignments', SurahAssignmentViewSet)
router.register(r'hijri-months', HijriMonthViewSet)
router.register(r'hijri-events', HijriEventViewSet)
router.register(r'astronomical-events', AstronomicalEventViewSet)

# Common API patterns
api_patterns = [
    path('hijri-calendar/', get_hijri_calendar, name='hijri-calendar'),
    path('juz/<int:juz_number>/text/', get_juz_text, name='juz-text'),
    path('surah/<int:surah_number>/text/', get_surah_text, name='surah-text'),
    path('qibla/<str:latitude>/<str:longitude>/', get_qibla_direction, name='qibla-direction'),
    path('', include(router.urls)),
]

urlpatterns = [
    # API documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Utility endpoints
    path('home/', home, name='home'),
    path('test/', test_api_view, name='test-api'),
    path('calendar-dashboard/', calendar_dashboard, name='calendar-dashboard'),
    path('compass/', compass_view, name='compass'),
    
    # API endpoints (both versioned and unversioned)
    *api_patterns,  # Unversioned endpoints
    path('v1/', include((api_patterns, 'v1'))),  # v1 endpoints
]