from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Dhul-Hijjah 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Dhul-Hijjah 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Dhul-Hijjah', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Dhul-Hijjah 1446H month and its related events'))
        
        # Create Dhul-Hijjah month
        dhul_hijjah = HijriMonth.objects.create(
            name_ar='ذي الحجة',
            name_en='Dhul-Hijjah',
            number=12,
            year=1446,
            gregorian_start=date(2025, 5, 29),  # Based on the image
            gregorian_end=date(2025, 6, 26),    # 29 days from May 29
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2025-05-28',
                    'time': '19:00',
                    'age': '36 hours',
                    'altitude': '19 degrees',
                    'stay_after_sunset': '1 hour 55 minutes',
                    'illumination_percentage': '3.48%',
                    'note': 'In this case, the crescent is expected to be seen very clearly.'
                },
                'alternative_sighting': {
                    'date': '2025-05-27',
                    'time': '19:00',
                    'age': '12 hours',
                    'altitude': '7 degrees',
                    'stay_after_sunset': '45 minutes',
                    'illumination_percentage': '0.60%',
                    'note': 'In this case, it is not possible to see the crescent with the naked eye.'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2025-05-29'},
                    {'hijri': 2, 'gregorian': '2025-05-30'},
                    {'hijri': 3, 'gregorian': '2025-05-31'},
                    {'hijri': 4, 'gregorian': '2025-06-01'},
                    {'hijri': 5, 'gregorian': '2025-06-02'},
                    {'hijri': 6, 'gregorian': '2025-06-03'},
                    {'hijri': 7, 'gregorian': '2025-06-04'},
                    {'hijri': 8, 'gregorian': '2025-06-05'},
                    {'hijri': 9, 'gregorian': '2025-06-06'},
                    {'hijri': 10, 'gregorian': '2025-06-07'},
                    {'hijri': 11, 'gregorian': '2025-06-08'},
                    {'hijri': 12, 'gregorian': '2025-06-09'},
                    {'hijri': 13, 'gregorian': '2025-06-10'},
                    {'hijri': 14, 'gregorian': '2025-06-11'},
                    {'hijri': 15, 'gregorian': '2025-06-12'},
                    {'hijri': 16, 'gregorian': '2025-06-13'},
                    {'hijri': 17, 'gregorian': '2025-06-14'},
                    {'hijri': 18, 'gregorian': '2025-06-15'},
                    {'hijri': 19, 'gregorian': '2025-06-16'},
                    {'hijri': 20, 'gregorian': '2025-06-17'},
                    {'hijri': 21, 'gregorian': '2025-06-18'},
                    {'hijri': 22, 'gregorian': '2025-06-19'},
                    {'hijri': 23, 'gregorian': '2025-06-20'},
                    {'hijri': 24, 'gregorian': '2025-06-21'},
                    {'hijri': 25, 'gregorian': '2025-06-22'},
                    {'hijri': 26, 'gregorian': '2025-06-23'},
                    {'hijri': 27, 'gregorian': '2025-06-24'},
                    {'hijri': 28, 'gregorian': '2025-06-25'},
                    {'hijri': 29, 'gregorian': '2025-06-26'}
                    # Dhul-Hijjah is 29 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Dhul-Hijjah 1446H month'))
        
        # Create historical events for Dhul-Hijjah based on the image
        events_data = [
            {
                'title_ar': 'زواج الإمام أمير المؤمنين علي ابن أبي طالب (ع) من فاطمة الزهراء (ع)',
                'title_en': 'Marriage of Imam Ali ibn Abi Talib (AS) to Lady Fatima al-Zahra (AS)',
                'description_ar': 'اليوم الأول منه زواج الإمام أمير المؤمنين علي ابن أبي طالب (ع) من فاطمة الزهراء (ع)، سنة (2هـ)',
                'day': 1,
                'year_of_event': 2,
                'event_type': 'historical'
            },
            {
                'title_ar': 'دخول النبي الأكرم (ص) مكة في حجة الوداع',
                'title_en': 'Entry of Prophet Muhammad (PBUH) to Mecca for the Farewell Pilgrimage',
                'description_ar': 'الثالث منه دخول النبي الأكرم (ص) مكة في حجة الوداع، سنة (10هـ)',
                'day': 3,
                'year_of_event': 10,
                'event_type': 'historical'
            },
            {
                'title_ar': 'سجن الإمام موسى بن جعفر (ع)',
                'title_en': 'Imprisonment of Imam Musa ibn Jafar (AS)',
                'description_ar': 'الرابع منه سجن الإمام موسى بن جعفر (ع)، سنة (179هـ)',
                'day': 4,
                'year_of_event': 179,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة الإمام محمد الباقر (ع)',
                'title_en': 'Martyrdom of Imam Muhammad al-Baqir (AS)',
                'description_ar': 'السابع منه شهادة الإمام محمد الباقر (ع)، سنة (114هـ)',
                'day': 7,
                'year_of_event': 114,
                'event_type': 'historical'
            },
            {
                'title_ar': 'الثامن منه يوم التروية',
                'title_en': 'Day of Tarwiyah',
                'description_ar': 'الثامن منه يوم التروية',
                'day': 8,
                'event_type': 'religious'
            },
            {
                'title_ar': 'خروج الإمام الحسين بن علي (ع) من مكة الى الكوفة',
                'title_en': 'Departure of Imam Hussein ibn Ali (AS) from Mecca to Kufa',
                'description_ar': 'الثامن منه خروج الإمام الحسين بن علي (ع) من مكة الى الكوفة، سنة (60هـ)',
                'day': 8,
                'year_of_event': 60,
                'event_type': 'historical'
            },
            {
                'title_ar': 'التاسع منه يوم عرفة',
                'title_en': 'Day of Arafah',
                'description_ar': 'التاسع منه يوم عرفة',
                'day': 9,
                'is_holiday': True,
                'event_type': 'religious'
            },
            {
                'title_ar': 'شهادة العبد الصالح سفير الحسين (ع) لأهل الكوفة مسلم بن عقيل (ع) مع هاني بن عروة (ع)',
                'title_en': 'Martyrdom of Muslim ibn Aqil (AS) and Hani ibn Urwah (AS)',
                'description_ar': 'التاسع منه شهادة العبد الصالح سفير الحسين (ع) لأهل الكوفة مسلم بن عقيل (ع) مع هاني بن عروة (ع)، سنة (60هـ)',
                'day': 9,
                'year_of_event': 60,
                'event_type': 'historical'
            },
            {
                'title_ar': 'العاشر منه عيد الأضحى المبارك',
                'title_en': 'Eid al-Adha',
                'description_ar': 'العاشر منه عيد الأضحى المبارك',
                'day': 10,
                'is_holiday': True,
                'event_type': 'religious'
            },
            {
                'title_ar': 'رمي الحجاج بن يوسف الثقفي الكعبة المشرفة بالمنجنيق',
                'title_en': 'Al-Hajjaj ibn Yusuf al-Thaqafi attacked the Holy Kaaba with catapults',
                'description_ar': 'الحادي عشر منه رمي الحجاج بن يوسف الثقفي الكعبة المشرفة بالمنجنيق، سنة (73هـ)',
                'day': 11,
                'year_of_event': 73,
                'event_type': 'historical'
            },
            {
                'title_ar': 'نحلة النبي الأكرم (ص) فدك لفاطمة الزهراء (ع)',
                'title_en': 'Prophet Muhammad (PBUH) gifted Fadak to Lady Fatima al-Zahra (AS)',
                'description_ar': 'الرابع عشر منه نحلة النبي الأكرم (ص) فدك لفاطمة الزهراء (ع)، سنة (7هـ)، على رواية',
                'day': 14,
                'year_of_event': 7,
                'event_type': 'historical'
            },
            {
                'title_ar': 'الثامن عشر منه عيد الغدير الأغر',
                'title_en': 'Eid al-Ghadir',
                'description_ar': 'الثامن عشر منه عيد الغدير الأغر، سنة (10هـ)',
                'day': 18,
                'year_of_event': 10,
                'is_holiday': True,
                'event_type': 'religious'
            },
            {
                'title_ar': 'بيعة المسلمين الإمام أمير المؤمنين علي بن أبي طالب (ع) بالخلافة',
                'title_en': 'Muslims\' allegiance to Imam Ali ibn Abi Talib (AS) as Caliph',
                'description_ar': 'التاسع عشر منه بيعة المسلمين الإمام أمير المؤمنين علي بن أبي طالب (ع) بالخلافة، سنة (35هـ)',
                'day': 19,
                'year_of_event': 35,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة ميثم التمار (ع)',
                'title_en': 'Martyrdom of Maytham al-Tammar (AS)',
                'description_ar': 'الثاني والعشرون منه شهادة ميثم التمار (ع)، سنة (60هـ)',
                'day': 22,
                'year_of_event': 60,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة طفلي مسلم بن عقيل (ع) واسمهما محمد وإبراهيم',
                'title_en': 'Martyrdom of the two children of Muslim ibn Aqil (AS), Muhammad and Ibrahim',
                'description_ar': 'الثالث والعشرون منه شهادة طفلي مسلم بن عقيل (ع) واسمهما محمد وإبراهيم، سنة (61هـ)',
                'day': 23,
                'year_of_event': 61,
                'event_type': 'historical'
            },
            {
                'title_ar': 'خروج النبي الأكرم (ص) بأهل بيته (ع) للمباهلة مع نصارى نجران',
                'title_en': 'Prophet Muhammad (PBUH) went out with his family for Mubahala with the Christians of Najran',
                'description_ar': 'الرابع والعشرون منه خروج النبي الأكرم (ص) بأهل بيته (ع) للمباهلة مع نصارى نجران، سنة (10هـ)',
                'day': 24,
                'year_of_event': 10,
                'event_type': 'historical'
            },
            {
                'title_ar': 'نزول سورة ﴿هل أتى﴾ في المدينة في شأن أهل البيت (ع)',
                'title_en': 'Revelation of Surah "Hal Ata" (Al-Insan) in Medina regarding Ahl al-Bayt (AS)',
                'description_ar': 'الخامس والعشرون منه نزول سورة ﴿هل أتى﴾ في المدينة في شأن أهل البيت (ع)',
                'day': 25,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة علي بن جعفر الصادق (ع) الملقب بـ(العريضي)',
                'title_en': 'Death of Ali ibn Jafar al-Sadiq (AS), known as al-Aridi',
                'description_ar': 'السابع والعشرون منه وفاة علي بن جعفر الصادق (ع) الملقب بـ(العريضي)، سنة (210هـ)',
                'day': 27,
                'year_of_event': 210,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وقعة الحرة والتي اجتاح فيها جيش يزيد بن معاوية المدينة المنورة',
                'title_en': 'Battle of al-Harrah, when the army of Yazid ibn Muawiyah invaded Medina',
                'description_ar': 'الثامن والعشرون منه وقعة الحرة والتي اجتاح فيها جيش يزيد بن معاوية المدينة المنورة، سنة (63هـ)',
                'day': 28,
                'year_of_event': 63,
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
                month=dhul_hijjah,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Dhul-Hijjah'))
        
        # Create astronomical events based on the image
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2025, 6, 7),
                'time': time(5, 24),  # 5:24 AM
                'description_ar': 'يدخل القمر في برج العقرب يوم السبت (7/حزيران/2025م) في الساعة (5:24) صباحاً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2025, 6, 9),
                'time': time(17, 56),  # 5:56 PM
                'description_ar': 'يخرج القمر من برج العقرب يوم الإثنين (9/حزيران/2025م) في الساعة (5:56) مساءً'
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
                month=dhul_hijjah,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Dhul-Hijjah')) 