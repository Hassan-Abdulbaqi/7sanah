<template>
  <div class="app-container">
    <header class="app-header">
      <div class="logo" @click="navigateTo('home')">
        <span class="logo-text">7sanah</span>
      </div>
      
      <!-- Mobile menu toggle button - only visible on mobile -->
      <button class="mobile-menu-toggle" @click="toggleMobileMenu" aria-label="Toggle menu">
        <span class="menu-bar"></span>
        <span class="menu-bar"></span>
        <span class="menu-bar"></span>
      </button>
      
      <!-- Responsive navigation -->
      <nav class="main-nav">
        <div 
          v-for="item in navItems" 
          :key="item.id"
          :class="['nav-item', { active: currentPage === item.id }]"
          @click="navigateAndCloseMenu(item.id)"
        >
          <div class="nav-icon">
            <component :is="item.icon" />
          </div>
          <span class="nav-text">{{ item.name }}</span>
        </div>
      </nav>
      
      <!-- Language switcher (visible on desktop) -->
      <LanguageSwitcher class="language-switcher" />
      
      <!-- Mobile Menu Container -->
      <div class="mobile-menu-container" :class="{ 'open': mobileMenuOpen }">
        <!-- Close button for mobile -->
        <div class="mobile-menu-close" @click="closeMobileMenu">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        
        <!-- Mobile navigation items -->
        <div class="mobile-nav-items">
          <div 
            v-for="item in navItems" 
            :key="item.id"
            :class="['mobile-nav-item', { active: currentPage === item.id }]"
            @click="navigateAndCloseMenu(item.id)"
          >
            <div class="nav-icon">
              <component :is="item.icon" />
            </div>
            <span class="nav-text">{{ item.name }}</span>
          </div>
          
          <!-- Language switcher in mobile menu -->
          <div class="mobile-language">
            <LanguageSwitcher />
          </div>
        </div>
      </div>
      
      <!-- Mobile menu overlay -->
      <div 
        v-if="mobileMenuOpen" 
        class="mobile-menu-overlay"
        @click="closeMobileMenu"
      ></div>
    </header>

    <main class="main-content">
      <!-- Wrap content in transition group -->
      <transition name="fade" mode="out-in">
        <!-- Home/Landing Page -->
        <div v-if="currentPage === 'home'" class="page-container landing-page amiri-font" :key="'home'">
          <div class="hero-section">
            <h1 class="app-title">{{ $t('app.title') }}</h1>
            <p class="app-description">{{ $t('app.description') }}</p>
            <div class="feature-grid">
              <div 
                v-for="feature in features" 
                :key="feature.id" 
                class="feature-card"
                @click="navigateTo(feature.id)"
              >
                <div class="feature-icon">
                  <component :is="feature.icon" />
                </div>
                <h3 class="feature-title">{{ feature.name }}</h3>
                <p class="feature-description">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Khatmah Page -->
        <div v-else-if="currentPage === 'khatmah'" class="page-container" :key="'khatmah'">
          <!-- Create new Khatmah button -->
          <div v-if="khatmahView === 'list'" class="mb-6 flex justify-between items-center">
            <h2 class="text-2xl font-bold text-gray-800">{{ $t('khatmahList.title') }}</h2>
            <button
              @click="khatmahView = 'create'"
              class="flex items-center px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
              {{ $t('khatmahList.createNew') }}
            </button>
          </div>

          <!-- Nested transition for khatmah views -->
          <transition name="slide" mode="out-in">
            <!-- Khatmah List -->
            <KhatmahList
              v-if="khatmahView === 'list'"
              :key="'khatmah-list'"
              :khatmahs="store.khatmahs"
              @select-khatmah="selectKhatmah"
            />
            
            <!-- Create Khatmah Form -->
            <CreateKhatmah
              v-else-if="khatmahView === 'create'"
              :key="'khatmah-create'"
              @khatmah-created="onKhatmahCreated"
              @cancel="khatmahView = 'list'"
            />
            
            <!-- Edit Khatmah Form -->
            <EditKhatmah
              v-else-if="khatmahView === 'edit'"
              :key="'khatmah-edit'"
              :khatmah-id="selectedKhatmahId"
              @khatmah-updated="onKhatmahUpdated"
              @cancel="khatmahView = 'detail'"
            />
            
            <!-- Khatmah Detail View -->
            <KhatmahDetail
              v-else-if="khatmahView === 'detail'"
              :key="'khatmah-detail'"
              :khatmah-id="selectedKhatmahId"
              @edit-khatmah="editKhatmah"
              @cancel="khatmahView = 'list'"
              @navigate-to-surah="navigateToSurah"
            />
          </transition>
        </div>

        <!-- Calendar Page -->
        <div v-else-if="currentPage === 'calendar'" class="page-container" :key="'calendar'">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">{{ $t('nav.calendar') }}</h2>
          <HijriCalendar />
        </div>

        <!-- Qibla Compass Page -->
        <div v-else-if="currentPage === 'qibla'" class="page-container" :key="'qibla'">
          <IslamicCompass />
        </div>

        <!-- Age Calculator Page -->
        <div v-else-if="currentPage === 'age-calculator'" class="page-container" :key="'age-calculator'">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">{{ $t('features.ageCalculator.title') }}</h2>
          <AgeCalculator />
        </div>

        <!-- Tasbeeh Counter Page -->
        <div v-else-if="currentPage === 'tasbeeh'" class="page-container" :key="'tasbeeh'">
          <TasbeehCounter />
        </div>
        
        <!-- Quran Reader Page -->
        <div v-else-if="currentPage === 'quran'" class="page-container" :key="'quran'">
          <QuranReader />
        </div>
        
        <!-- Quran Search Page -->
        <div v-else-if="currentPage === 'quran-search'" class="page-container" :key="'quran-search'">
          <QuranSearch @navigate-to-verse="navigateToVerse" />
        </div>

        <!-- Quran Book Page -->
        <div v-else-if="currentPage === 'quran-book'" class="full-width-container" :key="'quran-book'">
          <QuranBook />
        </div>

        <!-- Prayer Times Page -->
        <div v-else-if="currentPage === 'prayer-times'" class="page-container" :key="'prayer-times'">
          <PrayerTimes />
        </div>
      </transition>
    </main>

    <footer class="app-footer">
      <p>&copy; {{ new Date().getFullYear() }} 7sanah. {{ $t('app.rights_reserved') }}</p>
    </footer>
    
    <!-- Add the notification component -->
    <Notification ref="notification" />
  </div>
