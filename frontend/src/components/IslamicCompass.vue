<template>
  <div class="islamic-compass-wrapper">
    <div class="compass-container">
      <div class="compass">
        <div class="compass-circle"></div>
        
        <!-- Target marker (fixed at top) -->
        <div class="target-marker">
          <div class="target-arrow-line"></div>
          <div class="target-arrow-head"></div>
        </div>
        
        <!-- Loading spinner for Qibla -->
        <div class="qibla-loading" v-if="isQiblaLoading">
          <div class="spinner"></div>
          <div class="loading-text">{{ $t('compass.calculatingQibla') }}</div>
        </div>
        
        <!-- Qibla direction marker on compass (moves with compass) -->
        <div class="qibla-marker" ref="qiblaMarker">
          <div class="qibla-icon">🕋</div>
          <div class="qibla-label">{{ $t('compass.qibla') }}</div>
        </div>
        
        <!-- Center dot -->
        <div class="center-dot"></div>
      </div>
    </div>
    
    <div class="deg">
      <span>{{ direction }}</span> <span>{{ degree }}°</span>
    </div>
    
    <div class="controls">
      <button class="button stop-btn">
        <i class="icon-compass"></i> {{ $t('compass.stopCompass') }}
      </button>
      <div class="toggle-container">
        <span>{{ $t('compass.locationServices') }}</span>
        <div class="toggle"></div>
      </div>
    </div>
    
    <div class="location-note">
      {{ $t('compass.locationNote') }}
    </div>
    
    <div class="info-section">
    <div class="info-box">
      <div class="title_box">
        <h2>{{ $t('compass.locationInfo') }}</h2>
      </div>
      <div class="info-content locations-info">
        <div class="latitude">
          <span>{{ $t('compass.latitude') }}:</span> <span>{{ userLatitude || 0 }}</span>
        </div>
        <div class="longitude">
          <span>{{ $t('compass.longitude') }}:</span> <span>{{ userLongitude || 0 }}</span>
        </div>
        <div class="location">
          <span>{{ $t('compass.location') }}:</span> <span>{{ location || $t('compass.unknown') }}</span>
        </div>
        <div class="sea_level">
          <span>{{ $t('compass.height') }}:</span> <span>{{ altitude || '0 m = 0 ft' }}</span>
        </div>
      </div>
      
      <div class="title_box">
        <h2>{{ $t('compass.sunInfo') }}</h2>
      </div>
      <div class="info-content">
        <div class="locations-info">
          <div class="sunrise">
            <span>{{ $t('compass.sunrise') }}:</span> <span>{{ sunrise || '00:00:00' }}</span>
          </div>
          <div class="sunset">
            <span>{{ $t('compass.sunset') }}:</span> <span>{{ sunset || '00:00:00' }}</span>
          </div>
        </div>
      </div>
      
      <div class="title_box">
        <h2>{{ $t('compass.qiblaDirection') }}</h2>
      </div>
      <div class="info-content">
        <div id="qibla-direction" style="text-align: center;">
          {{ $t('compass.enableLocation') }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IslamicCompass',
  data() {
    return {
      qiblaDirection: 0,
      userLatitude: 0,
      userLongitude: 0,
      // Coordinates for Kaaba in Mecca
      kaabaLatitude: 21.4225,
      kaabaLongitude: 39.8262,
      isFacingQibla: false,
      direction: 'N',
      degree: 0,
      location: '',
      altitude: '',
      sunrise: '',
      sunset: '',
      isQiblaLoading: false
    }
  },
  // Add i18n translations
  i18n: {
    messages: {
      en: {
        qibla: 'QIBLA',
        stopCompass: 'Stop Compass',
        locationServices: 'Location Services',
        locationInfo: 'Location Information',
        latitude: 'Latitude',
        longitude: 'Longitude',
        location: 'Location',
        height: 'Height (AMSL)',
        sunInfo: 'Sun Information',
        sunrise: 'Sunrise',
        sunset: 'Sunset',
        qiblaDirection: 'Qibla Direction',
        enableLocation: 'Enable location services to display Qibla direction',
        unknown: 'Unknown',
        qiblaIs: 'Qibla is',
        fromYourLocation: 'from your location',
        distanceToMecca: 'Distance to Mecca',
        compassStopped: 'Compass Stopped',
        grantPermission: 'To access this feature, permission must be granted',
        notSupported: 'The required permission is not supported on your device',
        deviceOrientationNotSupported: 'Device orientation is not supported on your device',
        permissionDenied: 'User denied the request for Geolocation.',
        positionUnavailable: 'The location information is not available.',
        timeout: 'The attempt to obtain location has timed out.',
        locationNote: 'Location needs to be enabled for the qibla to appear',
        calculatingQibla: 'Calculating Qibla direction...'
      },
      ar: {
        qibla: 'قِبْلَة',
        stopCompass: 'إيقاف البوصلة',
        locationServices: 'خدمات الموقع',
        locationInfo: 'معلومات الموقع',
        latitude: 'خط العرض',
        longitude: 'خط الطول',
        location: 'الموقع',
        height: 'الارتفاع',
        sunInfo: 'معلومات الشمس',
        sunrise: 'شروق الشمس',
        sunset: 'غروب الشمس',
        qiblaDirection: 'اتجاه القبلة',
        enableLocation: 'تمكين خدمات الموقع لعرض اتجاه القبلة',
        unknown: 'غير معروف',
        qiblaIs: 'اتجاه القبلة هو',
        fromYourLocation: 'من موقعك',
        distanceToMecca: 'المسافة إلى مكة',
        compassStopped: 'تم إيقاف البوصلة',
        grantPermission: 'للوصول إلى هذه الميزة، يجب منح الإذن',
        notSupported: 'الإذن المطلوب غير مدعوم على جهازك',
        deviceOrientationNotSupported: 'توجيه الجهاز غير مدعوم على جهازك',
        permissionDenied: 'رفض المستخدم طلب تحديد الموقع الجغرافي.',
        positionUnavailable: 'معلومات الموقع غير متاحة.',
        timeout: 'انتهت مهلة محاولة الحصول على الموقع.',
        locationNote: 'يجب تمكين خدمات الموقع لعرض اتجاه القبلة'
      },
      ku: {
        qibla: 'قیبلە',
        stopCompass: 'ڕاگرتنی قیبلەنما',
        locationServices: 'خزمەتگوزاریەکانی شوێن',
        locationInfo: 'زانیاری شوێن',
        latitude: 'هێڵی پانی',
        longitude: 'هێڵی درێژی',
        location: 'شوێن',
        height: 'بەرزی',
        sunInfo: 'زانیاری خۆر',
        sunrise: 'هەڵاتنی خۆر',
        sunset: 'ئاوابوونی خۆر',
        qiblaDirection: 'ئاڕاستەی قیبلە',
        enableLocation: 'خزمەتگوزاریەکانی شوێن چالاک بکە بۆ نیشاندانی ئاڕاستەی قیبلە',
        unknown: 'نەزانراو',
        qiblaIs: 'قیبلە',
        fromYourLocation: 'لە شوێنی تۆوە',
        distanceToMecca: 'دووری بۆ مەککە',
        compassStopped: 'قیبلەنما ڕاگیرا',
        grantPermission: 'بۆ بەکارهێنانی ئەم تایبەتمەندیە، دەبێت ڕێگەپێدان بدرێت',
        deviceOrientationNotSupported: 'ئاڕاستەی ئامێر لەسەر ئامێرەکەت پشتگیری ناکرێت',
        permissionDenied: 'بەکارهێنەر داواکاری شوێنی جوگرافی ڕەتکردەوە.',
        positionUnavailable: 'زانیاری شوێن بەردەست نیە.',
        timeout: 'هەوڵدان بۆ بەدەستهێنانی شوێن کاتی تەواو بوو.',
        locationNote: 'پێویستە خزمەتگوزاریەکانی شوێن چالاک بکرێت بۆ دەرکەوتنی قیبلە'
      },
      fa: {
        qibla: 'قبله',
        stopCompass: 'توقف قطب‌نما',
        locationServices: 'خدمات مکان',
        locationInfo: 'اطلاعات مکان',
        latitude: 'عرض جغرافیایی',
        longitude: 'طول جغرافیایی',
        location: 'موقعیت',
        height: 'ارتفاع',
        sunInfo: 'اطلاعات خورشید',
        sunrise: 'طلوع آفتاب',
        sunset: 'غروب آفتاب',
        qiblaDirection: 'جهت قبله',
        enableLocation: 'برای نمایش جهت قبله، خدمات مکان را فعال کنید',
        unknown: 'نامشخص',
        qiblaIs: 'قبله',
        fromYourLocation: 'از موقعیت شما',
        distanceToMecca: 'فاصله تا مکه',
        compassStopped: 'قطب‌نما متوقف شد',
        grantPermission: 'برای دسترسی به این ویژگی، باید اجازه داده شود',
        notSupported: 'مجوز مورد نیاز در دستگاه شما پشتیبانی نمی‌شود',
        deviceOrientationNotSupported: 'جهت‌گیری دستگاه در دستگاه شما پشتیبانی نمی‌شود',
        permissionDenied: 'کاربر درخواست موقعیت جغرافیایی را رد کرد.',
        positionUnavailable: 'اطلاعات مکان در دسترس نیست.',
        timeout: 'تلاش برای دریافت مکان به پایان رسید.',
        locationNote: 'برای نمایش قبله باید خدمات مکان فعال باشد'
      }
    }
  },
  methods: {
    // Helper methods for calculations
    toRadians(degrees) {
      return degrees * (Math.PI / 180);
    },
    toDegrees(radians) {
      return radians * (180 / Math.PI);
    },
    // Calculate distance between two coordinates using Haversine formula
    calculateDistance(lat1, lon1, lat2, lon2) {
      const R = 6371; // Earth's radius in km
      const dLat = this.toRadians(lat2 - lat1);
      const dLon = this.toRadians(lon2 - lon1);
      const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) * 
        Math.sin(dLon/2) * Math.sin(dLon/2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      const distance = R * c;
      return distance.toFixed(0); // Return in km
    },
    // Get location name from coordinates using Reverse Geocoding API
    getLocationName(latitude, longitude) {
      // Using OpenStreetMap Nominatim API for reverse geocoding (free and open-source)
      const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&zoom=10&accept-language=${this.$i18n.locale || 'en'}`;
      
      return fetch(url, {
        headers: {
          'Accept-Language': this.$i18n.locale || 'en',
          'User-Agent': 'IslamicCompass/1.0' // Required by Nominatim API
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // Extract relevant location information
        const city = data.address.city || data.address.town || data.address.village || '';
        const state = data.address.state || data.address.county || '';
        const country = data.address.country || '';
        
        // Create a formatted location string
        let locationString = '';
        if (city) locationString += city;
        if (state && state !== city) locationString += locationString ? `, ${state}` : state;
        if (country) locationString += locationString ? `, ${country}` : country;
        
        return locationString || this.$t('compass.unknown');
      })
      .catch(error => {
        console.error('Error fetching location name:', error);
        return this.$t('compass.unknown');
      });
    },
    // Get altitude information from coordinates
    getAltitude(latitude, longitude) {
      // Using Open Elevation API
      const url = `https://api.open-elevation.com/api/v1/lookup?locations=${latitude},${longitude}`;
      
      return fetch(url)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          if (data.results && data.results.length > 0) {
            const altitude = data.results[0].elevation;
            return `${altitude} m = ${(altitude / 0.3048).toFixed(2)} ft`;
          }
          throw new Error('No elevation data found');
        })
        .catch(error => {
          console.error('Error fetching altitude:', error);
          return '0 m = 0 ft';
        });
    }
  },
  mounted() {
    // Set viewport for better mobile experience
    if (!document.querySelector('meta[name="viewport"]')) {
      const metaViewport = document.createElement('meta');
      metaViewport.name = 'viewport';
      metaViewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
      document.head.appendChild(metaViewport);
    }
    
    // Store component reference to access in event handlers
    const self = this; 
    const compassCircle = document.querySelector(".compass-circle");
    const qiblaMarker = this.$refs.qiblaMarker;
    let compass;
    let degCompass;
    let direction;

    // Calculate Qibla direction
    const calculateQiblaDirection = (lat1, lon1) => {
      // Convert to radians
      const lat1Rad = self.toRadians(lat1);
      const lon1Rad = self.toRadians(lon1);
      const lat2Rad = self.toRadians(self.kaabaLatitude);
      const lon2Rad = self.toRadians(self.kaabaLongitude);
      
      // Calculate the angle
      const y = Math.sin(lon2Rad - lon1Rad) * Math.cos(lat2Rad);
      const x = Math.cos(lat1Rad) * Math.sin(lat2Rad) - 
                Math.sin(lat1Rad) * Math.cos(lat2Rad) * Math.cos(lon2Rad - lon1Rad);
      let qiblaAngle = Math.atan2(y, x);
      
      // Convert to degrees
      qiblaAngle = self.toDegrees(qiblaAngle);
      
      // Normalize to 0-360
      qiblaAngle = (qiblaAngle + 360) % 360;
      
      self.qiblaDirection = qiblaAngle;
      return qiblaAngle;
    };

    function getDirection(compass) {
      if (compass >= 0 && compass < 22.5) {
        return "N";
      } else if (compass >= 22.5 && compass < 67.5) {
        return "NE";
      } else if (compass >= 67.5 && compass < 112.5) {
        return "E";
      } else if (compass >= 112.5 && compass < 157.5) {
        return "SE";
      } else if (compass >= 157.5 && compass < 202.5) {
        return "S";
      } else if (compass >= 202.5 && compass < 247.5) {
        return "SW";
      } else if (compass >= 247.5 && compass < 292.5) {
        return "W";
      } else if (compass >= 292.5 && compass < 337.5) {
        return "NW";
      } else {
        return "N";
      }
    }

    document.querySelector(".toggle")?.addEventListener("click", function(e) {
      e.preventDefault();
      this.classList.toggle("toggle-on");
      
      // Ensure the toggle has the right color when enabled
      if (this.classList.contains("toggle-on")) {
        this.style.backgroundColor = "#4CAF50";
        
        // Show loading state
        self.isQiblaLoading = true;
        
        navigator.geolocation.getCurrentPosition(
          function(position) {
            showPosition(position);
            
            // Start the compass
            startCompass();
            
            // Make the Qibla marker visible and hide loading after position is set
            if (qiblaMarker) {
              // Small delay to ensure smooth transition
              setTimeout(() => {
                self.isQiblaLoading = false;
                qiblaMarker.style.opacity = '1';
              }, 500);
            }
          },
          function(error) {
            self.isQiblaLoading = false;
            showError(error);
          }
        );
      } else {
        this.style.backgroundColor = "#ccc";
        // Hide the qibla marker when toggle is off
        if (qiblaMarker) {
          qiblaMarker.style.opacity = '0';
        }
        self.isQiblaLoading = false;
      }
    });

    function showPosition(position) {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;

      // Update component data
      self.userLatitude = latitude;
      self.userLongitude = longitude;

      // Calculate Qibla direction and update the marker
      const qiblaAngle = calculateQiblaDirection(latitude, longitude);
      
      // Calculate distance to Kaaba
      const distanceToKaaba = self.calculateDistance(
        latitude, 
        longitude, 
        self.kaabaLatitude, 
        self.kaabaLongitude
      );
      
      // Update Qibla info with angle and distance
      document.getElementById('qibla-direction').innerHTML = 
        `<p>${self.$t('compass.qiblaIs')} <strong>${Math.round(qiblaAngle)}°</strong> ${self.$t('compass.fromYourLocation')}</p>
         <p>${self.$t('compass.distanceToMecca')}: <strong>${distanceToKaaba} km</strong></p>`;

      // Update Qibla direction with backend API
      fetch(`/api/qibla/${latitude}/${longitude}/`)
        .then(response => response.json())
        .then(data => {
          if (data.direction) {
            self.qiblaDirection = parseFloat(data.direction);
            
            // Update Qibla info with API data
            document.getElementById('qibla-direction').innerHTML = 
              `<p>${self.$t('compass.qiblaIs')} <strong>${data.direction}°</strong> ${self.$t('compass.fromYourLocation')}</p>
               <p>${self.$t('compass.distanceToMecca')}: <strong>${distanceToKaaba} km</strong></p>`;
            
            // Position the Qibla marker on the compass circle
            positionQiblaMarker();
          }
        })
        .catch(error => {
          console.error('Error fetching qibla direction:', error);
          
          // Use calculated angle if API fails
          self.qiblaDirection = qiblaAngle;
          
          // Position the Qibla marker on the compass circle
          positionQiblaMarker();
        });

      // Get sunrise and sunset times
      const url = `https://api.sunrise-sunset.org/json?lat=${latitude}&lng=${longitude}&formatted=0`;
      fetch(url)
        .then(response => response.json())
        .then(data => {
          const sunrise = new Date(data.results.sunrise);
          const sunset = new Date(data.results.sunset);
          
          self.sunrise = sunrise.toLocaleTimeString();
          self.sunset = sunset.toLocaleTimeString();
        })
        .catch(error => {
          console.error('Error fetching sunrise/sunset:', error);
        });
      
      // Get location name using reverse geocoding
      self.getLocationName(latitude, longitude)
        .then(locationName => {
          self.location = locationName;
        });
      
      // Get altitude information
      self.getAltitude(latitude, longitude)
        .then(altitudeInfo => {
          self.altitude = altitudeInfo;
        });
    }

    function showError(error) {
      switch (error.code) {
        case error.PERMISSION_DENIED:
          alert(self.$t('compass.permissionDenied'));
          break;
        case error.POSITION_UNAVAILABLE:
          alert(self.$t('compass.positionUnavailable'));
          break;
        case error.TIMEOUT:
          alert(self.$t('compass.timeout'));
          break;
      }
    }

    const stopBtn = document.querySelector(".stop-btn");
    const isIOS =
      navigator.userAgent.match(/(iPod|iPhone|iPad)/) &&
      navigator.userAgent.match(/AppleWebKit/);

    function init() {
      // Change to stop button functionality
      document.querySelector(".stop-btn").addEventListener("click", stopCompass);
      
      // Open info boxes when clicked
      document.querySelectorAll('.title_box').forEach(element => {
        element.addEventListener("click", function() {
          element.classList.toggle("active");
        });
      });

      // Open the Qibla Direction info box by default to show information
      const qiblaInfoBox = document.querySelector('.title_box:nth-of-type(3)');
      if (qiblaInfoBox) {
        qiblaInfoBox.classList.add('active');
      }
      
      // Position the Qibla marker if we already have a direction
      if (self.qiblaDirection) {
        positionQiblaMarker();
      }

      // Start compass automatically
      startCompass();
    }

    function startCompass() {
      if (isIOS) {
        DeviceOrientationEvent.requestPermission()
          .then((response) => {
            if (response === "granted") {
              window.addEventListener("deviceorientation", handler, true);
            } else {
              alert(self.$t('compass.grantPermission'));
            }
          })
          .catch(() => alert(self.$t('compass.notSupported')));
      } else {
        // For non-iOS devices, just add the event listener
        window.addEventListener("deviceorientationabsolute", handler, true);
        if (!window.DeviceOrientationEvent) {
          alert(self.$t('compass.deviceOrientationNotSupported'));
        }
      }
    }

    function handler(e) {
      compass = e.webkitCompassHeading || Math.abs(e.alpha - 360);

      // Always update the compass - removed lock_location check
      var direction = getDirection(compass);
      
      // Update Vue reactive data
      self.direction = direction;
      self.degree = Math.round(compass * 100)/100;

      // Apply rotation to the compass circle
      // We need to invert the angle and apply the transform while preserving the centering
      const rotation = -compass;
      compassCircle.style.transform = `translate(-50%, -50%) rotate(${rotation}deg)`;
      
      // Reposition the Qibla marker if we have a direction
      if (self.qiblaDirection) {
        // Calculate Qibla relative to current heading
        const relativeQiblaAngle = (self.qiblaDirection - compass + 360) % 360;
        
        // Calculate position for the Qibla marker
        const radius = Math.min(compassCircle.offsetWidth, compassCircle.offsetHeight) * 0.35;
        const angle = relativeQiblaAngle * (Math.PI / 180); // Convert to radians
        
        // Calculate position using trigonometry
        const x = radius * Math.sin(angle);
        const y = -radius * Math.cos(angle); // Negative because Y is inverted in CSS
        
        // Update the Qibla marker position
        qiblaMarker.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
        
        // Check if user is facing Qibla (when device heading is close to Qibla direction)
        const angleDifference = Math.abs(((compass - self.qiblaDirection) + 360) % 360);
        self.isFacingQibla = angleDifference < 10 || angleDifference > 350;
        
        // Highlight the target when close to alignment
        const targetArrowLine = document.querySelector('.target-arrow-line');
        const targetArrowHead = document.querySelector('.target-arrow-head');
        if (targetArrowLine && targetArrowHead) {
          if (self.isFacingQibla) {
            targetArrowLine.classList.add('aligned');
            targetArrowHead.classList.add('aligned');
          } else {
            targetArrowLine.classList.remove('aligned');
            targetArrowHead.classList.remove('aligned');
          }
        }
      }
    }
    
    // Function to position the Qibla marker on the compass
    function positionQiblaMarker() {
      if (qiblaMarker && self.qiblaDirection) {
        // We need to place the marker directly on the compass at the Qibla direction
        // First, make sure it's visible
        qiblaMarker.style.opacity = '1';
        
        // Use pixel values for more precise positioning
        const compassSize = Math.min(compassCircle.offsetWidth, compassCircle.offsetHeight);
        const radius = compassSize * 0.35; // 35% of compass radius

        // If we have a compass heading, use relative positioning
        if (compass !== undefined) {
          // Calculate Qibla relative to current heading
          const relativeQiblaAngle = (self.qiblaDirection - compass + 360) % 360;
          const angle = relativeQiblaAngle * (Math.PI / 180); // Convert to radians
          
          // Calculate position using trigonometry
          const x = radius * Math.sin(angle);
          const y = -radius * Math.cos(angle); // Negative because Y is inverted in CSS
          
          // Set transform using translate
          qiblaMarker.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
        } else {
          // Use the absolute direction if we don't have compass data yet
          const angle = self.qiblaDirection * (Math.PI / 180); // Convert to radians
          
          // Calculate position using trigonometry
          const x = radius * Math.sin(angle);
          const y = -radius * Math.cos(angle); // Negative because Y is inverted in CSS
          
          // Set transform using translate
          qiblaMarker.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
        }
      }
    }

    function stopCompass() {
      // Remove compass event listeners
      window.removeEventListener("deviceorientationabsolute", handler, true);
      window.removeEventListener("deviceorientation", handler, true);
      document.querySelector(".stop-btn").innerHTML = `<i class="icon-compass"></i> ${self.$t('compass.compassStopped')}`;
      document.querySelector(".stop-btn").style.backgroundColor = "#888";
    }

    // Run initialization
    init();
  }
}
</script>

