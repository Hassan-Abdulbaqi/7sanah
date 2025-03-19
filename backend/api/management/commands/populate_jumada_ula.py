from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Jumada al-Ula 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Jumada al-Ula 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Jumada al-Ula', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Jumada al-Ula 1446H month and its related events'))
        
        # Create Jumada al-Ula month
        jumada_ula = HijriMonth.objects.create(
            name_ar='جمادى الأولى',
            name_en='Jumada al-Ula',
            number=5,
            year=1446,
            gregorian_start=date(2024, 11, 4),  # Based on the image
            gregorian_end=date(2024, 12, 2),    # 29 days from November 4
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2024-11-03',
                    'time': '19:10',
                    'age': '49 hours',
                    'altitude': '9 degrees',
                    'stay_after_sunset': '57 minutes',
                    'illumination_percentage': '3.24%'
                },
                'alternative_sighting': {
                    'date': '2024-11-02',
                    'time': '19:11',
                    'age': '25 hours',
                    'altitude': '2 degrees',
                    'stay_after_sunset': '18 minutes',
                    'illumination_percentage': '0.90%',
                    'note': 'Difficult to see with naked eye'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2024-11-04'},
                    {'hijri': 2, 'gregorian': '2024-11-05'},
                    {'hijri': 3, 'gregorian': '2024-11-06'},
                    {'hijri': 4, 'gregorian': '2024-11-07'},
                    {'hijri': 5, 'gregorian': '2024-11-08'},
                    {'hijri': 6, 'gregorian': '2024-11-09'},
                    {'hijri': 7, 'gregorian': '2024-11-10'},
                    {'hijri': 8, 'gregorian': '2024-11-11'},
                    {'hijri': 9, 'gregorian': '2024-11-12'},
                    {'hijri': 10, 'gregorian': '2024-11-13'},
                    {'hijri': 11, 'gregorian': '2024-11-14'},
                    {'hijri': 12, 'gregorian': '2024-11-15'},
                    {'hijri': 13, 'gregorian': '2024-11-16'},
                    {'hijri': 14, 'gregorian': '2024-11-17'},
                    {'hijri': 15, 'gregorian': '2024-11-18'},
                    {'hijri': 16, 'gregorian': '2024-11-19'},
                    {'hijri': 17, 'gregorian': '2024-11-20'},
                    {'hijri': 18, 'gregorian': '2024-11-21'},
                    {'hijri': 19, 'gregorian': '2024-11-22'},
                    {'hijri': 20, 'gregorian': '2024-11-23'},
                    {'hijri': 21, 'gregorian': '2024-11-24'},
                    {'hijri': 22, 'gregorian': '2024-11-25'},
                    {'hijri': 23, 'gregorian': '2024-11-26'},
                    {'hijri': 24, 'gregorian': '2024-11-27'},
                    {'hijri': 25, 'gregorian': '2024-11-28'},
                    {'hijri': 26, 'gregorian': '2024-11-29'},
                    {'hijri': 27, 'gregorian': '2024-11-30'},
                    {'hijri': 28, 'gregorian': '2024-12-01'},
                    {'hijri': 29, 'gregorian': '2024-12-02'}
                    # Jumada al-Ula is 29 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Jumada al-Ula 1446H month'))
        
        # Create historical events for Jumada al-Ula based on the image
        events_data = [
            {
                'title_ar': 'ولادة السيدة زينب بنت الإمام أمير المؤمنين (ع)',
                'title_en': 'Birth of Lady Zainab, daughter of Imam Ali (AS)',
                'description_ar': 'اليوم الخامس منه ولادة السيدة زينب بنت الإمام أمير المؤمنين (ع)، سنة (5هـ)',
                'day': 5,
                'year_of_event': 5,
                'event_type': 'historical'
            },
            {
                'title_ar': 'اليوم السادس منه حرب مؤتة واستشهاد جعفر بن أبي طالب (ع)',
                'title_en': 'Battle of Mu\'tah and martyrdom of Ja\'far ibn Abi Talib (AS)',
                'description_ar': 'اليوم السادس منه حرب مؤتة واستشهاد جعفر بن أبي طالب (ع)، سنة (8هـ)',
                'day': 6,
                'year_of_event': 8,
                'event_type': 'historical'
            },
            {
                'title_ar': 'العاشر منه واقعة الجمل',
                'title_en': 'Battle of the Camel',
                'description_ar': 'العاشر منه واقعة الجمل، سنة (36هـ)',
                'day': 10,
                'year_of_event': 36,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة سيدة نساء العالمين فاطمة الزهراء (ع)',
                'title_en': 'Martyrdom of Lady Fatima al-Zahra (AS)',
                'description_ar': 'الثالث عشر منه شهادة سيدة نساء العالمين فاطمة الزهراء (ع)، سنة (11هـ)، على رواية',
                'day': 13,
                'year_of_event': 11,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'فتح البصرة على يد الإمام أمير المؤمنين (ع)',
                'title_en': 'Conquest of Basra by Imam Ali (AS)',
                'description_ar': 'الخامس عشر منه فتح البصرة على يد الإمام أمير المؤمنين (ع)، سنة (36هـ)',
                'day': 15,
                'year_of_event': 36,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة زيد بن صوحان (رضي الله عنه) في حرب الجمل',
                'title_en': 'Martyrdom of Zayd ibn Suhan in the Battle of the Camel',
                'description_ar': 'التاسع عشر منه شهادة زيد بن صوحان (رضي الله عنه) في حرب الجمل، سنة (36هـ)',
                'day': 19,
                'year_of_event': 36,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة القاسم بن الإمام موسى بن جعفر (ع)',
                'title_en': 'Death of al-Qasim, son of Imam Musa ibn Ja\'far (AS)',
                'description_ar': 'الثاني والعشرون منه وفاة القاسم بن الإمام موسى بن جعفر (ع)، سنة (192هـ) على رواية',
                'day': 22,
                'year_of_event': 192,
                'event_type': 'historical'
            },
            {
                'title_ar': 'تجدد الاعتداء على مرقد الإمامين العسكريين (ع) في سامراء بتفجير المئذنتين الشريفتين',
                'title_en': 'Renewed attack on the shrine of the two Askari Imams (AS) in Samarra with the bombing of the two noble minarets',
                'description_ar': 'السابع والعشرون منه تجدد الاعتداء على مرقد الإمامين العسكريين (ع) في سامراء بتفجير المئذنتين الشريفتين، سنة (1428هـ)',
                'day': 27,
                'year_of_event': 1428,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة محمد بن عثمان بن سعيد الخلاني (رضي الله عنه) السفير الثاني للإمام المهدي (عجل الله تعالى فرجه الشريف)',
                'title_en': 'Death of Muhammad ibn Uthman ibn Sa\'id al-Khallani, the second ambassador of Imam al-Mahdi (AS)',
                'description_ar': 'آخر يوم منه وفاة محمد بن عثمان بن سعيد الخلاني (رضي الله عنه) السفير الثاني للإمام المهدي (عجل الله تعالى فرجه الشريف)، سنة (304هـ)',
                'day': 29,
                'year_of_event': 304,
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
                month=jumada_ula,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Jumada al-Ula'))
        
        # Create astronomical events based on the image
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2024, 11, 28),
                'time': time(3, 32),  # 3:32 AM
                'description_ar': 'يدخل القمر في برج العقرب يوم الخميس (28/تشرين الثاني/2024م) في الساعة (3:32) صباحاً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2024, 11, 30),
                'time': time(14, 53),  # 2:53 PM
                'description_ar': 'يخرج القمر من برج العقرب يوم السبت (30/تشرين الثاني/2024م) في الساعة (2:53) مساءً'
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
                month=jumada_ula,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Jumada al-Ula')) 