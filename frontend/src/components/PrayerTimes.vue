<template>
  <div class="prayer-times-container">
    <div class="location-selector">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          :placeholder="$t('prayerTimes.searchCity')"
          @input="searchCities"
          @click="showAllCities"
          @focus="showAllCities"
        />
        <div class="dropdown-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </div>
        <div v-if="showDropdown" class="search-results">
          <div 
            v-for="city in searchResults" 
            :key="city.name"
            class="city-item"
            @click="selectCity(city)"
          >
            <span class="city-name">{{ city.name }}</span>
            <span class="city-arabic-name">{{ city.arabicName }}</span>
          </div>
        </div>
      </div>
      <div class="location-actions">
        <button @click="getCurrentLocation" class="location-btn" :disabled="isLoadingLocation">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
          </svg>
          {{ isLoadingLocation ? $t('prayerTimes.gettingLocation') : $t('prayerTimes.useCurrentLocation') }}
        </button>
        <button @click="showMapSelector = true" class="map-btn">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="20" height="20">
            <path fill-rule="evenodd" d="M12 1.586l-4 4v12.828l4-4V1.586zM3.707 3.293A1 1 0 002 4v10a1 1 0 00.293.707L6 18.414V5.586L3.707 3.293zM17.707 5.293L14 1.586v12.828l2.293 2.293A1 1 0 0018 16V6a1 1 0 00-.293-.707z" clip-rule="evenodd" />
          </svg>
          {{ $t('prayerTimes.selectFromMap') }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoadingLocation" class="loading-state">
      <div class="loading-spinner"></div>
      <p>{{ $t('prayerTimes.loadingLocation') }}</p>
    </div>

    <!-- Prayer Times Loading State -->
    <div v-else-if="isLoadingPrayerTimes" class="loading-state">
      <div class="loading-spinner"></div>
      <p>{{ $t('prayerTimes.loading') }}</p>
    </div>

    <!-- Location Error State -->
    <div v-else-if="locationError" class="error-state">
      <p>{{ $t('prayerTimes.locationError') }}</p>
    </div>

    <!-- Prayer Times Display -->
    <div v-else-if="prayerTimes" class="prayer-card">
      <div class="date-section">
        <div class="current-location-display" v-if="currentLocationName">
          <svg xmlns="http://www.w3.org/2000/svg" class="location-icon" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" />
          </svg>
          <span class="location-name">{{ currentLocationName }}</span>
        </div>
        <div class="gregorian-date">
          <div class="english-date">{{ $t('prayerTimes.date.gregorian') }}: {{ currentDate.english }}</div>
          <div class="arabic-date">{{ $t('prayerTimes.date.hijri') }}: {{ currentDate.arabic }}</div>
        </div>
      </div>

      <!-- Next Prayer Section -->
      <div class="next-prayer-section" v-if="nextPrayer">
        <div class="next-prayer-header">
          {{ $t('prayerTimes.nextPrayer') }}
        </div>
        <div class="next-prayer-name">
          <span class="arabic-prayer-name">{{ $t(`prayerTimes.prayers.${nextPrayer.name}`) }}</span>
          <span class="next-prayer-time" v-if="prayerTimes && nextPrayer.name">
            ({{ formatPrayerTime(
              nextPrayer.name === 'fajr' ? prayerTimes.fajir :
              nextPrayer.name === 'dhuhr' ? prayerTimes.doher :
              prayerTimes.maghrib, 
              nextPrayer.name) }})
          </span>
        </div>
        <div class="countdown-timer">{{ nextPrayer.countdown }}</div>
      </div>

      <!-- Main Prayer Times Grid -->
      <div class="main-prayers">
        <div class="prayer-item" :class="{ 'next-prayer': isNextPrayer('fajr') }">
          <div class="prayer-name">
            <span class="arabic-name">{{ $t('prayerTimes.prayers.fajr') }}</span>
          </div>
          <div class="prayer-time">{{ formatPrayerTime(prayerTimes?.fajir, 'fajr') }}</div>
        </div>

        <div class="sun-card sunrise">
          <div class="sun-info">
            <span class="sun-label">{{ $t('prayerTimes.prayers.sunrise') }}</span>
            <span class="sun-time">{{ formatPrayerTime(prayerTimes?.sunrise, 'sunrise') }}</span>
          </div>
        </div>

        <div class="prayer-item" :class="{ 'next-prayer': isNextPrayer('dhuhr') }">
          <div class="prayer-name">
            <span class="arabic-name">{{ $t('prayerTimes.prayers.dhuhr') }}</span>
          </div>
          <div class="prayer-time">{{ formatPrayerTime(prayerTimes?.doher, 'dhuhr') }}</div>
        </div>

        <div class="sun-card sunset">
          <div class="sun-info">
            <span class="sun-label">{{ $t('prayerTimes.prayers.sunset') }}</span>
            <span class="sun-time">{{ formatPrayerTime(prayerTimes?.sunset, 'sunset') }}</span>
          </div>
        </div>

        <div class="prayer-item" :class="{ 'next-prayer': isNextPrayer('maghrib') }">
          <div class="prayer-name">
            <span class="arabic-name">{{ $t('prayerTimes.prayers.maghrib') }}</span>
          </div>
          <div class="prayer-time">{{ formatPrayerTime(prayerTimes?.maghrib, 'maghrib') }}</div>
        </div>
      </div>
    </div>

    <!-- Map Selector Modal -->
    <div v-if="showMapSelector" class="map-modal">
      <div class="map-modal-content">
        <button class="close-btn" @click="showMapSelector = false">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="20" height="20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
        <h3>{{ $t('prayerTimes.mapSelector.title') }}</h3>
        <MapSelector @location-selected="handleLocationSelected" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, onUnmounted, nextTick, watch } from 'vue'
