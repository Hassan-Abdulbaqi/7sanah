from django.core.management.base import BaseCommand
from api.models import HijriMonth, HijriEvent, AstronomicalEvent
from datetime import datetime, date, time

class Command(BaseCommand):
    help = 'Populates the database with Ramadan 1446H data'

    def handle(self, *args, **options):
        # First, delete any existing Ramadan 1446H data
        existing_month = HijriMonth.objects.filter(name_en='Ramadan', year=1446).first()
        
        if existing_month:
            # Delete related events first to avoid foreign key constraints
            HijriEvent.objects.filter(month=existing_month).delete()
            AstronomicalEvent.objects.filter(month=existing_month).delete()
            
            # Now delete the month itself
            existing_month.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted existing Ramadan 1446H month and its related events'))
        
        # Create Ramadan month
        ramadan = HijriMonth.objects.create(
            name_ar='رمضان',
            name_en='Ramadan',
            number=9,
            year=1446,
            gregorian_start=date(2025, 3, 2),  # Based on the image
            gregorian_end=date(2025, 3, 30),   # Updated to 29 days from March 2
            moon_sighting_data={
                'expected_sighting': {
                    'date': '2025-03-01',
                    'time': '18:00',
                    'age': '38 hours',
                    'altitude': '19 degrees',
                    'stay_after_sunset': '1 hour 42 minutes',
                    'illumination_percentage': '2.49%',
                    'note': 'In this case, the crescent is expected to be seen very clearly.'
                },
                'alternative_sighting': {
                    'date': '2025-02-28',
                    'time': '17:54',
                    'age': '14 hours',
                    'altitude': '6 degrees',
                    'stay_after_sunset': '33 minutes',
                    'illumination_percentage': '0.48%',
                    'note': 'In this case, it is not possible to see the crescent even with armed eyes.'
                }
            },
            calendar_data={
                'gregorian_dates': [
                    {'hijri': 1, 'gregorian': '2025-03-02'},
                    {'hijri': 2, 'gregorian': '2025-03-03'},
                    {'hijri': 3, 'gregorian': '2025-03-04'},
                    {'hijri': 4, 'gregorian': '2025-03-05'},
                    {'hijri': 5, 'gregorian': '2025-03-06'},
                    {'hijri': 6, 'gregorian': '2025-03-07'},
                    {'hijri': 7, 'gregorian': '2025-03-08'},
                    {'hijri': 8, 'gregorian': '2025-03-09'},
                    {'hijri': 9, 'gregorian': '2025-03-10'},
                    {'hijri': 10, 'gregorian': '2025-03-11'},
                    {'hijri': 11, 'gregorian': '2025-03-12'},
                    {'hijri': 12, 'gregorian': '2025-03-13'},
                    {'hijri': 13, 'gregorian': '2025-03-14'},
                    {'hijri': 14, 'gregorian': '2025-03-15'},
                    {'hijri': 15, 'gregorian': '2025-03-16'},
                    {'hijri': 16, 'gregorian': '2025-03-17'},
                    {'hijri': 17, 'gregorian': '2025-03-18'},
                    {'hijri': 18, 'gregorian': '2025-03-19'},
                    {'hijri': 19, 'gregorian': '2025-03-20'},
                    {'hijri': 20, 'gregorian': '2025-03-21'},
                    {'hijri': 21, 'gregorian': '2025-03-22'},
                    {'hijri': 22, 'gregorian': '2025-03-23'},
                    {'hijri': 23, 'gregorian': '2025-03-24'},
                    {'hijri': 24, 'gregorian': '2025-03-25'},
                    {'hijri': 25, 'gregorian': '2025-03-26'},
                    {'hijri': 26, 'gregorian': '2025-03-27'},
                    {'hijri': 27, 'gregorian': '2025-03-28'},
                    {'hijri': 28, 'gregorian': '2025-03-29'},
                    {'hijri': 29, 'gregorian': '2025-03-30'}
                    # Ramadan is 29 days
                ]
            }
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created Ramadan 1446H month'))
        
        # Create historical events for Ramadan based on the image
        events_data = [
            {
                'title_ar': 'وفاة عثمان بن سعيد (رضي الله عنه) النائب الأول للإمام المهدي (عجل الله تعالى فرجه الشريف)',
                'title_en': 'Death of Uthman ibn Sa\'id, the first ambassador of Imam al-Mahdi (AS)',
                'description_ar': 'اليوم الأول منه وفاة عثمان بن سعيد (رضي الله عنه) النائب الأول للإمام المهدي (عجل الله تعالى فرجه الشريف)، سنة (267هـ)',
                'day': 1,
                'year_of_event': 267,
                'event_type': 'historical'
            },
            {
                'title_ar': 'تولي الإمام الرضا (ع) ولاية عهد المأمون العباسي',
                'title_en': 'Imam al-Ridha (AS) appointed as heir to the Abbasid Caliph al-Ma\'mun',
                'description_ar': 'الثاني منه تولي الإمام الرضا (ع) ولاية عهد المأمون العباسي، سنة (201هـ) على رواية',
                'day': 2,
                'year_of_event': 201,
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
                'title_ar': 'بيعة الناس للإمام الرضا(ع)',
                'title_en': 'People\'s allegiance to Imam al-Ridha (AS)',
                'description_ar': 'السادس منه بيعة الناس للإمام الرضا(ع)، سنة (201هـ)، على رواية',
                'day': 6,
                'year_of_event': 201,
                'event_type': 'historical'
            },
            {
                'title_ar': 'خروج النبي الأكرم (ص) لغزوة بدر الكبرى',
                'title_en': 'Departure of Prophet Muhammad (PBUH) for the Battle of Badr',
                'description_ar': 'الثامن منه خروج النبي الأكرم (ص) لغزوة بدر الكبرى، سنة (2هـ)',
                'day': 8,
                'year_of_event': 2,
                'event_type': 'historical'
            },
            {
                'title_ar': 'وفاة الصديقة خديجة الكبرى (ع)',
                'title_en': 'Death of Lady Khadija al-Kubra (AS)',
                'description_ar': 'العاشر منه وفاة الصديقة خديجة الكبرى (ع)، سنة (3) قبل الهجرة',
                'day': 10,
                'year_of_event': -3,
                'event_type': 'historical'
            },
            {
                'title_ar': 'المؤاخاة بين المهاجرين والأنصار في المدينة المنورة',
                'title_en': 'Brotherhood established between the Emigrants and the Helpers in Medina',
                'description_ar': 'الثاني عشر منه المؤاخاة بين المهاجرين والأنصار في المدينة المنورة، السنة الأولى للهجرة',
                'day': 12,
                'year_of_event': 1,
                'event_type': 'historical'
            },
            {
                'title_ar': 'مقتل المختار الثقفي (ع)',
                'title_en': 'Killing of al-Mukhtar al-Thaqafi',
                'description_ar': 'الرابع عشر منه مقتل المختار الثقفي (ع)، سنة (67هـ)',
                'day': 14,
                'year_of_event': 67,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ولادة سبط النبي الأكرم (ص) الإمام الحسن بن علي بن ابي طالب (ع)',
                'title_en': 'Birth of Imam Hassan ibn Ali ibn Abi Talib (AS), grandson of Prophet Muhammad (PBUH)',
                'description_ar': 'الخامس عشر منه ولادة سبط النبي الأكرم (ص) الإمام الحسن بن علي بن ابي طالب (ع)، سنة (3هـ)',
                'day': 15,
                'year_of_event': 3,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'خروج مسلم بن عقيل (ع) رسولاً عن الإمام الحسين (ع) لأهل الكوفة',
                'title_en': 'Departure of Muslim ibn Aqil (AS) as a messenger from Imam Hussein (AS) to the people of Kufa',
                'description_ar': 'الخامس عشر منه خروج مسلم بن عقيل (ع) رسولاً عن الإمام الحسين (ع) لأهل الكوفة، سنة (60هـ)',
                'day': 15,
                'year_of_event': 60,
                'event_type': 'historical'
            },
            {
                'title_ar': 'عروج الرسول الأكرم (ص) الى السماء',
                'title_en': 'Ascension (Mi\'raj) of Prophet Muhammad (PBUH) to the heavens',
                'description_ar': 'السابع عشر منه عروج الرسول الأكرم (ص) الى السماء قبل ستة أشهر من الهجرة',
                'day': 17,
                'year_of_event': 0,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'معركة بدر',
                'title_en': 'Battle of Badr',
                'description_ar': 'السابع عشر منه معركة بدر، سنة (2هـ)',
                'day': 17,
                'year_of_event': 2,
                'event_type': 'historical'
            },
            {
                'title_ar': 'جرح الإمام أمير المؤمنين (ع) على يد أشقى الأولين والآخرين عبد الرحمن ابن ملجم (لعنه الله)',
                'title_en': 'Imam Ali (AS) wounded by Abd al-Rahman ibn Muljam',
                'description_ar': 'التاسع عشر منه جرح الإمام أمير المؤمنين (ع) على يد أشقى الأولين والآخرين عبد الرحمن ابن ملجم (لعنه الله)، سنة (40هـ)',
                'day': 19,
                'year_of_event': 40,
                'event_type': 'historical'
            },
            {
                'title_ar': 'فتح مكة',
                'title_en': 'Conquest of Mecca',
                'description_ar': 'العشرون منه فتح مكة، سنة (8هـ)',
                'day': 20,
                'year_of_event': 8,
                'event_type': 'historical'
            },
            {
                'title_ar': 'شهادة مولى المتقين الإمام أمير المؤمنين (ع)',
                'title_en': 'Martyrdom of Imam Ali (AS)',
                'description_ar': 'الحادي والعشرون منه شهادة مولى المتقين الإمام أمير المؤمنين (ع)، سنة (40هـ)',
                'day': 21,
                'year_of_event': 40,
                'is_holiday': True,
                'event_type': 'historical'
            },
            {
                'title_ar': 'ليلة الثالث والعشرين منه ليلة القدر على أقرب الاحتمالات فيها',
                'title_en': 'Laylat al-Qadr (Night of Decree)',
                'description_ar': 'ليلة الثالث والعشرين منه ليلة القدر على أقرب الاحتمالات فيها',
                'day': 22,
                'is_holiday': True,
                'event_type': 'religious'
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
                month=ramadan,
                year_of_event=event_data.get('year_of_event'),
                is_holiday=event_data.get('is_holiday', False),
                event_type=event_data.get('event_type')
            )
            events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {events_created} historical events for Ramadan'))
        
        # Create astronomical events based on the image
        astronomical_events_data = [
            {
                'title_ar': 'يدخل القمر في برج العقرب',
                'title_en': 'Moon enters Scorpio',
                'date': date(2025, 3, 17),
                'time': time(10, 32),  # 10:32 AM
                'description_ar': 'يدخل القمر في برج العقرب يوم الإثنين (17/آذار/2025م) في الساعة (10:32) صباحاً'
            },
            {
                'title_ar': 'يخرج القمر من برج العقرب',
                'title_en': 'Moon exits Scorpio',
                'date': date(2025, 3, 19),
                'time': time(23, 17),  # 11:17 PM
                'description_ar': 'يخرج القمر من برج العقرب يوم الأربعاء (19/آذار/2025م) في الساعة (11:17) مساءً'
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
                month=ramadan,
                description_ar=astro_event_data.get('description_ar'),
                description_en=astro_event_data.get('description_en')
            )
            astro_events_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {astro_events_created} astronomical events for Ramadan')) 