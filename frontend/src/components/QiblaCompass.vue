<template>
  <div class="qibla-compass-container">
    <div class="compass-wrapper">
      <div class="direction-instruction" v-if="compassActive">
        <span class="direction-arrow">⬆️</span> Face this way for Qibla
      </div>
      
      <div class="compass">
        <div class="compass-background"></div>
        <div class="compass-arrow" ref="compassArrow">
          <div class="arrow"></div>
          <div class="kaaba-icon">🕋</div>
          <div class="qibla-beam"></div>
        </div>
        <div class="qibla-indicator">QIBLA</div>
        
        <div class="you-indicator">YOU</div>
      </div>
      
      <div class="qibla-label">Qibla Direction</div>
      <div v-if="debugMode" class="debug-info">
        Compass Rotation: {{ currentRotation }}°
        <div v-if="deviceHeading !== null">Device Heading: {{ deviceHeading }}°</div>
        <div class="manual-controls" v-if="isSimulating">
          <button @click="rotateLeft">←</button>
          <button @click="rotateRight">→</button>
        </div>
      </div>
      
      <div class="usage-instructions">
        <h4>How to use the Qibla Compass:</h4>
        <ol>
          <li>Enable the compass by clicking the button below</li>
          <li>Hold your device flat with the screen facing up</li>
          <li>The <strong>🕋 Kaaba icon</strong> shows the Qibla direction from your location</li>
          <li>Rotate yourself until the arrow points <strong>upward (⬆️)</strong></li>
          <li>You are now facing the Qibla direction!</li>
        </ol>
      </div>
    </div>
    
    <div class="compass-info">
      <div class="info-text" :class="{ active: compassActive }">
        <div class="location-info">
          <div class="latitude">
            Latitude: <span>{{ latitude }}</span>
          </div>
          <div class="longitude">
            Longitude: <span>{{ longitude }}</span>
          </div>
          <div class="deg">
            Direction: <span>{{ directionAngle }}</span>
          </div>
          <div class="distance">
            Distance to Kaaba: <span>{{ distance }}</span>
          </div>
        </div>
      </div>
      
      <button class="toggle" :class="{ 'toggle-on': compassActive }" @click="toggleCompass">
        {{ compassActive ? 'Disable Compass' : 'Enable Compass' }}
      </button>
      
      <div class="prayer-times">
        <h3>Prayer Times</h3>
        <div class="prayer-time">
          <div id="time-fajr" class="dawn">
            <div class="head">Dawn</div>
            <i class="icon"></i>
            <span>{{ prayerTimes.fajr }}</span>
          </div>
          <div id="time-dhuhr" class="noon">
            <div class="head">Noon</div>
            <i class="icon"></i>
            <span>{{ prayerTimes.dhuhr }}</span>
          </div>
          <div id="time-asr" class="afternoon">
            <div class="head">Afternoon</div>
            <i class="icon"></i>
            <span>{{ prayerTimes.asr }}</span>
          </div>
          <div id="time-maghrib" class="maghrib">
            <div class="head">Maghrib</div>
            <i class="icon"></i>
            <span>{{ prayerTimes.maghrib }}</span>
          </div>
          <div id="time-isha" class="isha">
            <div class="head">Isha</div>
            <i class="icon"></i>
            <span>{{ prayerTimes.isha }}</span>
          </div>
        </div>
        
        <div class="next-time">
          <h4>Time until next prayer:</h4>
          <div id="countdown">{{ countdown }}</div>
        </div>
      </div>
      
      <div class="settings">
        <div class="calculation-method">
          <label for="calculation-method">Calculation Method:</label>
          <select id="calculation-method" v-model="calculationMethod" @change="updatePrayerTimes">
            <option value="MuslimWorldLeague">Muslim World League</option>
            <option value="Egyptian">Egyptian</option>
            <option value="Karachi">Karachi</option>
            <option value="UmmAlQura">Umm Al-Qura</option>
            <option value="Dubai">Dubai</option>
            <option value="MoonsightingCommittee">Moonsighting Committee</option>
            <option value="NorthAmerica">North America</option>
            <option value="Kuwait">Kuwait</option>
            <option value="Qatar">Qatar</option>
            <option value="Singapore">Singapore</option>
            <option value="Tehran">Tehran</option>
            <option value="Turkey">Turkey</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QiblaCompass',
  data() {
    return {
      // Location data
      latitude: 0,
      longitude: 0,
      position: null,
      
      // Compass data
      deviceHeading: null,
      deviceAngleDelta: 0,
      currentRotation: 0,
      geolocationID: null,
      permissionGranted: false,
      isIOS: /iPad|iPhone|iPod/.test(navigator.userAgent),
      
      // UI state
      compassActive: false,
      directionAngle: '',
      distance: '',
      qiblaPoint: {
        lat: 21.422487,
        lng: 39.826206,
      },
      
      // Prayer time data
      prayerTimes: {
        fajr: '00:00',
        dhuhr: '00:00',
        asr: '00:00',
        maghrib: '00:00',
        isha: '00:00'
      },
      nextPrayer: null,
      countdown: '00 : 00 : 00',
      countdownInterval: null,
      endTime: null,
      calculationMethod: 'MuslimWorldLeague',
      
      // Debug and simulation
      debugMode: true, // Set to false in production
      isSimulating: false,
      simulationInterval: null,
      orientationInterval: null
    };
  },
  mounted() {
    // Get stored calculation method if available
    const storedMethod = localStorage.getItem('calculation-method');
    if (storedMethod) {
      this.calculationMethod = storedMethod;
    }
  },
  methods: {
    async toggleCompass() {
      this.compassActive = !this.compassActive;
      
      if (this.compassActive) {
        await this.initCompass();
      } else {
        this.stopCompass();
      }
    },
    async initCompass() {
      try {
        // Request orientation permission on iOS
        if (typeof DeviceOrientationEvent.requestPermission === "function") {
          const permission = await DeviceOrientationEvent.requestPermission();
          if (permission !== "granted") {
            alert("Device orientation permission denied");
            this.compassActive = false;
            return;
          }
          this.permissionGranted = true;
        } else if (window.DeviceOrientationEvent) {
          this.permissionGranted = true;
        } else {
          this.permissionGranted = false;
          alert("Device orientation not supported");
        }
        
        // Get user location
        await this.watchPosition();
        
        // Set up device orientation
        if (this.permissionGranted) {
          this.setupDeviceOrientation();
        }
        
        // For desktop testing
        if (!this.permissionGranted || !window.DeviceOrientationEvent) {
          console.log("Device orientation not supported, using simulation");
          this.simulateCompass();
        }
        
        // Calculate qibla direction
        this.updateQiblaDirection();
        
        // Set up prayer times
        this.updatePrayerTimes();
        
        // Calculate distance to Kaaba
        this.calculateDistance();
        
        // Set up interval to regularly update our UI
        this.orientationInterval = setInterval(() => {
          this.updateRotation();
        }, 100);
        
      } catch (error) {
        console.error("Error initializing compass:", error);
        alert("Error initializing compass: " + error.message);
        this.compassActive = false;
      }
    },
    setupDeviceOrientation() {
      if (this.isIOS) {
        window.addEventListener("deviceorientation", this.deviceOrientationHandler, true);
      } else {
        window.addEventListener("deviceorientationabsolute", this.deviceOrientationHandler, true);
      }
    },
    deviceOrientationHandler(evt) {
      if (evt.webkitCompassHeading) {
        // iOS
        this.deviceAngleDelta = 360 - evt.webkitCompassHeading;
        this.deviceHeading = evt.webkitCompassHeading;
      } else if (evt.alpha) {
        // Android
        this.deviceAngleDelta = 360 - Math.abs(evt.alpha - 360);
        this.deviceHeading = evt.alpha;
      }
      
      // Round the angle
      this.deviceAngleDelta = Math.round(this.deviceAngleDelta);
      
      if (this.debugMode) {
        console.log("Device orientation:", this.deviceAngleDelta);
      }
    },
    async watchPosition() {
      try {
        this.geolocationID = navigator.geolocation.watchPosition((position) => {
          this.position = position;
          this.latitude = position.coords.latitude;
          this.longitude = position.coords.longitude;
          
          // Update direction and distance when position changes
          if (this.compassActive) {
            this.updateQiblaDirection();
            this.calculateDistance();
          }
        }, (error) => {
          console.error("Geolocation error:", error);
        }, { enableHighAccuracy: true });
        
        // Get initial position
        const initialPosition = await this.getPosition();
        this.position = initialPosition;
        this.latitude = initialPosition.coords.latitude;
        this.longitude = initialPosition.coords.longitude;
        
        return initialPosition;
      } catch (error) {
        console.error("Error watching position:", error);
        throw error;
      }
    },
    stopCompass() {
      // Clear our interval that updates the UI
      clearInterval(this.orientationInterval);
      
      // Remove orientation event listeners
      if (this.isIOS) {
        window.removeEventListener("deviceorientation", this.deviceOrientationHandler, true);
      } else {
        window.removeEventListener("deviceorientationabsolute", this.deviceOrientationHandler, true);
      }
      
      // Clear simulation interval if it exists
      if (this.simulationInterval) {
        clearInterval(this.simulationInterval);
        this.simulationInterval = null;
      }
      
      // Reset simulation flag
      this.isSimulating = false;
      
      // Stop watching position
      if (this.geolocationID) {
        navigator.geolocation.clearWatch(this.geolocationID);
      }
      
      clearInterval(this.countdownInterval);
    },
    getPosition() {
      return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          position => resolve(position),
          error => {
            console.error("Geolocation error:", error);
            reject(error);
          },
          { enableHighAccuracy: true }
        );
      });
    },
    updateQiblaDirection() {
      const qiblaAngle = this.calcQiblaDirection(this.latitude, this.longitude);
      const qiblaDirection = this.getCardinalDirection(qiblaAngle);
      this.directionAngle = `${qiblaDirection} ${qiblaAngle}°`;
    },
    calcQiblaDirection(userLatitude, userLongitude) {
      const phi1 = (userLatitude * Math.PI) / 180;
      const lambda1 = (userLongitude * Math.PI) / 180;
      const phi2 = (this.qiblaPoint.lat * Math.PI) / 180;
      const lambda2 = (this.qiblaPoint.lng * Math.PI) / 180;

      const deltaLambda = lambda2 - lambda1;
      const y = Math.sin(deltaLambda) * Math.cos(phi2);
      const x =
        Math.cos(phi1) * Math.sin(phi2) -
        Math.sin(phi1) * Math.cos(phi2) * Math.cos(deltaLambda);

      let psi = (Math.atan2(y, x) * 180) / Math.PI;

      if (psi < 0) {
        psi += 360;
      }

      return Math.round(psi);
    },
    getCardinalDirection(degree) {
      const directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
      const index = Math.round(degree / 45) % 8;
      return directions[index >= 0 ? index : index + 8];
    },
    updateRotation() {
      if (!this.compassActive) return;
      
      if (!this.position) return;
      
      // Get the bearing to Kaaba
      const angleToKaaba = this.getBearingToDestination(
        { lat: this.latitude, lng: this.longitude },
        this.qiblaPoint
      );
      
      const deg = Math.round(angleToKaaba);
      
      // Update current rotation for display
      this.currentRotation = deg;
      
      // Apply rotation to the arrow, not the whole compass
      if (this.$refs.compassArrow) {
        this.$refs.compassArrow.style.transform = `rotate(${deg}deg)`;
      }
      
      // Log for debugging
      if (this.debugMode) {
        console.log("Rotating compass to:", deg, "degrees");
      }
    },
    getBearingToDestination(origin, destination) {
      // Get the bearing from origin to destination
      const bearing = this.getBearing(origin, destination);
      
      // Combine with the device orientation
      // When the device points north, deviceAngleDelta is 0
      // When the device points east, deviceAngleDelta is 90, etc.
      return (bearing - this.deviceAngleDelta + 360) % 360;
    },
    getBearing(origin, destination) {
      return (
        this.calculateAngle(
          origin.lat,
          origin.lng,
          destination.lat,
          destination.lng
        ) * (180 / Math.PI)
      );
    },
    calculateAngle(userLat, userLon, desiredLat, desiredLon) {
      return Math.atan2(desiredLon - userLon, desiredLat - userLat);
    },
    updatePrayerTimes() {
      // Save calculation method to localStorage
      localStorage.setItem('calculation-method', this.calculationMethod);
      
      // Demo prayer times - these would come from a proper calculation
      this.prayerTimes = {
        fajr: '05:30',
        dhuhr: '12:30',
        asr: '15:45',
        maghrib: '18:15',
        isha: '19:45'
      };
      
      // Find next prayer
      this.findNextPrayer();
      
      // Set up countdown
      this.setupCountdown();
    },
    findNextPrayer() {
      const currentTime = this.getCurrentTime();
      const times = Object.keys(this.prayerTimes);
      let minDifference = Infinity;
      this.nextPrayer = null;

      times.forEach(prayer => {
        const timeDifference = this.timeToMinutes(this.prayerTimes[prayer]) - this.timeToMinutes(currentTime);

        if (timeDifference > 0 && timeDifference < minDifference) {
          minDifference = timeDifference;
          this.nextPrayer = prayer;
        }
      });
      
      // If no next prayer today, set to fajr for tomorrow
      if (this.nextPrayer === null) {
        this.nextPrayer = 'fajr';
        // Get next day's fajr time
        this.getNextDayPrayerTime();
      }
      
      // Reset active classes
      document.querySelectorAll('.prayer-time > div').forEach(el => {
        el.classList.remove('active');
      });
      
      // Add active class to next prayer
      document.querySelector(`#time-${this.nextPrayer}`)?.classList.add('active');
    },
    getCurrentTime() {
      const now = new Date();
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      return `${hours}:${minutes}`;
    },
    timeToMinutes(time) {
      const [hours, minutes] = time.split(':').map(Number);
      return hours * 60 + minutes;
    },
    getNextDayPrayerTime() {
      // For a real app, this should use proper prayer time calculation
      // Here we're just setting it to 05:30 for demo purposes
      this.prayerTimes.fajr = '05:30';
    },
    setupCountdown() {
      clearInterval(this.countdownInterval);
      
      if (!this.nextPrayer) return;
      
      const currentTime = this.getCurrentTime();
      const currentDate = new Date().toISOString().split('T')[0].replace("/-/g", "/");
      
      let currentDateTime = new Date(`${currentDate} ${currentTime}`);
      let nextDateTime = new Date(`${currentDate} ${this.prayerTimes[this.nextPrayer]}`);
      
      // If next prayer is fajr and it's for tomorrow
      if (this.nextPrayer === 'fajr' && this.timeToMinutes(this.prayerTimes.fajr) < this.timeToMinutes(currentTime)) {
        let nextDay = new Date();
        nextDay.setDate(nextDay.getDate() + 1);
        const nextDayStr = nextDay.toISOString().split('T')[0].replace("/-/g", "/");
        nextDateTime = new Date(`${nextDayStr} ${this.prayerTimes.fajr}`);
      }
      
      const difference = nextDateTime.getTime() - currentDateTime.getTime();
      this.endTime = Date.now() + difference;
      
      this.updateCountdown();
      this.countdownInterval = setInterval(this.updateCountdown, 1000);
    },
    updateCountdown() {
      const secondsLeftms = this.endTime - Date.now();
      const secondsLeft = Math.round(secondsLeftms / 1000);
      
      if (secondsLeft < 0) {
        clearInterval(this.countdownInterval);
        this.countdown = '00 : 00 : 00';
        // Recalculate next prayer
        this.findNextPrayer();
        this.setupCountdown();
        return;
      }
      
      let hours = Math.floor(secondsLeft / 3600);
      let minutes = Math.floor(secondsLeft / 60) - (hours * 60);
      let seconds = secondsLeft % 60;
      
      hours = hours < 10 ? `0${hours}` : hours;
      minutes = minutes < 10 ? `0${minutes}` : minutes;
      seconds = seconds < 10 ? `0${seconds}` : seconds;
      
      this.countdown = `${hours} : ${minutes} : ${seconds}`;
    },
    calculateDistance() {
      const earthRadiusKm = 6371;
      const earthRadiusMiles = 3958.8;
      
      const dLat = this.degreesToRadians(this.qiblaPoint.lat - this.latitude);
      const dLon = this.degreesToRadians(this.qiblaPoint.lng - this.longitude);
      
      const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(this.degreesToRadians(this.latitude)) * 
        Math.cos(this.degreesToRadians(this.qiblaPoint.lat)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
      
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      
      const distanceKm = earthRadiusKm * c;
      const distanceMiles = earthRadiusMiles * c;
      
      const distanceKmRounded = Math.round(distanceKm);
      const distanceMilesRounded = Math.round(distanceMiles);
      
      this.distance = `${distanceKmRounded.toLocaleString()} km (${distanceMilesRounded.toLocaleString()} miles)`;
    },
    degreesToRadians(degrees) {
      return degrees * Math.PI / 180;
    },
    formatTime(time) {
      if (time instanceof Date) {
        return time.toLocaleTimeString('en-US', { hour12: false });
      }
      return time;
    },
    // Add a simulation method for desktop testing
    simulateCompass() {
      this.isSimulating = true;
      
      // If we already have location data, calculate the initial angle
      if (this.latitude && this.longitude) {
        const qiblaAngle = this.calcQiblaDirection(this.latitude, this.longitude);
        this.currentRotation = qiblaAngle;
        this.rotateCompass(this.currentRotation);
      } else {
        // Default values for testing
        this.latitude = 37.7749;  // Example: San Francisco
        this.longitude = -122.4194;
        
        // Calculate Qibla direction using default values
        this.updateQiblaDirection();
        this.calculateDistance();
        
        const qiblaAngle = this.calcQiblaDirection(this.latitude, this.longitude);
        this.currentRotation = qiblaAngle;
        this.rotateCompass(this.currentRotation);
      }
      
      // For simulation, we'll rotate the device heading slowly
      this.simulationInterval = setInterval(() => {
        // Simulate device rotation
        this.deviceHeading = (this.deviceHeading === null) ? 0 : (this.deviceHeading + 5) % 360;
        this.deviceAngleDelta = 360 - this.deviceHeading;
        
        // Update rotation
        this.updateRotation();
      }, 100);
    },
    rotateCompass(degrees) {
      if (this.$refs.compassArrow) {
        this.$refs.compassArrow.style.transform = `rotate(${degrees}deg)`;
      }
    },
    rotateLeft() {
      // Simulate turning the device to the left
      this.deviceHeading = (this.deviceHeading - 15 + 360) % 360;
      this.deviceAngleDelta = 360 - this.deviceHeading;
      this.updateRotation();
    },
    rotateRight() {
      // Simulate turning the device to the right
      this.deviceHeading = (this.deviceHeading + 15) % 360;
      this.deviceAngleDelta = 360 - this.deviceHeading;
      this.updateRotation();
    }
  },
  beforeDestroy() {
    this.stopCompass();
  }
};
</script>