import MapSelector from './MapSelector.vue'

// Iraqi governorates with their coordinates
const iraqiCities = [
  { name: 'Baghdad', arabicName: 'بغداد', latitude: 33.3152, longitude: 44.3661, timezone: 3 },
  { name: 'Basra', arabicName: 'البصرة', latitude: 30.5085, longitude: 47.7804, timezone: 3 },
  { name: 'Mosul', arabicName: 'الموصل', latitude: 36.3350, longitude: 43.1189, timezone: 3 },
  { name: 'Erbil', arabicName: 'أربيل', latitude: 36.1901, longitude: 44.0091, timezone: 3 },
  { name: 'Najaf', arabicName: 'النجف', latitude: 32.0286, longitude: 44.3446, timezone: 3 },
  { name: 'Karbala', arabicName: 'كربلاء', latitude: 32.6167, longitude: 44.0333, timezone: 3 },
  { name: 'Sulaymaniyah', arabicName: 'السليمانية', latitude: 35.5556, longitude: 45.4350, timezone: 3 },
  { name: 'Kirkuk', arabicName: 'كركوك', latitude: 35.4681, longitude: 44.3922, timezone: 3 },
  { name: 'Duhok', arabicName: 'دهوك', latitude: 36.8669, longitude: 42.9509, timezone: 3 },
  { name: 'Al Hillah', arabicName: 'الحلة', latitude: 32.4721, longitude: 44.4217, timezone: 3 },
  { name: 'Diwaniyah', arabicName: 'الديوانية', latitude: 31.9889, longitude: 44.9247, timezone: 3 },
  { name: 'Ramadi', arabicName: 'الرمادي', latitude: 33.4258, longitude: 43.2992, timezone: 3 },
  { name: 'Nasiriyah', arabicName: 'الناصرية', latitude: 31.0531, longitude: 46.2567, timezone: 3 },
  { name: 'Amarah', arabicName: 'العمارة', latitude: 31.8350, longitude: 47.1440, timezone: 3 },
  { name: 'Fallujah', arabicName: 'الفلوجة', latitude: 33.3538, longitude: 43.7866, timezone: 3 },
  { name: 'Samawah', arabicName: 'السماوة', latitude: 31.3097, longitude: 45.2814, timezone: 3 },
  { name: 'Kut', arabicName: 'الكوت', latitude: 32.5130, longitude: 45.8185, timezone: 3 },
  { name: 'Baqubah', arabicName: 'بعقوبة', latitude: 33.7466, longitude: 44.6436, timezone: 3 },
  { name: 'Tikrit', arabicName: 'تكريت', latitude: 34.6071, longitude: 43.6782, timezone: 3 }
]

