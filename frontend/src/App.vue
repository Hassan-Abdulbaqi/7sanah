<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useI18n } from "vue-i18n";
import { store } from "./store";
import KhatmahList from "./components/KhatmahList.vue";
import KhatmahDetail from "./components/KhatmahDetail.vue";
import CreateKhatmah from "./components/CreateKhatmah.vue";
import EditKhatmah from "./components/EditKhatmah.vue";
import LanguageSwitcher from "./components/LanguageSwitcher.vue";
import HijriCalendar from "./components/HijriCalendar.vue";
import QiblaCompass from "./components/QiblaCompass.vue";

const { t, locale } = useI18n();

const currentView = ref('list');
const selectedKhatmahId = ref(null);
const transitionName = ref('slide-right');

// Prayer times location settings
const showLocationSettings = ref(false);
const timezone = ref('+3');
const longitude = ref('44.0228');
const latitude = ref('32.6143');
const locationName = ref('Baghdad, Iraq');
const detectingLocation = ref(false);
const showCityPresets = ref(false);
const selectedCountry = ref(null);

// Prayer times data
const prayerTimes = ref(null);
const loadingPrayerTimes = ref(false);
const prayerTimesError = ref(null);

// Hijri date data
const hijriDate = ref(null);
const loadingHijriDate = ref(false);
const isShiaCalendar = ref(false);

// Next prayer countdown
const nextPrayer = ref(null);
const countdownTime = ref('');
const countdownInterval = ref(null);

// City presets organized by country
const cityPresets = {
  'Saudi Arabia': [
    { name: 'Mecca', latitude: '21.4241', longitude: '39.8173', timezone: '+3' },
    { name: 'Medina', latitude: '24.5247', longitude: '39.5692', timezone: '+3' },
    { name: 'Riyadh', latitude: '24.7136', longitude: '46.6753', timezone: '+3' },
    { name: 'Jeddah', latitude: '21.4858', longitude: '39.1925', timezone: '+3' }
  ],
  'Iraq': [
    { name: 'Baghdad', latitude: '33.3152', longitude: '44.3661', timezone: '+3' },
    { name: 'Najaf', latitude: '32.0286', longitude: '44.3292', timezone: '+3' },
    { name: 'Karbala', latitude: '32.6143', longitude: '44.0228', timezone: '+3' },
    { name: 'Basra', latitude: '30.5085', longitude: '47.7804', timezone: '+3' }
  ],
  'Egypt': [
    { name: 'Cairo', latitude: '30.0444', longitude: '31.2357', timezone: '+2' },
    { name: 'Alexandria', latitude: '31.2001', longitude: '29.9187', timezone: '+2' },
    { name: 'Luxor', latitude: '25.6872', longitude: '32.6396', timezone: '+2' }
  ],
  'Turkey': [
    { name: 'Istanbul', latitude: '41.0082', longitude: '28.9784', timezone: '+3' },
    { name: 'Ankara', latitude: '39.9334', longitude: '32.8597', timezone: '+3' },
    { name: 'Konya', latitude: '37.8719', longitude: '32.4844', timezone: '+3' }
  ],
  'UAE': [
    { name: 'Dubai', latitude: '25.2048', longitude: '55.2708', timezone: '+4' },
    { name: 'Abu Dhabi', latitude: '24.4539', longitude: '54.3773', timezone: '+4' },
    { name: 'Sharjah', latitude: '25.3463', longitude: '55.4209', timezone: '+4' }
  ],
  'Pakistan': [
    { name: 'Karachi', latitude: '24.8607', longitude: '67.0011', timezone: '+5' },
    { name: 'Lahore', latitude: '31.5204', longitude: '74.3587', timezone: '+5' },
    { name: 'Islamabad', latitude: '33.6844', longitude: '73.0479', timezone: '+5' }
  ],
  'Indonesia': [
    { name: 'Jakarta', latitude: '-6.2088', longitude: '106.8456', timezone: '+7' },
    { name: 'Surabaya', latitude: '-7.2575', longitude: '112.7521', timezone: '+7' },
    { name: 'Bandung', latitude: '-6.9175', longitude: '107.6191', timezone: '+7' }
  ],
  'Malaysia': [
    { name: 'Kuala Lumpur', latitude: '3.1390', longitude: '101.6869', timezone: '+8' },
    { name: 'Putrajaya', latitude: '2.9264', longitude: '101.6964', timezone: '+8' }
  ],
  'Morocco': [
    { name: 'Rabat', latitude: '34.0209', longitude: '-6.8416', timezone: '+1' },
    { name: 'Casablanca', latitude: '33.5731', longitude: '-7.5898', timezone: '+1' },
    { name: 'Fez', latitude: '34.0181', longitude: '-5.0078', timezone: '+1' }
  ],
  'Jordan': [
    { name: 'Amman', latitude: '31.9454', longitude: '35.9284', timezone: '+3' },
    { name: 'Zarqa', latitude: '32.0667', longitude: '36.0944', timezone: '+3' }
  ]
};

// Computed property to get countries list
const countries = computed(() => {
  return Object.keys(cityPresets).sort();
});

// Computed property to get cities for selected country
const citiesForSelectedCountry = computed(() => {
  if (!selectedCountry.value) return [];
  return cityPresets[selectedCountry.value] || [];
});

function showKhatmahDetail(khatmahId) {
  transitionName.value = 'slide-left';
  selectedKhatmahId.value = khatmahId;
  currentView.value = 'detail';
  
  // Update URL without page reload
  const newUrl = `${window.location.origin}/khatmah/${khatmahId}`;
  window.history.pushState({ khatmahId }, '', newUrl);
}

function showCreateKhatmah() {
  transitionName.value = 'slide-left';
  currentView.value = 'create';
  
  // Update URL without page reload
  const newUrl = `${window.location.origin}/create`;
  window.history.pushState({}, '', newUrl);
}

function showEditKhatmah(khatmahId) {
  transitionName.value = 'slide-left';
  selectedKhatmahId.value = khatmahId;
  currentView.value = 'edit';
  
  // Update URL without page reload
  const newUrl = `${window.location.origin}/khatmah/${khatmahId}/edit`;
  window.history.pushState({ khatmahId }, '', newUrl);
}

function goToList() {
  transitionName.value = 'slide-right';
  currentView.value = 'list';
  
  // Update URL without page reload
  const newUrl = `${window.location.origin}/`;
  window.history.pushState({}, '', newUrl);
}

function handleKhatmahUpdated(khatmahId) {
  // After updating, go back to detail view
  showKhatmahDetail(khatmahId);
}

