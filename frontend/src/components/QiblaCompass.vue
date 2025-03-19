<template>
  <div class="qibla-container">
    <h2 class="qibla-title">{{ $t('qibla.title') }}</h2>
    <p class="qibla-subtitle">{{ $t('qibla.subtitle') }}</p>
    
    <div class="status-message" v-if="errorMessage">{{ errorMessage }}</div>
    <div class="status-message" v-if="!hasLocation && !errorMessage">{{ $t('qibla.noLocation') }}</div>
    
    <div class="map-wrapper" v-if="hasLocation">
      <!-- Real map with OpenStreetMap -->
      <div class="real-map-container">
        <div id="qibla-map" class="real-map" ref="qiblaMap"></div>
        <div class="navigation-mode" v-if="isFollowingUser">
          <div class="navigation-label">{{ $t('qibla.navigationMode') }}</div>
        </div>
      </div>
      
      <div class="info-panel">
        <div class="qibla-info">
          <div class="qibla-direction">
            <div class="direction-chip">{{ Math.round(qiblaDirection) }}°</div>
            <div class="direction-label">{{ $t('qibla.direction') }}</div>
          </div>
          
          <div class="navigation-instructions" v-if="isCompassActive">
            <div v-if="isNearQibla" class="facing-qibla">
              <span>🟢</span> {{ $t('qibla.facingQibla') }}
            </div>
            <div v-else class="turn-instruction">
              <span>↺</span> {{ $t('qibla.turnInstruction', { degrees: Math.round((qiblaDirection - heading + 360) % 360) }) }}
            </div>
          </div>
          
          <div class="location-info">
            <div class="distance-chip">
              <span>📏</span> {{ calculateDistance().toFixed(0) }} km
            </div>
          </div>
        </div>
        
        <div class="button-group">
          <button class="compass-button" @click="toggleCompass">
            <span class="button-icon">{{ isCompassActive ? '🧭 ✓' : '🧭' }}</span>
            <span class="button-text">{{ isCompassActive ? $t('qibla.compassActive') : $t('qibla.activateCompass') }}</span>
          </button>
          <button class="locate-button" @click="requestLocation">
            <span class="button-icon">📍</span>
            <span class="button-text">{{ $t('qibla.updateLocation') }}</span>
          </button>
        </div>
      </div>
    </div>
    
    <div class="location-controls" v-if="!hasLocation && !isLoading">
      <button @click="requestLocation" class="primary-button">
        {{ $t('qibla.detectLocation') }}
      </button>
    </div>
    
    <div class="loading" v-if="isLoading">
      <div class="spinner"></div>
      <div>{{ $t('qibla.detecting') }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QiblaCompass',
  data() {
    return {
      hasLocation: false,
      isCompassActive: false,
      isLoading: false,
      errorMessage: '',
      latitude: 0,
      longitude: 0,
      heading: 0,
      qiblaDirection: 0,
      watchId: null,
      orientationWatch: null,
      map: null,
      userMarker: null,
      kaabaMarker: null,
      directionLine: null,
      qiblaArrow: null,
      headingIndicator: null,
      isFollowingUser: true, // Auto-follow mode enabled by default
      previousPosition: null,
      // Kaaba coordinates
      kaabaLatitude: 21.4225,
      kaabaLongitude: 39.8262
    }
  },
  computed: {
    isNearQibla() {
      // Consider the user facing Qibla if within 5 degrees
      const diff = Math.abs(this.qiblaDirection - this.heading) % 360;
      return diff < 5 || diff > 355;
    }
  },
  mounted() {
    this.loadMapLibraries();
    this.requestLocation();
    // Start compass automatically when component is mounted
    this.startCompass();
  },
  beforeUnmount() {
    // Clean up event listeners and watchPosition
    this.stopCompass();
    if (this.watchId !== null) {
      navigator.geolocation.clearWatch(this.watchId);
    }
    if (this.map) {
      this.map.remove();
      this.map = null;
    }
  },
  methods: {
    loadMapLibraries() {
      // Load Leaflet CSS
      if (!document.getElementById('leaflet-css')) {
        const link = document.createElement('link');
        link.id = 'leaflet-css';
        link.rel = 'stylesheet';
        link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
        link.integrity = 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=';
        link.crossOrigin = '';
        document.head.appendChild(link);
      }
      
      // Load Leaflet JS only if it's not already loaded
      if (!window.L) {
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
        script.integrity = 'sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=';
        script.crossOrigin = '';
        script.onload = () => {
          // Initialize the map after Leaflet is loaded
          if (this.hasLocation) {
            this.initMap();
          }
        };
        document.head.appendChild(script);
      }
    },
    initMap() {
      if (!window.L || !this.$refs.qiblaMap) return;
      
      // If map already exists, remove it first
      if (this.map) {
        this.map.remove();
        this.map = null;
      }
      
      // Create map centered at user's location with higher zoom level for navigation
      this.map = L.map(this.$refs.qiblaMap).setView([this.latitude, this.longitude], 16);
      
      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);
      
      // Custom Kaaba icon
      const kaabaIcon = L.divIcon({
        html: '<span style="font-size: 24px;">🕋</span>',
        className: 'kaaba-map-icon',
        iconSize: [30, 30],
        iconAnchor: [15, 15]
      });
      
      // Custom user icon that rotates with heading
      this.createUserMarker();
      
      // Add Kaaba marker
      this.kaabaMarker = L.marker([this.kaabaLatitude, this.kaabaLongitude], {
        icon: kaabaIcon
      }).addTo(this.map);
      this.kaabaMarker.bindPopup('Kaaba, Mecca');
      
      // Draw a line between user and Kaaba
      this.directionLine = L.polyline(
        [[this.latitude, this.longitude], [this.kaabaLatitude, this.kaabaLongitude]], 
        {
          color: '#4caf50',
          weight: 2,
          opacity: 0.7,
          dashArray: '5, 5'
        }
      ).addTo(this.map);
      
      // Add navigation controls
      this.addCustomControls();
      
      // Handle map interaction to disable auto-follow
      this.map.on('dragstart', () => {
        this.isFollowingUser = false;
      });
      
      // Initial fit bounds to show context
      const bounds = L.latLngBounds([
        [this.latitude, this.longitude],
        [this.kaabaLatitude, this.kaabaLongitude]
      ]);
      this.map.fitBounds(bounds, { padding: [30, 30] });
    },
    createUserMarker() {
      // Remove existing marker if any
      if (this.userMarker) {
        this.map.removeLayer(this.userMarker);
      }
      
      // Create a custom HTML marker that shows direction
      const markerHtml = `
        <div class="user-marker-container">
          <div class="direction-arrow" style="transform: rotate(${this.heading}deg)">
            <svg viewBox="0 0 24 24" width="40" height="40">
              <path d="M12,2L18,12L12,22L6,12L12,2Z" fill="#f44336" />
            </svg>
          </div>
          <div class="user-dot"></div>
        </div>
      `;
      
      const userIcon = L.divIcon({
        html: markerHtml,
        className: 'user-map-icon',
        iconSize: [40, 40],
        iconAnchor: [20, 20]
      });
      
      // Add user marker
      this.userMarker = L.marker([this.latitude, this.longitude], {
        icon: userIcon,
        zIndexOffset: 1000
      }).addTo(this.map);
    },
    addCustomControls() {
      // Create follow mode toggle button
      const followControl = L.Control.extend({
        options: {
          position: 'topright'
        },
        
        onAdd: (map) => {
          const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
          container.style.backgroundColor = 'white';
          container.style.width = '34px';
          container.style.height = '34px';
          container.style.cursor = 'pointer';
          container.style.display = 'flex';
          container.style.alignItems = 'center';
          container.style.justifyContent = 'center';
          container.innerHTML = '<span style="font-size: 18px;">📱</span>';
          container.title = 'Toggle follow mode';
          container.setAttribute('data-mode', this.isFollowingUser ? 'on' : 'off');
          
          if (this.isFollowingUser) {
            container.style.backgroundColor = '#4caf5066';
          }
          
          container.onclick = () => {
            this.isFollowingUser = !this.isFollowingUser;
            container.style.backgroundColor = this.isFollowingUser ? '#4caf5066' : 'white';
            container.setAttribute('data-mode', this.isFollowingUser ? 'on' : 'off');
            if (this.isFollowingUser) {
              this.map.setView([this.latitude, this.longitude], 18);
            }
          };
          
          return container;
        }
      });
      
      // Full map view control (show both user and Kaaba)
      const fullViewControl = L.Control.extend({
        options: {
          position: 'topright'
        },
        
        onAdd: (map) => {
          const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
          container.style.backgroundColor = 'white';
          container.style.width = '34px';
          container.style.height = '34px';
          container.style.cursor = 'pointer';
          container.style.display = 'flex';
          container.style.alignItems = 'center';
          container.style.justifyContent = 'center';
          container.innerHTML = '<span style="font-size: 18px;">🗺️</span>';
          container.title = 'Show full route to Kaaba';
          
          container.onclick = () => {
            this.isFollowingUser = false;
            const bounds = L.latLngBounds([
              [this.latitude, this.longitude],
              [this.kaabaLatitude, this.kaabaLongitude]
            ]);
            this.map.fitBounds(bounds, { padding: [30, 30] });
          };
          
          return container;
        }
      });
      
      // Add the controls to the map
      this.map.addControl(new followControl());
      this.map.addControl(new fullViewControl());
    },
    updateMap() {
      if (!this.map || !this.userMarker) return;
      
      // Check if user has moved significantly
      const hasMoved = !this.previousPosition || 
        this.calculateDistance(
          this.latitude, this.longitude, 
          this.previousPosition.lat, this.previousPosition.lng
        ) > 0.005; // 5 meters threshold
      
      if (hasMoved) {
        // Update user marker position
        this.userMarker.setLatLng([this.latitude, this.longitude]);
        
        // Create a new user marker with updated heading
        this.createUserMarker();
        
        // Update direction line
        this.directionLine.setLatLngs([
          [this.latitude, this.longitude],
          [this.kaabaLatitude, this.kaabaLongitude]
        ]);
        
        // If in follow mode, center map on user
        if (this.isFollowingUser) {
          this.map.setView([this.latitude, this.longitude], this.map.getZoom());
        }
        
        // Store current position for next comparison
        this.previousPosition = {
          lat: this.latitude,
          lng: this.longitude
        };
      } else if (this.heading !== this.previousHeading) {
        // Just update the marker for heading changes
        this.createUserMarker();
        this.previousHeading = this.heading;
      }
    },
    requestLocation() {
      this.isLoading = true;
      this.errorMessage = '';
      
      if ('geolocation' in navigator) {
        const options = {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0
        };
        
        this.watchId = navigator.geolocation.watchPosition(
          this.locationSuccess,
          this.locationError,
          options
        );
      } else {
        this.isLoading = false;
        this.errorMessage = this.$t('qibla.geolocationNotSupported');
      }
    },
    locationSuccess(position) {
      this.hasLocation = true;
      this.isLoading = false;
      this.latitude = position.coords.latitude;
      this.longitude = position.coords.longitude;
      
      // Calculate Qibla direction
      this.calculateQiblaDirection();
      
      // Initialize or update the map
      if (!this.map && window.L) {
        this.initMap();
      } else if (this.map) {
        this.updateMap();
      }
    },
    locationError(error) {
      this.isLoading = false;
      
      switch(error.code) {
        case error.PERMISSION_DENIED:
          this.errorMessage = this.$t('qibla.permissionDenied');
          break;
        case error.POSITION_UNAVAILABLE:
          this.errorMessage = this.$t('qibla.locationError');
          break;
        case error.TIMEOUT:
          this.errorMessage = this.$t('qibla.timeout');
          break;
        default:
          this.errorMessage = this.$t('qibla.locationError');
      }
    },
    toggleCompass() {
      if (this.isCompassActive) {
        this.stopCompass();
      } else {
        this.startCompass();
      }
    },
    startCompass() {
      // Handle iOS permission request
      if (window.DeviceOrientationEvent && typeof DeviceOrientationEvent.requestPermission === 'function') {
        // iOS 13+ requires user interaction to request permission
        DeviceOrientationEvent.requestPermission()
          .then(permissionState => {
            if (permissionState === 'granted') {
              this.initCompass();
            } else {
              this.errorMessage = this.$t('qibla.permissionDenied');
            }
          })
          .catch(error => {
            // This might happen if called in a non-secure context or not from a user gesture
            // In that case, try to start the compass normally
            this.initCompass();
          });
      } else {
        // For non-iOS or older iOS versions
        this.initCompass();
      }
    },
    initCompass() {
      if (!window.DeviceOrientationEvent) {
        this.errorMessage = this.$t('qibla.compassNotSupported');
        return;
      }
      
      // Set compass as active
      this.isCompassActive = true;
      
      // Add event listener for device orientation
      window.addEventListener('deviceorientation', this.handleOrientation);
      
      // If we don't get any orientation events after a short delay, try the alternate approach
      this.orientationWatch = setTimeout(() => {
        if (this.heading === 0) {
          // Try to use the device motion event as a fallback
          window.addEventListener('devicemotion', this.handleDeviceMotion);
        }
      }, 1000);
    },
    stopCompass() {
      window.removeEventListener('deviceorientation', this.handleOrientation);
      window.removeEventListener('devicemotion', this.handleDeviceMotion);
      if (this.orientationWatch) {
        clearTimeout(this.orientationWatch);
      }
      this.isCompassActive = false;
    },
    handleOrientation(event) {
      // Alpha is the compass heading in degrees
      if (event.webkitCompassHeading) {
        // For iOS devices
        this.heading = event.webkitCompassHeading;
      } else if (event.alpha) {
        // For Android devices
        // Alpha returns values from 0 to 360 in a counterclockwise direction
        // Need to convert it to clockwise for compass
        this.heading = 360 - event.alpha;
      }
      
      // Update the marker with new heading
      if (this.map && this.hasLocation && this.userMarker) {
        this.createUserMarker();
      }
    },
    handleDeviceMotion(event) {
      // This is a fallback for devices that don't properly support deviceorientation
      // It's less accurate but better than nothing
      if (event.accelerationIncludingGravity) {
        const x = event.accelerationIncludingGravity.x;
        const y = event.accelerationIncludingGravity.y;
        
        // Calculate approximate heading from accelerometer
        // This is not as accurate as compass but can give a rough direction
        if (x !== null && y !== null) {
          let heading = Math.atan2(y, x) * 180 / Math.PI;
          heading = (heading + 360) % 360; // Convert to 0-360 range
          
          // Only update if significant change to reduce jitter
          if (Math.abs(heading - this.heading) > 5) {
            this.heading = heading;
            
            // Update the user marker
            if (this.map && this.hasLocation && this.userMarker) {
              this.createUserMarker();
            }
          }
        }
      }
    },
    calculateQiblaDirection() {
      // Convert latitude and longitude from degrees to radians
      const lat1 = this.toRadians(this.latitude);
      const lon1 = this.toRadians(this.longitude);
      const lat2 = this.toRadians(this.kaabaLatitude);
      const lon2 = this.toRadians(this.kaabaLongitude);
      
      // Calculate the qibla direction using the haversine formula
      const y = Math.sin(lon2 - lon1);
      const x = Math.cos(lat1) * Math.tan(lat2) - Math.sin(lat1) * Math.cos(lon2 - lon1);
      let qibla = Math.atan2(y, x);
      
      // Convert from radians to degrees
      qibla = this.toDegrees(qibla);
      
      // Make sure the result is between 0 and 360 degrees
      this.qiblaDirection = (qibla + 360) % 360;
    },
    calculateDistance(lat1 = this.latitude, lon1 = this.longitude, lat2 = this.kaabaLatitude, lon2 = this.kaabaLongitude) {
      // Implementation of the Haversine formula to calculate distance between two points on Earth
      const R = 6371; // Earth's radius in km
      const dLat = this.toRadians(lat2 - lat1);
      const dLon = this.toRadians(lon2 - lon1);
      
      const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) * 
        Math.sin(dLon/2) * Math.sin(dLon/2);
      
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      const distance = R * c; // Distance in km
      
      return distance;
    },
    toRadians(degrees) {
      return degrees * (Math.PI / 180);
    },
    toDegrees(radians) {
      return radians * (180 / Math.PI);
    }
  }
}
</script>

