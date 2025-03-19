from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Dhul-Qa\'dah 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Dhul-Qa'dah 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Dhul-Qa\'dah', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Dhul-Qa\'dah 1446H month and its related events'))
        
        # Create Dhul-Qa'dah month
        dhul_qadah = HijriMonth.objects.create(
            name_ar='ذي القعدة',
            name_en='Dhul-Qa\'dah',
            number=11,
            year=1446,
            gregorian_start=date(2025, 4, 29),  # Based on the image
            gregorian_end=date(2025, 5, 28),    # 30 days from April 29
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2025-04-28',
                    'time': '19:01',
                    'age': '20 hours',
                    'altitude': '10 degrees',
                    'stay_after_sunset': '1 hour',
                    'illumination_percentage': '8.21%',
                    'note': 'In this case, the crescent is expected to be seen with the naked eye.'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2025-04-29'},
                    {'hijri': 2, 'gregorian': '2025-04-30'},
                    {'hijri': 3, 'gregorian': '2025-05-01'},
                    {'hijri': 4, 'gregorian': '2025-05-02'},
                    {'hijri': 5, 'gregorian': '2025-05-03'},
                    {'hijri': 6, 'gregorian': '2025-05-04'},
                    {'hijri': 7, 'gregorian': '2025-05-05'},
                    {'hijri': 8, 'gregorian': '2025-05-06'},
                    {'hijri': 9, 'gregorian': '2025-05-07'},
                    {'hijri': 10, 'gregorian': '2025-05-08'},
                    {'hijri': 11, 'gregorian': '2025-05-09'},
                    {'hijri': 12, 'gregorian': '2025-05-10'},
                    {'hijri': 13, 'gregorian': '2025-05-11'},
                    {'hijri': 14, 'gregorian': '2025-05-12'},
                    {'hijri': 15, 'gregorian': '2025-05-13'},
                    {'hijri': 16, 'gregorian': '2025-05-14'},
                    {'hijri': 17, 'gregorian': '2025-05-15'},
                    {'hijri': 18, 'gregorian': '2025-05-16'},
                    {'hijri': 19, 'gregorian': '2025-05-17'},
                    {'hijri': 20, 'gregorian': '2025-05-18'},
                    {'hijri': 21, 'gregorian': '2025-05-19'},
                    {'hijri': 22, 'gregorian': '2025-05-20'},
                    {'hijri': 23, 'gregorian': '2025-05-21'},
                    {'hijri': 24, 'gregorian': '2025-05-22'},
                    {'hijri': 25, 'gregorian': '2025-05-23'},
                    {'hijri': 26, 'gregorian': '2025-05-24'},
                    {'hijri': 27, 'gregorian': '2025-05-25'},
                    {'hijri': 28, 'gregorian': '2025-05-26'},
                    {'hijri': 29, 'gregorian': '2025-05-27'},
                    {'hijri': 30, 'gregorian': '2025-05-28'}
                    # Dhul-Qa'dah is 30 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Dhul-Qa\'dah 1446H month'))
        
        # Create historical events for Dhul-Qa'dah based on the image
        events_data = [
            {
                'title_ar': 'ولادة السيدة فاطمة المعصومة بنت الإمام موسى بن جعفر الكاظم (ع)',
                'title_en': 'Birth of Lady Fatima al-Masouma, daughter of Imam Musa ibn Jafar al-Kadhim (AS)',
                'description_ar': 'اليوم الأول منه ولادة السيدة فاطمة المعصومة بنت الإمام موسى بن جعفر الكاظم (ع)، سنة (173هـ)، على رواية',
                'day': 1,
                'year_of_event': 173,
                'event_type': 'historical'
            },
            {
                'title_ar': 'تجديد بناء الكعبة المعظمة على يد إبراهيم الخليل وولده إسماعيل (ع)',
                'title_en': 'Renovation of the Holy Kaaba by Prophet Ibrahim and his son Ismail (AS)',
                'description_ar': 'الخامس منه تجديد بناء الكعبة المعظمة على يد إبراهيم الخليل وولده إسماعيل (ع)',
                'day': 5,
                'event_type': 'historical'
            },
            {
                'title_ar': 'إرسال مسلم بن عقيل (ع) رسالة الى الإمام الحسين (ع) عن أحوال الكوفة وأهلها',
                'title_en': 'Muslim ibn Aqil (AS) sent a letter to Imam Hussein (AS) about the situation in Kufa',
                'description_ar': 'التاسع منه إرسال مسلم بن عقيل (ع) رسالة الى الإمام الحسين (ع) عن أحوال الكوفة وأهلها، سنة (60هـ)',
                'day': 9,
                'year_of_event': 60,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة الإمام علي بن موسى الرضا (ع)',
                'title_en': 'Birth of Imam Ali ibn Musa al-Ridha (AS)',
                'description_ar': 'الحادي عشر منه ولادة الإمام علي بن موسى الرضا (ع)، سنة (148هـ)',
                'day': 11,
                'year_of_event': 148,
                'event_type': 'historical'
            },
            {
                'title_ar': 'غزوة بني قريظة',
                'title_en': 'Battle of Banu Qurayza',
                'description_ar': 'الثالث والعشرون منه غزوة بني قريظة، سنة (5هـ)',
                'day': 23,
                'year_of_event': 5,
                'event_type': 'historical'
            },
            {
                'title_ar': 'يوم دحو الأرض من تحت الكعبة المشرفة',
                'title_en': 'Day of the Earth\'s expansion from beneath the Holy Kaaba',
                'description_ar': 'الخامس والعشرون منه يوم دحو الأرض من تحت الكعبة المشرفة',
                'day': 25,
                'event_type': 'historical'
            },
            {
                'title_ar': 'خروج النبي الأكرم (ص) من المدينة لأداء فريضة الحج',
                'title_en': 'Departure of Prophet Muhammad (PBUH) from Medina to perform Hajj',
                'description_ar': 'الخامس والعشرون منه خروج النبي الأكرم (ص) من المدينة لأداء فريضة الحج، سنة (10هـ)',
                'day': 25,
                'year_of_event': 10,
                'event_type': 'historical'
            },
            {
                'title_ar': 'خروج الإمام علي بن موسى الرضا (ع) من المدينة المنورة الى خراسان',
                'title_en': 'Departure of Imam Ali ibn Musa al-Ridha (AS) from Medina to Khorasan',
                'description_ar': 'الخامس والعشرون منه خروج الإمام علي بن موسى الرضا (ع) من المدينة المنورة الى خراسان، سنة (200هـ)',
                'day': 25,
                'year_of_event': 200,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة محمد بن أبي بكر (رضي الله عنه)',
                'title_en': 'Birth of Muhammad ibn Abi Bakr',
                'description_ar': 'الخامس والعشرون منه ولادة محمد بن أبي بكر (رضي الله عنه)، سنة (10) للهجرة',
                'day': 25,
                'year_of_event': 10,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة الإمام محمد بن علي الجواد (ع)',
                'title_en': 'Martyrdom of Imam Muhammad ibn Ali al-Jawad (AS)',
                'description_ar': 'آخر يوم منه شهادة الإمام محمد بن علي الجواد (ع)، سنة (220هـ)',
                'day': 30,
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
                month=dhul_qadah,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Dhul-Qa\'dah'))
        
        # Create astronomical events based on the image
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2025, 5, 10),
                'time': time(22, 59),  # 10:59 PM
                'description_ar': 'يدخل القمر في برج العقرب يوم السبت (10/أيار/2025م) في الساعة (10:59) مساءً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2025, 5, 13),
                'time': time(11, 34),  # 11:34 AM
                'description_ar': 'يخرج القمر من برج العقرب يوم الثلاثاء (13/أيار/2025م) في الساعة (11:34) صباحاً'
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
                month=dhul_qadah,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Dhul-Qa\'dah')) 