// Handle browser back/forward buttons
window.addEventListener('popstate', (event) => {
  const path = window.location.pathname;
  
  if (path === '/' || path === '') {
    currentView.value = 'list';
  } else if (path === '/create') {
    currentView.value = 'create';
  } else if (path.startsWith('/khatmah/') && path.endsWith('/edit')) {
    const khatmahId = path.split('/')[2];
    selectedKhatmahId.value = khatmahId;
    currentView.value = 'edit';
  } else if (path.startsWith('/khatmah/')) {
    const khatmahId = path.split('/').pop();
    selectedKhatmahId.value = khatmahId;
    currentView.value = 'detail';
  }
});

onMounted(async () => {
  // Note: We don't need to call fetchKhatmahs here anymore
  // as it's now handled in the KhatmahList component with pagination
  
  // Check URL on initial load
  const path = window.location.pathname;
  
  if (path === '/' || path === '') {
    currentView.value = 'list';
  } else if (path === '/create') {
    currentView.value = 'create';
  } else if (path.startsWith('/khatmah/') && path.endsWith('/edit')) {
    const khatmahId = path.split('/')[2];
    if (khatmahId) {
      selectedKhatmahId.value = khatmahId;
      currentView.value = 'edit';
      await store.fetchKhatmah(khatmahId);
    }
  } else if (path.startsWith('/khatmah/')) {
    const khatmahId = path.split('/').pop();
    if (khatmahId) {
      selectedKhatmahId.value = khatmahId;
      currentView.value = 'detail';
      await store.fetchKhatmah(khatmahId);
    }
  }

  // Load saved prayer time settings from localStorage
  const savedTimezone = localStorage.getItem('prayer_timezone');
  const savedLongitude = localStorage.getItem('prayer_longitude');
  const savedLatitude = localStorage.getItem('prayer_latitude');
  const savedLocationName = localStorage.getItem('prayer_location_name');
  
  if (savedTimezone && savedLongitude && savedLatitude && savedLocationName) {
    timezone.value = savedTimezone;
    longitude.value = savedLongitude;
    latitude.value = savedLatitude;
    locationName.value = savedLocationName;
    
    // Fetch prayer times with saved settings
    fetchPrayerTimes();
  } else {
    // Try to detect user's location automatically
    detectUserLocation();
  }
});

