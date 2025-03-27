<template>
  <div class="hijri-calendar-container">
    <!-- Calendar Header (Removing Tab Navigation) -->
    <div class="calendar-header">
      <h2 class="calendar-title">{{ t('hijriCalendar.title') }}</h2>
      <div class="calendar-controls">
        <button @click="previousMonth" class="control-button" :disabled="isNavigating">
          <span class="icon">→</span>
        </button>
        <div class="month-display">
          <span class="month-name">{{ currentMonth?.name_ar || '' }}</span>
          <span class="month-name-en">{{ currentMonth?.name_en || '' }}</span>
          <span class="year" v-if="currentMonth?.year">{{ currentMonth.year }}{{ t('hijriCalendar.hijriYear') }}</span>
        </div>
        <button @click="nextMonth" class="control-button" :disabled="isNavigating">
          <span class="icon">←</span>
        </button>
      </div>
    </div>

    <!-- Calendar content with fixed height container -->
    <div class="calendar-container">
      <!-- Initial loading state -->
      <div v-if="loading && !isNavigating" class="calendar-loading">
        <div class="spinner-container">
          <div class="spinner"></div>
        </div>
        <p class="loading-text">{{ t('hijriCalendar.loading') }}</p>
      </div>

      <div v-else-if="error" class="calendar-error">
        <p>{{ t('hijriCalendar.error') }}: {{ error }}</p>
      </div>

      <!-- Calendar with transition effects -->
      <div v-else class="calendar-wrapper">
        <transition :name="navigationDirection" mode="out-in">
          <div :key="currentMonth?.name_en + currentMonth?.year" class="calendar-body">
            <div class="weekdays">
              <div class="weekday" v-for="day in weekdays" :key="day">{{ day }}</div>
            </div>
            
            <div class="days-grid">
              <!-- Empty cells for days before the month starts -->
              <div 
                v-for="n in firstDayOfMonth" 
                :key="`empty-${n}`" 
                class="day-cell empty">
              </div>
              
              <!-- Calendar days -->
              <div 
                v-for="day in calendarDays" 
                :key="day.hijri_day" 
                class="day-cell"
                :class="{ 
                  'has-events': day.events.length > 0,
                  'has-holiday': day.events.some(e => e.is_holiday),
                  'today': isToday(day.gregorian_date)
                }"
                @click="showDayDetails(day)"
              >
                <div class="day-content">
                  <div class="day-number-container">
                    <span class="day-number">{{ day.hijri_day }}</span>
                    <span class="hijri-indicator">هـ</span>
                  </div>
                  <div class="gregorian-date">{{ formatGregorianDate(day.gregorian_date) }}</div>
                  
                  <div v-if="day.events.length > 0" class="event-indicators">
                    <span 
                      v-for="(event, index) in day.events.slice(0, 2)" 
                      :key="index" 
                      class="event-dot"
                      :class="{ 'holiday': event.is_holiday }"
                    ></span>
                    <span v-if="day.events.length > 2" class="more-events">+{{ day.events.length - 2 }}</span>
                  </div>
                  
                  <!-- Event glimpse for all screen sizes -->
                  <div v-if="day.events.length > 0" class="event-glimpse">
                    <div class="event-glimpse-title">{{ formatEventTitle(day.events[0].title_ar) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </transition>
        
        <!-- Navigation loading overlay -->
        <div v-if="isNavigating && showSpinner" class="navigation-loading-overlay">
          <div class="spinner-container">
            <div class="spinner"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Day details modal -->
    <div v-if="selectedDay" class="day-details-modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">
            {{ formatHijriDate(selectedDay) }}
          </h3>
          <button @click="closeModal" class="close-button">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="date-info">
            <div class="gregorian-date-full">{{ formatGregorianDateFull(selectedDay.gregorian_date) }}</div>
          </div>
          
          <div class="events-container">
            <div v-if="selectedDay.events.length > 0" class="events-list">
              <h4>{{ t('hijriCalendar.events') }}</h4>
              <div 
                v-for="(event, index) in selectedDay.events" 
                :key="index"
                :class="['event-item', { 'holiday': event.is_holiday }]"
              >
                <div class="event-title">{{ event.title_ar }}</div>
                <div class="event-title-en">{{ event.title_en }}</div>
                <div v-if="event.description_ar" class="event-description">{{ event.description_ar }}</div>
              </div>
            </div>
            
            <div v-if="selectedDay.astronomical_events.length > 0" class="astro-events-list">
              <h4>{{ t('hijriCalendar.astronomicalEvents') }}</h4>
              <div 
                v-for="(event, index) in selectedDay.astronomical_events" 
                :key="index"
                class="astro-event-item"
              >
                <div class="event-title">{{ event.title_ar }}</div>
                <div class="event-time" v-if="event.time">{{ event.time }}</div>
                <div v-if="event.description_ar" class="event-description">{{ event.description_ar }}</div>
              </div>
            </div>
            
            <div v-if="selectedDay.events.length === 0 && selectedDay.astronomical_events.length === 0" class="no-events">
              {{ t('hijriCalendar.noEvents') }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Source information -->
    <div class="calendar-source-info">
      <p class="source-text">حسب رأي السيد علي السيستاني اطال الله عمره</p>
      <a href="https://www.sistani.org/arabic/archive/26889/" target="_blank" class="source-link">المصدر</a>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';
import axios from 'axios';
import { store } from '../store';

const { t } = useI18n();

// Extract base API URL from store
const API_BASE_URL = store.API_URL || 'https://api.7sanah.com/api';

// State variables
const loading = ref(true);
const error = ref(null);
const calendarData = ref(null);
const currentMonth = ref({
  name_ar: '',
  name_en: '',
  year: null,
  number: null,
  gregorian_start: null,
  gregorian_end: null
});
const selectedDay = ref(null);
const availableMonths = ref([]);

// Navigation state
const isNavigating = ref(false);
const navigationDirection = ref('slide-right');
const showSpinner = ref(false);

// Arabic weekdays
const weekdays = [
  t('hijriCalendar.weekdays.sunday'),
  t('hijriCalendar.weekdays.monday'),
  t('hijriCalendar.weekdays.tuesday'),
  t('hijriCalendar.weekdays.wednesday'),
  t('hijriCalendar.weekdays.thursday'),
  t('hijriCalendar.weekdays.friday'),
  t('hijriCalendar.weekdays.saturday')
];

// Screen width state for responsive title formatting
const windowWidth = ref(window.innerWidth);

// Update window width on resize
const handleResize = () => {
  windowWidth.value = window.innerWidth;
};

// Computed properties
const calendarDays = computed(() => {
  if (!calendarData.value) return [];
  return calendarData.value.calendar || [];
});

const firstDayOfMonth = computed(() => {
  if (!calendarData.value || !calendarData.value.month || !calendarData.value.month.gregorian_start) return 0;
  
  // Get the day of week (0 = Sunday, 1 = Monday, etc.)
  const startDate = new Date(calendarData.value.month.gregorian_start);
  return startDate.getDay(); // Sunday is 0, so this works for our Arabic calendar
});

// Methods
const normalizeMonthName = (monthName) => {
  if (!monthName) return '';
  
  // Create a mapping of possible variations to standardized names
  const monthNameMap = {
    // Standard names
    'muharram': 'Muharram',
    'safar': 'Safar',
    'rabi al-awwal': 'Rabi al-Awwal',
    'rabi al-thani': 'Rabi al-Thani',
    'jumada al-awwal': 'Jumada al-Awwal',
    'jumada al-thani': 'Jumada al-Thani',
    'rajab': 'Rajab',
    'shaban': 'Shaban',
    'ramadan': 'Ramadan',
    'shawwal': 'Shawwal',
    'dhul-qadah': 'Dhul-Qadah',
    'dhu al-qadah': 'Dhul-Qadah',
    'dhul qadah': 'Dhul-Qadah',
    'dhu al qadah': 'Dhul-Qadah',
    'dhul-hijjah': 'Dhul-Hijjah',
    'dhu al-hijjah': 'Dhul-Hijjah',
    'dhul hijjah': 'Dhul-Hijjah',
    'dhu al hijjah': 'Dhul-Hijjah',
    
    // Variations with different spellings
    'dhu-al-qadah': 'Dhul-Qadah',
    'dhulqadah': 'Dhul-Qadah',
    'zulqadah': 'Dhul-Qadah',
    'dhu-al-hijjah': 'Dhul-Hijjah',
    'dhulhijjah': 'Dhul-Hijjah',
    'zulhijjah': 'Dhul-Hijjah'
  };
  
  // Normalize the input by converting to lowercase
  const normalizedInput = monthName.toLowerCase();
  
  // Return the mapped standard name or the original if not found
  return monthNameMap[normalizedInput] || monthName;
};

const fetchCalendarData = async (monthNumber = null, year = null) => {
  isNavigating.value = true;
  error.value = null;
  
  // Set a delay timer for showing the loading spinner
  const loadingTimer = setTimeout(() => {
    // Only show the spinner if we're still loading after 1 second
    if (isNavigating.value) {
      showSpinner.value = true;
    }
  }, 1000);
  
  try {
    // Force year to be 1446 if provided
    if (year && year !== 1446) {
      console.warn(`Year ${year} provided, but only 1446 is supported. Forcing year to 1446.`);
      year = 1446;
    }
    
    // Construct the API URL with query parameters if provided
    let url = `${API_BASE_URL}/hijri-calendar/`;
    
    // If specific month number and year are provided, use them
    if (monthNumber !== null && year) {
      url += `?month_number=${encodeURIComponent(monthNumber)}&year=${encodeURIComponent(year)}`;
    } else {
      // Otherwise, try to get the current Hijri month based on today's date
      const today = new Date();
      url += `?gregorian_date=${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    }
    
    
    const response = await axios.get(url, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.data || response.status !== 200) {
      throw new Error('Invalid response from API');
    }
    
    
    
    // Set the data from the API response
    currentMonth.value = response.data.month;
    calendarData.value = response.data;
    
    
    
    // Fetch available months for navigation if we haven't already
    if (availableMonths.value.length === 0) {
      await fetchAvailableMonths();
    }
    
    
    error.value = null;
  } catch (err) {
    console.error('Error fetching calendar data:', err);
    
    // Special handling for 404 errors
    if (err.response && err.response.status === 404) {
      // Check if we were looking for Dhul-Hijjah
      if (monthNumber === 12 && year) {
        error.value = `Month ${monthNumber} (Dhul-Hijjah) ${year} not found. You may need to run the populate_dhul_hijjah script.`;
        
      } else {
        error.value = err.response.data.error || `Month not found: ${monthNumber || 'current month'}`;
      }
    } else {
      error.value = 'Error fetching calendar data: ' + (err.message || 'Unknown error');
    }
    
    // Log more detailed error information
    if (err.response) {
      console.error('Error response data:', err.response.data);
      
    } else if (err.request) {
      // The request was made but no response was received
      console.error('No response received:', err.request);
    }
  } finally {
    // Add a small delay to make the loading state visible
    setTimeout(() => {
      loading.value = false;
      isNavigating.value = false;
      showSpinner.value = false;
      clearTimeout(loadingTimer); // Clear the timer if it hasn't fired yet
    }, 300);
  }
};

const fetchAvailableMonths = async () => {
  try {
    
    
    // Function to fetch a page of months
    const fetchMonthsPage = async (url) => {
      const response = await axios.get(url, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      
      
      
      if (response.data && Array.isArray(response.data.results)) {
        // Process the months from this page
        const monthsFromPage = response.data.results.map(month => ({
          ...month,
          name_en: normalizeMonthName(month.name_en)
        }));
        
        // Add these months to our collection
        return {
          months: monthsFromPage,
          nextPage: response.data.next
        };
      }
      
      return { months: [], nextPage: null };
    };
    
    // Start with the first page
    let allMonths = [];
    let currentUrl = `${API_BASE_URL}/hijri-months/`;
    let hasMorePages = true;
    
    // Fetch all pages
    while (hasMorePages) {
      const { months, nextPage } = await fetchMonthsPage(currentUrl);
      allMonths = [...allMonths, ...months];
      
      if (nextPage) {
        
        currentUrl = nextPage;
      } else {
        hasMorePages = false;
      }
    }
    
    // Store all the months
    availableMonths.value = allMonths;
    
    // Define the correct Hijri month order
    const monthOrder = [
      'Muharram', 'Safar', 'Rabi al-Awwal', 'Rabi al-Thani', 
      'Jumada al-Awwal', 'Jumada al-Thani', 'Rajab', 'Shaban', 
      'Ramadan', 'Shawwal', 'Dhul-Qadah', 'Dhul-Hijjah'
    ];
    
    // Sort the months according to the correct Hijri order
    availableMonths.value.sort((a, b) => {
      // First sort by year
      if (a.year !== b.year) {
        return a.year - b.year;
      }
      
      // Then sort by month order
      return monthOrder.indexOf(a.name_en) - monthOrder.indexOf(b.name_en);
    });
    
    // Check if months 11 and 12 are available for year 1446
    const year1446Months = availableMonths.value.filter(month => month.year === 1446);
    const month11 = year1446Months.find(month => month.number === 11);
    const month12 = year1446Months.find(month => month.number === 12);
    
    
    
    // Log all available months with their numbers
    
    
    
    
  } catch (err) {
    console.error('Error fetching available months:', err);
    
    // Log more detailed error information
    if (err.response) {
      console.error('Error response data:', err.response.data);
      console.error('Error response status:', err.response.status);
    } else if (err.request) {
      console.error('No response received:', err.request);
    }
    
    availableMonths.value = [];
  }
};

const fetchSpecificMonth = async (monthId) => {
  if (!monthId) return;
  
  try {
    loading.value = true;
    error.value = null;
    
    const month = availableMonths.value.find(m => m.id === monthId);
    if (month) {
      await fetchCalendarData(month.number, month.year);
    } else {
      console.error(`Month with ID ${monthId} not found in available months`);
      error.value = 'Month not found';
    }
  } catch (err) {
    console.error('Error fetching specific month:', err);
    error.value = 'Error fetching month data: ' + (err.message || 'Unknown error');
  } finally {
    loading.value = false;
  }
};

const formatGregorianDate = (dateStr) => {
  if (!dateStr) return '';
  try {
    const date = new Date(dateStr);
    const day = date.getDate();
    
    // Get month name from translations
    const monthNames = [
      t('hijriCalendar.gregorianMonths.january'),
      t('hijriCalendar.gregorianMonths.february'),
      t('hijriCalendar.gregorianMonths.march'),
      t('hijriCalendar.gregorianMonths.april'),
      t('hijriCalendar.gregorianMonths.may'),
      t('hijriCalendar.gregorianMonths.june'),
      t('hijriCalendar.gregorianMonths.july'),
      t('hijriCalendar.gregorianMonths.august'),
      t('hijriCalendar.gregorianMonths.september'),
      t('hijriCalendar.gregorianMonths.october'),
      t('hijriCalendar.gregorianMonths.november'),
      t('hijriCalendar.gregorianMonths.december')
    ];
    const month = monthNames[date.getMonth()];
    
    return `${day} ${month}`;
  } catch (err) {
    console.error('Error formatting date:', err);
    return '';
  }
};

const formatGregorianDateFull = (dateStr) => {
  if (!dateStr) return '';
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString('ar-SA', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  } catch (err) {
    console.error('Error formatting date:', err);
    return dateStr;
  }
};

const formatTime = (timeStr) => {
  if (!timeStr) return '';
  // Format time as needed
  return timeStr;
};

const isToday = (dateStr) => {
  if (!dateStr) return false;
  try {
    const today = new Date();
    const date = new Date(dateStr);
    return today.toDateString() === date.toDateString();
  } catch (err) {
    console.error('Error checking if date is today:', err);
    return false;
  }
};

const showDayDetails = (day) => {
  selectedDay.value = day;
};

const previousMonth = () => {
  if (availableMonths.value.length === 0 || isNavigating.value) {
    console.warn('No available months to navigate or navigation in progress');
    return;
  }
  
  // Set navigation direction for transition
  navigationDirection.value = 'slide-right';
  
  try {
    // Get current month number and year
    const currentMonthNumber = currentMonth.value.number;
    const currentYear = currentMonth.value.year;
    
    
    // Calculate previous month number
    let prevMonthNumber = currentMonthNumber - 1;
    let prevYear = currentYear;
    
    // If we're at the beginning of the year, loop back to month 12
    if (prevMonthNumber < 1) {
      prevMonthNumber = 12;
      // Keep the same year since we're only supporting 1446
    }
    
    
    // Check if the previous month exists in our available months
    const prevMonthExists = availableMonths.value.some(
      month => month.number === prevMonthNumber && month.year === prevYear
    );
    
    if (prevMonthExists) {
      fetchCalendarData(prevMonthNumber, prevYear);
    } else {
      console.warn(`Month ${prevMonthNumber} of year ${prevYear} not found in available months`);
      
      // Find the previous available month
      const sortedMonths = [...availableMonths.value].sort((a, b) => {
        if (a.year !== b.year) return a.year - b.year;
        return a.number - b.number;
      });
      
      // Find the index of the current month
      const currentIndex = sortedMonths.findIndex(
        month => month.number === currentMonthNumber && month.year === currentYear
      );
      
      if (currentIndex > 0) {
        // Get the previous month in the sorted list
        const prevAvailableMonth = sortedMonths[currentIndex - 1];

        fetchCalendarData(prevAvailableMonth.number, prevAvailableMonth.year);
      } else if (sortedMonths.length > 0) {
        // Loop back to the last month
        const lastMonth = sortedMonths[sortedMonths.length - 1];
        
        fetchCalendarData(lastMonth.number, lastMonth.year);
      } else {
        error.value = 'No months available for navigation';
      }
    }
  } catch (err) {
    console.error('Error in previousMonth navigation:', err);
    error.value = 'Error navigating to previous month';
  }
};

const nextMonth = () => {
  if (availableMonths.value.length === 0 || isNavigating.value) {
    console.warn('No available months to navigate or navigation in progress');
    return;
  }
  
  // Set navigation direction for transition
  navigationDirection.value = 'slide-left';
  
  try {
    // Get current month number and year
    const currentMonthNumber = currentMonth.value.number;
    const currentYear = currentMonth.value.year;
    
    
    // Calculate next month number
    let nextMonthNumber = currentMonthNumber + 1;
    let nextYear = currentYear;
    
    // If we're at the end of the year, loop back to month 1
    if (nextMonthNumber > 12) {
      nextMonthNumber = 1;
      // Keep the same year since we're only supporting 1446
    }
    
    
    // Check if the next month exists in our available months
    const nextMonthExists = availableMonths.value.some(
      month => month.number === nextMonthNumber && month.year === nextYear
    );
    
    if (nextMonthExists) {
      fetchCalendarData(nextMonthNumber, nextYear);
    } else {
      console.warn(`Month ${nextMonthNumber} of year ${nextYear} not found in available months`);
      
      // Find the next available month
      const sortedMonths = [...availableMonths.value].sort((a, b) => {
        if (a.year !== b.year) return a.year - b.year;
        return a.number - b.number;
      });
      
      // Find the index of the current month
      const currentIndex = sortedMonths.findIndex(
        month => month.number === currentMonthNumber && month.year === currentYear
      );
      
      if (currentIndex !== -1 && currentIndex < sortedMonths.length - 1) {
        // Get the next month in the sorted list
        const nextAvailableMonth = sortedMonths[currentIndex + 1];

        fetchCalendarData(nextAvailableMonth.number, nextAvailableMonth.year);
      } else if (sortedMonths.length > 0) {
        // Loop back to the first month
        const firstMonth = sortedMonths[0];
        
        fetchCalendarData(firstMonth.number, firstMonth.year);
      } else {
        error.value = 'No months available for navigation';
      }
    }
  } catch (err) {
    console.error('Error in nextMonth navigation:', err);
    error.value = 'Error navigating to next month';
  }
};

// Initialize the calendar
onMounted(async () => {
  try {
    // Add resize event listener
    window.addEventListener('resize', handleResize);
    
    // First fetch available months to see what we have
    await fetchAvailableMonths();
    
    // Try to get the current Hijri month from the API
    try {
      
      const response = await axios.get(`${API_BASE_URL}/hijri-months/current/`, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      
      if (response.data && response.status === 200) {
        const currentMonth = response.data;
        
        // Initialize with the current month
        await fetchCalendarData(currentMonth.number, currentMonth.year);
        return;
      }
    } catch (err) {
      console.warn('Error fetching current month, falling back to default:', err);
      // Continue with fallback initialization
    }
    
    // Fallback: Filter to only get months from year 1446
    const year1446Months = availableMonths.value.filter(month => month.year === 1446);
    
    if (year1446Months.length > 0) {
      // Start with Muharram (month 1) or the first available month
      const targetMonth = year1446Months.find(m => m.number === 1) || year1446Months[0];
      await fetchCalendarData(targetMonth.number, 1446);
    } else {
      
      console.warn('No months found for year 1446, fetching current month');
      await fetchCalendarData();
    }
    
    console.log('Calendar initialized');
  } catch (err) {
    console.error('Error initializing calendar:', err);
    error.value = 'Failed to initialize calendar';
  }
});

// Remove event listener on component unmount
onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

// Formatted Hijri date for the modal title
const formatHijriDate = (day) => {
  if (!day || !currentMonth.value) return '';
  return `${day.hijri_day} ${currentMonth.value.name_ar || ''} ${currentMonth.value.year || ''}${t('hijriCalendar.hijriYear')}`;
};

// Close the modal
const closeModal = () => {
  selectedDay.value = null;
};

// Helper function to format event title based on screen size
const formatEventTitle = (title) => {
  if (!title) return '';
  
  // Use reactive window width
  const width = windowWidth.value;
  
  // Determine character limit based on screen size
  let charLimit = 20; // Default
  
  if (width <= 480) {
    charLimit = 12;
  } else if (width <= 768) {
    charLimit = 15;
  } else if (width <= 1024) {
    charLimit = 20;
  } else {
    charLimit = 25;
  }
  
  // Truncate title if needed
  return title.length > charLimit ? title.substring(0, charLimit) + '...' : title;
};
</script>

<style scoped>
.hijri-calendar-container {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
  padding: 15px;
  direction: rtl;
  position: relative;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

.calendar-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  margin-top: 10px; /* Add top margin since tabs are gone */
}

.calendar-title {
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: #2c3e50;
  font-weight: 700;
}

.calendar-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.control-button {
  background-color: #f8f9fa;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s, opacity 0.2s;
}

.control-button:hover:not(:disabled) {
  background-color: #e9ecef;
}

.control-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.month-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 150px;
}

.month-name {
  font-size: 1.4rem;
  font-weight: 600;
  color: #1e3a8a;
}

.month-name-en {
  font-size: 0.9rem;
  color: #64748b;
  margin-top: 2px;
}

.year {
  font-size: 1rem;
  color: #64748b;
  margin-top: 2px;
}

/* Calendar container to maintain consistent height */
.calendar-container {
  position: relative;
  min-height: 600px;
  height: auto;
}

/* Calendar wrapper for positioning the overlay */
.calendar-wrapper {
  position: relative;
  min-height: 600px; /* Set a fixed minimum height to prevent layout shifts */
  height: auto;
}

/* Navigation loading overlay */
.navigation-loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  border-radius: 8px;
  backdrop-filter: blur(2px);
}

.spinner-container {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Transition effects */
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease-out;
  position: absolute;
  width: 100%;
}

.slide-left-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.calendar-body {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
  margin-bottom: 10px;
  width: 100%;
}

.weekday {
  text-align: center;
  font-weight: 600;
  color: #64748b;
  padding: 10px 0;
  background-color: #f8fafc;
  border-radius: 8px;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
  width: 100%;
  flex-grow: 1;
}

.day-cell {
  border-radius: 8px;
  background-color: #f8fafc;
  padding: 5px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: 60px;
  box-sizing: border-box;
}

.day-cell:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #f1f5f9;
  z-index: 1; /* Ensure hover effect shows above other cells */
}

.day-cell.empty {
  background-color: transparent;
  cursor: default;
}

.day-cell.empty:hover {
  transform: none;
  box-shadow: none;
  background-color: transparent;
  z-index: auto;
}

.day-cell.has-events {
  background-color: #e0f2fe;
}

.day-cell.has-holiday {
  background-color: #fee2e2;
}

.day-cell.today {
  border: 2px solid #3b82f6;
}

.day-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  width: 100%;
}

.day-number-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.day-number {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e3a8a;
}

.hijri-indicator {
  font-size: 0.8rem;
  color: #64748b;
  margin-right: 2px;
}

.gregorian-date {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 2px;
  background-color: #f1f5f9;
  padding: 2px 4px;
  border-radius: 4px;
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.event-indicators {
  display: flex;
  gap: 3px;
  align-items: center;
  margin-top: auto;
  padding-top: 3px;
}

.event-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #3b82f6;
}

.event-dot.holiday {
  background-color: #ef4444;
}

.more-events {
  font-size: 0.7rem;
  color: #64748b;
}

.event-glimpse {
  display: block;
  margin-top: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.event-glimpse-title {
  font-size: 0.7rem;
  color: #1e3a8a;
  font-weight: 500;
}

.calendar-loading, .calendar-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 600px; /* Match the min-height of calendar-wrapper */
  gap: 15px;
}

.loading-text {
  color: #64748b;
  font-size: 0.9rem;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #3b82f6;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Modal styles */
.day-details-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e5e7eb;
  position: relative;
  display: flex;
  flex-direction: column;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #1e3a8a;
}

.modal-header .gregorian-date {
  font-size: 0.9rem;
  color: #64748b;
  margin-top: 5px;
}

.close-button {
  position: absolute;
  top: 15px;
  left: 15px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
}

.modal-body {
  padding: 20px;
}

.events-list, .astro-events-list {
  margin-bottom: 20px;
}

.events-list h4, .astro-events-list h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #1e3a8a;
  font-size: 1.2rem;
}

.event-item, .astro-event-item {
  background-color: #f8fafc;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
}

.event-item.holiday {
  background-color: #fee2e2;
}

.event-title {
  font-weight: 600;
  font-size: 1.1rem;
  color: #1e3a8a;
  margin-bottom: 5px;
}

.event-title-en {
  font-size: 0.9rem;
  color: #64748b;
  margin-bottom: 5px;
}

.event-time {
  font-size: 0.9rem;
  color: #64748b;
  margin-bottom: 5px;
}

.event-description {
  font-size: 0.9rem;
  color: #334155;
  line-height: 1.5;
}

.no-events {
  text-align: center;
  color: #64748b;
  padding: 20px 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .hijri-calendar-container {
    padding: 10px;
  }

  .weekday {
    font-size: 0.7rem;
    padding: 3px 0;
  }
  
  .day-cell {
    min-height: 75px; /* Further reduced height */
    padding: 4px;
  }
  
  .day-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    justify-content: flex-start;
    gap: 0;
  }
  
  .day-number-container {
    margin-bottom: 0; /* No margin after day number */
  }
  
  .day-number {
    font-size: 0.9rem;
  }
  
  .hijri-indicator {
    font-size: 0.6rem;
  }
  
  .gregorian-date {
    margin-top: 0;
    margin-bottom: 2px; /* Consistent small margin */
    font-size: 0.6rem;
    padding: 1px 2px;
  }
  
  .event-indicators {
    display: none; /* Hide event dots on mobile */
  }
  
  .event-glimpse {
    margin-top: 0;
    padding-top: 0;
  }
  
  .event-glimpse-title {
    font-size: 0.65rem;
    line-height: 1.2;
    color: #1e3a8a;
  }
  
  .calendar-title {
    font-size: 1.3rem;
  }

  .month-display {
    min-width: 100px;
  }

  .month-name {
    font-size: 1.1rem;
  }

  .month-name-en, .year {
    font-size: 0.8rem;
  }

  .control-button {
    width: 35px;
    height: 35px;
  }
}

@media (max-width: 480px) {
  .hijri-calendar-container {
    padding: 8px;
  }
  
  .weekday {
    font-size: 0.6rem;
    padding: 2px 0;
  }
  
  .days-grid {
    gap: 3px;
  }
  
  .day-cell {
    padding: 4px;
    min-height: 75px; /* Further reduced height */
  }
  
  .day-content {
    justify-content: flex-start;
    gap: 0;
  }
  
  .day-number {
    font-size: 0.85rem;
  }
  
  .hijri-indicator {
    font-size: 0.55rem;
  }
  
  .gregorian-date {
    margin-top: 0;
    margin-bottom: 1px; /* Minimum margin */
    padding: 1px;
    font-size: 0.55rem;
    max-width: 100%;
  }
  
  .event-glimpse {
    margin-top: 0;
    padding-top: 0;
  }
  
  .event-glimpse-title {
    font-size: 0.55rem;
    line-height: 1.1;
    max-height: 2.2em;
    -webkit-line-clamp: 2;
    text-overflow: ellipsis;
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    white-space: normal;
    color: #1e3a8a;
  }
  
  .calendar-container {
    min-height: 550px;
  }
  
  .calendar-wrapper {
    min-height: 550px;
  }
  
  .calendar-loading, .calendar-error {
    min-height: 550px;
  }
  
  .month-name {
    font-size: 1rem;
  }

  .calendar-controls {
    gap: 8px;
  }

  .control-button {
    width: 30px;
    height: 30px;
  }
}

/* Desktop optimization for square cells */
@media (min-width: 1024px) {
  .days-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    aspect-ratio: 7/6; /* Approximate ratio for the entire grid */
    gap: 10px;
  }
  
  .day-cell {
    position: relative;
    min-height: unset;
    aspect-ratio: 1/1; /* Make cells square on desktop */
    padding: 0; /* Remove padding as we'll handle it in day-content */
    overflow: hidden; /* Ensure content doesn't overflow */
  }
  
  .day-cell.empty {
    aspect-ratio: 1/1;
  }
  
  .day-cell:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #f1f5f9;
    z-index: 1; /* Ensure hover effect shows above other cells */
  }
  
  .day-cell.empty:hover {
    transform: none;
    box-shadow: none;
    background-color: transparent;
    z-index: auto;
  }
  
  .day-content {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    padding: 8px;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
    width: 100%;
    height: 100%;
  }
  
  .event-glimpse {
    display: block;
    margin-top: auto;
    max-height: 40%;
    overflow: hidden;
    padding-top: 4px;
  }
  
  .event-glimpse-title {
    font-size: 0.8rem;
    line-height: 1.3;
    max-height: 2.6em;
    -webkit-line-clamp: 2;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .calendar-container {
    min-height: 700px; /* Larger for desktop */
  }
  
  .calendar-wrapper {
    min-height: 700px; /* Larger for desktop */
  }
  
  .calendar-loading, .calendar-error {
    min-height: 700px; /* Match the desktop min-height */
  }
}

/* Extra large screens */
@media (min-width: 1440px) {
  .hijri-calendar-container {
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .days-grid {
    aspect-ratio: 7/5; /* Slightly shorter cells for better proportions on large screens */
  }
  
  .day-cell {
    /* Remove padding since it's now handled in day-content */
  }
  
  .day-content {
    padding: 10px; /* Increase padding for larger screens */
  }
  
  .day-number {
    font-size: 1.4rem;
  }
  
  .gregorian-date {
    font-size: 0.85rem;
    padding: 3px 6px;
  }
  
  .event-glimpse-title {
    font-size: 0.9rem;
  }
}

/* Source information styles */
.calendar-source-info {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e5e7eb;
  text-align: center;
  font-size: 0.9rem;
  color: #64748b;
}

.source-text {
  margin-bottom: 5px;
}

.source-link {
  color: #3b82f6;
  text-decoration: underline;
  transition: color 0.2s;
}

.source-link:hover {
  color: #1d4ed8;
}
</style> 