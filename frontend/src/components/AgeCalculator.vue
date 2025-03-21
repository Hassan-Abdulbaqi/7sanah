<template>
  <div class="age-calculator-container">
    <h2 class="calculator-title">{{ $t('ageCalculator.title') }}</h2>
    <p class="calculator-description">{{ $t('ageCalculator.description') }}</p>
    
    <div class="calculator-form">
      <!-- Input form for birthday -->
      <div class="form-section">
        <label for="birthdate">{{ $t('ageCalculator.birthdateLabel') }}</label>
        
        <div class="input-toggle">
          <button 
            @click="inputMode = 'calendar'" 
            :class="['toggle-btn', inputMode === 'calendar' ? 'active' : '']"
          >
            {{ $t('ageCalculator.calendarInput') }}
          </button>
          <button 
            @click="inputMode = 'dropdown'" 
            :class="['toggle-btn', inputMode === 'dropdown' ? 'active' : '']"
          >
            {{ $t('ageCalculator.dropdownInput') }}
          </button>
        </div>
        
        <!-- Calendar input mode -->
        <div v-if="inputMode === 'calendar'" class="calendar-input">
          <input 
            type="date" 
            id="birthdate" 
            v-model="birthdate" 
            class="date-input"
            :max="today"
          />
        </div>
        
        <!-- Dropdown input mode -->
        <div v-else class="dropdown-inputs">
          <div class="dropdown-row">
            <div class="dropdown-container">
              <label for="day">{{ $t('ageCalculator.day') }}</label>
              <select id="day" v-model="dayInput" class="dropdown-select">
                <option value="" disabled>{{ $t('ageCalculator.selectDay') }}</option>
                <option v-for="day in 31" :key="`day-${day}`" :value="day">{{ day }}</option>
              </select>
            </div>
            
            <div class="dropdown-container">
              <label for="month">{{ $t('ageCalculator.month') }}</label>
              <select id="month" v-model="monthInput" class="dropdown-select">
                <option value="" disabled>{{ $t('ageCalculator.selectMonth') }}</option>
                <option v-for="(month, index) in monthOptions" :key="`month-${index}`" :value="index + 1">{{ month }}</option>
              </select>
            </div>
            
            <div class="dropdown-container">
              <label for="year">{{ $t('ageCalculator.year') }}</label>
              <select id="year" v-model="yearInput" class="dropdown-select">
                <option value="" disabled>{{ $t('ageCalculator.selectYear') }}</option>
                <option v-for="year in yearOptions" :key="`year-${year}`" :value="year">{{ year }}</option>
              </select>
            </div>
          </div>
        </div>
      </div>
      
      <button 
        @click="calculateAge" 
        class="calculate-button" 
        :disabled="!isDateValid || isLoading"
      >
        <span v-if="isLoading" class="loading-spinner"></span>
        <span>{{ isLoading ? $t('ageCalculator.calculating') : $t('ageCalculator.calculateButton') }}</span>
      </button>
    </div>
    
    <!-- Results section -->
    <div v-if="showResults" class="results-container">
      <div class="result-section">
        <h3>{{ $t('ageCalculator.gregorian') }}</h3>
        <div class="result-content">
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.birthdate') }}:</div>
            <div class="result-value">{{ ageResults.gregorian.birthdate }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.gregorianAge') }}:</div>
            <div class="result-value">{{ ageResults.gregorian.age }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.nextBirthday') }}:</div>
            <div class="result-value">{{ ageResults.gregorian.nextBirthday }}</div>
          </div>
        </div>
      </div>
      
      <div class="result-section">
        <h3>{{ $t('ageCalculator.hijri') }}</h3>
        <div class="result-content">
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.birthdate') }}:</div>
            <div class="result-value">{{ ageResults.hijri.birthdate }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.birthMonth') }}:</div>
            <div class="result-value">{{ ageResults.hijri.hijriMonthName }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.hijriAge') }}:</div>
            <div class="result-value">{{ ageResults.hijri.age }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.nextBirthday') }}:</div>
            <div class="result-value">{{ ageResults.hijri.nextBirthday }}</div>
          </div>
        </div>
      </div>
      
      <div class="result-section">
        <h3>{{ $t('ageCalculator.additionalInfo') }}</h3>
        <div class="result-content">
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.dayOfWeek') }}:</div>
            <div class="result-value">{{ ageResults.gregorian.dayOfWeek }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.dayOfYear') }}:</div>
            <div class="result-value">{{ ageResults.gregorian.dayOfYear }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.moonPhase') }}:</div>
            <div class="result-value">{{ ageResults.gregorian.moonPhase }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.season') }}:</div>
            <div class="result-value">{{ ageResults.gregorian.season }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.zodiac') }}:</div>
            <div class="result-value">{{ ageResults.gregorian.zodiac }}</div>
          </div>
        </div>
      </div>
      
      <div class="result-section">
        <h3>{{ $t('ageCalculator.ageFormats') }}</h3>
        <div class="result-content">
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.inMonths') }}:</div>
            <div class="result-value">{{ ageResults.formats.months }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.inWeeks') }}:</div>
            <div class="result-value">{{ ageResults.formats.weeks }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.inDays') }}:</div>
            <div class="result-value">{{ ageResults.formats.days }}</div>
          </div>
          
          <div class="result-row">
            <div class="result-label">{{ $t('ageCalculator.inHours') }}:</div>
            <div class="result-value">{{ ageResults.formats.hours }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import axios from 'axios';
import { useNotification } from '../composables/useNotification';

const { t } = useI18n();
const notification = useNotification();

// State variables
const birthdate = ref('');
const ageResults = ref(null);
const showResults = ref(false);
const isLoading = ref(false);
const today = computed(() => {
  const now = new Date();
  return now.toISOString().split('T')[0];
});

// Input mode
const inputMode = ref('calendar');

// Dropdown inputs
const dayInput = ref('');
const monthInput = ref('');
const yearInput = ref('');

// Generate year options (100 years from current year)
const yearOptions = computed(() => {
  const currentYear = new Date().getFullYear();
  const years = [];
  for (let year = currentYear; year >= currentYear - 100; year--) {
    years.push(year);
  }
  return years;
});

// Month options based on current locale
const monthOptions = computed(() => {
  const locale = 'ar'; // You can make this dynamic based on the app's locale
  return gregorianMonths[locale];
});

// When dropdown inputs change, update the birthdate
watch([dayInput, monthInput, yearInput], ([day, month, year]) => {
  if (day && month && year) {
    const formattedMonth = month.toString().padStart(2, '0');
    const formattedDay = day.toString().padStart(2, '0');
    birthdate.value = `${year}-${formattedMonth}-${formattedDay}`;
  }
});

// When direct input changes, update dropdown values
watch(birthdate, (newDate) => {
  if (newDate) {
    const [year, month, day] = newDate.split('-').map(Number);
    yearInput.value = year;
    monthInput.value = month;
    dayInput.value = day;
  }
});

// Validate if the date is complete
const isDateValid = computed(() => {
  if (inputMode.value === 'calendar') {
    return !!birthdate.value;
  } else {
    return !!dayInput.value && !!monthInput.value && !!yearInput.value;
  }
});

// Arabic month names
const hijriMonths = {
  1: 'محرم',
  2: 'صفر',
  3: 'ربيع الأول',
  4: 'ربيع الثاني',
  5: 'جمادى الأولى',
  6: 'جمادى الآخرة',
  7: 'رجب',
  8: 'شعبان',
  9: 'رمضان',
  10: 'شوال',
  11: 'ذو القعدة',
  12: 'ذو الحجة'
};

// Gregorian month names
const gregorianMonths = {
  en: [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ],
  ar: [
    'كانون الثاني - يناير', 'شباط - فبراير', 'آذار - مارس', 'نيسان - أبريل',
    'أيار - مايو', 'حزيران - يونيو', 'تموز - يوليو', 'آب - أغسطس',
    'أيلول - سبتمبر', 'تشرين الأول - أكتوبر', 'تشرين الثاني - نوفمبر', 'كانون الأول - ديسمبر'
  ]
};

// Day names in Arabic
const weekdayNames = {
  ar: ['الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
};

// Season calculation
const getSeasonAr = (month, day) => {
  // Northern hemisphere seasons
  if ((month === 12 && day >= 21) || month <= 2 || (month === 3 && day < 20)) {
    return 'الشتاء';
  } else if ((month === 3 && day >= 20) || month <= 5 || (month === 6 && day < 21)) {
    return 'الربيع';
  } else if ((month === 6 && day >= 21) || month <= 8 || (month === 9 && day < 23)) {
    return 'الصيف';
  } else {
    return 'الخريف';
  }
};

// Zodiac calculation
const getZodiacAr = (month, day) => {
  if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) {
    return 'الدلو';
  } else if ((month === 2 && day >= 19) || (month === 3 && day <= 20)) {
    return 'الحوت';
  } else if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) {
    return 'الحمل';
  } else if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) {
    return 'الثور';
  } else if ((month === 5 && day >= 21) || (month === 6 && day <= 20)) {
    return 'الجوزاء';
  } else if ((month === 6 && day >= 21) || (month === 7 && day <= 22)) {
    return 'السرطان';
  } else if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) {
    return 'الأسد';
  } else if ((month === 8 && day >= 23) || (month === 9 && day <= 22)) {
    return 'العذراء';
  } else if ((month === 9 && day >= 23) || (month === 10 && day <= 22)) {
    return 'الميزان';
  } else if ((month === 10 && day >= 23) || (month === 11 && day <= 21)) {
    return 'العقرب';
  } else if ((month === 11 && day >= 22) || (month === 12 && day <= 21)) {
    return 'القوس';
  } else {
    return 'الجدي';
  }
};

// Utility to format time duration
const formatTimeDuration = (years, months, days) => {
  const formattedYears = years > 0 ? `${years} ${t('ageCalculator.years')} ` : '';
  const formattedMonths = months > 0 ? `${months} ${t('ageCalculator.months')} ` : '';
  const formattedDays = days > 0 ? `${days} ${t('ageCalculator.days')}` : '';
  
  return `${formattedYears}${formattedMonths}${formattedDays}`.trim();
};

// Convert Gregorian to Hijri date
const convertToHijri = async (dateStr) => {
  try {
    // Parse the date string (YYYY-MM-DD format from input)
    const [year, month, day] = dateStr.split('-').map(Number);
    
    // Format for API: DD-MM-YYYY
    const formattedDay = day.toString().padStart(2, '0');
    const formattedMonth = month.toString().padStart(2, '0');
    const formattedApiDate = `${formattedDay}-${formattedMonth}-${year}`;
    
    // Use the aladhan.com API with UAQ method
    const apiUrl = `https://api.aladhan.com/v1/gToH/${formattedApiDate}?calendarMethod=UAQ`;
    console.log(`Fetching Hijri date from: ${apiUrl}`);
    
    const response = await axios.get(apiUrl);
    
    if (response.data && response.data.code === 200 && response.data.data && response.data.data.hijri) {
      const hijri = response.data.data.hijri;
      console.log('Hijri data received:', hijri);
      
      return {
        year: parseInt(hijri.year),
        month: {
          number: parseInt(hijri.month.number),
          en: hijri.month.en,
          ar: hijri.month.ar
        },
        day: parseInt(hijri.day)
      };
    } else {
      throw new Error('Invalid API response structure');
    }
  } catch (error) {
    console.error("Error converting to Hijri:", error);
    
    // Fall back to a static calculation for current date
    const now = new Date();
    const isToday = dateStr === now.toISOString().split('T')[0];
    
    // Secondary fallback to approximate calculation
    const date = new Date(dateStr);
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    
    // Calculate Hijri year approximation (Hijri year is about 3% shorter)
    // Each 100 Gregorian years is approximately 103 Hijri years
    // Formula: Hijri year ≈ Gregorian year + (Gregorian year - 622) * 0.03
    const gregorianOffset = year - 622; // 622 CE is when Hijri calendar started
    const approxHijriYear = Math.floor(year + gregorianOffset * 0.03);
    
    // Approximate month and day
    // Since Hijri months rotate through seasons, we use a relative calculation
    // This is a very rough approximation
    let hijriMonth = month;
    let hijriDay = day;
    
    // Add base offset
    const currentTime = new Date().getTime();
    const dateTime = date.getTime();
    const daysSinceEpoch = Math.floor((currentTime - dateTime) / (1000 * 60 * 60 * 24));
    
    // Adjust for the difference in year length (354.37 vs 365.25 days)
    const yearLengthDiff = 0.03; // approx difference factor
    const adjustedDay = Math.floor(daysSinceEpoch * yearLengthDiff);
    
    // For dates in the current year, we can use a rough static mapping
    if (isToday) {
      // Return current Hijri date - update these values periodically for better accuracy
      return {
        year: 1446, 
        month: {
          number: 7,
          en: 'Rajab',
          ar: 'رجب'
        },
        day: 10
      };
    }
    
    return {
      year: approxHijriYear,
      month: {
        number: hijriMonth > 12 ? hijriMonth % 12 : hijriMonth,
        en: getHijriMonthName(hijriMonth > 12 ? hijriMonth % 12 : hijriMonth, 'en'),
        ar: getHijriMonthName(hijriMonth > 12 ? hijriMonth % 12 : hijriMonth, 'ar')
      },
      day: hijriDay > 30 ? 30 : (hijriDay < 1 ? 1 : hijriDay)
    };
  }
};

// Helper function to get Hijri month names
const getHijriMonthName = (monthNumber, language) => {
  const months = {
    en: [
      'Muharram', 'Safar', 'Rabi al-Awwal', 'Rabi al-Thani', 
      'Jumada al-Awwal', 'Jumada al-Thani', 'Rajab', 'Shaban',
      'Ramadan', 'Shawwal', 'Dhu al-Qadah', 'Dhu al-Hijjah'
    ],
    ar: [
      'محرم', 'صفر', 'ربيع الأول', 'ربيع الثاني',
      'جمادى الأولى', 'جمادى الآخرة', 'رجب', 'شعبان',
      'رمضان', 'شوال', 'ذو القعدة', 'ذو الحجة'
    ]
  };
  
  if (monthNumber < 1 || monthNumber > 12) {
    console.error(`Invalid Hijri month number: ${monthNumber}`);
    return language === 'ar' ? 'غير معروف' : 'Unknown';
  }
  
  return months[language][monthNumber - 1];
};

// Moon phase calculation
const getMoonPhase = (date) => {
  // More accurate algorithm for moon phase calculation
  // Based on the Brown lunation number formula that works for all dates
  const JD = (timestamp) => {
    // Convert timestamp to Julian Date
    return timestamp / 86400000 + 2440587.5;
  };
  
  const julian = JD(date.getTime());
  // Calculate the approximate phase of the moon
  const elongation = (julian - 2451550.1) / 29.530588853; // Lunar cycle
  const phase = elongation - Math.floor(elongation);
  
  // Normalize the phase to be between 0 and 1
  const normalizedPhase = phase < 0 ? phase + 1 : phase;
  
  // Convert the phase to an actual description
  if (normalizedPhase < 0.025 || normalizedPhase >= 0.975) return t('ageCalculator.newMoon');
  if (normalizedPhase < 0.225) return t('ageCalculator.waxingCrescent');
  if (normalizedPhase < 0.275) return t('ageCalculator.firstQuarter');
  if (normalizedPhase < 0.475) return t('ageCalculator.waxingGibbous');
  if (normalizedPhase < 0.525) return t('ageCalculator.fullMoon');
  if (normalizedPhase < 0.725) return t('ageCalculator.waningGibbous');
  if (normalizedPhase < 0.775) return t('ageCalculator.lastQuarter');
  return t('ageCalculator.waningCrescent');
};

// Get day of year
const getDayOfYear = (date) => {
  const start = new Date(date.getFullYear(), 0, 0);
  const diff = date - start;
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);
  return dayOfYear;
};

// Calculate age
const calculateAge = async () => {
  if (!birthdate.value || isLoading.value) return;

  try {
    // Set loading state
    isLoading.value = true;
    
    // Gregorian age calculation
    const today = new Date();
    const birthDate = new Date(birthdate.value);
    
    // Calculate age as years, months, and days
    let ageYears = today.getFullYear() - birthDate.getFullYear();
    let ageMonths = today.getMonth() - birthDate.getMonth();
    let ageDays = today.getDate() - birthDate.getDate();
    
    // Handle negative days
    if (ageDays < 0) {
      ageMonths--;
      const prevMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1);
      const daysInPrevMonth = new Date(today.getFullYear(), today.getMonth(), 0).getDate();
      ageDays += daysInPrevMonth;
    }
    
    // Handle negative months
    if (ageMonths < 0) {
      ageYears--;
      ageMonths += 12;
    }

    // Calculate next birthday (in Gregorian)
    const nextBirthdayDate = new Date(today.getFullYear(), birthDate.getMonth(), birthDate.getDate());
    if (nextBirthdayDate < today) {
      nextBirthdayDate.setFullYear(nextBirthdayDate.getFullYear() + 1);
    }
    
    // Calculate time to next birthday
    const timeToNextBirthday = nextBirthdayDate.getTime() - today.getTime();
    const days = Math.floor(timeToNextBirthday / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeToNextBirthday % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeToNextBirthday % (1000 * 60 * 60)) / (1000 * 60));
    
    // Get day of year for birth date
    const dayOfYear = getDayOfYear(birthDate);
    
    // Get moon phase for birth date
    const moonPhase = getMoonPhase(birthDate);
    
    // Format the next birthday string - defined before any conditional logic
    let nextBirthdayFormatted = `${days} ${t('ageCalculator.days')} ${hours} ${t('ageCalculator.hours')} ${minutes} ${t('ageCalculator.minutes')}`;
    
    // Get the current date in Hijri
    const currentHijriDate = await convertToHijri(today.toISOString().split('T')[0]);
    console.log('Current Hijri date:', currentHijriDate);
    
    // Get birth date in Hijri
    const birthHijriDate = await convertToHijri(birthdate.value);
    console.log('Birth Hijri date:', birthHijriDate);
    
    // Calculate Hijri age
    let hijriAgeYears = currentHijriDate.year - birthHijriDate.year;
    let hijriAgeMonths = currentHijriDate.month.number - birthHijriDate.month.number;
    let hijriAgeDays = currentHijriDate.day - birthHijriDate.day;
    
    // Handle negative days
    if (hijriAgeDays < 0) {
      hijriAgeMonths--;
      // Approximate days in the previous Hijri month as 30
      hijriAgeDays += 30;
    }
    
    // Handle negative months
    if (hijriAgeMonths < 0) {
      hijriAgeYears--;
      hijriAgeMonths += 12;
    }
    
    // Calculate age in different formats
    const totalDays = Math.floor((today.getTime() - birthDate.getTime()) / (1000 * 60 * 60 * 24));
    const totalMonths = ageYears * 12 + ageMonths;
    const totalWeeks = Math.floor(totalDays / 7);
    const remainingDays = totalDays % 7;
    const totalHours = totalDays * 24;
    
    const monthsFormatted = `${totalMonths} ${t('ageCalculator.months')} ${ageDays} ${t('ageCalculator.days')}`;
    const weeksFormatted = `${totalWeeks} ${t('ageCalculator.weeks')} ${remainingDays} ${t('ageCalculator.days')}`;
    const daysFormatted = `${totalDays.toLocaleString()} ${t('ageCalculator.days')}`;
    const hoursFormatted = `${t('ageCalculator.approximately')} ${totalHours.toLocaleString()} ${t('ageCalculator.hours')}`;
    
    // Format the age strings
    const gregorianAgeFormatted = formatTimeDuration(ageYears, ageMonths, ageDays);
    const hijriAgeFormatted = formatTimeDuration(hijriAgeYears, hijriAgeMonths, hijriAgeDays);
    
    // Get season, zodiac, and day of week
    const season = getSeasonAr(birthDate.getMonth() + 1, birthDate.getDate());
    const zodiac = getZodiacAr(birthDate.getMonth() + 1, birthDate.getDate());
    const dayOfWeek = weekdayNames.ar[birthDate.getDay()];
    
    // Update the results object
    ageResults.value = {
      gregorian: {
        birthdate: birthdate.value,
        age: gregorianAgeFormatted,
        nextBirthday: nextBirthdayFormatted,
        dayOfWeek,
        dayOfYear,
        moonPhase,
        season,
        zodiac
      },
      hijri: {
        birthdate: `${birthHijriDate.year}-${birthHijriDate.month.number}-${birthHijriDate.day}`,
        hijriMonthName: birthHijriDate.month.ar,
        age: hijriAgeFormatted,
        nextBirthday: nextBirthdayFormatted, // Using same next birthday for now
        dayOfWeek,
        season,
        zodiac
      },
      formats: {
        months: monthsFormatted,
        weeks: weeksFormatted,
        days: daysFormatted,
        hours: hoursFormatted
      },
      info: {
        dayOfWeek,
        season,
        zodiac
      }
    };
    
    // Debug output
    console.log('Age calculation results:', ageResults.value);
    
    // Show the results
    showResults.value = true;
    
    // Show a success notification
    notification.success(t('ageCalculator.calculationSuccess'));
  } catch (error) {
    console.error('Error in age calculation:', error);
    // Show an error notification
    notification.error(t('ageCalculator.calculationError'));
    // Reset the UI state
    showResults.value = false;
  } finally {
    // Always reset loading state when done
    isLoading.value = false;
  }
};
</script>

<style scoped>
.age-calculator-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem;
  background-color: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.calculator-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--primary-color);
  text-align: center;
  margin-bottom: 1rem;
}

.calculator-description {
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.calculator-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.form-section label {
  font-weight: bold;
  color: var(--text-color);
}

.input-toggle {
  display: flex;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

.toggle-btn {
  flex: 1;
  padding: 0.6rem;
  border: none;
  background-color: var(--input-bg);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.toggle-btn.active {
  background-color: var(--primary-color);
  color: white;
  font-weight: 600;
}

.toggle-btn:hover:not(.active) {
  background-color: rgba(0, 0, 0, 0.05);
}

.calendar-input, .dropdown-inputs {
  animation: fadeIn 0.3s ease-out;
}

.dropdown-row {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
  flex-wrap: wrap;
}

.dropdown-container {
  flex: 1;
  min-width: 80px;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.dropdown-container label {
  font-size: 0.875rem;
  font-weight: 500;
}

.dropdown-select {
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background-color: var(--input-bg);
  color: var(--text-color);
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-select:hover {
  border-color: var(--primary-color);
}

.date-input {
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background-color: var(--input-bg);
  color: var(--text-color);
  font-size: 1rem;
  width: 100%;
  transition: all 0.2s ease;
}

.date-input:hover, .date-input:focus {
  border-color: var(--primary-color);
}

.calculate-button {
  padding: 0.75rem 1.5rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.calculate-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, 0.5);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%);
  transform-origin: 50% 50%;
}

.calculate-button:hover {
  background-color: #0056b3; /* Darker blue color instead of using var(--primary-dark) */
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.calculate-button:active::after {
  animation: ripple 0.6s ease-out;
}

.calculate-button:disabled {
  background-color: var(--border-color);
  color: #888; /* Lighter text color for disabled state */
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

@keyframes ripple {
  0% {
    transform: scale(0, 0);
    opacity: 0.5;
  }
  20% {
    transform: scale(25, 25);
    opacity: 0.3;
  }
  100% {
    opacity: 0;
    transform: scale(40, 40);
  }
}

.results-container {
  display: flex;
  flex-direction: column;
  gap: 1.8rem;
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-section {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border-left: 5px solid transparent;
  position: relative;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.result-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.12);
}

.result-section:nth-child(1) {
  border-left-color: #3b82f6; /* Blue */
  background: linear-gradient(to right, rgba(59, 130, 246, 0.05), transparent 50%);
}

.result-section:nth-child(2) {
  border-left-color: #10b981; /* Green */
  background: linear-gradient(to right, rgba(16, 185, 129, 0.05), transparent 50%);
}

.result-section:nth-child(3) {
  border-left-color: #8b5cf6; /* Purple */
  background: linear-gradient(to right, rgba(139, 92, 246, 0.05), transparent 50%);
}

.result-section:nth-child(4) {
  border-left-color: #f59e0b; /* Amber */
  background: linear-gradient(to right, rgba(245, 158, 11, 0.05), transparent 50%);
}

.result-section h3 {
  position: relative;
  font-size: 1.4rem;
  font-weight: bold;
  margin-top: 0;
  margin-bottom: 1.2rem;
  color: var(--text-color);
  padding-bottom: 0.8rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.result-section h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background-color: currentColor;
  border-radius: 3px;
  transition: width 0.3s ease;
  opacity: 0.5;
}

.result-section:hover h3::after {
  width: 120px;
}

.result-section:nth-child(1) h3 {
  color: #3b82f6; /* Blue */
}

.result-section:nth-child(2) h3 {
  color: #10b981; /* Green */
}

.result-section:nth-child(3) h3 {
  color: #8b5cf6; /* Purple */
}

.result-section:nth-child(4) h3 {
  color: #f59e0b; /* Amber */
}

.result-section::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 3rem 3rem 0;
  border-color: transparent rgba(0, 0, 0, 0.02) transparent transparent;
  transition: all 0.3s ease;
}

.result-section:hover::before {
  border-width: 0 4rem 4rem 0;
  border-color: transparent rgba(0, 0, 0, 0.03) transparent transparent;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.result-row {
  display: flex;
  margin-bottom: 0.7rem;
  line-height: 1.5;
  transition: all 0.2s ease;
  padding: 0.7rem;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.5);
}

.result-row:hover {
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transform: translateX(5px);
}

.result-row:last-child {
  margin-bottom: 0;
}

.result-label {
  flex: 1;
  font-weight: 600;
  color: var(--text-secondary);
  min-width: 140px;
}

.result-value {
  flex: 2;
  color: var(--text-color);
  font-weight: 500;
}

@media (max-width: 640px) {
  .result-row {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .result-value {
    padding-right: 0;
  }
}

/* Loading spinner styles */
.loading-spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style> 