// Function to detect user's location
async function detectUserLocation() {
  if (!navigator.geolocation) {
    console.error('Geolocation is not supported by this browser.');
    prayerTimesError.value = 'Geolocation is not supported by your browser. Please enter your location manually.';
    return;
  }
  
  // Reset any previous error
  prayerTimesError.value = null;
  
  // Set detecting flag to show loading state
  detectingLocation.value = true;
  
  try {
    console.log('Requesting geolocation from browser...');
    
    // Try to get location from browser's geolocation API
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject, {
        enableHighAccuracy: true,
        timeout: 15000, // 15 seconds timeout
        maximumAge: 0
      });
    });
    
    // Format coordinates to 4 decimal places
    const newLatitude = position.coords.latitude.toFixed(4);
    const newLongitude = position.coords.longitude.toFixed(4);
    
    console.log('Location detected:', newLatitude, newLongitude);
    console.log('Previous location:', latitude.value, longitude.value);
    
    // Update the reactive variables
    latitude.value = newLatitude;
    longitude.value = newLongitude;
    
    // Try to get city name using reverse geocoding
    try {
      console.log('Fetching location name from geocoding service...');
      
      // Use BigDataCloud reverse geocoding API (client-side, no API key needed)
      const response = await fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude.value}&longitude=${longitude.value}&localityLanguage=en`);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Geocoding response:', data);
        
        let newLocationName = 'Current Location';
        
        if (data) {
          const city = data.city || data.locality || '';
          const country = data.countryName || '';
          
          // Build location name with available information
          if (city && country) {
            newLocationName = `${city}, ${country}`;
          } else if (country) {
            newLocationName = country;
          }
          
          console.log('Location name set to:', newLocationName);
        }
        
        // Update the reactive variable
        locationName.value = newLocationName;
      } else {
        throw new Error(`Geocoding API error: ${response.status}`);
      }
    } catch (error) {
      console.error('Error getting location name:', error);
      locationName.value = 'Current Location';
    }
    
    // Use browser's built-in timezone
    try {
      const offset = new Date().getTimezoneOffset();
      const offsetHours = Math.abs(offset) / 60;
      timezone.value = offset <= 0 ? `+${offsetHours}` : `-${offsetHours}`;
      console.log('Using browser timezone:', timezone.value);
    } catch (error) {
      console.error('Error getting timezone:', error);
      // Keep current timezone
    }
    
    // Fetch prayer times with detected location
    console.log('Fetching prayer times with new location...');
    await fetchPrayerTimes();
    
    // Show the updated location in the UI
    console.log('Location detection complete. UI should be updated.');
  } catch (error) {
    console.error('Error getting location:', error);
    
    // Provide more specific error messages
    if (error.code === 1) {
      prayerTimesError.value = 'Location access was denied. Please enable location services in your browser settings or enter your location manually.';
    } else if (error.code === 2) {
      prayerTimesError.value = 'Location information is unavailable. Please enter your location manually.';
    } else if (error.code === 3) {
      prayerTimesError.value = 'Location request timed out. Please try again or enter your location manually.';
    } else {
      prayerTimesError.value = `Error detecting location: ${error.message || 'Unknown error'}. Please enter your location manually.`;
    }
  } finally {
    detectingLocation.value = false;
  }
}

// Function to select a preset city
function selectCity(city) {
  latitude.value = city.latitude;
  longitude.value = city.longitude;
  timezone.value = city.timezone;
  locationName.value = `${city.name}, ${selectedCountry.value}`;
  showCityPresets.value = false;
  fetchPrayerTimes();
}

// Function to calculate the next prayer time
function calculateNextPrayer() {
  if (!prayerTimes.value) return;
  
  const now = new Date();
  
  // Define the three prayers we want to track
  const prayers = [
    { name: 'fajr', time: prayerTimes.value.fajir?.trim(), translationKey: 'prayerTimes.fajr', isPM: false },
    { name: 'dhuhr', time: prayerTimes.value.doher?.trim(), translationKey: 'prayerTimes.dhuhr', isPM: true },
    { name: 'maghrib', time: prayerTimes.value.maghrib?.trim(), translationKey: 'prayerTimes.maghrib', isPM: true }
  ];
  
  console.log('Calculating next prayer. Current time:', now.toLocaleTimeString());
  console.log('Available prayer times:', prayers);
  
  // Convert prayer times to Date objects for today
  const prayerDateObjects = [];
  
  for (const prayer of prayers) {
    if (!prayer.time) {
      console.warn(`Missing time for prayer: ${prayer.name}`);
      continue;
    }
    
    // Split the time string and parse as numbers, handling any format issues
    const timeParts = prayer.time.split(':');
    if (timeParts.length < 2) {
      console.warn(`Invalid time format for ${prayer.name}: ${prayer.time}`);
      continue;
    }
    
    let hours = parseInt(timeParts[0]);
    let minutes = parseInt(timeParts[1]);
    
    // Handle invalid parsing results
    if (isNaN(hours) || isNaN(minutes)) {
      console.warn(`Failed to parse time for ${prayer.name}: ${prayer.time}`);
      continue;
    }
    
    // Convert to 24-hour format for PM prayers
    // For PM prayers (Dhuhr and Maghrib), if the hour is less than 12, add 12 hours
    if (prayer.isPM && hours < 12) {
      hours += 12;
      console.log(`Converted ${prayer.name} time to PM: ${hours}:${minutes}`);
    }
    
    // Create a date object for this prayer time today
    const prayerDate = new Date(now);
    prayerDate.setHours(hours, minutes, 0, 0);
    
    // Format for display
    const displayTime = formatPrayerTimeWithAMPM(prayer.time, prayer.isPM);
    
    prayerDateObjects.push({ 
      ...prayer, 
      date: prayerDate,
      timeString: displayTime,
      hours: hours,
      minutes: minutes
    });
    
    console.log(`Parsed ${prayer.name} time: ${hours}:${minutes} (${prayerDate.toLocaleTimeString()})`);
  }
  
  // Sort prayer times chronologically for today
  prayerDateObjects.sort((a, b) => a.date - b.date);
  
  console.log('Sorted prayer times for today:', prayerDateObjects.map(p => `${p.name}: ${p.timeString}`));
  
  // Current hour and minute for comparison
  const currentHour = now.getHours();
  const currentMinute = now.getMinutes();
  console.log(`Current time: ${currentHour}:${currentMinute}`);
  
  // Find the next prayer for today
  let nextPrayerObj = null;
  
  // Check if any prayers are remaining today
  for (const prayer of prayerDateObjects) {
    // Compare hours and minutes directly for more reliable comparison
    if (prayer.hours > currentHour || (prayer.hours === currentHour && prayer.minutes > currentMinute)) {
      nextPrayerObj = prayer;
      console.log('Next prayer found for today:', prayer.name, 'at', prayer.timeString);
      break;
    }
  }
  
  // If no prayers remaining today, use first prayer (Fajr) of tomorrow
  if (!nextPrayerObj && prayerDateObjects.length > 0) {
    console.log('No prayers remaining today, using Fajr for tomorrow');
    
    // Find the Fajr prayer
    const fajrPrayer = prayerDateObjects.find(p => p.name === 'fajr');
    
    if (fajrPrayer) {
      // Create a new date for tomorrow
      const tomorrowDate = new Date(now);
      tomorrowDate.setDate(tomorrowDate.getDate() + 1);
      
      // Set the hours and minutes from the Fajr prayer time
      tomorrowDate.setHours(fajrPrayer.hours, fajrPrayer.minutes, 0, 0);
      
      nextPrayerObj = { 
        ...fajrPrayer, 
        date: tomorrowDate
      };
      
      console.log('Tomorrow Fajr set for:', tomorrowDate.toLocaleString());
    } else {
      console.error('Could not find Fajr prayer for tomorrow');
    }
  }
  
  if (nextPrayerObj) {
    nextPrayer.value = nextPrayerObj;
    console.log('Next prayer set to:', nextPrayer.value.name);
    updateCountdown();
  } else {
    console.error('Failed to determine next prayer time');
  }
}

// Function to update the countdown timer
function updateCountdown() {
  if (!nextPrayer.value) return;
  
  const now = new Date();
  const prayerTime = nextPrayer.value.date;
  
  // Calculate time difference in milliseconds
  const diff = prayerTime - now;
  
  if (diff <= 0) {
    // Time has passed, recalculate next prayer
    console.log('Prayer time has passed, recalculating next prayer');
    calculateNextPrayer();
    return;
  }
  
  // Convert to hours, minutes, seconds
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);
  
  // Format the countdown string
  countdownTime.value = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
}

// Start the countdown timer
function startCountdownTimer() {
  // Clear any existing interval
  if (countdownInterval.value) {
    clearInterval(countdownInterval.value);
  }
  
  // Calculate initial next prayer
  calculateNextPrayer();
  
  // Set up interval to update countdown every second
  countdownInterval.value = setInterval(() => {
    updateCountdown();
  }, 1000);
}

// Stop the countdown timer
function stopCountdownTimer() {
  if (countdownInterval.value) {
    clearInterval(countdownInterval.value);
    countdownInterval.value = null;
  }
}

// Function to fetch prayer times from the API
async function fetchPrayerTimes() {
  loadingPrayerTimes.value = true;
  prayerTimesError.value = null;
  
  try {
    console.log('Fetching prayer times with:', {
      timezone: timezone.value,
      longitude: longitude.value,
      latitude: latitude.value,
      locationName: locationName.value
    });
    
    const apiUrl = `https://hq.alkafeel.net/Api/init/init.php?v=jsonPrayerTimes&timezone=${timezone.value}&long=${longitude.value}&lati=${latitude.value}`;
    const response = await fetch(apiUrl, {
      cache: 'no-store' // Ensure no caching
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch prayer times: ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log('Prayer times API response:', data);
    
    // Clean up the prayer times data by trimming any whitespace
    if (data) {
      if (data.fajir) data.fajir = data.fajir.trim();
      if (data.doher) data.doher = data.doher.trim();
      if (data.maghrib) data.maghrib = data.maghrib.trim();
      if (data.sunrise) data.sunrise = data.sunrise.trim();
      if (data.sunset) data.sunset = data.sunset.trim();
      
      console.log('Cleaned prayer times:', {
        fajr: data.fajir,
        dhuhr: data.doher,
        maghrib: data.maghrib,
        sunrise: data.sunrise,
        sunset: data.sunset
      });
    }
    
    // Update the reactive variable
    prayerTimes.value = data;
    
    // Stop any existing countdown timer
    stopCountdownTimer();
    
    // Calculate next prayer and start countdown
    startCountdownTimer();
    
    // Fetch Hijri date after prayer times are loaded
    await fetchHijriDate();
    
    // Save settings to localStorage
    localStorage.setItem('prayer_timezone', timezone.value);
    localStorage.setItem('prayer_longitude', longitude.value);
    localStorage.setItem('prayer_latitude', latitude.value);
    localStorage.setItem('prayer_location_name', locationName.value);
    
    // Hide the settings panel
    showLocationSettings.value = false;
  } catch (error) {
    console.error('Error fetching prayer times:', error);
    prayerTimesError.value = error.message;
    
    // Clear any existing timer if there's an error
    stopCountdownTimer();
  } finally {
    loadingPrayerTimes.value = false;
  }
}

// Function to update prayer times location
function updatePrayerTimesLocation() {
  fetchPrayerTimes();
}

// Clean up the interval when component is unmounted
watch(() => prayerTimes.value, (newValue) => {
  if (newValue) {
    // Start countdown timer when prayer times are loaded
    startCountdownTimer();
  } else {
    // Stop countdown timer when prayer times are cleared
    stopCountdownTimer();
  }
});

