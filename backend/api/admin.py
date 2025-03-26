from django.contrib import admin
from .models import Khatmah, Participant, JuzAssignment, HijriMonth, HijriEvent, AstronomicalEvent

# Inline admin classes
class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0
    fields = ['name', 'created_at']
    readonly_fields = ['created_at']

class JuzAssignmentInline(admin.TabularInline):
    model = JuzAssignment
    extra = 0
    fields = ['juz_number', 'participant', 'completed', 'created_at']
    readonly_fields = ['created_at']
    autocomplete_fields = ['participant']

class HijriEventInline(admin.TabularInline):
    model = HijriEvent
    extra = 0
    fields = ['title_ar', 'title_en', 'day', 'is_holiday', 'event_type']

class AstronomicalEventInline(admin.TabularInline):
    model = AstronomicalEvent
    extra = 0
    fields = ['title_ar', 'title_en', 'date', 'time']

# Main admin classes
@admin.register(Khatmah)
class KhatmahAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'is_private', 'require_name', 'end_date', 'participant_count', 'completed_juz_count']
    list_filter = ['is_private', 'require_name', 'created_at']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at']
    inlines = [ParticipantInline, JuzAssignmentInline]
    fieldsets = (
        (None, {
            'fields': ('id', 'name', 'created_at')
        }),
        ('Settings', {
            'fields': ('is_private', 'require_name', 'end_date', 'image', 'image_url', 'khatmah_type')
        }),
    )
    
    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = 'Participants'
    
    def completed_juz_count(self, obj):
        return obj.assignments.filter(completed=True).count()
    completed_juz_count.short_description = 'Completed Juz'

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'khatmah', 'created_at', 'assignment_count']
    list_filter = ['khatmah', 'created_at']
    search_fields = ['name', 'khatmah__name']
    readonly_fields = ['id', 'created_at']
    autocomplete_fields = ['khatmah']
    inlines = [JuzAssignmentInline]
    
    def assignment_count(self, obj):
        return obj.assignments.count()
    assignment_count.short_description = 'Assignments'

@admin.register(JuzAssignment)
class JuzAssignmentAdmin(admin.ModelAdmin):
    list_display = ['juz_number', 'participant', 'khatmah', 'completed', 'created_at']
    list_filter = ['completed', 'khatmah', 'created_at']
    search_fields = ['participant__name', 'khatmah__name']
    readonly_fields = ['id', 'created_at']
    autocomplete_fields = ['participant', 'khatmah']
    list_editable = ['completed']
    actions = ['mark_as_completed', 'mark_as_not_completed']
    
    def mark_as_completed(self, request, queryset):
        queryset.update(completed=True)
    mark_as_completed.short_description = "Mark selected assignments as completed"
    
    def mark_as_not_completed(self, request, queryset):
        queryset.update(completed=False)
    mark_as_not_completed.short_description = "Mark selected assignments as not completed"

@admin.register(HijriMonth)
class HijriMonthAdmin(admin.ModelAdmin):
    list_display = ['name_ar', 'name_en', 'number', 'year', 'gregorian_start', 'gregorian_end', 'event_count']
    list_filter = ['year', 'number']
    search_fields = ['name_ar', 'name_en']
    readonly_fields = ['id']
    inlines = [HijriEventInline, AstronomicalEventInline]
    fieldsets = (
        (None, {
            'fields': ('id', 'name_ar', 'name_en', 'number', 'year')
        }),
        ('Gregorian Dates', {
            'fields': ('gregorian_start', 'gregorian_end')
        }),
        ('Additional Data', {
            'fields': ('moon_sighting_data', 'calendar_data'),
            'classes': ('collapse',),
        }),
    )
    
    def event_count(self, obj):
        return obj.events.count()
    event_count.short_description = 'Events'

@admin.register(HijriEvent)
class HijriEventAdmin(admin.ModelAdmin):
    list_display = ['title_ar', 'title_en', 'day', 'month', 'is_holiday', 'event_type']
    list_filter = ['is_holiday', 'event_type', 'month__year', 'month__number']
    search_fields = ['title_ar', 'title_en', 'description_ar', 'description_en']
    readonly_fields = ['id']
    autocomplete_fields = ['month']
    fieldsets = (
        (None, {
            'fields': ('id', 'day', 'month', 'year_of_event')
        }),
        ('Event Details', {
            'fields': ('title_ar', 'title_en', 'description_ar', 'description_en', 'is_holiday', 'event_type')
        }),
    )

@admin.register(AstronomicalEvent)
class AstronomicalEventAdmin(admin.ModelAdmin):
    list_display = ['title_ar', 'title_en', 'date', 'time', 'month']
    list_filter = ['month__year', 'month__number', 'date']
    search_fields = ['title_ar', 'title_en', 'description_ar', 'description_en']
    readonly_fields = ['id']
    autocomplete_fields = ['month']
    fieldsets = (
        (None, {
            'fields': ('id', 'date', 'time', 'month')
        }),
        ('Event Details', {
            'fields': ('title_ar', 'title_en', 'description_ar', 'description_en')
        }),
    )