<style scoped>
.qibla-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  margin: 0 auto;
  max-width: 500px;
}

.qibla-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  text-align: center;
}

.qibla-subtitle {
  font-size: 1rem;
  color: #666;
  margin-bottom: 1.5rem;
  text-align: center;
}

.map-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  position: relative;
}

/* Real Map styles */
.real-map-container {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.real-map {
  width: 100%;
  height: 350px;
  z-index: 1;
}

.navigation-mode {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(76, 175, 80, 0.8);
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  z-index: 2;
}

/* Custom map marker styles */
.user-marker-container {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.direction-arrow {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.2s ease;
}

.user-dot {
  position: absolute;
  width: 12px;
  height: 12px;
  background-color: #f44336;
  border: 2px solid white;
  border-radius: 50%;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.3);
}

.user-map-icon, .kaaba-map-icon {
  background: none;
  border: none;
}

/* Info panel styles */
.info-panel {
  margin-top: 1rem;
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 1rem;
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.qibla-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}

.qibla-direction {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 0.5rem;
}

.direction-chip {
  background-color: #4caf50;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 0.2rem;
}

.direction-label {
  font-size: 0.8rem;
  color: #666;
}

.navigation-instructions {
  margin: 0.8rem 0;
  padding: 0.5rem;
  border-radius: 5px;
  background-color: #f0f7ff;
  width: 100%;
  text-align: center;
}

.facing-qibla {
  color: #4caf50;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
}

.turn-instruction {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
}

.location-info {
  display: flex;
  justify-content: center;
  margin-top: 0.5rem;
}

.distance-chip {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #f0f0f0;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.9rem;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
  gap: 10px;
}

.compass-button, .locate-button {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.8rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.compass-button {
  background-color: #f0f7ff;
  color: #0277bd;
}

.locate-button {
  background-color: #fff8e1;
  color: #f57c00;
}

.compass-button:hover, .locate-button:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.button-icon {
  font-size: 1.2rem;
  margin-bottom: 0.3rem;
}

.button-text {
  font-size: 0.8rem;
  font-weight: bold;
}

.location-controls {
  margin: 1.5rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.status-message {
  padding: 1rem;
  margin: 1rem 0;
  background-color: #fff3cd;
  border-radius: 5px;
  text-align: center;
  width: 100%;
}

.primary-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s;
}

.primary-button:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem 0;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 480px) {
  .real-map {
    height: 300px;
  }
}
</style>

