<template>
  <div class="prayer-times-container">
    <div class="location-selector">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          type="text" 
          :placeholder="$t('prayerTimes.searchCity')"
          @input="searchCities"
        />
        <div v-if="searchResults.length > 0" class="search-results">
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
      <div class="current-location">
        <button @click="getCurrentLocation" class="location-btn" :disabled="isLoadingLocation">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
          </svg>
          {{ isLoadingLocation ? $t('prayerTimes.gettingLocation') : $t('prayerTimes.useCurrentLocation') }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoadingLocation" class="loading-state">
      <div class="loading-spinner"></div>
      <p>جاري تحديد موقعك...</p>
    </div>

    <!-- Location Error State -->
    <div v-else-if="locationError" class="error-state">
      <p>لم نتمكن من تحديد موقعك</p>
      <p>الرجاء اختيار مدينتك من القائمة أعلاه</p>
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
        <div class="gregorian-date">{{ currentDate }}</div>
      </div>

      <!-- Next Prayer Section - Moved to top for prominence -->
      <div class="next-prayer-section" v-if="nextPrayer">
        <div class="next-prayer-header">
          {{ $t('prayerTimes.nextPrayer') }}
        </div>
        <div class="next-prayer-name">
          <span class="arabic-prayer-name">{{ nextPrayer.arabicName }}</span>
          <span class="english-prayer-name">{{ $t(`prayerTimes.${nextPrayer.name}`) }}</span>
        </div>
        <div class="countdown-timer">{{ nextPrayer.countdown }}</div>
      </div>

      <!-- Main Prayer Times Grid -->
      <div class="main-prayers">
        <div class="prayer-item" :class="{ 'next-prayer': isNextPrayer('fajr') }">
          <div class="prayer-name">
            <span class="arabic-name">الفجر</span>
          </div>
          <div class="prayer-time">{{ prayerTimes?.fajir || '--:--' }}</div>
        </div>

        <div class="sun-card sunrise">
          <div class="sun-info">
            <span class="sun-label">الشروق</span>
            <span class="sun-time">{{ prayerTimes?.sunrise || '--:--' }}</span>
          </div>
        </div>

        <div class="prayer-item" :class="{ 'next-prayer': isNextPrayer('dhuhr') }">
          <div class="prayer-name">
            <span class="arabic-name">الظهر</span>
          </div>
          <div class="prayer-time">{{ prayerTimes?.doher || '--:--' }}</div>
        </div>

        <div class="sun-card sunset">
          <div class="sun-info">
            <span class="sun-label">الغروب</span>
            <span class="sun-time">{{ prayerTimes?.sunset || '--:--' }}</span>
          </div>
        </div>

        <div class="prayer-item" :class="{ 'next-prayer': isNextPrayer('maghrib') }">
          <div class="prayer-name">
            <span class="arabic-name">المغرب</span>
          </div>
          <div class="prayer-time">{{ prayerTimes?.maghrib || '--:--' }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, onUnmounted } from 'vue'

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
  setup() {
    const prayerTimes = ref(null)
    const currentLocation = ref(null) // Changed to null initially
    const searchQuery = ref('')
    const searchResults = ref([])
    const nextPrayer = ref(null)
    const currentLocationName = ref('')
    const isLoadingLocation = ref(true) // Changed to true initially
    const locationError = ref(false) // New ref for tracking location errors
    
    const currentDate = computed(() => {
      return new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    })

    const fetchPrayerTimes = async () => {
      if (!currentLocation.value) return // Don't fetch if no location

      try {
        const response = await fetch(
          `https://hq.alkafeel.net/Api/init/init.php?v=jsonPrayerTimes&timezone=${currentLocation.value.timezone}&long=${currentLocation.value.longitude}&lati=${currentLocation.value.latitude}`
        )
        const data = await response.json()
        prayerTimes.value = data
        calculateNextPrayer()
      } catch (error) {
        console.error('Error fetching prayer times:', error)
        prayerTimes.value = null
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
      
      // Fetch prayer times for selected city
      fetchPrayerTimes()
    }

    const calculateNextPrayer = () => {
      if (!prayerTimes.value) return

      const now = new Date()
      // Only include Fajr, Dhuhr, and Maghrib with updated Arabic names
      const prayers = [
        { name: 'fajr', time: prayerTimes.value.fajir, arabicName: 'الفجر' },
        { name: 'dhuhr', time: prayerTimes.value.doher, arabicName: 'الظهر' },
        { name: 'maghrib', time: prayerTimes.value.maghrib, arabicName: 'المغرب' }
      ]

      // Convert prayer times to Date objects
      const prayerDates = prayers.map(prayer => {
        const [hours, minutes] = prayer.time.split(':').map(Number)
        const date = new Date()
        date.setHours(hours, minutes, 0)
        
        // If prayer time has passed for today, set it for tomorrow
        if (date < now) {
          date.setDate(date.getDate() + 1)
        }
        
        return { ...prayer, date }
      })

      // Find next prayer (closest future prayer time)
      const next = prayerDates.reduce((closest, prayer) => {
        if (!closest || prayer.date < closest.date) {
          return prayer
        }
        return closest
      }, null)
      
      if (next) {
        const timeDiff = next.date - now
        nextPrayer.value = {
          name: next.name,
          arabicName: next.arabicName,
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
            // Time for prayer has come, recalculate next prayer
            calculateNextPrayer()
          } else {
            // Update the countdown
            nextPrayer.value = {
              ...nextPrayer.value,
              countdown: formatCountdown(timeDiff)
            }
          }
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

    return {
      prayerTimes,
      currentDate,
      searchQuery,
      searchResults,
      nextPrayer,
      currentLocationName,
      isLoadingLocation,
      locationError,
      getCurrentLocation,
      searchCities,
      selectCity,
      isNextPrayer
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
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  background-color: var(--input-bg);
  transition: all 0.2s ease;
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

.location-btn {
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
}

.location-btn:hover {
  background-color: var(--primary-hover);
}

.location-btn svg {
  width: 1.25rem;
  height: 1.25rem;
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
  font-size: 1.25rem;
  color: var(--text-color);
  margin-bottom: 0.5rem;
}

/* Next Prayer Section Styles */
.next-prayer-section {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  border-radius: 12px;
  padding: 1.5rem;
  color: white;
  text-align: center;
  box-shadow: 0 4px 15px rgba(var(--primary-color-rgb), 0.3);
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
}

.next-prayer-name .arabic-prayer-name {
  font-family: var(--arabic-font);
  font-size: 2rem;
  color: white;
  margin: 0;
}

.next-prayer-name .english-prayer-name {
  font-size: 1.25rem;
  opacity: 0.9;
}

.countdown-timer {
  font-family: monospace;
  font-size: 3rem;
  font-weight: bold;
  color: white;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Main Prayers Grid */
.main-prayers {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.5rem;
}

.prayer-item {
  background: linear-gradient(135deg, var(--primary-light), var(--primary-color));
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.prayer-item.next-prayer {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  transform: translateY(-4px);
  box-shadow: 0 4px 15px rgba(var(--primary-color-rgb), 0.2);
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
}

.prayer-name .arabic-name {
  font-family: var(--arabic-font);
  font-size: 1.75rem;
  color: white;
}

.prayer-time {
  font-size: 1.75rem;
  font-weight: bold;
  color: white;
  font-family: monospace;
  margin-top: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.prayer-item.next-prayer .prayer-time {
  color: white;
}

/* Sun Cards Styles */
.sun-card {
  padding: 1.5rem;
  text-align: center;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
}

.sun-label {
  font-family: var(--arabic-font);
  font-size: 1.75rem;
  color: white;
  font-weight: 500;
}

.sun-time {
  font-family: monospace;
  font-size: 1.75rem;
  font-weight: bold;
  letter-spacing: 1px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media (max-width: 1024px) {
  .main-prayers {
    grid-template-columns: repeat(3, 1fr);
  }

  .prayer-time, .sun-time {
    font-size: 1.5rem;
  }

  .prayer-name .arabic-name {
    font-size: 1.5rem;
  }
}

@media (max-width: 768px) {
  .main-prayers {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .prayer-time, .sun-time {
    font-size: 1.25rem;
  }

  .prayer-name .arabic-name {
    font-size: 1.25rem;
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
</style> 