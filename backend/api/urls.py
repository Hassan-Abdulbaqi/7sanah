from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, get_juz_text, KhatmahViewSet, ParticipantViewSet, JuzAssignmentViewSet

router = DefaultRouter()
router.register(r'khatmahs', KhatmahViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'assignments', JuzAssignmentViewSet)

urlpatterns = [
    path('home/', home),
    path('juz/<int:juz_number>/text/', get_juz_text, name='juz-text'),
    path('', include(router.urls)),
]
