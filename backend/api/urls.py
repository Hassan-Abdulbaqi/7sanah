from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home, get_juz_text, KhatmahViewSet, ParticipantViewSet, JuzAssignmentViewSet,
    HijriMonthViewSet, HijriEventViewSet, AstronomicalEventViewSet, test_api_view,
    get_hijri_calendar, calendar_dashboard, get_qibla_direction, compass_view
)

router = DefaultRouter()
router.register(r'khatmahs', KhatmahViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'assignments', JuzAssignmentViewSet)
router.register(r'hijri-months', HijriMonthViewSet)
router.register(r'hijri-events', HijriEventViewSet)
router.register(r'astronomical-events', AstronomicalEventViewSet)

urlpatterns = [
    path('home/', home),
    path('test/', test_api_view, name='test-api'),
    path('hijri-calendar/', get_hijri_calendar, name='hijri-calendar'),
    path('juz/<int:juz_number>/text/', get_juz_text, name='juz-text'),
    path('calendar-dashboard/', calendar_dashboard, name='calendar-dashboard'),
    path('qibla/<str:latitude>/<str:longitude>/', get_qibla_direction, name='qibla-direction'),
    path('compass/', compass_view, name='compass'),
    path('', include(router.urls)),
]