</template>

<script>
import { BookOutline, CalendarOutline, CompassOutline, HomeOutline, CalculatorOutline, TimeOutline } from '@vicons/ionicons5'
import KhatmahList from './components/KhatmahList.vue'
import KhatmahDetail from './components/KhatmahDetail.vue'
import CreateKhatmah from './components/CreateKhatmah.vue'
import EditKhatmah from './components/EditKhatmah.vue'
import HijriCalendar from './components/HijriCalendar.vue'
import QiblaCompass from './components/QiblaCompass.vue'
import IslamicCompass from './components/IslamicCompass.vue'
import AgeCalculator from './components/AgeCalculator.vue'
import TasbeehCounter from './components/TasbeehCounter.vue'
import QuranReader from './components/QuranReader.vue'
import QuranSearch from './components/QuranSearch.vue'
import QuranBook from './components/quran/views/BookView.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
import Notification from './components/Notification.vue'
import TasbeehIcon from './components/icons/TasbeehIcon.vue'
import QuranIcon from './components/icons/QuranIcon.vue'
import PrayerTimes from './components/PrayerTimes.vue'
import { store } from './store'
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'App',
  components: {
    KhatmahList,
    KhatmahDetail,
    CreateKhatmah,
    EditKhatmah,
    HijriCalendar,
    QiblaCompass,
    IslamicCompass,
    AgeCalculator,
    TasbeehCounter,
    QuranReader,
    QuranSearch,
    QuranBook,
    LanguageSwitcher,
    Notification,
    BookOutline,
    CalendarOutline,
    CompassOutline,
    HomeOutline,
    CalculatorOutline,
    TimeOutline,
    TasbeehIcon,
    QuranIcon,
    PrayerTimes
  },
  data() {
    return {
      currentPage: 'home',
      khatmahView: 'list',
      selectedKhatmahId: null,
      store,
      mobileMenuOpen: false
    }
  },
  computed: {
    navItems() {
      return [
        { id: 'home', name: this.$t('nav.home'), icon: HomeOutline },
        { id: 'khatmah', name: this.$t('nav.khatmah'), icon: BookOutline },
        { id: 'calendar', name: this.$t('nav.calendar'), icon: CalendarOutline },
        { id: 'qibla', name: this.$t('nav.qibla'), icon: CompassOutline },
        { id: 'prayer-times', name: this.$t('nav.prayerTimes'), icon: TimeOutline },
        { id: 'tasbeeh', name: this.$t('nav.tasbeeh'), icon: TasbeehIcon },
        { id: 'quran', name: this.$t('nav.quran'), icon: QuranIcon }
      ]
    },
    features() {
      return [
        { 
          id: 'khatmah',
          name: this.$t('features.khatmah.title'),
          description: this.$t('features.khatmah.description'),
          icon: BookOutline
        },
        { 
          id: 'calendar',
          name: this.$t('features.calendar.title'),
          description: this.$t('features.calendar.description'),
          icon: CalendarOutline
        },
        { 
          id: 'qibla',
          name: this.$t('features.qibla.title'),
          description: this.$t('features.qibla.description'),
          icon: CompassOutline
        },
        {
          id: 'prayer-times',
          name: this.$t('features.prayerTimes.title'),
          description: this.$t('features.prayerTimes.description'),
          icon: TimeOutline
        },
        { 
          id: 'age-calculator',
          name: this.$t('features.ageCalculator.title'),
          description: this.$t('features.ageCalculator.description'),
          icon: CalculatorOutline
        },
        { 
          id: 'tasbeeh',
          name: this.$t('features.tasbeeh.title'),
          description: this.$t('features.tasbeeh.description'),
          icon: TasbeehIcon
        },
        { 
          id: 'quran',
          name: this.$t('features.quran.title'),
          description: this.$t('features.quran.description'),
          icon: QuranIcon
        }
      ]
    }
  },
  created() {
    console.log('App created - checking route:', this.$route.path)
    
    // Initialize store with data migrations
    store.init()
    
    this.initializeFromRoute(this.$route)
  },
  mounted() {
    console.log('App mounted - current state:', {
      page: this.currentPage,
      khatmahView: this.khatmahView,
      khatmahId: this.selectedKhatmahId,
      route: this.$route.path
    })
    
    // Connect notification component to global notification service
    if (this.$refs.notification) {
      this.$notification.info = this.$refs.notification.info
      this.$notification.success = this.$refs.notification.success
      this.$notification.warning = this.$refs.notification.warning
      this.$notification.error = this.$refs.notification.error
      this.$notification.clearAll = this.$refs.notification.removeAll
    }
  },
  watch: {
    // Watch for route changes
    $route(to, from) {
      console.log(`Route changed from ${from.path} to ${to.path}`)
      this.initializeFromRoute(to)
    }
  },
  methods: {
    // Initialize state based on the current route
    async initializeFromRoute(route) {
      console.log('Initializing from route:', route.path, 'Meta:', route.meta)
      
      // For direct khatmah detail access
      if (route.name === 'khatmah-detail') {
        console.log('Processing khatmah detail route with ID:', route.params.id)
        this.currentPage = 'khatmah'
        this.khatmahView = 'detail'
        this.selectedKhatmahId = route.params.id
        
        // Load khatmah data
        await this.loadKhatmahDetail(route.params.id)
        return
      }
      
      // General page navigation based on route name
      switch (route.name) {
        case 'home':
          this.currentPage = 'home'
          break
        case 'khatmah':
          this.currentPage = 'khatmah'
          this.khatmahView = 'list'
          this.selectedKhatmahId = null
          this.store.fetchKhatmahs()
          break
        case 'calendar':
          this.currentPage = 'calendar'
          break
        case 'qibla':
          this.currentPage = 'qibla'
          break
        case 'prayer-times':
          this.currentPage = 'prayer-times'
          break
        case 'age-calculator':
          this.currentPage = 'age-calculator'
          break
        case 'tasbeeh':
          this.currentPage = 'tasbeeh'
          break
        case 'quran':
          this.currentPage = 'quran'
          break
        case 'quran-book':
          this.currentPage = 'quran-book'
          break
        case 'quran-search':
          this.currentPage = 'quran-search'
          break
      }
    },
    
    // Navigation methods
    navigateTo(pageId) {
      console.log('Navigating to page:', pageId)
      
      // Update URL using named routes
      if (pageId === 'home') {
        this.$router.push({ name: 'home' })
      } else {
        this.$router.push({ name: pageId })
      }
    },
    
    selectKhatmah(khatmahId) {
      console.log('Selecting khatmah:', khatmahId)
      
      // Update URL using named route
      this.$router.push({ 
        name: 'khatmah-detail', 
        params: { id: khatmahId }
      })
    },
    
    async loadKhatmahDetail(khatmahId) {
      console.log('Loading khatmah detail with ID:', khatmahId)
      
      if (!khatmahId) {
        console.error('Cannot load khatmah detail: No ID provided')
        return
      }
      
      try {
        console.log('Fetching khatmah data from API')
        await this.store.fetchKhatmah(khatmahId)
        
        if (!this.store.currentKhatmah) {
          console.error(`Failed to load khatmah with ID: ${khatmahId}`)
          this.khatmahView = 'list'
          this.selectedKhatmahId = null
          return
        }
        
        console.log('Khatmah data loaded successfully:', this.store.currentKhatmah.name)
      } catch (error) {
        console.error(`Error loading khatmah: ${error}`)
        this.khatmahView = 'list'
        this.selectedKhatmahId = null
      }
    },
    
    editKhatmah(khatmahId) {
      this.selectedKhatmahId = khatmahId
      this.khatmahView = 'edit'
    },
    
    onKhatmahCreated(khatmah) {
      console.log('Khatmah created:', khatmah.id)
      
      // Navigate to the detail view
      this.$router.push({ 
        name: 'khatmah-detail', 
        params: { id: khatmah.id }
      })
    },
    
    onKhatmahUpdated() {
      this.khatmahView = 'detail'
    },
    
    navigateToVerse(verse) {
      console.log('Navigating to verse:', verse)
      
      try {
        // Validate the verse data
        if (!verse || typeof verse !== 'object' || !verse.surah || !verse.verse) {
          console.error('Invalid verse data for navigation:', verse)
          this.$notification?.error?.(this.$t('quran.invalidVerseData'))
          return
        }
        
        // First, ensure that we're on the Quran page
        if (this.currentPage !== 'quran') {
          // Set current page to Quran Reader
          this.navigateTo('quran')
          
          // We'll use localStorage to pass the verse information, but we also need
          // to give the component time to mount before attempting to navigate
          setTimeout(() => {
            this.passVerseToQuranReader(verse)
          }, 300) // Short delay to allow the page transition
        } else {
          // We're already on the Quran page, pass the data directly
          this.passVerseToQuranReader(verse)
        }
      } catch (error) {
        console.error('Error during navigation to verse:', error)
        // If using notification system
        if (this.$notification) {
          this.$notification.error(this.$t('quran.navigationError') || 'Navigation error. Please try again.')
        }
      }
    },
    
    passVerseToQuranReader(verse) {
      try {
        // Pass the verse information to the Quran Reader component via localStorage
        localStorage.setItem('quranNavigationTarget', JSON.stringify({
          surah: verse.surah,
          verse: verse.verse,
          edition: verse.edition || null,
          timestamp: new Date().getTime() // Add timestamp to ensure freshness
        }))
        
        // Dispatch a custom event to notify QuranReader that navigation data is available
        window.dispatchEvent(new CustomEvent('quran-navigation', {
          detail: {
            surah: parseInt(verse.surah),
            verse: parseInt(verse.verse),
            edition: verse.edition || null
          }
        }))
        
        console.log('Verse navigation data passed to QuranReader component', {
          surah: parseInt(verse.surah),
          verse: parseInt(verse.verse)
        })
      } catch (storageError) {
        console.error('Error storing verse navigation data:', storageError)
        // Try an alternative approach if localStorage fails
        // The QuranReader can potentially check URL parameters as fallback
        this.$router.push({ 
          name: 'quran', 
          query: { surah: verse.surah, verse: verse.verse }
        })
      }
    },
    
    // Handle navigation to a specific surah from KhatmahDetail
    navigateToSurah(surahData) {
      console.log('Navigating to surah:', surahData);
      
      try {
        // Validate the surah data
        if (!surahData || typeof surahData !== 'object' || !surahData.surah) {
          console.error('Invalid surah data for navigation:', surahData);
          this.$notification?.error?.(this.$t('quran.invalidSurahData') || 'Invalid surah data');
          return;
        }
        
        // First, ensure that we're on the Quran page
        if (this.currentPage !== 'quran') {
          // Set current page to Quran Reader
          this.navigateTo('quran');
          
          // Use setTimeout to allow the Quran component to mount
          setTimeout(() => {
            this.passSurahToQuranReader(surahData);
          }, 300); // Short delay to allow the page transition
        } else {
          // We're already on the Quran page, pass the data directly
          this.passSurahToQuranReader(surahData);
        }
      } catch (error) {
        console.error('Error during navigation to surah:', error);
        // If using notification system
        if (this.$notification) {
          this.$notification.error(this.$t('quran.navigationError') || 'Navigation error. Please try again.');
        }
      }
    },
    
    passSurahToQuranReader(surahData) {
      try {
        // Pass the surah information to the Quran Reader component via localStorage
        localStorage.setItem('quranNavigationTarget', JSON.stringify({
          surah: surahData.surah,
          verse: null, // Explicitly set to null to indicate no specific verse
          timestamp: new Date().getTime() // Add timestamp to ensure freshness
        }));
        
        // Dispatch a custom event to notify QuranReader that navigation data is available
        window.dispatchEvent(new CustomEvent('quran-navigation', {
          detail: {
            surah: parseInt(surahData.surah),
            verse: null // Explicitly set to null to indicate no specific verse
          }
        }));
        
        console.log('Surah navigation data passed to QuranReader component', {
          surah: parseInt(surahData.surah),
          verse: null // Logging the null to be clear about intent
        });
      } catch (storageError) {
        console.error('Error storing surah navigation data:', storageError);
        // Try an alternative approach if localStorage fails
        this.$router.push({ 
          name: 'quran', 
          query: { surah: surahData.surah }
        });
      }
    },
    
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen;
      
      // Prevent body scrolling when menu is open
      if (this.mobileMenuOpen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    },
    
    closeMobileMenu() {
      this.mobileMenuOpen = false;
      document.body.style.overflow = '';
    },
    
    navigateAndCloseMenu(pageId) {
      this.navigateTo(pageId);
      this.closeMobileMenu();
    }
  }
}
</script>

