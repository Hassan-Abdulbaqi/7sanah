from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Muharram 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Muharram 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Muharram', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Muharram 1446H month and its related events'))
        
        # Create Muharram month
        muharram = HijriMonth.objects.create(
            name_ar='محرم الحرام',
            name_en='Muharram',
            number=1,
            year=1446,
            gregorian_start=date(2024, 7, 8),  # Updated to July 8
            gregorian_end=date(2024, 8, 5),    # End date remains August 5
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2024-07-08',  # Updated to July 8
                    'time': '21:01',
                    'age': '20 hours',
                    'altitude': '16 degrees',
                    'stay_after_sunset': '1 hour 28 minutes',
                    'illumination_percentage': '2.70%'
                },
                'alternative_sighting': {
                    'date': '2024-07-07',  # Keep as July 7 for alternative sighting
                    'time': '21:01',
                    'age': '17 hours',
                    'altitude': '8 degrees',
                    'stay_after_sunset': '47 minutes',
                    'illumination_percentage': '0.62%',
                    'note': 'Difficult to see with naked eye'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2024-07-08'},  # Updated to July 8
                    {'hijri': 2, 'gregorian': '2024-07-09'},
                    {'hijri': 3, 'gregorian': '2024-07-10'},
                    {'hijri': 4, 'gregorian': '2024-07-11'},
                    {'hijri': 5, 'gregorian': '2024-07-12'},
                    {'hijri': 6, 'gregorian': '2024-07-13'},
                    {'hijri': 7, 'gregorian': '2024-07-14'},
                    {'hijri': 8, 'gregorian': '2024-07-15'},
                    {'hijri': 9, 'gregorian': '2024-07-16'},
                    {'hijri': 10, 'gregorian': '2024-07-17'},
                    {'hijri': 11, 'gregorian': '2024-07-18'},
                    {'hijri': 12, 'gregorian': '2024-07-19'},
                    {'hijri': 13, 'gregorian': '2024-07-20'},
                    {'hijri': 14, 'gregorian': '2024-07-21'},
                    {'hijri': 15, 'gregorian': '2024-07-22'},
                    {'hijri': 16, 'gregorian': '2024-07-23'},
                    {'hijri': 17, 'gregorian': '2024-07-24'},
                    {'hijri': 18, 'gregorian': '2024-07-25'},
                    {'hijri': 19, 'gregorian': '2024-07-26'},
                    {'hijri': 20, 'gregorian': '2024-07-27'},
                    {'hijri': 21, 'gregorian': '2024-07-28'},
                    {'hijri': 22, 'gregorian': '2024-07-29'},
                    {'hijri': 23, 'gregorian': '2024-07-30'},
                    {'hijri': 24, 'gregorian': '2024-07-31'},
                    {'hijri': 25, 'gregorian': '2024-08-01'},
                    {'hijri': 26, 'gregorian': '2024-08-02'},
                    {'hijri': 27, 'gregorian': '2024-08-03'},
                    {'hijri': 28, 'gregorian': '2024-08-04'},
                    {'hijri': 29, 'gregorian': '2024-08-05'}
                    # Muharram is 29 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Muharram 1446H month'))
        
        # Create historical events for Muharram
        events_data = [
            {
                'title_ar': 'بداية السنة الهجرية',
                'title_en': 'Beginning of the Hijri Year',
                'description_ar': 'اليوم الأول من السنة الهجرية',
                'day': 1,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'بداية محاصرة النبي الأكرم (ص) في شعب أبي طالب',
                'title_en': 'Beginning of the siege of Prophet Muhammad (PBUH) in Shib Abi Talib',
                'description_ar': 'بداية محاصرة النبي الأكرم (ص) في شعب أبي طالب، سنة (3) قبل الهجرة',
                'day': 1,
                'year_of_event': -3,  # 3 years before Hijra
                'event_type': 'historical'
            },
            {
                'title_ar': 'ورود الإمام الحسين بن علي بن أبي طالب (ع) أرض كربلاء',
                'title_en': 'Arrival of Imam Hussein (AS) to Karbala',
                'description_ar': 'ورود الإمام الحسين بن علي بن أبي طالب (ع) أرض كربلاء، سنة (61هـ)',
                'day': 2,
                'year_of_event': 61,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ورود عمر بن سعد مع جيشه أرض كربلاء',
                'title_en': 'Arrival of Omar bin Saad with his army to Karbala',
                'description_ar': 'ورود عمر بن سعد مع جيشه أرض كربلاء، سنة (61هـ)',
                'day': 3,
                'year_of_event': 61,
                'event_type': 'historical'
            },
            {
                'title_ar': 'واقعة الطف واستشهاد الإمام الحسين (ع)',
                'title_en': 'Battle of Karbala and Martyrdom of Imam Hussein (AS)',
                'description_ar': 'واقعة الطف واستشهاد الإمام الحسين (ع)، سنة (61هـ)',
                'day': 10,
                'year_of_event': 61,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'دخول سبايا أهل البيت (ع) إلى الكوفة',
                'title_en': 'Entry of the captives of Ahlul Bayt (AS) to Kufa',
                'description_ar': 'دخول سبايا أهل البيت (ع) إلى الكوفة، سنة (61هـ)',
                'day': 12,
                'year_of_event': 61,
                'event_type': 'historical'
            },
            {
                'title_ar': 'دفن أجساد شهداء الطف (ع)',
                'title_en': 'Burial of the martyrs of Karbala',
                'description_ar': 'دفن أجساد شهداء الطف (ع)، سنة (61هـ)',
                'day': 13,
                'year_of_event': 61,
                'event_type': 'historical'
            },
            {
                'title_ar': 'خروج سبايا أهل البيت (ع) من الكوفة إلى الشام',
                'title_en': 'Departure of the captives of Ahlul Bayt (AS) from Kufa to Damascus',
                'description_ar': 'خروج سبايا أهل البيت (ع) من الكوفة إلى الشام، سنة (61هـ)',
                'day': 19,
                'year_of_event': 61,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وصول الإمام أمير المؤمنين (ع) إلى صفين',
                'title_en': 'Arrival of Imam Ali (AS) to Siffin',
                'description_ar': 'وصول الإمام أمير المؤمنين (ع) إلى صفين، سنة (37هـ)',
                'day': 22,
                'year_of_event': 37,
                'event_type': 'historical'
            },
            {
                'title_ar': 'الاعتداء الآثم بتفجير حرم الإمامين العسكريين (ع)',
                'title_en': 'Criminal attack on the shrine of the two Askari Imams (AS)',
                'description_ar': 'الاعتداء الآثم بتفجير حرم الإمامين العسكريين (ع)، سنة (1427هـ)',
                'day': 23,
                'year_of_event': 1427,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة الإمام علي بن الحسين زين العابدين(ع) في المدينة المنورة',
                'title_en': 'Martyrdom of Imam Ali bin Hussein Zain al-Abidin (AS) in Medina',
                'description_ar': 'شهادة الإمام علي بن الحسين زين العابدين(ع) في المدينة المنورة، سنة (95هـ)',
                'day': 25,
                'year_of_event': 95,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة علي بن الحسن المثلث (علي الخير) (رضي الله عنه)',
                'title_en': 'Martyrdom of Ali bin al-Hassan al-Muthallath (Ali al-Khair)',
                'description_ar': 'شهادة علي بن الحسن المثلث (علي الخير) (رضي الله عنه)، سنة (146هـ)',
                'day': 26,
                'year_of_event': 146,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة الصحابي الجليل حذيفة بن اليمان (رضي الله عنه)',
                'title_en': 'Death of the companion Hudhayfah ibn al-Yaman',
                'description_ar': 'وفاة الصحابي الجليل حذيفة بن اليمان (رضي الله عنه)، سنة (36هـ)',
                'day': 28,
                'year_of_event': 36,
                'event_type': 'historical'
            },
            {
                'title_ar': 'إحضار الإمام محمد بن علي الجواد (ع) من المدينة المنورة إلى بغداد',
                'title_en': 'Bringing Imam Muhammad bin Ali al-Jawad (AS) from Medina to Baghdad',
                'description_ar': 'إحضار الإمام محمد بن علي الجواد (ع) من المدينة المنورة إلى بغداد، سنة (220هـ)',
                'day': 28,
                'year_of_event': 220,
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
                month=muharram,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Muharram'))
        
        # Create astronomical events
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2024, 7, 14),
                'time': time(17, 5),  # 5:05 PM
                'description_ar': 'يدخل القمر برج العقرب يوم الأحد (14/تموز/2024م) في الساعة (5:05) مساءً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2024, 7, 17),
                'time': time(4, 25),  # 4:25 AM
                'description_ar': 'يخرج القمر من برج العقرب يوم الأربعاء (17/تموز/2024م) في الساعة (4:25) صباحاً'
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
                month=muharram,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Muharram')) 