export default {
  name: 'PrayerTimes',
  components: {
    MapSelector
  },
  setup() {
    const prayerTimes = ref(null)
    const currentLocation = ref(null)
    const searchQuery = ref('')
    const searchResults = ref([])
    const nextPrayer = ref(null)
    const currentLocationName = ref('')
    const isLoadingLocation = ref(true)
    const locationError = ref(false)
    const showDropdown = ref(false)
    const showMapSelector = ref(false)
    const isLoadingPrayerTimes = ref(false)
    
    const currentDate = computed(() => {
      // Create date formatters for both languages
      const englishFormatter = new Intl.DateTimeFormat('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })

      const arabicFormatter = new Intl.DateTimeFormat('ar', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })

      const now = new Date()
      const englishDate = englishFormatter.format(now)
      const arabicDate = arabicFormatter.format(now)

      return {
        english: englishDate,
        arabic: arabicDate
      }
    })

    const fetchPrayerTimes = async () => {
      if (!currentLocation.value) return // Don't fetch if no location

      try {
        isLoadingPrayerTimes.value = true // Set loading state to true before fetching
        const response = await fetch(
          `https://hq.alkafeel.net/Api/init/init.php?v=jsonPrayerTimes&timezone=${currentLocation.value.timezone}&long=${currentLocation.value.longitude}&lati=${currentLocation.value.latitude}`
        )
        const data = await response.json()
        prayerTimes.value = data
        calculateNextPrayer()
        // Add a delay to ensure the DOM has updated with new values
        setTimeout(adjustTextSizes, 100);
      } catch (error) {
        console.error('Error fetching prayer times:', error)
        prayerTimes.value = null
      } finally {
        isLoadingPrayerTimes.value = false // Set loading state to false after fetching
      }
    }

    const handleLocationError = (error) => {
      console.error('Error getting location:', error)
      isLoadingLocation.value = false
      locationError.value = true
      currentLocation.value = null
      prayerTimes.value = null
    }

    const getCurrentLocation = () => {
      if (navigator.geolocation) {
        isLoadingLocation.value = true
        locationError.value = false
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            currentLocation.value = {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
              timezone: new Date().getTimezoneOffset() / -60
            }
            await getLocationName(position.coords.latitude, position.coords.longitude)
            await fetchPrayerTimes()
            isLoadingLocation.value = false
          },
          handleLocationError,
          { timeout: 10000 } // 10 second timeout
        )
      } else {
        handleLocationError(new Error('Geolocation not supported'))
      }
    }

    const getLocationName = async (lat, lon) => {
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&accept-language=en`
        )
        const data = await response.json()
        
        // Extract relevant location information
        const address = data.address
        let locationName = ''
        
        // For Iraq, show governorate in both English and Arabic
        if (address.country === 'Iraq' || address.country === 'العراق') {
          // Find the closest Iraqi city based on coordinates
          const closestCity = iraqiCities.reduce((closest, city) => {
            const distance = Math.sqrt(
              Math.pow(city.latitude - lat, 2) + 
              Math.pow(city.longitude - lon, 2)
            )
            return distance < closest.distance ? { city, distance } : closest
          }, { city: null, distance: Infinity }).city

          if (closestCity) {
            locationName = `${closestCity.name} (${closestCity.arabicName})`
          } else {
            locationName = `${address.state || address.city}, Iraq`
          }
        } else {
          // For other countries, show city and country
          locationName = `${address.city || address.town || address.village || address.state}, ${address.country}`
        }
        
        currentLocationName.value = locationName
      } catch (error) {
        console.error('Error getting location name:', error)
        currentLocationName.value = `${lat.toFixed(4)}, ${lon.toFixed(4)}`
      }
    }

    const searchCities = () => {
      // Filter cities based on search query
      searchResults.value = iraqiCities.filter(city => {
        const query = searchQuery.value.toLowerCase()
        return city.name.toLowerCase().includes(query) || 
               city.arabicName.includes(query)
      })
      showDropdown.value = true
    }

    const showAllCities = () => {
      searchResults.value = [...iraqiCities]
      showDropdown.value = true
    }

    const selectCity = (city) => {
      // Reset error and loading states
      locationError.value = false
      isLoadingLocation.value = false
      
      // Set the location
      currentLocation.value = {
        latitude: city.latitude,
        longitude: city.longitude,
        timezone: city.timezone
      }
      currentLocationName.value = `${city.name} (${city.arabicName})`
      searchQuery.value = city.name
      searchResults.value = []
      showDropdown.value = false
      
      // Fetch prayer times for selected city
      fetchPrayerTimes()
    }

    const calculateNextPrayer = () => {
      if (!prayerTimes.value) return

      const now = new Date()
      
      // Define prayer times with their expected time ranges
      const prayers = [
        { name: 'fajr', time: prayerTimes.value.fajir }, // Fajr is early morning (AM)
        { name: 'dhuhr', time: prayerTimes.value.doher }, // Dhuhr is around noon
        { name: 'maghrib', time: prayerTimes.value.maghrib } // Maghrib is evening (PM)
      ]

      // Convert prayer times to Date objects with correct 24-hour format
      const prayerDates = prayers.map(prayer => {
        const [hoursStr, minutesStr] = prayer.time.trim().split(':')
        let hours = parseInt(hoursStr, 10)
        const minutes = parseInt(minutesStr, 10)
        const date = new Date()
        
        // Apply time conversion rules based on prayer name and time patterns
        // Note: API returns times in 12-hour format without AM/PM indicators
        switch (prayer.name) {
          case 'fajr':
            // Fajr is before sunrise (AM)
            // 12 should be treated as 12 AM (0 in 24-hour)
            if (hours === 12) hours = 0
            break;
            
          case 'dhuhr':
            // Dhuhr is midday
            // If hours is 12, keep as 12 PM (noon)
            // If hours < 12, it's AM before noon (common in many regions)
            // Only convert to PM if specifically needed
            if (hours === 12) {
              // 12 PM (noon), no change needed
            } 
            // No else condition here as we keep hours < 12 in AM format
            break;
            
          case 'maghrib':
            // Maghrib is after sunset (PM)
            // If it's 12, keep it as 12 PM
            // Otherwise convert to PM unless already in 24-hour format
            if (hours !== 12 && hours < 12) {
              hours += 12
            }
            break;
        }
        
        // Set the time components on our date object
        date.setHours(hours, minutes, 0, 0)
        
        // If prayer time has passed for today, set it for tomorrow
        if (date < now) {
          date.setDate(date.getDate() + 1)
        }
        
        return { ...prayer, date }
      })

      // Sort by closest future time
      prayerDates.sort((a, b) => a.date - b.date)
      
      // The first prayer in the sorted array is the next one
      const next = prayerDates[0]
      
      if (next) {
        const timeDiff = next.date - now
        nextPrayer.value = {
          name: next.name,
          countdown: formatCountdown(timeDiff),
          date: next.date
        }
      }
    }

    const formatCountdown = (ms) => {
      const hours = Math.floor(ms / (1000 * 60 * 60))
      const minutes = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60))
      const seconds = Math.floor((ms % (1000 * 60)) / 1000)
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
    }

    // Update countdown every second instead of every minute
    let countdownInterval
    onMounted(() => {
      getCurrentLocation()
      // Start the countdown interval
      countdownInterval = setInterval(() => {
        if (nextPrayer.value?.date) {
          const now = new Date()
          const timeDiff = nextPrayer.value.date - now
          
          if (timeDiff <= 0) {
            // Prayer time has arrived - recalculate next prayer
            calculateNextPrayer()
            
            // If we have prayer times but failed to calculate next prayer,
            // try again in case there was a timing issue
            if (!nextPrayer.value && prayerTimes.value) {
              setTimeout(calculateNextPrayer, 1000)
            }
          } else {
            // Just update the countdown display
            nextPrayer.value = {
              ...nextPrayer.value,
              countdown: formatCountdown(timeDiff)
            }
          }
        } else if (prayerTimes.value) {
          // If we have prayer times but no next prayer, try to calculate it
          calculateNextPrayer()
        }
      }, 1000)
    })

    // Clean up interval on component unmount
    onUnmounted(() => {
      if (countdownInterval) {
        clearInterval(countdownInterval)
      }
    })

    const isNextPrayer = (prayerName) => {
      return nextPrayer.value?.name === prayerName
    }

    // Close dropdown when clicking outside
    const handleClickOutside = (event) => {
      const searchBox = document.querySelector('.search-box')
      if (searchBox && !searchBox.contains(event.target)) {
        showDropdown.value = false
      }
    }

    // Add a function to automatically adjust text size based on container width
    const adjustTextSizes = async () => {
      // Wait for DOM to update
      await nextTick();
      
      // Set standard font sizes
      const standardFontSize = {
        '.prayer-name .arabic-name': '1.5rem',
        '.sun-label': '1.5rem',
        '.prayer-time': '1.5rem', 
        '.sun-time': '1.5rem',
        '.next-prayer-name .arabic-prayer-name': '1.5rem',
        '.countdown-timer': '2.5rem'
      };
      
      // Reset all elements to standard sizes
      Object.entries(standardFontSize).forEach(([selector, size]) => {
        document.querySelectorAll(selector).forEach(el => {
          el.style.fontSize = size;
        });
      });
      
      // Wait for sizes to apply
      await nextTick();
    };

    // Multiple lifecycle hooks where we need to check/adjust text sizes
    onMounted(() => {
      // Existing mounted code
      getCurrentLocation();
      
      // Add event listener for clicking outside dropdown
      document.addEventListener('click', handleClickOutside);
      
      // Set up resize observer to adjust text on container resize
      const resizeObserver = new ResizeObserver(() => {
        setTimeout(adjustTextSizes, 100); // Small delay to let DOM update
      });
      
      // Adjust text size after component has fully rendered
      setTimeout(adjustTextSizes, 500); // Longer delay for initial render
      
      // Observe both card containers for size changes
      const containers = document.querySelectorAll('.prayer-card, .main-prayers, .prayer-item, .sun-card');
      containers.forEach(container => {
        if (container) {
          resizeObserver.observe(container);
        }
      });
      
      // Handle window resize
      const handleResize = () => {
        setTimeout(adjustTextSizes, 100);
      };
      
      // Also observe window resize
      window.addEventListener('resize', handleResize);
      
      // Clean up
      onUnmounted(() => {
        document.removeEventListener('click', handleClickOutside);
        window.removeEventListener('resize', handleResize);
        resizeObserver.disconnect();
      });
    });
    
    // Adjust text sizes whenever prayer times change
    const watchPrayerTimes = (val) => {
      if (val) {
        // Slight delay to let the DOM update
        setTimeout(adjustTextSizes, 100);
      }
    };
    
    // Add watcher for prayer times data
    watch(() => prayerTimes.value, watchPrayerTimes);

    const handleLocationSelected = (location) => {
      // Reset error and loading states
      locationError.value = false
      isLoadingLocation.value = false
      
      // Set the location
      currentLocation.value = {
        latitude: location.lat,
        longitude: location.lng,
        timezone: new Date().getTimezoneOffset() / -60
      }
      currentLocationName.value = location.name
      showMapSelector.value = false
      
      // Fetch prayer times for selected location
      fetchPrayerTimes()
    }

    const formatPrayerTime = (timeString, prayerName) => {
      if (!timeString) return '--:--'
      
      const [hoursStr, minutesStr] = timeString.trim().split(':')
      let hours = parseInt(hoursStr, 10)
      const minutes = parseInt(minutesStr, 10)
      let period = ''
      
      // Determine the correct period based on prayer name
      switch (prayerName) {
        case 'fajr':
        case 'sunrise':
          // Morning prayers are always AM
          period = ' AM'
          // If 12 AM is shown as 12, display as 12 AM
          // Otherwise convert 24-hour format to 12-hour if needed
          if (hours > 12) hours = hours % 12
          break
          
        case 'dhuhr':
          // Dhuhr (noon prayer) depends on time:
          // If it's exactly 12, it's PM (noon)
          // If it's before 12, it's AM (common in many regions)
          if (hours === 12) {
            period = ' PM'
          } else {
            period = ' AM'
            // Convert from 24-hour format if needed
            if (hours > 12) {
              hours = hours % 12
              period = ' PM'  // After noon is PM
            }
          }
          break
          
        case 'sunset':
        case 'maghrib':
          // Evening prayers are always PM
          period = ' PM'
          // Convert to 12-hour format if in 24-hour
          if (hours > 12) hours = hours % 12
          // If it's shown as 0, display as 12 PM
          if (hours === 0) hours = 12
          break
      }
      
      // Format with leading zeros for minutes
      return `${hours}:${minutes.toString().padStart(2, '0')}${period}`
    }

    return {
      prayerTimes,
      currentDate,
      searchQuery,
      searchResults,
      nextPrayer,
      currentLocationName,
      isLoadingLocation,
      locationError,
      showDropdown,
      getCurrentLocation,
      searchCities,
      selectCity,
      showAllCities,
      isNextPrayer,
      showMapSelector,
      handleLocationSelected,
      isLoadingPrayerTimes,
      formatPrayerTime,
      adjustTextSizes
    }
  }
}
</script>

<style scoped>
.prayer-times-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.location-selector {
  margin-bottom: 2rem;
}

.search-box {
  position: relative;
  margin-bottom: 1rem;
}

.search-box input {
  width: 100%;
  padding: 0.75rem 1rem;
  padding-right: 2.5rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  background-color: var(--input-bg);
  transition: all 0.2s ease;
  cursor: pointer;
}

.dropdown-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  pointer-events: none;
}

.search-box input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
  margin-top: 4px;
}

.city-item {
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.city-item:hover {
  background-color: var(--hover-color);
}

.city-name {
  font-size: 1rem;
  font-weight: 500;
}

.city-arabic-name {
  font-family: var(--arabic-font);
  color: var(--text-secondary);
}

.location-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.location-btn,
.map-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  font-size: 0.875rem;
  flex: 1;
}

.location-btn:hover,
.map-btn:hover {
  background-color: var(--primary-hover);
}

.map-btn {
  background-color: var(--secondary-color, #4a5568);
}

.map-btn:hover {
  background-color: var(--secondary-hover, #2d3748);
}

.prayer-card {
  background-color: var(--card-bg);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.date-section {
  text-align: center;
  margin-bottom: 2rem;
}

.current-location-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.location-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.location-name {
  font-size: 1.125rem;
  font-weight: 500;
}

.gregorian-date {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: center;
}

.english-date {
  font-size: 1.25rem;
  color: var(--text-color);
}

.arabic-date {
  font-family: var(--arabic-font);
  font-size: 1.25rem;
  color: var(--text-color);
  direction: rtl;
}

/* Next Prayer Section Styles */
.next-prayer-section {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  border-radius: 12px;
  padding: 1.5rem;
  color: white;
  text-align: center;
  box-shadow: 0 4px 15px rgba(var(--primary-color-rgb), 0.3);
  position: relative;
  width: 100%;
  overflow: visible;
}

.next-prayer-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 12px;
  background: inherit;
  z-index: -1;
  filter: blur(10px);
  opacity: 0.7;
  transform-origin: center;
}

.next-prayer-section::after {
  content: "";
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border-radius: 15px;
  border: 2px solid rgba(255, 255, 255, 0.7);
  opacity: 0.8;
  z-index: 1;
  pointer-events: none;
}

.next-prayer-header {
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.next-prayer-name {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.next-prayer-name .arabic-prayer-name {
  font-family: var(--arabic-font);
  font-size: 1.5rem;
  color: white;
  max-width: 100%;
  overflow: visible;
  white-space: normal;
  transition: font-size 0.2s ease;
  line-height: 1.2;
}

.next-prayer-time {
  font-size: 1rem;
  opacity: 0.8;
  margin-left: 0.5rem;
  max-width: 100%;
  overflow: visible;
  white-space: normal;
  transition: font-size 0.2s ease;
}

.countdown-timer {
  font-family: monospace;
  font-size: 2.5rem;
  font-weight: bold;
  color: white;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 100%;
  overflow: visible;
  white-space: normal;
  transition: font-size 0.2s ease;
  line-height: 1.1;
}

/* Main Prayer Times Grid */
.main-prayers {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.5rem;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
}

.prayer-item {
  background: linear-gradient(135deg, var(--primary-light), var(--primary-color));
  border-radius: 12px;
  padding: 1.5rem 0.75rem;
  text-align: center;
  transition: all 0.3s ease;
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 0;
  word-break: break-word;
  overflow: hidden;
  height: 100%; /* Ensure consistent height */
  min-height: 120px; /* Minimum height to ensure content fits */
}

.prayer-item.next-prayer {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  box-shadow: 0 4px 15px rgba(var(--primary-color-rgb), 0.4);
  position: relative;
  overflow: visible;
  border: 2px solid rgba(255, 255, 255, 0.7);
  transform: translateY(-2px);
}

.prayer-item.next-prayer::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 12px;
  background: inherit;
  z-index: -1;
  filter: blur(10px);
  opacity: 0.7;
  transform-origin: center;
}

.prayer-item.next-prayer::after {
  content: "";
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border-radius: 15px;
  border: 2px solid rgba(255, 255, 255, 0.7);
  opacity: 0.8;
  z-index: 1;
  pointer-events: none;
}

/* Custom gradients for each prayer */
.prayer-item:nth-child(1) {
  background: linear-gradient(135deg, #4facfe, #00f2fe); /* Fajr - Dawn blue */
}

.prayer-item:nth-child(3) {
  background: linear-gradient(135deg, #f6d365, #fda085); /* Dhuhr - Midday orange */
}

.prayer-item:nth-child(5) {
  background: linear-gradient(135deg, #6a11cb, #2575fc); /* Maghrib - Evening purple */
}

.prayer-name {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 1rem;
  width: 100%;
  overflow: visible;
}

.prayer-name .arabic-name {
  font-family: var(--arabic-font);
  font-size: 1.5rem;
  color: white;
  width: 100%;
  overflow: visible;
  white-space: normal;
  transition: font-size 0.2s ease;
  line-height: 1.2;
}

.prayer-time {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  font-family: monospace;
  margin-top: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  overflow: visible;
  white-space: normal;
  transition: font-size 0.2s ease;
}

.prayer-item.next-prayer .prayer-time {
  color: white;
}

/* Sun Cards Styles */
.sun-card {
  padding: 1.5rem 0.75rem;
  text-align: center;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 0;
  word-break: break-word;
  overflow: hidden;
  min-height: 120px; /* Minimum height to ensure content fits */
}

.sun-card.sunrise {
  background: linear-gradient(135deg, #ff9966, #ff5e62);
}

.sun-card.sunset {
  background: linear-gradient(135deg, #ff5e62, #904e95);
}

.sun-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
  overflow: hidden;
}

.sun-label {
  font-family: var(--arabic-font);
  font-size: 1.5rem;
  color: white;
  font-weight: 500;
  width: 100%;
  overflow: visible;
  white-space: normal;
  transition: font-size 0.2s ease;
  line-height: 1.2;
}

.sun-time {
  font-family: monospace;
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 1px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  overflow: visible;
  white-space: normal;
  transition: font-size 0.2s ease;
}

@media (max-width: 1200px) {
  .main-prayers {
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }

  .prayer-item, .sun-card {
    min-height: 110px;
  }
}

@media (max-width: 1024px) {
  .prayer-item, .sun-card {
    padding: 1.25rem 0.75rem;
    min-height: 110px;
  }
  
  .countdown-timer {
    font-size: 2.25rem;
  }
}

@media (max-width: 768px) {
  .main-prayers {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  .prayer-item, .sun-card {
    padding: 1.25rem 0.75rem;
    min-height: 100px;
  }
  
  .countdown-timer {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .main-prayers {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .prayer-item, .sun-card {
    padding: 1.25rem 1rem;
    min-height: 90px;
  }
  
  .countdown-timer {
    font-size: 1.75rem;
  }
  
  .next-prayer-section {
    padding: 1.25rem 1rem;
  }
  
  .next-prayer-name {
    flex-direction: column;
  }
  
  .next-prayer-time {
    margin-left: 0;
    margin-top: 0.25rem;
  }
}

/* Add these new styles */
.loading-state,
.error-state {
  text-align: center;
  padding: 2rem;
  background: var(--card-bg);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--primary-light);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  margin: 0 auto 1rem;
  animation: spin 1s linear infinite;
}

.error-state {
  color: var(--text-color);
}

.error-state p {
  margin: 0.5rem 0;
  font-family: var(--arabic-font);
  font-size: 1.25rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.map-modal {
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
  padding: 1rem;
}

.map-modal-content {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 1rem;
  width: 100%;
  max-width: 800px;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: var(--text-color);
  z-index: 1;
}

.close-btn:hover {
  color: var(--text-secondary);
}
</style>