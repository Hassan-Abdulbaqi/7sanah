from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Sha\'ban 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Sha'ban 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Sha\'ban', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Sha\'ban 1446H month and its related events'))
        
        # Create Sha'ban month
        shaaban = HijriMonth.objects.create(
            name_ar='شعبان',
            name_en='Sha\'ban',
            number=8,
            year=1446,
            gregorian_start=date(2025, 1, 31),  # Based on the image
            gregorian_end=date(2025, 3, 1),     # 30 days from January 31
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2025-01-30',
                    'time': '17:34',
                    'age': '25 hours',
                    'altitude': '10 degrees',
                    'stay_after_sunset': '1 hour 16 minutes',
                    'illumination_percentage': '1.45%',
                    'note': 'In this case, the crescent is expected to be seen clearly.'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2025-01-31'},
                    {'hijri': 2, 'gregorian': '2025-02-01'},
                    {'hijri': 3, 'gregorian': '2025-02-02'},
                    {'hijri': 4, 'gregorian': '2025-02-03'},
                    {'hijri': 5, 'gregorian': '2025-02-04'},
                    {'hijri': 6, 'gregorian': '2025-02-05'},
                    {'hijri': 7, 'gregorian': '2025-02-06'},
                    {'hijri': 8, 'gregorian': '2025-02-07'},
                    {'hijri': 9, 'gregorian': '2025-02-08'},
                    {'hijri': 10, 'gregorian': '2025-02-09'},
                    {'hijri': 11, 'gregorian': '2025-02-10'},
                    {'hijri': 12, 'gregorian': '2025-02-11'},
                    {'hijri': 13, 'gregorian': '2025-02-12'},
                    {'hijri': 14, 'gregorian': '2025-02-13'},
                    {'hijri': 15, 'gregorian': '2025-02-14'},
                    {'hijri': 16, 'gregorian': '2025-02-15'},
                    {'hijri': 17, 'gregorian': '2025-02-16'},
                    {'hijri': 18, 'gregorian': '2025-02-17'},
                    {'hijri': 19, 'gregorian': '2025-02-18'},
                    {'hijri': 20, 'gregorian': '2025-02-19'},
                    {'hijri': 21, 'gregorian': '2025-02-20'},
                    {'hijri': 22, 'gregorian': '2025-02-21'},
                    {'hijri': 23, 'gregorian': '2025-02-22'},
                    {'hijri': 24, 'gregorian': '2025-02-23'},
                    {'hijri': 25, 'gregorian': '2025-02-24'},
                    {'hijri': 26, 'gregorian': '2025-02-25'},
                    {'hijri': 27, 'gregorian': '2025-02-26'},
                    {'hijri': 28, 'gregorian': '2025-02-27'},
                    {'hijri': 29, 'gregorian': '2025-02-28'},
                    {'hijri': 30, 'gregorian': '2025-03-01'}
                    # Sha'ban is 30 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Sha\'ban 1446H month'))
        
        # Create historical events for Sha'ban based on the image
        events_data = [
            {
                'title_ar': 'ولادة سبط النبي الأكرم (ص) الإمام الحسين بن علي (ع)',
                'title_en': 'Birth of Imam Hussein ibn Ali (AS), grandson of Prophet Muhammad (PBUH)',
                'description_ar': 'الثالث منه ولادة سبط النبي الأكرم (ص) الإمام الحسين بن علي (ع)، سنة (4هـ)',
                'day': 3,
                'year_of_event': 4,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'دخول الإمام الحسين (ع) مكة',
                'title_en': 'Entry of Imam Hussein (AS) to Mecca',
                'description_ar': 'الثالث منه دخول الإمام الحسين (ع) مكة، سنة (60هـ)',
                'day': 3,
                'year_of_event': 60,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة العباس بن علي بن أبي طالب (ع)',
                'title_en': 'Birth of al-Abbas ibn Ali ibn Abi Talib (AS)',
                'description_ar': 'الرابع منه ولادة العباس بن علي بن أبي طالب (ع)، سنة (26هـ)',
                'day': 4,
                'year_of_event': 26,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة الإمام علي بن الحسين زين العابدين (ع)',
                'title_en': 'Birth of Imam Ali ibn al-Hussein Zain al-Abidin (AS)',
                'description_ar': 'الخامس منه ولادة الإمام علي بن الحسين زين العابدين (ع)، سنة (38هـ)',
                'day': 5,
                'year_of_event': 38,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة علي الأكبر بن الإمام الحسين (ع)',
                'title_en': 'Birth of Ali al-Akbar, son of Imam Hussein (AS)',
                'description_ar': 'الحادي عشر منه ولادة علي الأكبر بن الإمام الحسين (ع)، سنة (33هـ)',
                'day': 11,
                'year_of_event': 33,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة الحسين بن روح (رضي الله عنه) السفير الثالث للإمام المهدي (عجل الله تعالى فرجه الشريف)',
                'title_en': 'Death of Hussein ibn Ruh, the third ambassador of Imam al-Mahdi (AS)',
                'description_ar': 'الثاني عشر منه وفاة الحسين بن روح (رضي الله عنه) السفير الثالث للإمام المهدي (عجل الله تعالى فرجه الشريف)، سنة (326هـ)',
                'day': 12,
                'year_of_event': 326,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة بقية الله الأعظم الحجة بن الحسن العسكري (عجل الله تعالى فرجه الشريف)',
                'title_en': 'Birth of Imam al-Mahdi (AS)',
                'description_ar': 'الخامس عشر منه ولادة بقية الله الأعظم الحجة بن الحسن العسكري (عجل الله تعالى فرجه الشريف)، سنة (255هـ)',
                'day': 15,
                'year_of_event': 255,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة علي بن محمد السمري (رضي الله عنه) السفير الرابع للإمام المهدي (عجل الله تعالى فرجه الشريف)',
                'title_en': 'Death of Ali ibn Muhammad al-Samari, the fourth ambassador of Imam al-Mahdi (AS)',
                'description_ar': 'الخامس عشر منه وفاة علي بن محمد السمري (رضي الله عنه) السفير الرابع للإمام المهدي (عجل الله تعالى فرجه الشريف)، سنة (329هـ) وفي هذا اليوم بدأت الغيبة الكبرى',
                'day': 15,
                'year_of_event': 329,
                'event_type': 'historical'
            },
            {
                'title_ar': 'غزوة بني المصطلق',
                'title_en': 'Battle of Bani al-Mustaliq',
                'description_ar': 'التاسع عشر منه غزوة بني المصطلق، سنة (5هـ)',
                'day': 19,
                'year_of_event': 5,
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
                month=shaaban,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Sha\'ban'))
        
        # Create astronomical events based on the image
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2025, 2, 18),
                'time': time(3, 20),  # 3:20 AM
                'description_ar': 'يدخل القمر في برج العقرب يوم الثلاثاء (18/شباط/2025م) في الساعة (3:20) صباحاً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2025, 2, 20),
                'time': time(15, 5),  # 3:05 PM
                'description_ar': 'يخرج القمر من برج العقرب يوم الخميس (20/شباط/2025م) في الساعة (3:05) مساءً'
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
                month=shaaban,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Sha\'ban')) 