// Function to fetch Hijri date from Islamic Developers API
async function fetchHijriDate() {
  if (!latitude.value || !longitude.value) return;
  
  loadingHijriDate.value = true;
  
  try {
    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth() + 1; // JavaScript months are 0-indexed
    const day = today.getDate();
    
    const apiUrl = `https://api.islamicdevelopers.com/v1/calendar?calendar=gregorian&year=${year}&month=${month}&day=${day}&method=MuslimWorldLeague&latitude=${latitude.value}&longitude=${longitude.value}`;
    
    console.log('Fetching Hijri date with:', { year, month, day, latitude: latitude.value, longitude: longitude.value });
    
    // First try direct fetch with no-cors mode
    try {
      console.log('Trying direct fetch with no-cors mode');
      const directResponse = await fetch(apiUrl, { 
        method: 'GET',
        mode: 'no-cors', // This will give an opaque response that can't be read
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Accept': 'application/json'
        }
      });
      
      // If we get here, the request didn't throw, but we can't read the response
      // due to CORS. We'll continue with the proxies.
      console.log('Direct fetch completed but response is opaque due to CORS');
    } catch (directError) {
      console.warn('Direct fetch failed:', directError);
    }
    
    // Try different CORS proxies in sequence
    const corsProxies = [
      `https://api.allorigins.win/get?url=${encodeURIComponent(apiUrl)}`,
      `https://corsproxy.io/?${encodeURIComponent(apiUrl)}`,
      `https://cors-anywhere.herokuapp.com/${apiUrl}`
    ];
    
    let proxySuccess = false;
    
    // Try each proxy in sequence
    for (const proxyUrl of corsProxies) {
      if (proxySuccess) break;
      
      try {
        console.log(`Trying CORS proxy: ${proxyUrl}`);
        const response = await fetch(proxyUrl, { 
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error(`Failed to fetch Hijri date: ${response.statusText}`);
        }
        
        let data;
        
        // Handle different proxy response formats
        if (proxyUrl.includes('allorigins')) {
          // allorigins wraps the response in a 'contents' property
          const proxyResponse = await response.json();
          data = JSON.parse(proxyResponse.contents);
        } else {
          data = await response.json();
        }
        
        console.log('Hijri date API response:', data);
        
        if (data && data.length > 0 && data[0].calendar && data[0].calendar.hijri) {
          hijriDate.value = data[0].calendar.hijri;
          proxySuccess = true;
          console.log('Successfully fetched Hijri date using proxy');
          break; // Success, exit the loop
        } else {
          console.error('Invalid Hijri date data format');
          throw new Error('Invalid data format');
        }
      } catch (proxyError) {
        console.warn(`CORS proxy attempt failed for ${proxyUrl}:`, proxyError);
        // Continue to next proxy
      }
    }
    
    // If all proxies failed, try Aladhan API as a fallback
    if (!proxySuccess) {
      console.warn('All CORS proxies failed, trying Aladhan API as fallback');
      
      try {
        // Aladhan API is known to have CORS headers enabled
        const aladhanUrl = `https://api.aladhan.com/v1/gToH?date=${day}-${month}-${year}`;
        console.log(`Trying Aladhan API: ${aladhanUrl}`);
        
        const aladhanResponse = await fetch(aladhanUrl);
        
        if (!aladhanResponse.ok) {
          throw new Error(`Failed to fetch from Aladhan API: ${aladhanResponse.statusText}`);
        }
        
        const aladhanData = await aladhanResponse.json();
        console.log('Aladhan API response:', aladhanData);
        
        if (aladhanData && aladhanData.code === 200 && aladhanData.data && aladhanData.data.hijri) {
          // Convert Aladhan API format to match Islamic Developers API format
          const aladhanHijri = aladhanData.data.hijri;
          
          hijriDate.value = {
            day: aladhanHijri.day,
            month: {
              number: parseInt(aladhanHijri.month.number),
              en: aladhanHijri.month.en,
              ar: aladhanHijri.month.ar
            },
            year: aladhanHijri.year,
            weekday: {
              en: aladhanHijri.weekday.en,
              ar: aladhanHijri.weekday.ar
            },
            designation: aladhanHijri.designation
          };
          
          console.log('Successfully fetched Hijri date using Aladhan API');
          return;
        } else {
          console.error('Invalid Aladhan API data format');
          throw new Error('Invalid Aladhan data format');
        }
      } catch (aladhanError) {
        console.warn('Aladhan API attempt failed:', aladhanError);
        // Continue to client-side calculation
      }
      
      // Final fallback: Client-side calculation
      console.warn('All API methods failed, using client-side calculation');
      
      // Method 3: Fallback to using a client-side Hijri date calculation
      // This uses the browser's built-in date and converts it to Hijri
      try {
        // Create a new date object for today
        const date = new Date();
        
        // Use Intl.DateTimeFormat with 'islamic' calendar if supported
        if (typeof Intl !== 'undefined' && Intl.DateTimeFormat) {
          try {
            const formatter = new Intl.DateTimeFormat('ar-SA-u-ca-islamic', {
              day: 'numeric',
              month: 'long',
              year: 'numeric',
              weekday: 'long'
            });
            
            const parts = formatter.formatToParts(date);
            const hijriParts = {};
            
            parts.forEach(part => {
              if (part.type !== 'literal') {
                hijriParts[part.type] = part.value;
              }
            });
            
            // Create a simplified hijri date object that matches the API structure
            hijriDate.value = {
              day: hijriParts.day || day.toString(),
              month: {
                number: date.getMonth() + 1,
                en: hijriParts.month || '',
                ar: hijriParts.month || ''
              },
              year: hijriParts.year || year.toString(),
              weekday: {
                en: hijriParts.weekday || '',
                ar: hijriParts.weekday || ''
              },
              designation: {
                abbreviated: 'AH',
                expanded: 'Anno Hegirae'
              }
            };
            
            console.log('Generated Hijri date using Intl API:', hijriDate.value);
            return;
          } catch (intlError) {
            console.warn('Intl.DateTimeFormat with islamic calendar failed:', intlError);
          }
        }
        
        // If Intl API fails, use a simple approximation
        // This is a very basic approximation - not accurate for all dates
        // Hijri year is approximately 33/32 years less than Gregorian
        const approximateHijriYear = Math.floor(year - (year / 32.5));
        const approximateHijriMonth = month; // Simple approximation
        const approximateHijriDay = day;     // Simple approximation
        
        // Create a simplified hijri date object
        hijriDate.value = {
          day: approximateHijriDay.toString(),
          month: {
            number: approximateHijriMonth,
            en: getHijriMonthName(approximateHijriMonth, 'en'),
            ar: getHijriMonthName(approximateHijriMonth, 'ar')
          },
          year: approximateHijriYear.toString(),
          weekday: {
            en: date.toLocaleDateString('en', { weekday: 'long' }),
            ar: date.toLocaleDateString('ar', { weekday: 'long' })
          },
          designation: {
            abbreviated: 'AH',
            expanded: 'Anno Hegirae'
          }
        };
        
        console.log('Generated approximate Hijri date:', hijriDate.value);
      } catch (fallbackError) {
        console.error('All Hijri date methods failed:', fallbackError);
        hijriDate.value = null;
      }
    }
  } catch (error) {
    console.error('Error fetching Hijri date:', error);
    hijriDate.value = null;
  } finally {
    loadingHijriDate.value = false;
  }
}

