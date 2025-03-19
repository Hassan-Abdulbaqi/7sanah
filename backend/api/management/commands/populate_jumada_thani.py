from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Jumada al-Thani 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Jumada al-Thani 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Jumada al-Thani', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Jumada al-Thani 1446H month and its related events'))
        
        # Create Jumada al-Thani month
        jumada_thani = HijriMonth.objects.create(
            name_ar='جمادى الآخرة',
            name_en='Jumada al-Thani',
            number=6,
            year=1446,
            gregorian_start=date(2024, 12, 3),  # Based on the image
            gregorian_end=date(2025, 1, 1),     # 30 days from December 3
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2024-12-02',
                    'time': '16:57',
                    'age': '31 hours',
                    'altitude': '6 degrees',
                    'stay_after_sunset': '41 minutes',
                    'illumination_percentage': '1.62%',
                    'note': 'In this case, the crescent is expected to be seen very faintly with clear skies.'
                },
                'alternative_sighting': {
                    'date': '2024-12-01',
                    'time': '16:57',
                    'age': '25 hours',
                    'altitude': '2 degrees',
                    'stay_after_sunset': '18 minutes',
                    'illumination_percentage': '0.90%',
                    'note': 'In this case, it is not possible to see the crescent even with armed eyes.'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2024-12-03'},
                    {'hijri': 2, 'gregorian': '2024-12-04'},
                    {'hijri': 3, 'gregorian': '2024-12-05'},
                    {'hijri': 4, 'gregorian': '2024-12-06'},
                    {'hijri': 5, 'gregorian': '2024-12-07'},
                    {'hijri': 6, 'gregorian': '2024-12-08'},
                    {'hijri': 7, 'gregorian': '2024-12-09'},
                    {'hijri': 8, 'gregorian': '2024-12-10'},
                    {'hijri': 9, 'gregorian': '2024-12-11'},
                    {'hijri': 10, 'gregorian': '2024-12-12'},
                    {'hijri': 11, 'gregorian': '2024-12-13'},
                    {'hijri': 12, 'gregorian': '2024-12-14'},
                    {'hijri': 13, 'gregorian': '2024-12-15'},
                    {'hijri': 14, 'gregorian': '2024-12-16'},
                    {'hijri': 15, 'gregorian': '2024-12-17'},
                    {'hijri': 16, 'gregorian': '2024-12-18'},
                    {'hijri': 17, 'gregorian': '2024-12-19'},
                    {'hijri': 18, 'gregorian': '2024-12-20'},
                    {'hijri': 19, 'gregorian': '2024-12-21'},
                    {'hijri': 20, 'gregorian': '2024-12-22'},
                    {'hijri': 21, 'gregorian': '2024-12-23'},
                    {'hijri': 22, 'gregorian': '2024-12-24'},
                    {'hijri': 23, 'gregorian': '2024-12-25'},
                    {'hijri': 24, 'gregorian': '2024-12-26'},
                    {'hijri': 25, 'gregorian': '2024-12-27'},
                    {'hijri': 26, 'gregorian': '2024-12-28'},
                    {'hijri': 27, 'gregorian': '2024-12-29'},
                    {'hijri': 28, 'gregorian': '2024-12-30'},
                    {'hijri': 29, 'gregorian': '2024-12-31'},
                    {'hijri': 30, 'gregorian': '2025-01-01'}
                    # Jumada al-Thani is 30 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Jumada al-Thani 1446H month'))
        
        # Create historical events for Jumada al-Thani based on the image
        events_data = [
            {
                'title_ar': 'شهادة سيدة نساء العالمين فاطمة الزهراء (ع)',
                'title_en': 'Martyrdom of Lady Fatima al-Zahra (AS)',
                'description_ar': 'اليوم الثالث منه شهادة سيدة نساء العالمين فاطمة الزهراء (ع)، سنة (11هـ)، على رواية',
                'day': 3,
                'year_of_event': 11,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة أم البنين أم العباس وإخوته (سلام الله عليهم)',
                'title_en': 'Death of Umm al-Banin, mother of al-Abbas and his brothers',
                'description_ar': 'الثالث عشر منه وفاة أم البنين أم العباس وإخوته (سلام الله عليهم)، سنة (64هـ)',
                'day': 13,
                'year_of_event': 64,
                'event_type': 'historical'
            },
            {
                'title_ar': 'زواج عبد الله وآمنة والدي النبي الأكرم (ص)',
                'title_en': 'Marriage of Abdullah and Amina, parents of Prophet Muhammad (PBUH)',
                'description_ar': 'التاسع عشر منه زواج عبد الله وآمنة والدي النبي الأكرم (ص)',
                'day': 19,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة سيدة نساء العالمين فاطمة الزهراء (ع)',
                'title_en': 'Birth of Lady Fatima al-Zahra (AS)',
                'description_ar': 'العشرون منه ولادة سيدة نساء العالمين فاطمة الزهراء (ع)، سنة (8) قبل الهجرة',
                'day': 20,
                'year_of_event': -8,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'رجوع الإمام أمير المؤمنين (ع) من حرب الجمل',
                'title_en': 'Return of Imam Ali (AS) from the Battle of the Camel',
                'description_ar': 'الحادي والعشرون منه رجوع الإمام أمير المؤمنين (ع) من حرب الجمل، سنة (36هـ)',
                'day': 21,
                'year_of_event': 36,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة أم كلثوم بنت الإمام أمير المؤمنين (ع)',
                'title_en': 'Death of Umm Kulthum, daughter of Imam Ali (AS)',
                'description_ar': 'الحادي والعشرون منه وفاة أم كلثوم بنت الإمام أمير المؤمنين (ع)، سنة (61هـ)',
                'day': 21,
                'year_of_event': 61,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة السيد محمد بن الإمام علي الهادي (ع)',
                'title_en': 'Death of Sayyid Muhammad, son of Imam Ali al-Hadi (AS)',
                'description_ar': 'التاسع والعشرون منه وفاة السيد محمد بن الإمام علي الهادي (ع)، سنة 252 هـ',
                'day': 29,
                'year_of_event': 252,
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
                month=jumada_thani,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Jumada al-Thani'))
        
        # Create astronomical events based on the image
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2024, 12, 25),
                'time': time(11, 8),  # 11:08 AM
                'description_ar': 'يدخل القمر في برج العقرب يوم الأربعاء (25/كانون الأول/2024م) في الساعة (11:08) صباحاً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2024, 12, 27),
                'time': time(22, 46),  # 10:46 PM
                'description_ar': 'يخرج القمر من برج العقرب يوم الجمعة (27/كانون الأول/2024م) في الساعة (10:46) مساءً'
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
                month=jumada_thani,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Jumada al-Thani')) 