<style>
/* Adding :root with CSS variables including RGB primary color */
:root {
  --primary-color: #10b981;
  --primary-color-rgb: 16, 185, 129; /* RGB values of #10b981 for opacity */
  --primary-hover: #059669;
  --primary-light: rgba(16, 185, 129, 0.1);
  --primary-bg: rgba(16, 185, 129, 0.15);
  --hover-color: rgba(0, 0, 0, 0.05);
  --bg-color: #f9fafb;
  --card-bg: #ffffff;
  --text-color: #1f2937;
  --text-secondary: #6b7280;
  --border-color: #e5e7eb;
  --input-bg: #f9fafb;
  --arabic-font: 'Amiri', 'Noto Sans Arabic', serif;
}

/* Arabic text styling */
.arabic-text, [lang="ar"] {
  font-family: var(--arabic-font);
}

/* Apply Amiri font for RTL content */
[dir="rtl"] {
  font-family: var(--arabic-font);
}

/* Apply Amiri font to home page */
.amiri-font,
.amiri-font * {
  font-family: var(--arabic-font);
}

/* Special styling for home page with Amiri font */
.amiri-font .app-title {
  font-weight: 700;
  letter-spacing: -0.5px;
}

.amiri-font .app-description {
  line-height: 1.7;
  font-size: 1.3rem;
}

