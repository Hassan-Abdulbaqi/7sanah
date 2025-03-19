from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Rabi al-Thani 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Rabi al-Thani 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Rabi al-Thani', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Rabi al-Thani 1446H month and its related events'))
        
        # Create Rabi al-Thani month
        rabi_thani = HijriMonth.objects.create(
            name_ar='ربيع الآخر',
            name_en='Rabi al-Thani',
            number=4,
            year=1446,
            gregorian_start=date(2024, 10, 5),  # Based on the image
            gregorian_end=date(2024, 11, 3),    # 30 days from October 5
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2024-10-04',
                    'time': '19:43',
                    'age': '23 hours',
                    'altitude': '7 degrees',
                    'stay_after_sunset': '42 minutes',
                    'illumination_percentage': '2.31%'
                },
                'alternative_sighting': {
                    'date': '2024-10-03',
                    'time': '19:44',
                    'age': '19 hours',
                    'altitude': '2 degrees',
                    'stay_after_sunset': '15 minutes',
                    'illumination_percentage': '0.48%',
                    'note': 'Difficult to see with naked eye'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2024-10-05'},
                    {'hijri': 2, 'gregorian': '2024-10-06'},
                    {'hijri': 3, 'gregorian': '2024-10-07'},
                    {'hijri': 4, 'gregorian': '2024-10-08'},
                    {'hijri': 5, 'gregorian': '2024-10-09'},
                    {'hijri': 6, 'gregorian': '2024-10-10'},
                    {'hijri': 7, 'gregorian': '2024-10-11'},
                    {'hijri': 8, 'gregorian': '2024-10-12'},
                    {'hijri': 9, 'gregorian': '2024-10-13'},
                    {'hijri': 10, 'gregorian': '2024-10-14'},
                    {'hijri': 11, 'gregorian': '2024-10-15'},
                    {'hijri': 12, 'gregorian': '2024-10-16'},
                    {'hijri': 13, 'gregorian': '2024-10-17'},
                    {'hijri': 14, 'gregorian': '2024-10-18'},
                    {'hijri': 15, 'gregorian': '2024-10-19'},
                    {'hijri': 16, 'gregorian': '2024-10-20'},
                    {'hijri': 17, 'gregorian': '2024-10-21'},
                    {'hijri': 18, 'gregorian': '2024-10-22'},
                    {'hijri': 19, 'gregorian': '2024-10-23'},
                    {'hijri': 20, 'gregorian': '2024-10-24'},
                    {'hijri': 21, 'gregorian': '2024-10-25'},
                    {'hijri': 22, 'gregorian': '2024-10-26'},
                    {'hijri': 23, 'gregorian': '2024-10-27'},
                    {'hijri': 24, 'gregorian': '2024-10-28'},
                    {'hijri': 25, 'gregorian': '2024-10-29'},
                    {'hijri': 26, 'gregorian': '2024-10-30'},
                    {'hijri': 27, 'gregorian': '2024-10-31'},
                    {'hijri': 28, 'gregorian': '2024-11-01'},
                    {'hijri': 29, 'gregorian': '2024-11-02'},
                    {'hijri': 30, 'gregorian': '2024-11-03'}
                    # Rabi al-Thani is 30 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Rabi al-Thani 1446H month'))
        
        # Create historical events for Rabi al-Thani based on the image
        events_data = [
            {
                'title_ar': 'شهادة سيدة نساء العالمين فاطمة الزهراء (ع)',
                'title_en': 'Martyrdom of Lady Fatima al-Zahra (AS)',
                'description_ar': 'الثامن منه شهادة سيدة نساء العالمين فاطمة الزهراء (ع)، سنة (11هـ)، على رواية',
                'day': 8,
                'year_of_event': 11,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة الإمام الحسن العسكري (ع)',
                'title_en': 'Birth of Imam Hassan al-Askari (AS)',
                'description_ar': 'العاشر منه ولادة الإمام الحسن العسكري (ع)، سنة (232هـ)، على رواية',
                'day': 10,
                'year_of_event': 232,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة السيدة فاطمة المعصومة بنت الإمام موسى بن جعفر الكاظم (ع)',
                'title_en': 'Death of Lady Fatima al-Masouma, daughter of Imam Musa ibn Jafar al-Kadhim (AS)',
                'description_ar': 'العاشر منه وفاة السيدة فاطمة المعصومة بنت الإمام موسى بن جعفر الكاظم (ع)، سنة (201هـ)، على رواية',
                'day': 10,
                'year_of_event': 201,
                'event_type': 'historical'
            },
            {
                'title_ar': 'خروج المختار الثقفي (ع) في الكوفة للأخذ بثأر الإمام الحسين (ع)',
                'title_en': 'Uprising of al-Mukhtar al-Thaqafi in Kufa to avenge Imam Hussein (AS)',
                'description_ar': 'الرابع عشر منه خروج المختار الثقفي (ع) في الكوفة للأخذ بثأر الإمام الحسين (ع)، سنة (66هـ)',
                'day': 14,
                'year_of_event': 66,
                'event_type': 'historical'
            }
        ]
        
        # Create events
        events_created = 0
        for event_data in events_data:
            event = HijriEvent.objects.create(
                title_ar=event_data['title_ar'],
                title_en=event_data.get('title_en'),
                description_ar=event_data.get('description_ar'),
                description_en=event_data.get('description_en'),
                day=event_data['day'],
                month=rabi_thani,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Rabi al-Thani'))
        
        # Create astronomical events based on the image
        astronomical_events_data = [
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2024, 10, 7),
                'time': time(2, 34),  # 2:34 AM
                'description_ar': 'يخرج القمر من برج العقرب يوم الإثنين (7/تشرين الأول/2024م) في الساعة (2:34) صباحاً'
            },
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2024, 10, 31),
                'time': time(8, 31),  # 8:31 PM
                'description_ar': 'يدخل القمر في برج العقرب يوم الخميس (31/تشرين الأول/2024م) في الساعة (8:31) مساءً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2024, 11, 3),
                'time': time(8, 19),  # 8:19 AM
                'description_ar': 'يخرج القمر من برج العقرب يوم الأحد (3/تشرين الثاني/2024م) في الساعة (8:19) صباحاً'
            }
        ]
        
        # Create astronomical events
        astro_events_created = 0
        for astro_event_data in astronomical_events_data:
            astro_event = AstronomicalEvent.objects.create(
                title_ar=astro_event_data['title_ar'],
                title_en=astro_event_data.get('title_en'),
                date=astro_event_data['date'],
                time=astro_event_data['time'],
                month=rabi_thani,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Rabi al-Thani')) 