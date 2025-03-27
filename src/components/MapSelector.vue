<template>
  <div class="map-selector">
    <div class="map-wrapper">
      <div class="map-container" ref="mapContainer"></div>
    </div>
    <div class="selected-location-wrapper" v-if="selectedLocation">
      <div class="selected-location">
        <p class="section-title">{{ $t('prayerTimes.selectedLocation') }}:</p>
        <p class="coordinates">
          {{ selectedLocation.lat.toFixed(4) }}, {{ selectedLocation.lng.toFixed(4) }}
        </p>
        <p class="location-name">{{ locationName }}</p>
        <button class="confirm-btn" @click="confirmLocation">
          {{ $t('prayerTimes.useThisLocation') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import L from '../utils/leaflet-setup'

export default defineComponent({
  name: 'MapSelector',
  data() {
    return {
      map: null,
      marker: null,
      selectedLocation: null,
      locationName: '',
    }
  },
  mounted() {
    this.initMap()
  },
  methods: {
    initMap() {
      // Initialize the map
      this.map = L.map(this.$refs.mapContainer).setView([33.3152, 44.3661], 6) // Default center on Baghdad

      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(this.map)

      // Handle map click
      this.map.on('click', this.handleMapClick)
    },
    async handleMapClick(e) {
      const { lat, lng } = e.latlng

      // Update or create marker
      if (this.marker) {
        this.marker.setLatLng([lat, lng])
      } else {
        this.marker = L.marker([lat, lng]).addTo(this.map)
      }

      this.selectedLocation = { lat, lng }

      // Get location name using reverse geocoding
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&accept-language=en`
        )
        const data = await response.json()
        
        // Extract relevant location information
        const address = data.address
        const city = address.city || address.town || address.village || address.state || ''
        const country = address.country || ''
        this.locationName = city && country ? `${city}, ${country}` : `${lat.toFixed(4)}, ${lng.toFixed(4)}`
      } catch (error) {
        console.error('Error getting location name:', error)
        this.locationName = `${lat.toFixed(4)}, ${lng.toFixed(4)}`
      }
    },
    confirmLocation() {
      if (this.selectedLocation) {
        this.$emit('location-selected', {
          ...this.selectedLocation,
          name: this.locationName
        })
      }
    }
  },
  beforeUnmount() {
    if (this.map) {
      this.map.remove()
    }
  }
}) 
</script>

<style scoped>
.map-selector {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.map-wrapper {
  width: 100%;
  height: 300px;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border-color, #e2e8f0);
}

.map-container {
  width: 100%;
  height: 100%;
}

.selected-location-wrapper {
  width: 100%;
}

.selected-location {
  background: var(--bg-secondary, #f7fafc);
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color, #e2e8f0);
}

.section-title {
  font-size: 1.1em;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  text-align: center;
}

.coordinates {
  font-family: monospace;
  color: var(--text-color);
  font-size: 1.2em;
  background: var(--card-bg, white);
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  text-align: center;
  font-weight: 500;
}

.location-name {
  font-weight: 500;
  color: var(--text-color);
  font-size: 1.2em;
  margin: 1rem 0 1.5rem;
  text-align: center;
}

.confirm-btn {
  display: block;
  width: 100%;
  padding: 1rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1.1em;
  font-weight: 500;
}

.confirm-btn:hover {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.confirm-btn:active {
  transform: translateY(0);
}
</style> 