.amiri-font .feature-title {
  font-weight: 700;
  font-size: 1.3rem;
}

.amiri-font .feature-description {
  line-height: 1.6;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-color);
}

.app-header {
  display: flex;
  align-items: center;
  background-color: var(--card-bg);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 0 2rem;
  height: 4rem;
  border-bottom: 1px solid var(--border-color);
}

.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin-right: 1.5rem;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color);
  margin-left: 0.5rem;
}

/* Mobile menu toggle */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 21px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 10;
}

.menu-bar {
  width: 30px;
  height: 3px;
  background-color: var(--primary-color);
  border-radius: 3px;
  transition: all 0.3s ease;
}

/* Desktop Navigation */
.main-nav {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
  justify-content: center;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  height: 2.5rem;
}

.nav-item:hover {
  background-color: var(--hover-color);
}

.nav-item.active {
  color: var(--primary-color);
  background-color: var(--primary-bg);
}

.nav-icon {
  width: 1.25rem;
  height: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-icon svg {
  width: 100%;
  height: 100%;
}

/* Language Switcher Positioning */
.language-switcher {
  position: relative;
  z-index: 20;
  margin-left: 1.5rem;
}

/* Mobile Menu Container */
.mobile-menu-container {
  display: none;
  position: fixed;
  top: 0;
  right: -100%;
  width: 80%;
  max-width: 300px;
  height: 100vh;
  background-color: var(--card-bg);
  box-shadow: -5px 0 15px rgba(0, 0, 0, 0.1);
  padding: 5rem 1.5rem 2rem;
  transition: right 0.3s ease;
  z-index: 50;
  overflow-y: auto;
}

.mobile-menu-container.open {
  right: 0;
}

.mobile-nav-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-nav-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.mobile-nav-item:hover {
  background-color: var(--hover-color);
}

.mobile-nav-item.active {
  color: var(--primary-color);
  background-color: var(--primary-bg);
}

.mobile-language {
  padding: 1rem 0;
  border-top: 1px solid var(--border-color);
  margin-top: 1rem;
  width: 100%;
  display: flex;
  justify-content: center;
}

/* Mobile menu close button */
.mobile-menu-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  color: var(--text-color);
  cursor: pointer;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.mobile-menu-close:hover {
  background-color: var(--hover-color);
}

/* Mobile menu overlay */
.mobile-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 40;
}

