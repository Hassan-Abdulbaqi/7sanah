from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Shawwal 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Shawwal 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Shawwal', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Shawwal 1446H month and its related events'))
        
        # Create Shawwal month
        shawwal = HijriMonth.objects.create(
            name_ar='شوال',
            name_en='Shawwal',
            number=10,
            year=1446,
            gregorian_start=date(2025, 3, 31),  # Updated to March 31 (Monday)
            gregorian_end=date(2025, 4, 28),    # Updated to April 28
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2025-03-30',
                    'time': '18:16',
                    'age': '28 hours',
                    'altitude': '15 degrees',
                    'stay_after_sunset': '1 hour 21 minutes',
                    'illumination_percentage': '2.14%',
                    'note': 'In this case, the crescent is expected to be seen clearly.'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2025-03-31'},  # Updated to March 31
                    {'hijri': 2, 'gregorian': '2025-04-01'},
                    {'hijri': 3, 'gregorian': '2025-04-02'},
                    {'hijri': 4, 'gregorian': '2025-04-03'},
                    {'hijri': 5, 'gregorian': '2025-04-04'},
                    {'hijri': 6, 'gregorian': '2025-04-05'},
                    {'hijri': 7, 'gregorian': '2025-04-06'},
                    {'hijri': 8, 'gregorian': '2025-04-07'},
                    {'hijri': 9, 'gregorian': '2025-04-08'},
                    {'hijri': 10, 'gregorian': '2025-04-09'},
                    {'hijri': 11, 'gregorian': '2025-04-10'},
                    {'hijri': 12, 'gregorian': '2025-04-11'},
                    {'hijri': 13, 'gregorian': '2025-04-12'},
                    {'hijri': 14, 'gregorian': '2025-04-13'},
                    {'hijri': 15, 'gregorian': '2025-04-14'},
                    {'hijri': 16, 'gregorian': '2025-04-15'},
                    {'hijri': 17, 'gregorian': '2025-04-16'},
                    {'hijri': 18, 'gregorian': '2025-04-17'},
                    {'hijri': 19, 'gregorian': '2025-04-18'},
                    {'hijri': 20, 'gregorian': '2025-04-19'},
                    {'hijri': 21, 'gregorian': '2025-04-20'},
                    {'hijri': 22, 'gregorian': '2025-04-21'},
                    {'hijri': 23, 'gregorian': '2025-04-22'},
                    {'hijri': 24, 'gregorian': '2025-04-23'},
                    {'hijri': 25, 'gregorian': '2025-04-24'},
                    {'hijri': 26, 'gregorian': '2025-04-25'},
                    {'hijri': 27, 'gregorian': '2025-04-26'},
                    {'hijri': 28, 'gregorian': '2025-04-27'},
                    {'hijri': 29, 'gregorian': '2025-04-28'}  # Updated to April 28
                    # Shawwal is 29 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Shawwal 1446H month'))
        
        # Create historical events for Shawwal based on the image
        events_data = [
            {
                'title_ar': 'عيد الفطر المبارك',
                'title_en': 'Eid al-Fitr',
                'description_ar': 'اليوم الأول منه عيد الفطر المبارك',
                'day': 1,
                'is_holiday': True,
                'event_type': 'religious'
            },
            {
                'title_ar': 'معركة الخندق',
                'title_en': 'Battle of the Trench (Khandaq)',
                'description_ar': 'الثالث منه معركة الخندق، سنة (5هـ)، على رواية',
                'day': 3,
                'year_of_event': 5,
                'event_type': 'historical'
            },
            {
                'title_ar': 'غزوة حنين',
                'title_en': 'Battle of Hunayn',
                'description_ar': 'الرابع منه غزوة حنين، سنة (8هـ)، على رواية',
                'day': 4,
                'year_of_event': 8,
                'event_type': 'historical'
            },
            {
                'title_ar': 'توجه الإمام أمير المؤمنين (ع) الى صفين',
                'title_en': 'Departure of Imam Ali (AS) to Siffin',
                'description_ar': 'الخامس منه توجه الإمام أمير المؤمنين (ع) الى صفين، سنة (36هـ)',
                'day': 5,
                'year_of_event': 36,
                'event_type': 'historical'
            },
            {
                'title_ar': 'هدم قبور أئمة البقيع (ع)',
                'title_en': 'Demolition of the graves of the Imams in al-Baqi',
                'description_ar': 'الثامن منه هدم قبور أئمة البقيع (ع)، سنة (1344هـ)',
                'day': 8,
                'year_of_event': 1344,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة السيد عبد العظيم الحسني (رضي الله عنه)',
                'title_en': 'Death of Sayyid Abdul Azim al-Hasani',
                'description_ar': 'الخامس عشر منه وفاة السيد عبد العظيم الحسني (رضي الله عنه)، سنة (252هـ)',
                'day': 15,
                'year_of_event': 252,
                'event_type': 'historical'
            },
            {
                'title_ar': 'معركة أحد وشهادة حمزة سيد الشهداء (ع)',
                'title_en': 'Battle of Uhud and martyrdom of Hamza, the Master of Martyrs',
                'description_ar': 'الخامس عشر منه معركة أحد وشهادة حمزة سيد الشهداء (ع)، سنة (3هـ)',
                'day': 15,
                'year_of_event': 3,
                'event_type': 'historical'
            },
            {
                'title_ar': 'رد الشمس للإمام أمير المؤمنين (ع) في المدينة المنورة في مسجد الفضيخ والمعروف بمسجد رد الشمس',
                'title_en': 'The sun was returned for Imam Ali (AS) in Medina at Masjid al-Fadikh',
                'description_ar': 'الخامس عشر منه رد الشمس للإمام أمير المؤمنين (ع) في المدينة المنورة في مسجد الفضيخ والمعروف بمسجد رد الشمس، سنة (3هـ)',
                'day': 15,
                'year_of_event': 3,
                'event_type': 'historical'
            },
            {
                'title_ar': 'غزوة بني القينقاع',
                'title_en': 'Battle of Banu Qaynuqa',
                'description_ar': 'الخامس عشر منه غزوة بني القينقاع، سنة (2هـ)',
                'day': 15,
                'year_of_event': 2,
                'event_type': 'historical'
            },
            {
                'title_ar': 'غزوة بني سليم',
                'title_en': 'Battle of Banu Sulaym',
                'description_ar': 'السابع عشر منه غزوة بني سليم، سنة (2هـ)',
                'day': 17,
                'year_of_event': 2,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة الإمام جعفر بن محمد الصادق (ع)',
                'title_en': 'Martyrdom of Imam Jafar ibn Muhammad al-Sadiq (AS)',
                'description_ar': 'الخامس والعشرون منه شهادة الإمام جعفر بن محمد الصادق (ع)، سنة (148هـ)',
                'day': 25,
                'year_of_event': 148,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'خروج النبي الأكرم (ص) الى الطائف لدعوتهم الى الإسلام',
                'title_en': 'Departure of Prophet Muhammad (PBUH) to Taif to invite them to Islam',
                'description_ar': 'السابع والعشرون منه خروج النبي الأكرم (ص) الى الطائف لدعوتهم الى الإسلام',
                'day': 27,
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
                month=shawwal,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Shawwal'))
        
        # Create astronomical events based on the image
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2025, 4, 13),
                'time': time(16, 55),  # 4:55 PM
                'description_ar': 'يدخل القمر في برج العقرب يوم الأحد (13/نيسان/2025م) في الساعة (4:55) مساءً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2025, 4, 16),
                'time': time(5, 37),  # 5:37 AM
                'description_ar': 'يخرج القمر من برج العقرب يوم الأربعاء (16/نيسان/2025م) في الساعة (5:37) صباحاً'
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
                month=shawwal,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Shawwal')) 