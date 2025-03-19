from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Rajab 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Rajab 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Rajab', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Rajab 1446H month and its related events'))
        
        # Create Rajab month
        rajab = HijriMonth.objects.create(
            name_ar='رجب',
            name_en='Rajab',
            number=7,
            year=1446,
            gregorian_start=date(2025, 1, 2),  # Based on the image
            gregorian_end=date(2025, 1, 30),   # 29 days from January 2
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2025-01-01',
                    'time': '17:04',
                    'age': '39 hours',
                    'altitude': '13 degrees',
                    'stay_after_sunset': '1 hour 26 minutes',
                    'illumination_percentage': '2.90%',
                    'note': 'In this case, the crescent is expected to be seen clearly.'
                },
                'alternative_sighting': {
                    'date': '2024-12-31',
                    'time': '17:08',
                    'age': '15 hours',
                    'altitude': '2 degrees',
                    'stay_after_sunset': '18 minutes',
                    'illumination_percentage': '0.51%',
                    'note': 'In this case, it is not possible to see the crescent even with armed eyes.'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2025-01-02'},
                    {'hijri': 2, 'gregorian': '2025-01-03'},
                    {'hijri': 3, 'gregorian': '2025-01-04'},
                    {'hijri': 4, 'gregorian': '2025-01-05'},
                    {'hijri': 5, 'gregorian': '2025-01-06'},
                    {'hijri': 6, 'gregorian': '2025-01-07'},
                    {'hijri': 7, 'gregorian': '2025-01-08'},
                    {'hijri': 8, 'gregorian': '2025-01-09'},
                    {'hijri': 9, 'gregorian': '2025-01-10'},
                    {'hijri': 10, 'gregorian': '2025-01-11'},
                    {'hijri': 11, 'gregorian': '2025-01-12'},
                    {'hijri': 12, 'gregorian': '2025-01-13'},
                    {'hijri': 13, 'gregorian': '2025-01-14'},
                    {'hijri': 14, 'gregorian': '2025-01-15'},
                    {'hijri': 15, 'gregorian': '2025-01-16'},
                    {'hijri': 16, 'gregorian': '2025-01-17'},
                    {'hijri': 17, 'gregorian': '2025-01-18'},
                    {'hijri': 18, 'gregorian': '2025-01-19'},
                    {'hijri': 19, 'gregorian': '2025-01-20'},
                    {'hijri': 20, 'gregorian': '2025-01-21'},
                    {'hijri': 21, 'gregorian': '2025-01-22'},
                    {'hijri': 22, 'gregorian': '2025-01-23'},
                    {'hijri': 23, 'gregorian': '2025-01-24'},
                    {'hijri': 24, 'gregorian': '2025-01-25'},
                    {'hijri': 25, 'gregorian': '2025-01-26'},
                    {'hijri': 26, 'gregorian': '2025-01-27'},
                    {'hijri': 27, 'gregorian': '2025-01-28'},
                    {'hijri': 28, 'gregorian': '2025-01-29'},
                    {'hijri': 29, 'gregorian': '2025-01-30'}
                    # Rajab is 29 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Rajab 1446H month'))
        
        # Create historical events for Rajab based on the image
        events_data = [
            {
                'title_ar': 'ولادة الإمام محمد بن علي الباقر (ع)',
                'title_en': 'Birth of Imam Muhammad ibn Ali al-Baqir (AS)',
                'description_ar': 'اليوم الأول منه ولادة الإمام محمد بن علي الباقر (ع)، سنة (57هـ)، على رواية',
                'day': 1,
                'year_of_event': 57,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة الإمام علي بن محمد الهادي (ع)',
                'title_en': 'Birth of Imam Ali ibn Muhammad al-Hadi (AS)',
                'description_ar': 'الثاني منه ولادة الإمام علي بن محمد الهادي (ع)، سنة (212هـ)',
                'day': 2,
                'year_of_event': 212,
                'event_type': 'historical'
            },
            {
                'title_ar': 'غزوة تبوك',
                'title_en': 'Battle of Tabuk',
                'description_ar': 'الثالث منه غزوة تبوك، سنة (9هـ)',
                'day': 3,
                'year_of_event': 9,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة الإمام علي بن محمد الهادي (ع)',
                'title_en': 'Martyrdom of Imam Ali ibn Muhammad al-Hadi (AS)',
                'description_ar': 'الثالث منه شهادة الإمام علي بن محمد الهادي (ع)، سنة (254هـ)',
                'day': 3,
                'year_of_event': 254,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة الإمام محمد بن علي الجواد (ع)',
                'title_en': 'Birth of Imam Muhammad ibn Ali al-Jawad (AS)',
                'description_ar': 'العاشر منه ولادة الإمام محمد بن علي الجواد (ع)، سنة (195هـ)',
                'day': 10,
                'year_of_event': 195,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وصول الإمام أمير المؤمنين (ع) الى الكوفة بعد حرب الجمل',
                'title_en': 'Arrival of Imam Ali (AS) to Kufa after the Battle of the Camel',
                'description_ar': 'الحادي عشر منه وصول الإمام أمير المؤمنين (ع) الى الكوفة بعد حرب الجمل، سنة (36هـ)',
                'day': 11,
                'year_of_event': 36,
                'event_type': 'historical'
            },
            {
                'title_ar': 'دخول الإمام أمير المؤمنين (ع) الكوفة واتخاذها مقراً للخلافة',
                'title_en': 'Entry of Imam Ali (AS) to Kufa and making it the capital of the caliphate',
                'description_ar': 'الثاني عشر منه دخول الإمام أمير المؤمنين (ع) الكوفة واتخاذها مقراً للخلافة، سنة (36هـ)',
                'day': 12,
                'year_of_event': 36,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة الإمام أمير المؤمنين (ع)',
                'title_en': 'Birth of Imam Ali (AS)',
                'description_ar': 'الثالث عشر منه ولادة الإمام أمير المؤمنين (ع)، سنة (23) قبل الهجرة',
                'day': 13,
                'year_of_event': -23,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'تحويل القبلة من بيت المقدس الى الكعبة المشرفة',
                'title_en': 'Changing of the Qibla from Jerusalem to the Holy Kaaba',
                'description_ar': 'الخامس عشر منه تحويل القبلة من بيت المقدس الى الكعبة المشرفة، سنة (2هـ)، على رواية',
                'day': 15,
                'year_of_event': 2,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة السيدة زينب بنت الإمام أمير المؤمنين (ع)',
                'title_en': 'Death of Lady Zainab, daughter of Imam Ali (AS)',
                'description_ar': 'الخامس عشر منه وفاة السيدة زينب بنت الإمام أمير المؤمنين (ع)، سنة (62هـ)، على رواية',
                'day': 15,
                'year_of_event': 62,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة إبراهيم بن الرسول الأكرم (ص)',
                'title_en': 'Death of Ibrahim, son of Prophet Muhammad (PBUH)',
                'description_ar': 'الثامن عشر منه وفاة إبراهيم بن الرسول الأكرم (ص)، سنة (10هـ)',
                'day': 18,
                'year_of_event': 10,
                'event_type': 'historical'
            },
            {
                'title_ar': 'فتح خيبر على يد الإمام علي بن أبي طالب (ع)',
                'title_en': 'Conquest of Khaybar by Imam Ali ibn Abi Talib (AS)',
                'description_ar': 'الرابع والعشرون منه فتح خيبر على يد الإمام علي بن أبي طالب (ع)، سنة (7هـ)، وعودة جعفر بن أبي طالب(ع) من الحبشة',
                'day': 24,
                'year_of_event': 7,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة الإمام موسى بن جعفر الكاظم (ع)',
                'title_en': 'Martyrdom of Imam Musa ibn Jafar al-Kadhim (AS)',
                'description_ar': 'الخامس والعشرون منه شهادة الإمام موسى بن جعفر الكاظم (ع)، سنة (183هـ)',
                'day': 25,
                'year_of_event': 183,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة أبي طالب (ع) عم النبي الأكرم (ص)',
                'title_en': 'Death of Abu Talib (AS), uncle of Prophet Muhammad (PBUH)',
                'description_ar': 'السادس والعشرون منه وفاة أبي طالب (ع) عم النبي الأكرم (ص)، سنة (3) قبل الهجرة، على رواية',
                'day': 26,
                'year_of_event': -3,
                'event_type': 'historical'
            },
            {
                'title_ar': 'بعثة النبي الأكرم (ص)',
                'title_en': 'Beginning of the Prophetic Mission of Prophet Muhammad (PBUH)',
                'description_ar': 'السابع والعشرون منه بعثة النبي الأكرم (ص)، سنة (13) قبل الهجرة',
                'day': 27,
                'year_of_event': -13,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'خروج الإمام الحسين (ع) من المدينة الى مكة',
                'title_en': 'Departure of Imam Hussein (AS) from Medina to Mecca',
                'description_ar': 'الثامن والعشرون منه خروج الإمام الحسين (ع) من المدينة الى مكة، سنة (60هـ)',
                'day': 28,
                'year_of_event': 60,
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
                month=rajab,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Rajab'))
        
        # Create astronomical events based on the image
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2025, 1, 21),
                'time': time(19, 26),  # 7:26 PM
                'description_ar': 'يدخل القمر في برج العقرب يوم الثلاثاء (21/كانون الثاني/2025م) في الساعة (7:26) مساءً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2025, 1, 24),
                'time': time(7, 26),  # 7:26 AM
                'description_ar': 'يخرج القمر من برج العقرب يوم الجمعة (24/كانون الثاني/2025م) في الساعة (7:26) صباحاً'
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
                month=rajab,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Rajab')) 