// Helper function to get Hijri month names
function getHijriMonthName(month, language) {
  const monthNames = {
    en: [
      'Muharram', 'Safar', 'Rabi al-Awwal', 'Rabi al-Thani',
      'Jumada al-Awwal', 'Jumada al-Thani', 'Rajab', 'Shaban',
      'Ramadan', 'Shawwal', 'Dhu al-Qadah', 'Dhu al-Hijjah'
    ],
    ar: [
      'محرم', 'صفر', 'ربيع الأول', 'ربيع الثاني',
      'جمادى الأولى', 'جمادى الآخرة', 'رجب', 'شعبان',
      'رمضان', 'شوال', 'ذو القعدة', 'ذو الحجة'
    ],
    fa: [
      'محرم', 'صفر', 'ربیع‌الاول', 'ربیع‌الثانی',
      'جمادی‌الاول', 'جمادی‌الثانی', 'رجب', 'شعبان',
      'رمضان', 'شوال', 'ذی‌القعده', 'ذی‌الحجه'
    ],
    ku: [
      'موحەڕەم', 'سەفەر', 'ڕەبیعولئەوەڵ', 'ڕەبیعولئاخیر',
      'جومادیلئەوەڵ', 'جومادیلئاخیر', 'ڕەجەب', 'شەعبان',
      'ڕەمەزان', 'شەوال', 'زولقەعدە', 'زولحەججە'
    ]
  };
  
  // Default to English if the requested language is not available
  const availableLanguage = monthNames[language] ? language : 'en';
  
  // Ensure month is between 1-12 and convert to 0-11 for array index
  const index = ((month - 1) % 12 + 12) % 12;
  return monthNames[availableLanguage][index];
}

// Format Hijri date for display
function formatHijriDate() {
  if (!hijriDate.value) return '';
  
  const { locale } = useI18n();
  
  const hijri = hijriDate.value;
  console.log('Formatting Hijri date:', hijri); // Debug log
  
  // Check the structure of the hijriDate object
  // Some APIs return different structures
  let day, month, year, monthName;
  
  // Apply Shia adjustment if needed (typically 1 day earlier)
  const dayAdjustment = isShiaCalendar.value ? -1 : 0;
  
  try {
    // Handle different API response structures
    if (hijri.numeric && hijri.numeric.day) {
      // Format from Islamic Developers API
      day = parseInt(hijri.numeric.day) + dayAdjustment;
      month = parseInt(hijri.numeric.month);
      year = parseInt(hijri.numeric.year);
      
      // Get month name based on current locale
      if (hijri.names && hijri.names.month && hijri.names.month.arabic) {
        if (locale.value === 'ar') {
          monthName = hijri.names.month.arabic.native;
        } else if (locale.value === 'fa') {
          // For Persian, we'll use the Arabic name as a fallback
          monthName = hijri.names.month.arabic.latin;
        } else if (locale.value === 'ku') {
          // For Kurdish, we'll use the Arabic name as a fallback
          monthName = hijri.names.month.arabic.latin;
        } else {
          // Default to Latin transliteration for English and other languages
          monthName = hijri.names.month.arabic.latin;
        }
      } else {
        // If names are not available, use our helper function
        monthName = getHijriMonthName(month, locale.value);
      }
    } else if (hijri.day) {
      // Format from Aladhan API or client-side calculation
      day = parseInt(hijri.day) + dayAdjustment;
      
      // Check if month is an object with a number property or just a number
      if (typeof hijri.month === 'object' && hijri.month !== null) {
        month = hijri.month.number ? parseInt(hijri.month.number) : 1;
        
        // Use the month name from the API if available, otherwise use our helper function
        if (locale.value === 'ar' && hijri.month.ar) {
          monthName = hijri.month.ar;
        } else if (hijri.month.en) {
          monthName = hijri.month.en;
        } else {
          monthName = getHijriMonthName(month, locale.value);
        }
      } else if (typeof hijri.month === 'number') {
        month = hijri.month;
        monthName = getHijriMonthName(month, locale.value);
      } else {
        // Default to month 1 if we can't determine it
        month = 1;
        monthName = getHijriMonthName(1, locale.value);
      }
      
      year = hijri.year ? parseInt(hijri.year) : new Date().getFullYear() - 579; // Approximate Hijri year
    } else {
      // Fallback to a simple format if structure is unknown
      console.warn('Unknown hijriDate structure:', hijri);
      return 'Unknown Hijri date format';
    }
    
    // Handle month boundary cases
    if (day < 1) {
      // Move to previous month
      month--;
      if (month < 1) {
        month = 12;
        year--;
      }
      // Get days in previous month (approximation)
      const daysInPrevMonth = month === 8 || month === 10 || month === 12 ? 30 : 29;
      day = daysInPrevMonth + day;
      
      // Use our helper function for month name since we've changed the month
      monthName = getHijriMonthName(month, locale.value);
    }
    
    return `${day} ${monthName} ${year}`;
  } catch (error) {
    console.error('Error formatting Hijri date:', error, hijri);
    return 'Error formatting date';
  }
}