/* Media queries for responsive design */
@media (max-width: 768px) {
  .app-header {
    padding: 0 1rem;
    justify-content: space-between;
  }
  
  .mobile-menu-toggle {
    display: flex;
    order: 3;
  }
  
  .main-nav {
    display: none;
  }
  
  .mobile-menu-container {
    display: block;
  }
  
  /* Hide desktop language switcher on mobile */
  .app-header > .language-switcher {
    display: none;
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  /* Make main content padding responsive */
  .main-content {
    padding: 1rem;
  }
}

.main-content {
  flex: 1;
  padding: 2rem;
}

.page-container {
  max-width: 1200px;
  margin: 0 auto;
}

.landing-page {
  text-align: center;
}

.hero-section {
  padding: 3rem 0;
}

.app-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.app-description {
  font-size: 1.25rem;
  margin-bottom: 3rem;
  color: var(--text-secondary);
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 3rem;
  height: 3rem;
  margin: 0 auto 1rem;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-icon svg {
  width: 100%;
  height: 100%;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.75rem;
}

.feature-description {
  color: var(--text-secondary);
  line-height: 1.6;
}

.app-footer {
  background-color: var(--card-bg);
  text-align: center;
  padding: 1.5rem;
  margin-top: 2rem;
}

/* Page Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Khatmah View Transitions */
.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Full width container for special pages like QuranBook */
.full-width-container {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0;
}

/* Adjust padding for the main content when displaying full-width components */
.main-content .full-width-container {
  margin-left: -2rem;
  margin-right: -2rem;
  width: calc(100% + 4rem);
}

/* Responsive adjustments for full-width container */
@media (max-width: 768px) {
  .main-content .full-width-container {
    margin-left: -1rem;
    margin-right: -1rem;
    width: calc(100% + 2rem);
  }
}
</style>