<style scoped>
/* Define color as a direct variable instead of using :root */
.islamic-compass-wrapper {
  --main-color: #4CAF50;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  padding: 10px;
}

/* Add loading spinner styles */
.qibla-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 40;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(76, 175, 80, 0.1);
  border-left-color: #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  margin-top: 10px;
  color: #4CAF50;
  font-size: 14px;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 12px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.toggle-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 5px 0;
}

.info-section {
  width: 100%;
}

.compass-container {
  position: relative;
  width: 300px;
  height: 300px;
  margin: 20px auto;
}
.compass {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  position: relative;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
}
.compass-circle {
  position: absolute;
  width: 90%;
  height: 90%;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="49" fill="white" stroke="%234CAF50" stroke-width="0.5"/><line x1="50" y1="1" x2="50" y2="10" stroke="%234CAF50" stroke-width="1.5"/><text x="50" y="16" text-anchor="middle" font-family="Arial" font-size="8" fill="%234CAF50">N</text><line x1="50" y1="99" x2="50" y2="90" stroke="%234CAF50" stroke-width="1.5"/><text x="50" y="87" text-anchor="middle" font-family="Arial" font-size="8" fill="%234CAF50">S</text><line x1="1" y1="50" x2="10" y2="50" stroke="%234CAF50" stroke-width="1.5"/><text x="16" y="53" text-anchor="middle" font-family="Arial" font-size="8" fill="%234CAF50">W</text><line x1="99" y1="50" x2="90" y2="50" stroke="%234CAF50" stroke-width="1.5"/><text x="84" y="53" text-anchor="middle" font-family="Arial" font-size="8" fill="%234CAF50">E</text><circle cx="50" cy="50" r="2" fill="%234CAF50"/></svg>');
  background-size: cover;
  transform-origin: center;
  transition: transform 0.3s ease;
}
.target-marker {
  position: absolute;
  top: 2%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 30;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.target-arrow-line {
  width: 2px;
  height: 20px;
  background-color: #00c853;
  animation: pulse-arrow 1.5s infinite alternate;
}
.target-arrow-head {
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 10px solid #00c853;
  margin-top: -1px;
  animation: pulse-arrow 1.5s infinite alternate;
}
@keyframes pulse-arrow {
  from {
    transform: translateY(0);
    filter: drop-shadow(0 0 3px white);
  }
  to {
    transform: translateY(5px);
    filter: drop-shadow(0 0 5px white);
  }
}
.target-arrow-line.aligned,
.target-arrow-head.aligned {
  animation: pulse-arrow-aligned 1s infinite alternate;
}
@keyframes pulse-arrow-aligned {
  from {
    transform: translateY(0) scale(1);
    filter: drop-shadow(0 0 5px #00c853);
  }
  to {
    transform: translateY(5px) scale(1.2);
    filter: drop-shadow(0 0 15px #00c853);
  }
}
.qibla-marker {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.5s ease;
  z-index: 25;
  pointer-events: none;
  top: 50%;
  left: 50%;
  transition: transform 0.3s ease;
}
.qibla-icon {
  font-size: 22px;
  text-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
  margin-bottom: 5px;
  filter: drop-shadow(0 0 5px white);
}
.qibla-label {
  font-size: 12px;
  font-weight: bold;
  color: #4CAF50;
  background-color: white;
  padding: 2px 6px;
  border-radius: 10px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  text-align: center;
  white-space: nowrap;
}
.toggle.toggle-on ~ .compass-container .qibla-marker,
.compass-container .qibla-marker.active {
  opacity: 1;
}
.check-icon {
  display: inline-block;
  color: white;
  font-weight: bold;
  background-color: #00c853;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  line-height: 20px;
  text-align: center;
}
.center-dot {
  position: absolute;
  width: 8px;
  height: 8px;
  background-color: #4CAF50;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 20;
}

/* Enhanced media queries */
@media (max-width: 480px) {
  .compass-container {
    width: 280px;
    height: 280px;
    margin: 15px auto;
  }
  
  .deg {
    margin: 15px 0;
    font-size: 20px;
  }
  
  .info-box {
    padding: 12px;
    margin-top: 15px;
  }
  
  .button {
    padding: 12px 10px;
    min-height: 44px; /* Minimum touch target size */
  }
  
  .locations-info {
    font-size: 14px;
  }
  
  .toggle {
    min-height: 30px; /* Ensure toggle is touch-friendly */
  }
}

.location-note {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-top: 5px;
  margin-bottom: 15px;
  padding: 0 15px;
  font-style: italic;
}
.controls {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 90%;
  max-width: 350px;
  margin-left: auto;
  margin-right: auto;
}
.info-box {
  margin-top: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  width: 90%;
  max-width: 350px;
  background-color: white;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}
.title_box {
  margin-bottom: 12px;
  cursor: pointer;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}
.title_box h2 {
  margin: 0;
  font-size: 16px;
  color: #4CAF50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}
.title_box h2::after {
  content: '▼';
  font-size: 12px;
}
.title_box.active h2::after {
  content: '▲';
}
.info-content {
  display: none;
}
.title_box.active + .info-content {
  display: block;
}
.deg {
  font-size: 24px;
  font-weight: bold;
  color: #4CAF50;
  text-align: center;
  margin: 15px 0;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 30px;
  padding: 5px 15px;
  display: inline-block;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 12px 15px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 500;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: background-color 0.2s ease, transform 0.1s ease;
}
.button:active {
  transform: translateY(1px);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}
.button i {
  font-size: 18px;
}
.toggle {
  position: relative;
  width: 60px;
  height: 30px;
  border-radius: 15px;
  background-color: #ccc;
  cursor: pointer;
  transition: background-color 0.3s;
}
.toggle::after {
  content: '';
  position: absolute;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  top: 2px;
  left: 2px;
  background-color: white;
  transition: transform 0.3s;
}
.toggle.toggle-on {
  background-color: #4CAF50; /* Set direct color instead of using var */
}
.toggle.toggle-on::after {
  transform: translateX(30px);
}
.locations-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 15px;
}
.locations-info div {
  display: flex;
  justify-content: space-between;
  padding: 2px 0;
}
.locations-info span {
  font-weight: bold;
}
.colors {
  display: none;
  position: absolute;
  top: 50px;
  right: 10px;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  padding: 10px;
}
.colors.active {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}
.color {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  cursor: pointer;
}
.color.active {
  border: 2px solid black;
}
.lang {
  display: none;
  position: absolute;
  top: 50px;
  left: 10px;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  padding: 10px;
}
.lang.active {
  display: block;
}
</style>