// Get Hijri weekday name
function getHijriWeekday() {
  if (!hijriDate.value) return '';
  
  const { locale } = useI18n();
  
  // Check if weekday property exists
  if (!hijriDate.value.weekday) {
    // Fallback to current day of week
    const today = new Date();
    const weekdays = {
      en: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      ar: ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
    };
    
    const dayIndex = today.getDay(); // 0-6, starting with Sunday
    return weekdays[locale.value === 'ar' ? 'ar' : 'en'][dayIndex];
  }
  
  // For Shia calendar, adjust the weekday if needed
  if (isShiaCalendar.value && hijriDate.value.weekday.en) {
    // Get current weekday index (0-6)
    const weekdayIndex = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
      .indexOf(hijriDate.value.weekday.en);
    
    if (weekdayIndex !== -1) {
      // Move one day earlier
      const newIndex = (weekdayIndex - 1 + 7) % 7;
      const weekdays = {
        en: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        ar: ['الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
      };
      
      return weekdays[locale.value === 'ar' ? 'ar' : 'en'][newIndex];
    }
  }
  
  // Check if the requested locale exists in weekday
  const localeKey = locale.value === 'ar' ? 'ar' : 'en';
  if (hijriDate.value.weekday[localeKey]) {
    return hijriDate.value.weekday[localeKey];
  }
  
  // Fallback to any available locale
  if (hijriDate.value.weekday.en) {
    return hijriDate.value.weekday.en;
  } else if (hijriDate.value.weekday.ar) {
    return hijriDate.value.weekday.ar;
  }
  
  // Last resort fallback
  return '';
}

// Check if it's a Hijri leap year
function isHijriLeapYear() {
  if (!hijriDate.value) return false;
  
  const hijri = hijriDate.value;
  
  // If the API directly provides the leap year information, use it
  if (typeof hijri.leapYear === 'boolean') {
    return hijri.leapYear;
  }
  
  // Get the Hijri year
  let year;
  if (hijri.numeric && hijri.numeric.year) {
    year = parseInt(hijri.numeric.year);
  } else if (hijri.year) {
    year = parseInt(hijri.year);
  } else {
    // If we can't determine the year, return false
    return false;
  }
  
  // Calculate if it's a leap year
  // In the Hijri calendar, leap years follow a 30-year cycle
  // Years 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, and 29 in the 30-year cycle are leap years
  const leapYears = [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29];
  const cycleYear = year % 30;
  
  return leapYears.includes(cycleYear === 0 ? 30 : cycleYear);
}

// Helper function to get Hijri month number safely
function getHijriMonthNumber() {
  if (!hijriDate.value) return '';
  
  const hijri = hijriDate.value;
  
  if (hijri.numeric && hijri.numeric.month) {
    return parseInt(hijri.numeric.month);
  } else if (typeof hijri.month === 'object' && hijri.month !== null && hijri.month.number) {
    return parseInt(hijri.month.number);
  } else if (typeof hijri.month === 'number') {
    return hijri.month;
  }
  
  // Default to current month if we can't determine it
  return new Date().getMonth() + 1;
}

// Helper function to get Hijri year safely
function getHijriYear() {
  if (!hijriDate.value) return '';
  
  const hijri = hijriDate.value;
  
  if (hijri.numeric && hijri.numeric.year) {
    return hijri.numeric.year;
  } else if (hijri.year) {
    return hijri.year;
  }
  
  // Default to approximate Hijri year if we can't determine it
  return (new Date().getFullYear() - 579).toString();
}

// Function to format prayer time
function formatPrayerTime(timeString) {
  if (!timeString) return '';
  
  // Trim any whitespace
  const trimmed = timeString.trim();
  
  // Split by colon
  const parts = trimmed.split(':');
  if (parts.length < 2) return trimmed;
  
  // Format as HH:MM
  const hours = parseInt(parts[0]);
  const minutes = parseInt(parts[1]);
  
  if (isNaN(hours) || isNaN(minutes)) return trimmed;
  
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}

// Function to format prayer time with AM/PM for display
function formatPrayerTimeWithAMPM(timeString, isPM = false) {
  if (!timeString) return '';
  
  // Trim any whitespace
  const trimmed = timeString.trim();
  
  // Split by colon
  const parts = trimmed.split(':');
  if (parts.length < 2) return trimmed;
  
  // Parse hours and minutes
  let hours = parseInt(parts[0]);
  let minutes = parseInt(parts[1]);
  
  if (isNaN(hours) || isNaN(minutes)) return trimmed;
  
  // Determine if it's AM or PM
  let period = 'AM';
  let displayHours = hours;
  
  // For prayers that are typically in the afternoon/evening (Dhuhr, Asr, Maghrib, Isha)
  if (isPM) {
    // If hours is less than 12, it's PM (e.g., 6:26 PM)
    if (hours < 12) {
      period = 'PM';
    } 
    // If hours is 12, it's noon (12:00 PM)
    else if (hours === 12) {
      period = 'PM';
    } 
    // If hours is greater than 12, it's PM but display as 1-12
    else {
      period = 'PM';
      displayHours = hours - 12;
    }
  } else {
    // For morning prayers (Fajr, Sunrise)
    // If hours is 12, it's midnight (12:00 AM)
    if (hours === 12) {
      period = 'AM';
      displayHours = 12;
    } 
    // If hours is greater than 12, it's PM
    else if (hours > 12) {
      period = 'PM';
      displayHours = hours - 12;
    }
    // Otherwise it's AM (e.g., 4:48 AM)
  }
  
  // Format the time with AM/PM
  return `${displayHours}:${minutes.toString().padStart(2, '0')} ${period}`;
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-b from-emerald-50 to-white">
    <header class="bg-gradient-to-r from-emerald-600 to-teal-500 text-white shadow-md">
      <div class="container mx-auto px-4 py-8">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold tracking-tight">{{ t('app.title') }}</h1>
            <p class="mt-2 text-emerald-100 font-light">{{ t('app.subtitle') }}</p>
          </div>
          <div class="flex items-center space-x-4">
            <LanguageSwitcher />
            <div class="hidden md:block">
              <img src="./assets/7sanah_logo.png" alt="7sanah Logo" class="h-16 w-auto" />
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="container mx-auto px-4 py-8 max-w-6xl">
      <!-- Error Alert -->
      <transition name="slide-down">
        <div v-if="store.error" 
             class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-md mb-6 flex items-start">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          <span>{{ store.error }}</span>
        </div>
      </transition>

      <!-- Loading Indicator -->
      <transition name="fade">
        <div v-if="store.loading" class="flex justify-center my-12">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-500"></div>
        </div>
      </transition>

      <!-- Main Content -->
      <transition :name="transitionName" mode="out-in">
        <!-- Home Page with Grid Layout -->
        <div v-if="currentView === 'list'" key="home-page" class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <!-- Left Column - Prayer Times -->
          <div class="lg:col-span-6">
            <!-- Prayer Times Component -->
            <div class="bg-white rounded-xl shadow-sm p-6 mb-8 h-full">
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-xl font-semibold text-emerald-700 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
                  </svg>
                  {{ t('prayerTimes.title') || 'أوقات الصلاة' }}
                </h2>
                
                <div class="flex items-center">
                  <span class="text-sm text-gray-600 mr-2">{{ locationName }}</span>
                  <button 
                    @click="showLocationSettings = !showLocationSettings"
                    class="text-emerald-600 hover:text-emerald-700 focus:outline-none"
                    title="Change Location"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
              
              <!-- Location Settings Panel -->
              <div v-if="showLocationSettings" class="bg-gray-50 p-4 rounded-lg mb-6">
                <h3 class="text-lg font-medium text-gray-900 mb-3">{{ t('prayerTimes.locationSettings') || 'إعدادات الموقع' }}</h3>
                
                <div class="flex flex-wrap gap-2 mb-4">
                  <button 
                    @click="detectUserLocation" 
                    class="inline-flex items-center px-3 py-1.5 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors"
                    :disabled="detectingLocation"
                    :class="{ 'opacity-50 cursor-not-allowed': detectingLocation }"
                  >
                    <svg v-if="!detectingLocation" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="animate-spin h-4 w-4 mr-1" viewBox="0 0 24 24" fill="none">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span v-if="!detectingLocation">{{ t('prayerTimes.detectLocation') || 'اكتشاف موقعك' }}</span>
                    <span v-else>{{ t('prayerTimes.detecting') || 'جاري الكشف...' }}</span>
                  </button>
                  
                  <button 
                    @click="showCityPresets = !showCityPresets" 
                    class="inline-flex items-center px-3 py-1.5 bg-emerald-100 text-emerald-700 rounded-md hover:bg-emerald-200 transition-colors"
                    :disabled="detectingLocation"
                    :class="{ 'opacity-50 cursor-not-allowed': detectingLocation }"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" />
                    </svg>
                    {{ t('prayerTimes.selectFromPresets') || 'اختر من المدن المعروفة' }}
                  </button>
                </div>
                
                <!-- Display error message if there is one -->
                <div v-if="prayerTimesError" class="mb-4 bg-red-50 text-red-700 p-3 rounded-md">
                  <p class="text-sm">{{ prayerTimesError }}</p>
                </div>
                
                <!-- City Presets -->
                <div v-if="showCityPresets" class="mb-4 bg-white p-3 rounded-md border border-gray-200">
                  <div class="mb-3">
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('prayerTimes.selectCountry') || 'اختر الدولة' }}</label>
                    <select 
                      v-model="selectedCountry" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
                    >
                      <option value="">{{ t('prayerTimes.selectCountryPrompt') || 'اختر الدولة' }}</option>
                      <option v-for="country in countries" :key="country" :value="country">{{ country }}</option>
                    </select>
                  </div>
                  
                  <div v-if="selectedCountry" class="grid grid-cols-2 sm:grid-cols-3 gap-2">
                    <button 
                      v-for="city in citiesForSelectedCountry" 
                      :key="city.name"
                      @click="selectCity(city)"
                      class="px-3 py-2 bg-gray-100 text-gray-800 rounded-md hover:bg-gray-200 transition-colors text-sm"
                    >
                      {{ city.name }}
                    </button>
                  </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('prayerTimes.locationName') || 'اسم الموقع' }}</label>
                    <input 
                      v-model="locationName" 
                      type="text" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
                    />
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('prayerTimes.timezone') || 'المنطقة الزمنية' }}</label>
                    <input 
                      v-model="timezone" 
                      type="text" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
                      placeholder="+3"
                    />
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('prayerTimes.longitude') || 'خط الطول' }}</label>
                    <input 
                      v-model="longitude" 
                      type="text" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
                      placeholder="44.0228"
                    />
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('prayerTimes.latitude') || 'خط العرض' }}</label>
                    <input 
                      v-model="latitude" 
                      type="text" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500"
                      placeholder="32.6143"
                    />
                  </div>
                </div>
                
                <div class="flex justify-end space-x-3">
                  <button 
                    @click="showLocationSettings = false"
                    class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
                  >
                    {{ t('common.cancel') || 'إلغاء' }}
                  </button>
                  <button 
                    @click="updatePrayerTimesLocation"
                    class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
                  >
                    {{ t('common.save') || 'حفظ' }}
                  </button>
                </div>
              </div>
              
              <!-- Prayer Times Display -->
              <div class="prayer-times-container">
                <!-- Loading state -->
                <div v-if="loadingPrayerTimes || detectingLocation" class="flex flex-col items-center justify-center py-8">
                  <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-500 mb-3"></div>
                  <p v-if="detectingLocation" class="text-sm text-gray-600">{{ t('prayerTimes.detectingLocation') || 'جاري تحديد موقعك...' }}</p>
                  <p v-else class="text-sm text-gray-600">{{ t('prayerTimes.loading') || 'جاري تحميل أوقات الصلاة...' }}</p>
                </div>
                
                <!-- Error state -->
                <div v-else-if="prayerTimesError" class="bg-red-50 text-red-700 p-4 rounded-lg">
                  <p>{{ prayerTimesError }}</p>
                  <button 
                    @click="fetchPrayerTimes" 
                    class="mt-2 px-3 py-1 bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors"
                  >
                    Retry
                  </button>
                </div>
                
                <!-- Prayer times data -->
                <div v-else-if="prayerTimes" class="text-center">
                 
                  
                  <!-- Next Prayer Countdown -->
                  <div v-if="nextPrayer" class="mb-6 bg-indigo-50 rounded-lg p-4 max-w-md mx-auto shadow-sm">
                    <div class="text-indigo-800 font-medium mb-1">{{ t('prayerTimes.nextPrayer') || 'Next Prayer' }}: {{ t(nextPrayer.translationKey) || nextPrayer.name }}</div>
                    <div class="text-3xl font-bold text-indigo-700 font-mono">{{ countdownTime }}</div>
                  </div>
                  
                  <div class="flex flex-col space-y-4">
                    <!-- Fajr -->
                    <div class="bg-emerald-50 rounded-lg p-4 flex justify-between items-center" 
                         :class="{ 'ring-2 ring-emerald-500 shadow-md': nextPrayer && nextPrayer.name === 'fajr' }">
                      <div class="text-emerald-800 font-medium">{{ t('prayerTimes.fajr') || 'الفجر' }}</div>
                      <div class="text-xl font-bold text-emerald-700">{{ formatPrayerTimeWithAMPM(prayerTimes.fajir, false) }}</div>
                    </div>
                    
                    <!-- Sunrise -->
                    <div class="bg-amber-50 rounded-lg p-4 flex justify-between items-center">
                      <div class="text-amber-800 font-medium">{{ t('prayerTimes.sunrise') || 'الشروق' }}</div>
                      <div class="text-xl font-bold text-amber-600">{{ formatPrayerTimeWithAMPM(prayerTimes.sunrise, false) }}</div>
                    </div>
                    
                    <!-- Dhuhr -->
                    <div class="bg-blue-50 rounded-lg p-4 flex justify-between items-center"
                         :class="{ 'ring-2 ring-blue-500 shadow-md': nextPrayer && nextPrayer.name === 'dhuhr' }">
                      <div class="text-blue-800 font-medium">{{ t('prayerTimes.dhuhr') || 'الظهر' }}</div>
                      <div class="text-xl font-bold text-blue-600">{{ formatPrayerTimeWithAMPM(prayerTimes.doher, true) }}</div>
                    </div>
                    
                    <!-- Sunset -->
                    <div class="bg-orange-50 rounded-lg p-4 flex justify-between items-center">
                      <div class="text-orange-800 font-medium">{{ t('prayerTimes.sunset') || 'الغروب' }}</div>
                      <div class="text-xl font-bold text-orange-600">{{ formatPrayerTimeWithAMPM(prayerTimes.sunset, true) }}</div>
                    </div>
                    
                    <!-- Maghrib -->
                    <div class="bg-purple-50 rounded-lg p-4 flex justify-between items-center"
                         :class="{ 'ring-2 ring-purple-500 shadow-md': nextPrayer && nextPrayer.name === 'maghrib' }">
                      <div class="text-purple-800 font-medium">{{ t('prayerTimes.maghrib') || 'المغرب' }}</div>
                      <div class="text-xl font-bold text-purple-600">{{ formatPrayerTimeWithAMPM(prayerTimes.maghrib, true) }}</div>
                    </div>
                  </div>
                </div>
                
                <!-- No data state -->
                <div v-else class="text-center py-8 text-gray-500">
                  {{ t('prayerTimes.noData') || 'لا توجد بيانات متاحة' }}
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column - Khatmah Management -->
          <div class="lg:col-span-6">
            <!-- Khatmah Management Card -->
            <div class="bg-white rounded-xl shadow-sm p-6 mb-8 h-full">
              <!-- Card Header with Title and Add Button -->
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-xl font-semibold text-emerald-700 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                  </svg>
                  {{ t('khatmahList.management') || 'إدارة الختمات' }}
                </h2>
                
                <!-- Add New Khatmah Button -->
                <div class="flex" :class="{ 'justify-start': locale === 'ar', 'justify-end': locale !== 'ar' }">
                  <button 
                    @click="showCreateKhatmah" 
                    class="flex items-center px-4 py-2 bg-emerald-600 rounded-md shadow-sm text-sm font-medium text-white hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
                    </svg>
                    {{ t('navigation.createNew') }}
                  </button>
                </div>
              </div>

              <!-- Khatmah List View -->
              <KhatmahList 
                :khatmahs="store.khatmahs"
                @select-khatmah="showKhatmahDetail" />
            </div>
          </div>
          
          <!-- Full Width Calendar Row -->
          <div class="lg:col-span-12">
            <!-- Hijri Calendar Component -->
            <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
              <HijriCalendar />
            </div>
            
            <!-- Qibla Compass Component -->
            <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
              <h2 class="text-xl font-semibold text-emerald-700 flex items-center mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                </svg>
                {{ t('compass.title') || 'Compass' }}
              </h2>
              <QiblaCompass />
            </div>
          </div>
        </div>

        <!-- Khatmah Detail Page (Full Page) -->
        <div v-else-if="currentView === 'detail'" key="detail-page" class="bg-white rounded-xl shadow-sm p-6 mb-8">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-semibold text-emerald-700 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
              </svg>
              {{ t('khatmahDetail.title') || 'تفاصيل الختمة' }}
            </h2>
            
            <!-- Back Button -->
            <button 
              @click="goToList" 
              class="flex items-center px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
              </svg>
              {{ t('navigation.backToList') }}
            </button>
          </div>
          
          <KhatmahDetail 
            :khatmah-id="selectedKhatmahId"
            @edit-khatmah="showEditKhatmah"
            @select-khatmah="showKhatmahDetail"
            @khatmah-created="showKhatmahDetail"
            @khatmah-updated="handleKhatmahUpdated"
            @cancel="goToList" />
        </div>
        
        <!-- Khatmah Edit Page (Full Page) -->
        <div v-else-if="currentView === 'edit'" key="edit-page" class="bg-white rounded-xl shadow-sm p-6 mb-8">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-semibold text-emerald-700 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
              {{ t('khatmahEdit.title') || 'تعديل الختمة' }}
            </h2>
            
            <!-- Back Button -->
            <button 
              @click="showKhatmahDetail(selectedKhatmahId)" 
              class="flex items-center px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
              </svg>
              {{ t('navigation.backToDetail') || 'العودة إلى التفاصيل' }}
            </button>
          </div>
          
          <EditKhatmah 
            :khatmah-id="selectedKhatmahId"
            @khatmah-updated="handleKhatmahUpdated"
            @cancel="showKhatmahDetail(selectedKhatmahId)" />
        </div>
        
        <!-- Create Khatmah Page (Full Page) -->
        <div v-else key="create-page" class="bg-white rounded-xl shadow-sm p-6 mb-8">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-semibold text-emerald-700 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
              {{ t('khatmahCreate.title') || 'إنشاء ختمة جديدة' }}
            </h2>
            
            <!-- Back Button -->
            <button 
              @click="goToList" 
              class="flex items-center px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
              </svg>
              {{ t('navigation.backToList') }}
            </button>
          </div>
          
          <CreateKhatmah 
            @khatmah-created="showKhatmahDetail" />
        </div>
      </transition>
    </main>

    <footer class="bg-gray-900 text-white py-8 mt-auto">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="mb-4 md:mb-0">
            <h3 class="text-xl font-semibold mb-2">{{ t('app.title') }}</h3>
            <p class="text-gray-400">{{ t('app.subtitle') }}</p>
          </div>
          <div class="flex items-center space-x-4">
            <img src="./assets/7sanah_logo.png" alt="7sanah Logo" class="h-10 w-auto mr-4" />
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <span class="sr-only">{{ t('footer.about') }}</span>
              <span>{{ t('footer.about') }}</span>
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <span class="sr-only">{{ t('footer.help') }}</span>
              <span>{{ t('footer.help') }}</span>
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <span class="sr-only">{{ t('footer.contact') }}</span>
              <span>{{ t('footer.contact') }}</span>
            </a>
          </div>
        </div>
        <div class="mt-8 pt-6 border-t border-gray-800 text-center text-gray-500 text-sm">
          <p>&copy; {{ new Date().getFullYear() }} {{ t('app.title') }}. {{ t('footer.rights') }}</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
/* Page Transition Animations */
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease-out;
}

/* Slide Left Animation (going forward) */
.slide-left-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-left-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Slide Right Animation (going back) */
.slide-right-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.slide-right-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* Fade Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Slide Down Animation */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease-out;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* RTL Support */
[dir="rtl"] .slide-left-enter-from {
  transform: translateX(-30px);
}

[dir="rtl"] .slide-left-leave-to {
  transform: translateX(30px);
}

[dir="rtl"] .slide-right-enter-from {
  transform: translateX(30px);
}

[dir="rtl"] .slide-right-leave-to {
  transform: translateX(-30px);
}

/* Prayer Times Component Styling */
.prayer-times-container {
  min-height: 200px;
}

/* RTL fixes for prayer times */
[dir="rtl"] .mr-2 {
  margin-right: 0;
  margin-left: 0.5rem;
}

[dir="rtl"] .flex.space-x-3 > * + * {
  margin-right: 0.75rem;
  margin-left: 0;
}

[dir="rtl"] .flex.space-x-3 {
  margin-left: 0;
}

/* Countdown timer styles */
.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

/* Hijri Calendar styles */
.font-arabic {
  font-family: "Traditional Arabic", "Scheherazade New", "Amiri", serif;
}
</style>
