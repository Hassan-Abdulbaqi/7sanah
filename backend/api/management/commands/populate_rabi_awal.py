from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Rabi al-Awwal 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Rabi al-Awwal 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Rabi al-Awwal', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Rabi al-Awwal 1446H month and its related events'))
        
        # Create Rabi al-Awwal month
        rabi_awal = HijriMonth.objects.create(
            name_ar='ربيع الأول',
            name_en='Rabi al-Awwal',
            number=3,
            year=1446,
            gregorian_start=date(2024, 9, 5),  # Based on user input
            gregorian_end=date(2024, 10, 4),   # 30 days from September 5
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2024-09-04',
                    'time': '20:02',
                    'age': '27 hours',
                    'altitude': '8 degrees',
                    'stay_after_sunset': '44 minutes',
                    'illumination_percentage': '1.09%'
                },
                'alternative_sighting': {
                    'date': '2024-09-03',
                    'time': '20:03',
                    'age': '13 hours',
                    'altitude': '3 degrees',
                    'stay_after_sunset': '19 minutes',
                    'illumination_percentage': '0.24%',
                    'note': 'Difficult to see with naked eye'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2024-09-05'},
                    {'hijri': 2, 'gregorian': '2024-09-06'},
                    {'hijri': 3, 'gregorian': '2024-09-07'},
                    {'hijri': 4, 'gregorian': '2024-09-08'},
                    {'hijri': 5, 'gregorian': '2024-09-09'},
                    {'hijri': 6, 'gregorian': '2024-09-10'},
                    {'hijri': 7, 'gregorian': '2024-09-11'},
                    {'hijri': 8, 'gregorian': '2024-09-12'},
                    {'hijri': 9, 'gregorian': '2024-09-13'},
                    {'hijri': 10, 'gregorian': '2024-09-14'},
                    {'hijri': 11, 'gregorian': '2024-09-15'},
                    {'hijri': 12, 'gregorian': '2024-09-16'},
                    {'hijri': 13, 'gregorian': '2024-09-17'},
                    {'hijri': 14, 'gregorian': '2024-09-18'},
                    {'hijri': 15, 'gregorian': '2024-09-19'},
                    {'hijri': 16, 'gregorian': '2024-09-20'},
                    {'hijri': 17, 'gregorian': '2024-09-21'},
                    {'hijri': 18, 'gregorian': '2024-09-22'},
                    {'hijri': 19, 'gregorian': '2024-09-23'},
                    {'hijri': 20, 'gregorian': '2024-09-24'},
                    {'hijri': 21, 'gregorian': '2024-09-25'},
                    {'hijri': 22, 'gregorian': '2024-09-26'},
                    {'hijri': 23, 'gregorian': '2024-09-27'},
                    {'hijri': 24, 'gregorian': '2024-09-28'},
                    {'hijri': 25, 'gregorian': '2024-09-29'},
                    {'hijri': 26, 'gregorian': '2024-09-30'},
                    {'hijri': 27, 'gregorian': '2024-10-01'},
                    {'hijri': 28, 'gregorian': '2024-10-02'},
                    {'hijri': 29, 'gregorian': '2024-10-03'},
                    {'hijri': 30, 'gregorian': '2024-10-04'}
                    # Rabi al-Awwal is 30 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Rabi al-Awwal 1446H month'))
        
        # Create historical events for Rabi al-Awwal based on the image
        events_data = [
            {
                'title_ar': 'مبيت الإمام أمير المؤمنين علي بن أبي طالب (ع) في فراش النبي الأكرم (ص) وهجرة النبي(ص) الى المدينة المنورة',
                'title_en': 'Imam Ali (AS) sleeping in the bed of Prophet Muhammad (PBUH) and the Prophet\'s migration to Medina',
                'description_ar': 'اليوم الأول منه مبيت الإمام أمير المؤمنين علي بن أبي طالب (ع) في فراش النبي الأكرم (ص) وهجرة النبي(ص) الى المدينة المنورة',
                'day': 1,
                'event_type': 'historical'
            },
            {
                'title_ar': 'إحراق الكعبة المشرفة بالمنجنيق بأمر حصين بن نمير قائد جيش يزيد',
                'title_en': 'Burning of the Holy Kaaba by catapult by order of Husayn bin Numayr, commander of Yazid\'s army',
                'description_ar': 'الثالث منه إحراق الكعبة المشرفة بالمنجنيق بأمر حصين بن نمير قائد جيش يزيد، سنة (64هـ)',
                'day': 3,
                'year_of_event': 64,
                'event_type': 'historical'
            },
            {
                'title_ar': 'خروج النبي(ص) من غار ثور متوجهاً الى المدينة المنورة',
                'title_en': 'Prophet Muhammad (PBUH) leaving the Cave of Thawr heading to Medina',
                'description_ar': 'الرابع منه خروج النبي(ص) من غار ثور متوجهاً الى المدينة المنورة في السنة الأولى من الهجرة',
                'day': 4,
                'year_of_event': 1,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة السيدة سكينة بنت الإمام الحسين (ع)',
                'title_en': 'Death of Lady Sakina, daughter of Imam Hussein (AS)',
                'description_ar': 'الخامس منه وفاة السيدة سكينة بنت الإمام الحسين (ع)، سنة (117هـ)',
                'day': 5,
                'year_of_event': 117,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة الإمام الحسن العسكري (ع) وبداية إمامة بقية الله الأعظم الحجة بن الحسن العسكري',
                'title_en': 'Martyrdom of Imam Hassan al-Askari (AS) and beginning of the Imamate of Imam al-Mahdi (AS)',
                'description_ar': 'الثامن منه شهادة الإمام الحسن العسكري (ع)، سنة (260هـ)، وبداية إمامة بقية الله الأعظم الحجة بن الحسن العسكري (عجل الله تعالى فرجه الشريف)، على رواية',
                'day': 8,
                'year_of_event': 260,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة عبد المطلب جد النبي الأكرم (ص)',
                'title_en': 'Death of Abdul Muttalib, grandfather of Prophet Muhammad (PBUH)',
                'description_ar': 'العاشر منه وفاة عبد المطلب جد النبي الأكرم (ص) في السنة الثامنة من ولادته، سنة (45) قبل الهجرة',
                'day': 10,
                'year_of_event': -45,
                'event_type': 'historical'
            },
            {
                'title_ar': 'زواج الرسول الأكرم (ص) من خديجة الكبرى (ع)',
                'title_en': 'Marriage of Prophet Muhammad (PBUH) to Khadija al-Kubra (AS)',
                'description_ar': 'العاشر منه زواج الرسول الأكرم (ص) من خديجة الكبرى (ع)، وهو في سن الخامسة والعشرين، سنة (28) قبل الهجرة',
                'day': 10,
                'year_of_event': -28,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة النبي الأكرم (ص)',
                'title_en': 'Birth of Prophet Muhammad (PBUH)',
                'description_ar': 'الثاني عشر منه ولادة النبي الأكرم (ص)، على رواية',
                'day': 12,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'دخول النبي الأكرم (ص) المدينة المنورة',
                'title_en': 'Entry of Prophet Muhammad (PBUH) to Medina',
                'description_ar': 'الثاني عشر منه دخول النبي الأكرم (ص) المدينة المنورة في السنة الأولى من الهجرة',
                'day': 12,
                'year_of_event': 1,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة سيد الرسل محمد بن عبد الله (ص)',
                'title_en': 'Birth of the Master of Messengers, Muhammad ibn Abdullah (PBUH)',
                'description_ar': 'السابع عشر منه ولادة سيد الرسل محمد بن عبد الله (ص)، سنة (53) قبل الهجرة، على الرواية المشهورة',
                'day': 17,
                'year_of_event': -53,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة الإمام جعفر بن محمد الصادق (ع)',
                'title_en': 'Birth of Imam Ja\'far ibn Muhammad al-Sadiq (AS)',
                'description_ar': 'السابع عشر منه ولادة الإمام جعفر بن محمد الصادق (ع)، سنة (83هـ)',
                'day': 17,
                'year_of_event': 83,
                'event_type': 'historical'
            },
            {
                'title_ar': 'غزوة بني النضير',
                'title_en': 'Battle of Banu Nadir',
                'description_ar': 'الثاني والعشرون منه غزوة بني النضير، سنة (4) للهجرة',
                'day': 22,
                'year_of_event': 4,
                'event_type': 'historical'
            },
            {
                'title_ar': 'استشهاد سعيد بن جبير (رضي الله عنه) على يد الحجاج',
                'title_en': 'Martyrdom of Sa\'id ibn Jubayr by al-Hajjaj',
                'description_ar': 'الخامس والعشرون منه استشهاد سعيد بن جبير (رضي الله عنه) على يد الحجاج، سنة (95هـ)',
                'day': 25,
                'year_of_event': 95,
                'event_type': 'historical'
            },
            {
                'title_ar': 'إبرام معاهدة الصلح بين الإمام الحسن بن علي بن أبي طالب (ع) ومعاوية بن أبي سفيان',
                'title_en': 'Peace treaty between Imam Hassan (AS) and Muawiyah',
                'description_ar': 'السادس والعشرون منه إبرام معاهدة الصلح بين الإمام الحسن بن علي بن أبي طالب (ع) ومعاوية بن أبي سفيان، سنة (41هـ)',
                'day': 26,
                'year_of_event': 41,
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
                month=rabi_awal,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Rabi al-Awwal'))
        
        # Create astronomical events based on the image
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2024, 9, 7),
                'time': time(8, 20),  # 8:20 AM
                'description_ar': 'يدخل القمر في برج العقرب يوم السبت (7/أيلول/2024م) في الساعة (8:20) صباحاً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2024, 9, 9),
                'time': time(20, 26),  # 8:26 PM
                'description_ar': 'يخرج القمر من برج العقرب يوم الإثنين (9/أيلول/2024م) في الساعة (8:26) مساءً'
            },
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2024, 10, 4),
                'time': time(20, 24),  # 8:24 PM
                'description_ar': 'يدخل القمر في برج العقرب يوم الجمعة (4/تشرين الأول/2024م) في الساعة (8:24) مساءً'
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
                month=rabi_awal,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Rabi al-Awwal')) 