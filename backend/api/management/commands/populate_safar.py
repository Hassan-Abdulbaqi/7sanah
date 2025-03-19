from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Safar 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Safar 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Safar', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Safar 1446H month and its related events'))
        
        # Create Safar month
        safar = HijriMonth.objects.create(
            name_ar='صفر',
            name_en='Safar',
            number=2,
            year=1446,
            gregorian_start=date(2024, 8, 6),  # Updated to August 6
            gregorian_end=date(2024, 9, 4),    # 30 days from August 6
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2024-08-06',
                    'time': '20:06',
                    'age': '28 hours',
                    'altitude': '9 degrees',
                    'stay_after_sunset': '50 minutes',
                    'illumination_percentage': '1.17%',
                    'note': 'In this case, it is expected to be able to see the crescent with the naked eye.'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2024-08-06'},
                    {'hijri': 2, 'gregorian': '2024-08-07'},
                    {'hijri': 3, 'gregorian': '2024-08-08'},
                    {'hijri': 4, 'gregorian': '2024-08-09'},
                    {'hijri': 5, 'gregorian': '2024-08-10'},
                    {'hijri': 6, 'gregorian': '2024-08-11'},
                    {'hijri': 7, 'gregorian': '2024-08-12'},
                    {'hijri': 8, 'gregorian': '2024-08-13'},
                    {'hijri': 9, 'gregorian': '2024-08-14'},
                    {'hijri': 10, 'gregorian': '2024-08-15'},
                    {'hijri': 11, 'gregorian': '2024-08-16'},
                    {'hijri': 12, 'gregorian': '2024-08-17'},
                    {'hijri': 13, 'gregorian': '2024-08-18'},
                    {'hijri': 14, 'gregorian': '2024-08-19'},
                    {'hijri': 15, 'gregorian': '2024-08-20'},
                    {'hijri': 16, 'gregorian': '2024-08-21'},
                    {'hijri': 17, 'gregorian': '2024-08-22'},
                    {'hijri': 18, 'gregorian': '2024-08-23'},
                    {'hijri': 19, 'gregorian': '2024-08-24'},
                    {'hijri': 20, 'gregorian': '2024-08-25'},
                    {'hijri': 21, 'gregorian': '2024-08-26'},
                    {'hijri': 22, 'gregorian': '2024-08-27'},
                    {'hijri': 23, 'gregorian': '2024-08-28'},
                    {'hijri': 24, 'gregorian': '2024-08-29'},
                    {'hijri': 25, 'gregorian': '2024-08-30'},
                    {'hijri': 26, 'gregorian': '2024-08-31'},
                    {'hijri': 27, 'gregorian': '2024-09-01'},
                    {'hijri': 28, 'gregorian': '2024-09-02'},
                    {'hijri': 29, 'gregorian': '2024-09-03'},
                    {'hijri': 30, 'gregorian': '2024-09-04'}
                    # Safar is 30 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Safar 1446H month'))
        
        # Create historical events for Safar
        events_data = [
            {
                'title_ar': 'اليوم الأول منه واقعة صفين',
                'title_en': 'First day of the Battle of Siffin',
                'description_ar': 'اليوم الأول منه واقعة صفين، سنة (37هـ)',
                'day': 1,
                'year_of_event': 37,
                'event_type': 'historical'
            },
            {
                'title_ar': 'الأول منه دخول سبايا آل البيت (ع) الى بلاد الشام',
                'title_en': 'Entry of the captives of Ahlul Bayt (AS) to Damascus',
                'description_ar': 'الأول منه دخول سبايا آل البيت (ع) الى بلاد الشام، سنة (61هـ)',
                'day': 1,
                'year_of_event': 61,
                'event_type': 'historical'
            },
            {
                'title_ar': 'الثاني منه شهادة زيد بن علي بن الحسين(ع)',
                'title_en': 'Martyrdom of Zayd ibn Ali ibn Husayn (AS)',
                'description_ar': 'الثاني منه شهادة زيد بن علي بن الحسين(ع)، سنة (121هـ)',
                'day': 2,
                'year_of_event': 121,
                'event_type': 'historical'
            },
            {
                'title_ar': 'الخامس منه شهادة رقية بنت الإمام الحسين(ع)',
                'title_en': 'Martyrdom of Ruqayyah bint Imam Husayn (AS)',
                'description_ar': 'الخامس منه شهادة رقية بنت الإمام الحسين(ع)، سنة (61هـ)',
                'day': 5,
                'year_of_event': 61,
                'event_type': 'historical'
            },
            {
                'title_ar': 'السابع منه شهادة الإمام الحسن بن علي بن ابي طالب (ع)',
                'title_en': 'Martyrdom of Imam Hasan ibn Ali ibn Abi Talib (AS)',
                'description_ar': 'السابع منه شهادة الإمام الحسن بن علي بن ابي طالب (ع)، سنة (50هـ)',
                'day': 7,
                'year_of_event': 50,
                'event_type': 'historical'
            },
            {
                'title_ar': 'الثامن منه وفاة الصحابي الجليل سلمان الفارسي (رضي الله عنه)',
                'title_en': 'Death of the companion Salman al-Farsi (RA)',
                'description_ar': 'الثامن منه وفاة الصحابي الجليل سلمان الفارسي (رضي الله عنه)، سنة (35هـ)',
                'day': 8,
                'year_of_event': 35,
                'event_type': 'historical'
            },
            {
                'title_ar': 'التاسع منه شهادة الصحابي الجليل عمار بن ياسر (رضي الله عنه)',
                'title_en': 'Martyrdom of the companion Ammar ibn Yasir (RA)',
                'description_ar': 'التاسع منه شهادة الصحابي الجليل عمار بن ياسر (رضي الله عنه)، سنة (37هـ)، في معركة صفين',
                'day': 9,
                'year_of_event': 37,
                'event_type': 'historical'
            },
            {
                'title_ar': 'التاسع منه واقعة النهروان',
                'title_en': 'Battle of Nahrawan',
                'description_ar': 'التاسع منه واقعة النهروان، سنة (38هـ)',
                'day': 9,
                'year_of_event': 38,
                'event_type': 'historical'
            },
            {
                'title_ar': 'الرابع عشر منه شهادة محمد بن أبي بكر (رضي الله عنه) في مصر',
                'title_en': 'Martyrdom of Muhammad ibn Abi Bakr (RA) in Egypt',
                'description_ar': 'الرابع عشر منه شهادة محمد بن أبي بكر (رضي الله عنه) في مصر، سنة (38هـ)',
                'day': 14,
                'year_of_event': 38,
                'event_type': 'historical'
            },
            {
                'title_ar': 'السابع عشر منه شهادة الإمام علي بن موسى الرضا (ع)',
                'title_en': 'Martyrdom of Imam Ali ibn Musa al-Ridha (AS)',
                'description_ar': 'السابع عشر منه شهادة الإمام علي بن موسى الرضا (ع)، سنة (203هـ)، على رواية',
                'day': 17,
                'year_of_event': 203,
                'event_type': 'historical'
            },
            {
                'title_ar': 'العشرون منه ورود السبايا من آل بيت النبي(ص) أرض كربلاء',
                'title_en': 'Arrival of the captives of Ahlul Bayt (AS) to Karbala',
                'description_ar': 'العشرون منه ورود السبايا من آل بيت النبي(ص) أرض كربلاء، سنة (61هـ)',
                'day': 20,
                'year_of_event': 61,
                'event_type': 'historical'
            },
            {
                'title_ar': 'الثامن والعشرون منه وفاة النبي الأكرم (ص)',
                'title_en': 'Death of Prophet Muhammad (PBUH)',
                'description_ar': 'الثامن والعشرون منه وفاة النبي الأكرم (ص)، سنة (11هـ)',
                'day': 28,
                'year_of_event': 11,
                'is_holiday': True,
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
                month=safar,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Safar'))
        
        # Create astronomical events
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2024, 8, 11),
                'time': time(1, 36),  # 1:36 AM (after midnight)
                'description_ar': 'يدخل القمر في برج العقرب يوم الأحد (11/آب/2024م) في الساعة (1:36) بعد منتصف الليل'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2024, 8, 13),
                'time': time(12, 0),  # 12:00 PM (noon)
                'description_ar': 'يخرج القمر من برج العقرب يوم الثلاثاء (13/آب/2024م) في الساعة (12:00) ظهراً'
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
                month=safar,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Safar')) 