<style scoped>
.qibla-compass-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  max-width: 500px;
  margin: 0 auto;
}

.compass-wrapper {
  position: relative;
  margin-bottom: 40px;
}

.qibla-label {
  text-align: center;
  font-weight: bold;
  margin-top: 10px;
  color: #ff5722;
  text-shadow: 0 0 2px rgba(255, 255, 255, 0.8);
}

.compass {
  width: 300px;
  height: 300px;
  position: relative;
  border-radius: 50%;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
  border: 2px solid #ccc;
  overflow: hidden;
}

.compass-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="49" fill="white" stroke="%23333" stroke-width="0.5"/><text x="50" y="15" text-anchor="middle" fill="%23333" font-size="6">N</text><text x="85" y="50" text-anchor="middle" fill="%23333" font-size="6">E</text><text x="50" y="85" text-anchor="middle" fill="%23333" font-size="6">S</text><text x="15" y="50" text-anchor="middle" fill="%23333" font-size="6">W</text></svg>') center center no-repeat;
  background-size: contain;
}

.compass-arrow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transition: transform 0.2s ease-out;
  transform-origin: center center;
  z-index: 5;
}

.arrow {
  position: absolute;
  top: 0;
  left: 50%;
  width: 8px;
  height: 45%;
  transform: translateX(-50%);
  background: linear-gradient(to bottom, #ff5722, transparent);
  z-index: 5;
  border-radius: 4px;
  box-shadow: 0 0 5px rgba(255, 87, 34, 0.5);
}

/* Hide the triangle at the top of the arrow since we have the Kaaba icon */
.arrow::before {
  display: none;
}

.kaaba-icon {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 28px;
  z-index: 30;
  text-shadow: 0 0 10px rgba(255, 87, 34, 0.9);
  animation: glow 2s infinite;
}

@keyframes glow {
  0% { text-shadow: 0 0 10px rgba(255, 87, 34, 0.5); }
  50% { text-shadow: 0 0 20px rgba(255, 87, 34, 1); }
  100% { text-shadow: 0 0 10px rgba(255, 87, 34, 0.5); }
}

.qibla-indicator {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  font-weight: bold;
  font-size: 14px;
  z-index: 20;
  background-color: rgba(255, 87, 34, 0.9);
  padding: 3px 10px;
  border-radius: 10px;
}

/* Modify the north indicator to make it clearer */
.compass::before {
  content: 'N';
  position: absolute;
  top: 5px;
  left: 50%;
  transform: translateX(-50%);
  font-weight: bold;
  font-size: 12px;
  color: white;
  background-color: #f44336;
  width: 18px;
  height: 18px;
  line-height: 18px;
  text-align: center;
  border-radius: 50%;
  z-index: 6;
}

/* Remove the old ::after that was on .compass-arrow */
.compass-arrow::after {
  content: none;
}

/* Remove the old ::after that was on .compass */
.compass::after {
  content: none;
}

.compass-info {
  width: 100%;
}

.info-text {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  opacity: 0;
  height: 0;
  overflow: hidden;
  transition: all 0.3s ease;
}

.info-text.active {
  opacity: 1;
  height: auto;
}

.location-info div {
  margin-bottom: 10px;
  font-size: 14px;
}

.toggle {
  display: block;
  width: 100%;
  padding: 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s;
}

.toggle:hover {
  background-color: #45a049;
}

.toggle-on {
  background-color: #f44336;
}

.toggle-on:hover {
  background-color: #d32f2f;
}

.prayer-times {
  background-color: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.prayer-times h3 {
  margin-top: 0;
  margin-bottom: 15px;
  text-align: center;
  color: #333;
}

.prayer-time {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.prayer-time > div {
  padding: 10px;
  border-radius: 4px;
  background-color: #f5f5f5;
  text-align: center;
}

.prayer-time > div.active {
  background-color: #e8f5e9;
}

.prayer-time > div.active .head {
  background-color: #4caf50;
}

.head {
  font-weight: bold;
  margin-bottom: 5px;
  background-color: #ddd;
  padding: 5px;
  border-radius: 3px;
}

.next-time {
  margin-top: 20px;
  text-align: center;
}

#countdown {
  font-size: 24px;
  font-weight: bold;
  color: #4caf50;
}

.settings {
  margin-top: 20px;
}

.calculation-method {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.calculation-method label {
  font-weight: bold;
}

select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.debug-info {
  text-align: center;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px;
  border-radius: 4px;
  margin-top: 10px;
  font-family: monospace;
}

.manual-controls {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.manual-controls button {
  background-color: #ff5722;
  border: none;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.manual-controls button:hover {
  background-color: #e64a19;
}

/* Add styles for the "YOU" indicator at the center */
.you-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  font-weight: bold;
  font-size: 12px;
  padding: 3px 6px;
  border-radius: 12px;
  z-index: 25;
}

/* Add styles for directional instructions */
.direction-instruction {
  text-align: center;
  margin-bottom: 15px;
  font-weight: bold;
  font-size: 18px;
  color: #333;
  animation: pulse 2s infinite;
}

.direction-arrow {
  font-size: 30px;
  display: block;
  margin-bottom: 5px;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* Add a beam of light effect from center to Kaaba */
.qibla-beam {
  position: absolute;
  top: 0;
  left: 50%;
  width: 20px;
  height: 50%;
  transform: translateX(-50%);
  background: linear-gradient(to bottom, rgba(255, 87, 34, 0.3), transparent);
  z-index: 4;
  border-radius: 10px;
}

/* Add styles for the usage instructions */
.usage-instructions {
  margin-top: 20px;
  background-color: #fff9c4;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.usage-instructions h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #ff5722;
  text-align: center;
}

.usage-instructions ol {
  margin: 0;
  padding-left: 20px;
}

.usage-instructions li {
  margin-bottom: 8px;
}

.usage-instructions strong {
  color: #ff5722;
}
</style>
