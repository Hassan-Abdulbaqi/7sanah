<template>
  <div class="book-view-container">
    <div class="controls" v-if="navControlsVisible">
      <div class="control-groups-container">
        <!-- Control Group: Page Navigation -->
        <div class="control-group page-controls">
          <label for="pageInput" class="control-label">{{ $t('quran.bookViewPage.page') }}</label>
          <div class="page-selector flex items-center">
            <input 
              id="pageInput"
              v-model="currentPage"
              type="number" 
              class="page-input"
              min="1" 
              :max="totalPages"
              @keyup.enter="loadPage"
            />
            <span class="page-counter">/ {{ totalPages }}</span>
            <button class="go-button" @click="loadPage" :disabled="isLoading">{{ $t('quran.go') }}</button>
          </div>
        </div>
          
        <!-- Control Group: Text Type -->
        <div class="control-group">
          <label for="textTypeSelect" class="control-label">{{ $t('quran.bookViewPage.displayType') }}</label>
          <select id="textTypeSelect" v-model="selectedTextType" class="select-input" @change="loadPage">
            <option value="quran">{{ $t('quran.bookViewPage.quran') }}</option>
            <option value="quran-simple">{{ $t('quran.bookViewPage.quranSimple') }}</option>
            <option value="translation">{{ $t('quran.bookViewPage.translation') }}</option>
            <option value="quran-and-translation">{{ $t('quran.bookViewPage.quranAndTranslation') }}</option>
          </select>
        </div>
        
        <!-- Control Group: Translation -->
        <div class="control-group" v-if="showTranslationSelect">
          <label for="translationSelect" class="control-label">{{ $t('quran.bookViewPage.translation') }}</label>
          <select id="translationSelect" v-model="selectedTranslation" class="select-input" @change="loadPage">
            <option 
              v-for="translation in translations" 
              :key="translation.id" 
              :value="translation.id"
            >
              {{ translation.language }} - {{ translation.name }}
            </option>
          </select>
        </div>
          
        <!-- Control Group: Reciter -->
        <div class="control-group" v-if="audioAvailable">
          <label for="reciterSelect" class="control-label">{{ $t('quran.bookViewPage.reciter') }}</label>
          <div class="reciter-selector">
            <select id="reciterSelect" v-model="selectedReciter" class="select-input" @change="loadPage">
              <option 
                v-for="reciter in reciters" 
                :key="reciter.id" 
                :value="reciter.id"
              >
                {{ getReciterDisplayName(reciter) }}
              </option>
            </select>
            <button 
              class="audio-button" 
              @click="playPageAudio" 
              :disabled="isLoadingAudio || !pageAudiosReady || isLoading"
              aria-label="Play audio"
            >
              <span class="sr-only md:not-sr-only">{{ $t('quran.bookViewPage.play') }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 md:ml-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-message">
      <div class="spinner"></div>
      <p>{{ $t('quran.bookViewPage.loading', { page: currentPage }) }}</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <button class="px-4 py-2 bg-indigo-600 text-white rounded-lg" @click="loadPage">
        {{ $t('common.retry') }}
      </button>
    </div>
    
    <!-- No Page State -->
    <div v-else-if="!page" class="no-page">
      <p>{{ $t('quran.bookViewPage.noPage') }}</p>
      </div>
      
    <!-- Quran Content -->
    <div v-else class="quran-text-wrapper">
      <!-- Arabic Text -->
      <div v-if="showQuranText" class="quran-text-flow arabic-text">
        <template v-for="(ayah, index) in page.ayahs" :key="`arabic-${ayah.number}`">
          <template v-if="shouldAddSurahHeader(index, ayah)">
            <div class="surah-decoration">
              <div class="decoration-left"></div>
              <span class="surah-name">{{ ayah.surah.name }}</span>
              <div class="decoration-right"></div>
            </div>
            <div v-if="ayah.numberInSurah === 1 && shouldDisplayBismillah(ayah.surah.number)" class="bismillah">
              {{ extractBismillah() }}
            </div>
          </template>
          <div :id="`ayah-${ayah.number}`" class="ayah-wrapper" :class="{ 'playing-ayah-audio': currentAudioAyah === ayah.number }">
              <button 
              v-if="audioAvailable && ayah.audio" 
              @click="playAyahAudio(ayah.number)" 
                class="ayah-audio-button"
              :class="{ 'active': currentAudioAyah === ayah.number }"
              :disabled="isLoadingAudio"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                </svg>
              </button>
            <span class="ayah-text">{{ cleanAyahText(ayah.text, ayah.surah.number, ayah.numberInSurah) }}</span>
            <span class="ayah-number">﴿{{ ayah.numberInSurah }}﴾</span>
            <span v-if="ayah.sajda" class="sajda-mark">۩</span>
          </div>
        </template>
        
        <!-- Decorative page marker -->
        <div class="quran-page-marker"></div>
        </div>

      <!-- Translation Text -->
      <div v-if="showTranslation" class="mt-8 translation-container">
        <div v-for="ayah in page.ayahs" :key="`translation-${ayah.number}`" class="ayah translation-text" :class="{ 'playing-ayah-audio': currentAudioAyah === ayah.number }">
            <div class="ayah-header">
            <span>{{ ayah.surah.name }} {{ ayah.numberInSurah }}</span>
              <button 
              v-if="audioAvailable && ayah.audio" 
              @click="playAyahAudio(ayah.number)" 
                class="ayah-audio-button-translation"
              :class="{ 'active': currentAudioAyah === ayah.number }"
              :disabled="isLoadingAudio"
            >
              {{ $t('quran.bookViewPage.playButton') }}
              </button>
            </div>
          <div class="ayah-text">{{ cleanAyahText(ayah.translation, ayah.surah.number, ayah.numberInSurah) }}</div>
          </div>
        </div>
        
      <!-- Page Number -->
        <div class="page-number">
          <div class="page-number-container">
          {{ currentPage }}
          </div>
        </div>
    
      <!-- Navigation Buttons -->
      <div class="flex justify-center gap-4 mt-6 mb-4">
        <button 
          class="bottom-nav-button"
          @click="loadNextPage"
          :disabled="isLoading || currentPage >= totalPages"
        >
          <!-- Left-pointing arrow for "Next" in Arabic reading direction -->
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
          {{ $t('quran.bookViewPage.nextPage') }}
        </button>
        <button 
          class="bottom-nav-button"
          @click="loadPreviousPage"
          :disabled="isLoading || currentPage <= 1"
        >
          {{ $t('quran.bookViewPage.previousPage') }}
          <!-- Right-pointing arrow for "Previous" in Arabic reading direction -->
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Audio Player -->
    <div v-if="isPlayingAudio && audioElement" class="audio-player fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-4 flex items-center justify-between shadow-lg">
      <div class="text-sm text-gray-600">
        <span v-if="currentAudioAyah">
          {{ getCurrentAudioAyahText() }}
        </span>
        <span v-else>
          {{ $t('quran.bookViewPage.playingPage', { page: currentPage }) }}
        </span>
      </div>
      <div class="flex items-center space-x-4">
        <button class="play-pause-button" @click="toggleAudioPlayPause">
          <svg v-if="audioElement && !audioElement.paused" xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-[#8a672a]" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-[#8a672a]" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
          </svg>
        </button>
        <button class="stop-button" @click="stopAudio">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-[#8a672a]" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookView',
  props: {
    groupedTranslations: {
      type: Object,
      required: false,
      default: () => ({})
    },
    languages: {
      type: Object,
      required: false,
      default: () => ({})
    },
    groupedReciters: {
      type: Object,
      default: () => ({})
    },
    loadingReciters: {
      type: Boolean,
      default: false
    },
    isPlayingFullPage: {
      type: Boolean,
      default: false
    },
    downloadingPageAudio: {
      type: Boolean,
      default: false
    },
    paused: {
      type: Boolean,
      default: false
    },
    audioPlayer: {
      type: Object,
      default: null
    },
    audioProgress: {
      type: Number,
      default: 0
    },
    audioDuration: {
      type: Number,
      default: 0
    },
    loadingAyahAudio: {
      type: Number,
      default: null
    },
    currentPlayingAyah: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      currentPage: 1,
      totalPages: 604,
      isLoading: false,
      error: null,
      page: null,
      selectedTextType: 'quran',
      selectedTranslation: 'en.sahih',
      selectedReciter: 'ar.alafasy',
      audioAvailable: true,
      navControlsVisible: true,
      
      // For standalone mode
      translations: [],
      reciters: [],
      languagesLocal: {},
      groupedTranslationsLocal: {},
      loadingTranslations: false,
      
      // Audio state
      audioElement: null,
      isPlayingAudio: false,
      isLoadingAudio: false,
      currentAudioAyah: null,
      pageAudiosReady: false,
      audioPlaylist: [],
      currentPlaylistIndex: 0,
      _boundPlayNextInPlaylist: null
    }
  },
  computed: {
    // Use either prop or local data based on what's available
    effectiveLanguages() {
      return Object.keys(this.languages).length > 0 ? this.languages : this.languagesLocal;
    },
    
    effectiveGroupedTranslations() {
      return Object.keys(this.groupedTranslations).length > 0 ? this.groupedTranslations : this.groupedTranslationsLocal;
    },
    
    showQuranText() {
      return this.selectedTextType === 'quran' || 
             this.selectedTextType === 'quran-simple' || 
             this.selectedTextType === 'quran-and-translation';
    },
    
    showTranslation() {
      return this.selectedTextType === 'translation' || 
             this.selectedTextType === 'quran-and-translation';
    },
    
    showTranslationSelect() {
      return this.selectedTextType === 'translation' || 
             this.selectedTextType === 'quran-and-translation';
    },
    
    isArabicEdition() {
      return this.selectedEdition === 'quran-uthmani' || this.selectedEdition.startsWith('ar.');
    },
    textDirection() {
      if (this.selectedEdition === 'quran-uthmani' || this.selectedEdition.startsWith('ar.')) {
        return 'rtl';
      }
      return 'ltr';
    },
    showBismillah() {
      if (!this.pageData || !this.pageData.ayahs || this.pageData.ayahs.length === 0) {
        return false;
      }
      
      // Show Bismillah at the beginning of each Surah except Surah 9
      const firstAyah = this.pageData.ayahs[0];
      return firstAyah.numberInSurah === 1 && firstAyah.surah.number !== 9;
    },
    showSurahHeader() {
      if (!this.pageData || !this.pageData.ayahs || this.pageData.ayahs.length === 0) {
        return false;
      }
      
      // Show Surah header when the first ayah on the page is the first ayah of a surah
      const firstAyah = this.pageData.ayahs[0];
      return firstAyah.numberInSurah === 1;
    },
    
    firstAyahSurahName() {
      if (!this.pageData || !this.pageData.ayahs || this.pageData.ayahs.length === 0) {
        return '';
      }
      
      return this.pageData.ayahs[0].surah.name;
    }
  },
  created() {
    console.log('BookView component created');
    // Load user preferences from localStorage
    this.loadUserPreferences();
    
    // Fetch required data
    this.fetchEditions();
    this.fetchReciters();
  },
  mounted() {
    console.log('BookView mounted - loading first page');
    // Load the first page on component mount
    this.loadPage();
  },
  beforeUnmount() {
    // Clean up audio player
    this.stopAnyPlayingAudio();
    
    if (this.audioPlayerLocal) {
      this.audioPlayerLocal.removeEventListener('timeupdate', this.updateAudioProgress);
      
      // Also remove the bound playlist method
      if (this._boundPlayNextInPlaylist) {
        this.audioPlayerLocal.removeEventListener('ended', this._boundPlayNextInPlaylist);
      }
      
      // Remove any ended event listeners
      const newAudio = new Audio();
      this.audioPlayerLocal = newAudio;
      this.audioPlayerLocal = null;
    }
    
    // Clear any intervals
    if (this.audioUpdateInterval) {
      clearInterval(this.audioUpdateInterval);
      this.audioUpdateInterval = null;
    }
  },
  methods: {
    // Add getReciterDisplayName as the first method
    getReciterDisplayName(reciter) {
      // If current locale is Arabic, show Arabic name if available, otherwise fallback to English name
      if (this.$i18n.locale === 'ar' && reciter.name) {
        return reciter.name;
      } 
      // For other locales or if Arabic name is not available, show English name
      return reciter.englishName || reciter.name;
    },
    
    // Add the method to clean ayah text and remove Bismillah
    cleanAyahText(ayahText, surahNumber, ayahNumberInSurah) {
      // Only process the first ayah of each surah (except for Surah Al-Fatiha and At-Tawbah)
      if (ayahNumberInSurah === 1 && surahNumber !== 1 && surahNumber !== 9) {
        // Find where the Bismillah ends by checking for space or special character after it
        let cleanedText = '';
        
        // Start with standard length of 38-40 characters which is typically the Bismillah length
        if (ayahText.length > 39) {
          cleanedText = ayahText.substring(39);
        } else if (ayahText.length > 38) {
          cleanedText = ayahText.substring(38);
        } else {
          cleanedText = ayahText;
        }
        
        return cleanedText;
      }
      return ayahText;
    },
    
    // Function to extract Bismillah for display
    extractBismillah() {
      return 'بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ';
    },
    
    // Function to check if a surah should display Bismillah
    shouldDisplayBismillah(surahNumber) {
      return surahNumber !== 9; // Surah At-Tawbah (9) doesn't have Bismillah
    },
    
    getLanguageName(langCode) {
      return this.effectiveLanguages[langCode] || langCode.toUpperCase();
    },
    
    convertToArabicNumeral(num) {
      const arabicNumerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
      return num.toString().split('').map(digit => arabicNumerals[parseInt(digit)]).join('');
    },
    
    async loadPage() {
      if (this.currentPage < 1 || this.currentPage > this.totalPages) {
        return;
      }
      
      this.isLoading = true;
      this.error = null;
      
      try {
        console.log(`Loading page ${this.currentPage} with text type ${this.selectedTextType}`);
        
        let endpoint = `http://api.alquran.cloud/v1/page/${this.currentPage}`;
        
        if (this.selectedTextType === 'quran') {
          endpoint += '/quran-uthmani';
        } else if (this.selectedTextType === 'quran-simple') {
          endpoint += '/quran-simple';
        } else if (this.selectedTextType === 'translation') {
          endpoint += `/${this.selectedTranslation}`;
        } else if (this.selectedTextType === 'quran-and-translation') {
          // We'll need to make two requests for this mode
          const quranResponse = await fetch(`http://api.alquran.cloud/v1/page/${this.currentPage}/quran-uthmani`);
          const quranData = await quranResponse.json();
          
          const translationResponse = await fetch(`http://api.alquran.cloud/v1/page/${this.currentPage}/${this.selectedTranslation}`);
          const translationData = await translationResponse.json();
          
          if (quranData.code === 200 && translationData.code === 200) {
            // Combine the data
            const combinedData = { ...quranData.data };
            
            // Add translations to each ayah
            combinedData.ayahs = combinedData.ayahs.map((ayah, index) => {
              return {
                ...ayah,
                translation: translationData.data.ayahs[index].text
              };
            });
            
            this.page = combinedData;
            await this.loadAudioForPage();
            return;
          } else {
            throw new Error('Failed to load quran and translation');
          }
        }
        
        const response = await fetch(endpoint);
        const data = await response.json();
        
        if (data.code === 200) {
          this.page = data.data;
          await this.loadAudioForPage();
        } else {
          this.error = data.status || 'Error loading page';
          this.page = null;
        }
      } catch (error) {
        console.error('Error loading Quran page:', error);
        this.error = 'Network error. Please check your connection.';
        this.page = null;
      } finally {
        this.isLoading = false;
      }
    },
    
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.jumpToPage = this.currentPage;
        this.loadPage();
      }
    },
    
    nextPage() {
      if (this.currentPage < 604) {
        this.currentPage++;
        this.jumpToPage = this.currentPage;
        this.loadPage();
      }
    },
    
    goToPage() {
      if (this.jumpToPage >= 1 && this.jumpToPage <= 604) {
        this.currentPage = this.jumpToPage;
        this.loadPage();
      } else {
        // Reset jumpToPage to current valid page
        this.jumpToPage = this.currentPage;
      }
    },
    
    shouldInsertSajdaSymbol(ayah) {
      // List of ayahs where sajda is recommended - just a sample for demonstration
      // In a complete implementation, this would include all sajda positions
      const sajdaPositions = [
        {surah: 7, ayah: 206}, {surah: 13, ayah: 15}, {surah: 16, ayah: 50},
        {surah: 17, ayah: 109}, {surah: 19, ayah: 58}, {surah: 22, ayah: 18}
        // Add other sajda positions as needed
      ];
      
      return sajdaPositions.some(pos => 
        pos.surah === ayah.surah.number && pos.ayah === ayah.numberInSurah
      );
    },
    
    // Audio control methods
    listenToFullPage() {
      this.downloadPageAudio(this.currentPage, this.selectedReciter);
    },
    
    async downloadPageAudio(page, reciter) {
      if (this.downloadingPageAudioLocal || this.isPlayingFullPageLocal) return;
      
      this.downloadingPageAudioLocal = true;
      this.stopAnyPlayingAudio(); // Stop any currently playing audio
      
      try {
        // Get all ayahs for the current page
        if (!this.pageData || !this.pageData.ayahs || this.pageData.ayahs.length === 0) {
          throw new Error('No ayahs available on this page');
        }
        
        const ayahsToPlay = [...this.pageData.ayahs];
        const audioUrls = [];
        
        // Get audio URLs for each ayah
        for (const ayah of ayahsToPlay) {
          const audioUrl = await this.getAyahAudioUrl(ayah.number, reciter);
          if (audioUrl) {
            audioUrls.push(audioUrl);
          }
        }
        
        if (audioUrls.length === 0) {
          throw new Error('Could not load audio for this page');
        }
        
        // Create a playlist and play it
        await this.playAudioPlaylist(audioUrls);
        
        this.isPlayingFullPageLocal = true;
      } catch (error) {
        console.error('Error playing page audio:', error);
        alert(error.message || 'Error playing audio. Please try again.');
      } finally {
        this.downloadingPageAudioLocal = false;
      }
    },
    
    async getAyahAudioUrl(ayahNumber, reciter) {
      // Check cache first
      const cacheKey = `${reciter}-${ayahNumber}`;
      if (this.ayahAudioUrls[cacheKey]) {
        return this.ayahAudioUrls[cacheKey];
      }
      
      try {
        const response = await fetch(`http://api.alquran.cloud/v1/ayah/${ayahNumber}/${reciter}`);
        const data = await response.json();
        
        if (data.code === 200 && data.data && data.data.audio) {
          // Cache the URL
          this.ayahAudioUrls[cacheKey] = data.data.audio;
          return data.data.audio;
        } else {
          throw new Error(`Could not get audio for ayah ${ayahNumber}`);
        }
      } catch (error) {
        console.error(`Error fetching audio for ayah ${ayahNumber}:`, error);
        return null;
      }
    },
    
    async playAudioPlaylist(audioUrls) {
      if (!audioUrls || audioUrls.length === 0) return;
      
      // Set up audio player if we need to
      if (!this.audioPlayerLocal) {
        this.audioPlayerLocal = new Audio();
      } else {
        // Remove any existing event listeners to avoid duplicates
        this.audioPlayerLocal.removeEventListener('timeupdate', this.updateAudioProgress);
        
        // Important: Remove the ended event listener properly
        if (this._boundPlayNextInPlaylist) {
          this.audioPlayerLocal.removeEventListener('ended', this._boundPlayNextInPlaylist);
        }
      }
      
      // Set up event listeners
      this.audioPlayerLocal.addEventListener('timeupdate', this.updateAudioProgress);
      
      // Store a bound reference to the method to ensure proper cleanup later
      this._boundPlayNextInPlaylist = this.playNextInPlaylist.bind(this);
      this.audioPlayerLocal.addEventListener('ended', this._boundPlayNextInPlaylist);
      
      this.audioPlayerLocal.addEventListener('loadedmetadata', () => {
        this.audioDurationLocal = this.audioPlayerLocal.duration;
      });
      
      // Set the playlist
      this.audioPlayerLocal._playlist = audioUrls;
      this.audioPlayerLocal._currentTrack = 0;
      
      // Store ayah numbers associated with each track for highlighting
      if (this.pageData && this.pageData.ayahs) {
        this.audioPlayerLocal._playlistAyahNumbers = this.pageData.ayahs.map(ayah => ayah.number);
      }
      
      // Start playing the first track
      await this.playCurrentTrack();
    },
    
    async playCurrentTrack() {
      if (!this.audioPlayerLocal || 
          !this.audioPlayerLocal._playlist || 
          this.audioPlayerLocal._currentTrack >= this.audioPlayerLocal._playlist.length) {
        this.stopAnyPlayingAudio();
        return;
      }
      
      const currentUrl = this.audioPlayerLocal._playlist[this.audioPlayerLocal._currentTrack];
      this.audioPlayerLocal.src = currentUrl;
      this.audioPlayerLocal.load();
      
      // Update the currently playing ayah for highlighting
      if (this.audioPlayerLocal._playlistAyahNumbers && 
          this.audioPlayerLocal._playlistAyahNumbers[this.audioPlayerLocal._currentTrack]) {
        this.currentPlayingAyahLocal = this.audioPlayerLocal._playlistAyahNumbers[this.audioPlayerLocal._currentTrack];
      }
      
      try {
        await this.audioPlayerLocal.play();
        this.pausedLocal = false;
      } catch (error) {
        console.error('Error playing audio:', error);
      }
    },
    
    playNextInPlaylist() {
      this.currentPlaylistIndex++;
      if (this.currentPlaylistIndex < this.audioPlaylist.length) {
        this.playCurrentInPlaylist();
      } else {
        // End of playlist
        console.log('Playlist finished, stopping audio');
        this.stopAnyPlayingAudio();
      }
    },
    
    updateAudioProgress() {
      if (this.audioPlayerLocal) {
        this.audioProgressLocal = this.audioPlayerLocal.currentTime;
      }
    },
    
    togglePause() {
      if (!this.audioPlayerLocal) return;
      
      if (this.pausedLocal) {
        this.audioPlayerLocal.play();
        this.pausedLocal = false;
      } else {
        this.audioPlayerLocal.pause();
        this.pausedLocal = true;
      }
    },
    
    stopAudio() {
      this.isPlayingAudio = false;
      this.isLoadingAudio = false;
      this.currentAudioAyah = null;
      
      if (this.audioElement) {
        // Clean up listeners
        this.audioElement.oncanplaythrough = null;
        this.audioElement.onended = null;
        this.audioElement.onerror = null;
        
        if (this._boundPlayNextInPlaylist) {
          this.audioElement.removeEventListener('ended', this._boundPlayNextInPlaylist);
        }
        
        // Stop playback
        this.audioElement.pause();
        this.audioElement.src = '';
        this.audioElement = null;
      }
    },
    
    seekAudio(event) {
      if (!this.audioPlayerLocal) return;
      
      const seekTime = parseFloat(event.target.value);
      this.audioPlayerLocal.currentTime = seekTime;
      this.audioProgressLocal = seekTime;
    },
    
    stopAnyPlayingAudio() {
      // Stop any currently playing audio
      if (this.audioPlayerLocal) {
        this.audioPlayerLocal.pause();
        this.audioPlayerLocal.currentTime = 0;
      }
      
      // Reset state
      this.isPlayingFullPageLocal = false;
      this.currentPlayingAyahLocal = null;
      this.pausedLocal = false;
      this.audioProgressLocal = 0;
    },
    
    async toggleAyahAudio(ayah) {
      // If this ayah is already playing, either pause or resume it
      if (this.currentPlayingAyahLocal === ayah.number) {
        this.togglePause();
        return;
      }
      
      // Stop any currently playing audio
      this.stopAnyPlayingAudio();
      
      // Start loading this ayah's audio
      this.loadingAyahAudioLocal = ayah.number;
      
      try {
        const audioUrl = await this.getAyahAudioUrl(ayah.number, this.selectedReciter);
        
        if (!audioUrl) {
          throw new Error('Could not load audio for this verse');
        }
        
        // Set up audio player if needed
        if (!this.audioPlayerLocal) {
          this.audioPlayerLocal = new Audio();
        } else {
          // Remove any existing event listeners to avoid duplicates
          this.audioPlayerLocal.removeEventListener('timeupdate', this.updateAudioProgress);
          this.audioPlayerLocal.removeEventListener('ended', this.playNextInPlaylist);
        }
        
        // Set up event listeners
        this.audioPlayerLocal.addEventListener('timeupdate', this.updateAudioProgress);
        
        // Use a direct function reference for single ayah playback
        this.audioPlayerLocal.addEventListener('ended', () => {
          // Reset after playback ends - immediately stop for single ayah playback
          this.currentPlayingAyahLocal = null;
          this.audioProgressLocal = 0;
          this.isPlayingFullPageLocal = false; // Ensure this is false for single ayah
        });
        
        this.audioPlayerLocal.addEventListener('loadedmetadata', () => {
          this.audioDurationLocal = this.audioPlayerLocal.duration;
        });
        
        // Set the source and play
        this.audioPlayerLocal.src = audioUrl;
        this.audioPlayerLocal.load();
        await this.audioPlayerLocal.play();
        
        // Update state
        this.currentPlayingAyahLocal = ayah.number;
        this.pausedLocal = false;
        this.isPlayingFullPageLocal = false; // Make sure this is false to distinguish from full page mode
      } catch (error) {
        console.error('Error playing ayah audio:', error);
        alert(error.message || 'Error playing audio. Please try again.');
      } finally {
        this.loadingAyahAudioLocal = null;
      }
    },
    
    onReciterChange() {
      // Save preferences to localStorage
      this.saveUserPreferences();
    },
    
    saveUserPreferences() {
      try {
        const preferences = {
          selectedEdition: this.selectedEdition,
          selectedReciter: this.selectedReciter,
          timestamp: new Date().getTime()
        };
        localStorage.setItem('quranBookViewPreferences', JSON.stringify(preferences));
      } catch (error) {
        console.error('Error saving preferences:', error);
      }
    },
    
    loadUserPreferences() {
      try {
        const savedPreferences = localStorage.getItem('quranBookViewPreferences');
        if (savedPreferences) {
          const preferences = JSON.parse(savedPreferences);
          
          // Check if preferences are still valid (not too old)
          const now = new Date().getTime();
          const oneMonthInMs = 30 * 24 * 60 * 60 * 1000;
          
          if (preferences.timestamp && (now - preferences.timestamp) < oneMonthInMs) {
            // Apply saved preferences
            if (preferences.selectedEdition) {
              this.selectedEdition = preferences.selectedEdition;
            }
            
            if (preferences.selectedReciter) {
              this.selectedReciter = preferences.selectedReciter;
            }
          } else {
            // Preferences are too old, remove them
            localStorage.removeItem('quranBookViewPreferences');
          }
        }
      } catch (error) {
        console.error('Error loading preferences:', error);
      }
    },
    
    formatTime(seconds) {
      if (!seconds || isNaN(seconds)) return '0:00';
      
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = Math.floor(seconds % 60);
      
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    },
    
    async fetchReciters() {
      try {
        console.log('Fetching reciters...');
        
        // Make the API call to get all editions
        const response = await fetch('http://api.alquran.cloud/v1/edition/format/audio');
        const data = await response.json();
        
        if (data.code === 200) {
          // Map the data to include both name and englishName
          this.reciters = data.data.map(reciter => ({
            id: reciter.identifier,
            name: reciter.name,
            englishName: reciter.englishName,
            language: reciter.language
          }));
          
          console.log(`Loaded ${this.reciters.length} reciters`);
          
          // Set a default reciter if none selected
          if (!this.selectedReciter && this.reciters.length > 0) {
            this.selectedReciter = this.reciters[0].id;
          }
        }
      } catch (error) {
        console.error('Error fetching reciters:', error);
      }
    },
    
    async fetchEditions() {
      try {
        this.loadingTranslations = true;
        console.log('Fetching editions...');
        
        // Use the specified API endpoint to get all editions
        const response = await fetch('http://api.alquran.cloud/v1/edition/type/translation');
        const data = await response.json();
        
        if (data.code === 200) {
          // Filter and populate translations
          this.translations = data.data.map(translation => ({
            id: translation.identifier,
            name: translation.englishName || translation.name,
            language: translation.language
          }));
          
          console.log(`Loaded ${this.translations.length} translations`);
          
          // Set a default translation if none selected
          if (!this.selectedTranslation && this.translations.length > 0) {
            // Try to find an English translation first
            const englishTranslation = this.translations.find(t => t.language === 'en');
            this.selectedTranslation = englishTranslation ? englishTranslation.id : this.translations[0].id;
          }
        }
      } catch (error) {
        console.error('Error fetching editions:', error);
      } finally {
        this.loadingTranslations = false;
      }
    },
    
    async loadAudioForPage() {
      // Reset audio state
      this.pageAudiosReady = false;
      this.audioPlaylist = [];
      
      if (!this.page || !this.page.ayahs || !this.audioAvailable || !this.selectedReciter) {
        console.log("Cannot load audio due to missing data:", {
          hasPage: !!this.page,
          hasAyahs: !!(this.page && this.page.ayahs),
          audioAvailable: this.audioAvailable,
          selectedReciter: this.selectedReciter
        });
        return;
      }
      
      console.log(`Loading audio for page ${this.currentPage} with reciter ${this.selectedReciter}`);
      
      try {
        // Prepare ayah audio URLs
        for (const ayah of this.page.ayahs) {
          try {
            // Format: http://api.alquran.cloud/v1/ayah/{ayah_number}/{edition}
            const audioUrl = `http://api.alquran.cloud/v1/ayah/${ayah.number}/${this.selectedReciter}`;
            console.log(`Fetching audio for ayah ${ayah.number} from: ${audioUrl}`);
            
            const response = await fetch(audioUrl);
            const data = await response.json();
            
            if (data.code === 200 && data.data && data.data.audio) {
              // Attach audio URL to the ayah
              ayah.audio = data.data.audio;
              this.audioPlaylist.push(data.data.audio);
              console.log(`Added audio for ayah ${ayah.number}: ${data.data.audio}`);
            } else {
              console.warn(`No audio found for ayah ${ayah.number}:`, data);
            }
          } catch (error) {
            console.error(`Error loading audio for ayah ${ayah.number}:`, error);
          }
        }
        
        this.pageAudiosReady = this.audioPlaylist.length > 0;
        console.log(`Audio playlist ready with ${this.audioPlaylist.length} tracks`);
      } catch (error) {
        console.error('Error preparing page audio:', error);
      }
    },
    
    loadNextPage() {
      if (this.currentPage < this.totalPages && !this.isLoading) {
        this.currentPage++;
        this.loadPage();
      }
    },
    
    loadPreviousPage() {
      if (this.currentPage > 1 && !this.isLoading) {
        this.currentPage--;
        this.loadPage();
      }
    },
    
    playPageAudio() {
      if (this.isLoadingAudio || !this.pageAudiosReady || this.audioPlaylist.length === 0) {
        return;
      }
      
      // Stop any currently playing audio
      this.stopAudio();
      
      this.isLoadingAudio = true;
      
      // Set up new audio element
      this.audioElement = new Audio();
      
      // Store a bound reference to the method to ensure proper cleanup later
      this._boundPlayNextInPlaylist = this.playNextInPlaylist.bind(this);
      this.audioElement.addEventListener('ended', this._boundPlayNextInPlaylist);
      
      // Start playing the playlist
      this.currentPlaylistIndex = 0;
      this.playCurrentInPlaylist();
    },
    
    playNextInPlaylist() {
      this.currentPlaylistIndex++;
      if (this.currentPlaylistIndex < this.audioPlaylist.length) {
        this.playCurrentInPlaylist();
      } else {
        // End of playlist
        this.stopAudio();
      }
    },
    
    playCurrentInPlaylist() {
      if (!this.audioElement || this.currentPlaylistIndex >= this.audioPlaylist.length) {
        this.stopAudio();
        return;
      }
      
      const audioUrl = this.audioPlaylist[this.currentPlaylistIndex];
      this.audioElement.src = audioUrl;
      
      // Set the current ayah for highlighting
      if (this.page && this.page.ayahs) {
        this.currentAudioAyah = this.page.ayahs[this.currentPlaylistIndex].number;
      }
      
      this.audioElement.oncanplaythrough = () => {
        this.isLoadingAudio = false;
        this.isPlayingAudio = true;
        this.audioElement.play().catch(err => {
          console.error('Error playing audio:', err);
          this.stopAudio();
        });
      };
      
      this.audioElement.onerror = () => {
        console.error('Audio loading error');
        this.playNextInPlaylist(); // Skip to the next one on error
      };
      
      this.audioElement.load();
    },
    
    playAyahAudio(ayahNumber) {
      if (this.isLoadingAudio) {
        return;
      }
      
      // Stop any currently playing audio
      this.stopAudio();
      
      // Find the ayah
      const ayah = this.page.ayahs.find(a => a.number === ayahNumber);
      if (!ayah || !ayah.audio) {
        return;
      }
      
      this.isLoadingAudio = true;
      this.currentAudioAyah = ayahNumber;
      
      // Set up new audio element
      this.audioElement = new Audio();
      this.audioElement.src = ayah.audio;
      
      this.audioElement.oncanplaythrough = () => {
        this.isLoadingAudio = false;
        this.isPlayingAudio = true;
        this.audioElement.play().catch(err => {
          console.error('Error playing audio:', err);
          this.stopAudio();
        });
      };
      
      this.audioElement.onended = () => {
        this.stopAudio();
      };
      
      this.audioElement.onerror = () => {
        console.error('Audio loading error');
        this.stopAudio();
      };
      
      this.audioElement.load();
    },
    
    toggleAudioPlayPause() {
      if (!this.audioElement) {
        return;
      }
      
      if (this.audioElement.paused) {
        this.audioElement.play().catch(err => {
          console.error('Error playing audio:', err);
        });
      } else {
        this.audioElement.pause();
      }
    },
    
    getCurrentAudioAyahText() {
      if (!this.currentAudioAyah || !this.page || !this.page.ayahs) {
        return '';
      }
      
      const ayah = this.page.ayahs.find(a => a.number === this.currentAudioAyah);
      if (ayah) {
        return this.$t('quran.bookViewPage.playingAyah', { surah: ayah.surah.name, ayah: ayah.numberInSurah });
      }
      
      return '';
    },
    
    shouldAddSurahHeader(index, ayah) {
      // Add surah header if this is the first ayah in the page, or
      // if it's the first ayah of a new surah
      if (index === 0) {
        return true;
      }
      
      if (index > 0 && this.page.ayahs[index-1].surah.number !== ayah.surah.number) {
        return true;
      }
      
      return false;
    }
  }
}
</script>

<style scoped>
.book-view-container {
  min-height: calc(100vh - 4rem); /* Subtract navbar height */
  height: calc(100vh - 4rem); /* Set explicit height */
  width: 100%;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f3eee1; /* Warmer parchment color */
  background-image: url("data:image/svg+xml,%3Csvg width='52' height='26' viewBox='0 0 52 26' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23a77e2d' fill-opacity='0.05'%3E%3Cpath d='M10 10c0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6h2c0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4v2c-3.314 0-6-2.686-6-6 0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6zm25.464-1.95l8.486 8.486-1.414 1.414-8.486-8.486 1.414-1.414z' /%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  overflow-y: auto; /* Enable vertical scrolling */
  overflow-x: hidden;
  margin: 0;
  padding: 0;
  /* Position to cover the entire viewport below navbar */
  position: fixed;
  top: 4rem; /* Match the header height from App.vue */
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 40; /* Higher than App content but lower than header */
  box-sizing: border-box;
}

.controls {
  width: 100%;
  background-color: rgba(243, 238, 225, 0.95);
  border-bottom: 1px solid #d7c89b;
  margin: 0;
  padding: 0.75rem 1rem;
  box-shadow: 0 2px 10px rgba(167, 126, 45, 0.1);
  z-index: 10;
  position: sticky;
  top: 0; /* Stick to the top of the book view container */
}

/* New control groups container with better organization */
.control-groups-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  align-items: start;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.control-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b5128;
  margin-bottom: 0.25rem;
}

.page-input {
  width: 60px;
  padding: 0.35rem 0.5rem;
  border: 1px solid #d7c89b;
  border-radius: 0.25rem;
  text-align: center;
  font-size: 0.875rem;
}

.select-input {
  width: 100%;
  border: 1px solid #d7c89b;
  border-radius: 0.25rem;
  padding: 0.35rem 0.75rem;
  padding-right: 30px; /* Ensure enough space for the dropdown arrow */
  background-color: white;
  font-size: 0.875rem;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath d='M0,0 L5,5 L10,0 Z' fill='%238a672a' /%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  box-sizing: border-box;
}

.page-counter {
  color: #8a672a;
  font-size: 0.875rem;
  margin: 0 0.5rem;
  white-space: nowrap;
}

.page-selector {
  display: flex;
  align-items: center;
}

.reciter-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Responsive refinements */
@media (max-width: 640px) {
  .controls {
    padding: 0.4rem 0.5rem;
  }
  
  .control-groups-container {
    grid-template-columns: 1fr 1fr;
    gap: 0.4rem;
  }
  
  .control-group {
    gap: 0.25rem;
    margin-bottom: 0.25rem;
  }
  
  .control-label {
    font-size: 0.75rem;
    margin-bottom: 0.1rem;
  }
  
  .page-input, .select-input {
    padding: 0.25rem 0.4rem;
    font-size: 0.75rem;
    height: 28px;
  }
  
  .page-counter {
    font-size: 0.75rem;
    margin: 0 0.25rem;
  }
  
  .go-button, .audio-button {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
    height: 28px;
  }
  
  .reciter-selector {
    gap: 0.25rem;
  }
  
  /* Make the play button more compact on mobile */
  .audio-button .sr-only {
    display: none;
  }
  
  .audio-button svg {
    margin: 0;
  }
  
  /* Optimize select dropdowns on mobile */
  .select-input {
    padding-right: 22px; /* Ensure space for dropdown arrow */
    background-position: right 5px center;
    width: 100%;
  }
}

@media (min-width: 641px) and (max-width: 960px) {
  .control-groups-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 961px) {
  .control-groups-container {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 768px) {
  .controls {
    padding: 0.75rem 1rem;
  }
}

.quran-text-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100%; /* Allow to take full width */
  margin: 0;
  padding: 0; /* Remove all padding */
  min-height: 70vh;
  background-color: #fcf9ee; /* Slightly lighter parchment color for text area */
  box-shadow: none; /* Remove box shadow for full-width look */
  border-radius: 0; /* Remove border radius for full-width look */
  position: relative;
  border: none; /* Remove border for full-width look */
  /* Add subtle texture to mimic paper */
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23a77e2d' fill-opacity='0.02' fill-rule='evenodd'/%3E%3C/svg%3E");
}

/* Remove responsive adjustments that limit width */
@media (max-width: 768px) {
  .quran-text-wrapper {
    margin: 0;
    width: 100%;
  }
}

/* Ornate border design */
.quran-text-wrapper::before {
  display: none;
}

/* Traditional Quran page frame with ornate corners - remove for full-width view */
.quran-text-wrapper::after {
  display: none;
}

.quran-text-flow {
  text-align: justify;
  line-height: 2.6;
  white-space: normal;
  text-justify: inter-word;
  padding: 2rem 1.5rem;
  margin: 0;
  width: 100%;
  column-count: 1;
  overflow-wrap: break-word;
  direction: rtl;
  font-size: 1.6rem;
  background-color: transparent;
  position: relative;
  z-index: 1;
  box-sizing: border-box;
}

/* Surah header decoration */
.surah-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1rem 0 1.5rem;
  padding-top: 1.5rem;
  position: relative;
}

/* More elaborate surah separator */
.surah-decoration::before {
  content: "";
  position: absolute;
  top: 0;
  left: 10%;
  right: 10%;
  height: 12px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='12' viewBox='0 0 300 12'%3E%3Cpath d='M0,6 C50,0 100,12 150,6 C200,0 250,12 300,6' stroke='%23a77e2d' stroke-width='1' fill='none' stroke-opacity='0.5'/%3E%3Ccircle cx='150' cy='6' r='4' fill='%23a77e2d' fill-opacity='0.5'/%3E%3Ccircle cx='50' cy='6' r='3' fill='%23a77e2d' fill-opacity='0.3'/%3E%3Ccircle cx='250' cy='6' r='3' fill='%23a77e2d' fill-opacity='0.3'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100% 12px;
}

.decoration-left, .decoration-right {
  flex-grow: 1;
  height: 1px;
  margin-left: 2rem;
  margin-right: 2rem;
  background: linear-gradient(to right, rgba(167, 126, 45, 0.05), rgba(167, 126, 45, 0.4), rgba(167, 126, 45, 0.05));
}

.surah-name {
  font-size: 1.8rem;
  font-family: "Amiri", "QuranFont", "Traditional Arabic", serif;
  color: #8a672a;
  letter-spacing: 0.05em;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  font-weight: bold;
}

.bismillah {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #8a672a;
  font-family: "Amiri", "QuranFont", "Traditional Arabic", serif;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  position: relative;
}

/* Add decorative element under bismillah */
.bismillah::after {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 25%;
  right: 25%;
  height: 6px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='6' viewBox='0 0 200 6'%3E%3Cpath d='M0,3 C33.3,1 66.7,5 100,3 C133.3,1 166.7,5 200,3' stroke='%23a77e2d' stroke-width='1' fill='none' stroke-opacity='0.3'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100% 6px;
}

.arabic-text {
  font-size: 0;  /* Remove space between inline elements */
  text-align: justify;
  word-spacing: 0;
  padding: 0.5rem;
}

.arabic-text .ayah-text {
  display: inline;
  letter-spacing: normal;
  margin: 0;
  padding: 0;
  font-family: "Amiri", "QuranFont", "Traditional Arabic", "Scheherazade New", "KFGQPC Uthmanic Script HAFS", serif;
  font-size: 1.6rem;
  color: #000;
  word-spacing: normal;
  white-space: normal;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.03);
}

.ayah-wrapper {
  position: relative;
  display: inline;
  margin: 0;
  padding: 0.6em 0 0;
}

.ayah-wrapper.playing-ayah-audio {
  background-color: rgba(167, 126, 45, 0.1);
  border-radius: 3px;
  padding: 0.6em 2px 0 2px;
}

.arabic-text .ayah-number {
  display: inline;
  color: #8a672a;
  font-family: "Amiri", "QuranFont", "Traditional Arabic", serif;
  margin: 0 1px;
  padding: 0;
  font-size: 0.7em;
  vertical-align: middle;
  opacity: 0.8;
}

.sajda-mark {
  display: inline;
  color: #a03030;
  font-family: "Amiri", "QuranFont", "Traditional Arabic", serif;
  margin: 0 2px;
  padding: 0;
  font-size: 0.8em;
  vertical-align: middle;
}

/* Page number decoration */
.page-number {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 1rem 0;
}

.page-number-container {
  @apply flex items-center justify-center text-[#8a672a] font-quran text-xl;
  width: 4rem;
  height: 4rem;
  background-color: rgba(201, 169, 89, 0.12);
  border: 1px solid rgba(201, 169, 89, 0.3);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.07);
  position: relative;
  z-index: 10;
  border-radius: 50%;
  /* Add decorative elements */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 60 60'%3E%3Ccircle cx='30' cy='30' r='29' fill='none' stroke='%23a77e2d' stroke-width='1' stroke-opacity='0.3' stroke-dasharray='3,3'/%3E%3C/svg%3E");
  background-size: cover;
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .quran-text-flow {
    padding: 1.5rem 1rem 1.5rem;
    font-size: 1.2rem;
    line-height: 2.2;
  }
  
  .arabic-text .ayah-text {
    font-size: 1.2rem;
  }
  
  .quran-text-wrapper {
    max-width: 100%;
    width: 100%;
    padding: 0;
    margin: 0;
  }
  
  .bismillah {
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .surah-name {
    font-size: 1.4rem;
  }
}

@media (min-width: 481px) and (max-width: 767px) {
  .quran-text-flow {
    padding: 2rem 1.25rem 1.75rem;
    font-size: 1.3rem;
    line-height: 2.3;
  }
  
  .arabic-text .ayah-text {
    font-size: 1.3rem;
  }
  
  .bismillah {
    font-size: 1.7rem;
  }
  
  .quran-text-wrapper {
    max-width: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .quran-text-flow {
    padding: 2.5rem 1.5rem 2rem;
    font-size: 1.5rem;
    line-height: 2.4;
  }
  
  .arabic-text .ayah-text {
    font-size: 1.5rem;
  }
  
  .bismillah {
    font-size: 1.9rem;
  }
  
  .quran-text-wrapper {
    max-width: 100%;
    width: 100%;
    margin: 0;
    padding: 0;
  }
}

@media (min-width: 1024px) {
  .quran-text-flow {
    padding: 2.5rem 2.5rem 2.5rem;
    font-size: 1.8rem;
    line-height: 2.6;
  }
  
  .arabic-text .ayah-text {
    font-size: 1.8rem;
  }
  
  /* Remove max-width and padding constraints for full-width view */
  .quran-text-wrapper {
    max-width: 100%;
    padding: 0;
  }
  
  .bismillah {
    font-size: 2.2rem;
    margin-bottom: 2.5rem;
  }
}

/* Navigation buttons styled to fit the Quran theme */
.bottom-nav-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  background-color: #f5f1e4;
  color: #8a672a;
  border-radius: 0.5rem;
  border: 1px solid #d7c89b;
  transition: all 0.2s ease;
  font-family: "Amiri", "QuranFont", "Traditional Arabic", serif;
}

.bottom-nav-button:hover {
  background-color: #ebe3d0;
  border-color: #c4aa6e;
}

.bottom-nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Audio control styling */
.ayah-audio-button {
  position: absolute;
  top: -0.5em;
  right: 50%;
  transform: translateX(50%);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.2em;
  height: 1.2em;
  background-color: rgba(255, 255, 255, 0.6); /* More transparent background */
  color: rgba(138, 103, 42, 0.7); /* Slightly transparent color */
  border-radius: 50%;
  border: 1px solid rgba(209, 213, 219, 0.5); /* More transparent border */
  cursor: pointer;
  opacity: 0.5; /* Reduced opacity from 0.7 to 0.5 */
  z-index: 10;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* Lighter shadow */
}

.ayah-audio-button svg {
  width: 100%;
  height: 100%;
  padding: 15%;
}

.ayah-audio-button:hover {
  transform: translateX(50%) scale(1.1);
  opacity: 0.8; /* Hover opacity increased but still transparent */
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.ayah-audio-button.active {
  background-color: rgba(138, 103, 42, 0.8); /* More transparent when active */
  color: white;
  border-color: rgba(138, 103, 42, 0.6);
  opacity: 0.8;
}

/* Font faces */
@font-face {
  font-family: "QuranFont";
  src: url("/fonts/ScheherazadeNew-Regular.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: "QuranFont";
  src: url("/fonts/ScheherazadeNew-Bold.ttf") format("truetype");
  font-weight: bold;
  font-style: normal;
  font-display: swap;
}

/* Additional font options */
@font-face {
  font-family: "KFGQPC Uthmanic Script HAFS";
  src: url("/fonts/UthmanicHafs1Ver09.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

.font-quran {
  font-family: "Amiri", "QuranFont", "Traditional Arabic", "Scheherazade New", "KFGQPC Uthmanic Script HAFS", serif;
}

/* Add decorative side markers */
.quran-text-flow::before {
  content: ""; /* Remove the star/decorative element */
  position: absolute;
  top: 50%;
  right: 5px;
  font-size: 1.5rem;
  color: rgba(167, 126, 45, 0.4);
  transform: translateY(-50%);
}

.quran-text-flow::after {
  content: ""; /* Remove the star/decorative element */
  position: absolute;
  top: 50%;
  left: 5px;
  font-size: 1.5rem;
  color: rgba(167, 126, 45, 0.4);
  transform: translateY(-50%);
}

/* New decorative elements for Quran page */
.page-border {
  display: none; /* Hide the page border instead of removing the class entirely */
}

.quran-page-marker {
  position: absolute;
  top: 30px;
  right: 30px;
  width: 30px;
  height: 30px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'%3E%3Ccircle cx='30' cy='30' r='25' fill='none' stroke='%23a77e2d' stroke-width='1.5' stroke-opacity='0.4'/%3E%3Cpath d='M30,5 L30,55 M5,30 L55,30' stroke='%23a77e2d' stroke-width='1' stroke-opacity='0.3'/%3E%3Ccircle cx='30' cy='30' r='5' fill='%23a77e2d' fill-opacity='0.3'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-size: contain;
  z-index: 2;
  opacity: 0.7;
}

.translation-container {
  position: relative;
  background-color: rgba(253, 251, 245, 0.7);
  border-radius: 0;
  padding: 1rem;
  margin: 0;
  box-shadow: none;
  border: none;
  border-top: 1px solid rgba(167, 126, 45, 0.15);
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23a77e2d' fill-opacity='0.02' fill-rule='evenodd'/%3E%3C/svg%3E");
}

/* Enhanced spinner for loading state */
.spinner {
  width: 40px;
  height: 40px;
  background-color: transparent;
  margin: 0 auto 1rem;
  border-radius: 50%;
  border: 3px solid rgba(167, 126, 45, 0.1);
  border-top: 3px solid rgba(167, 126, 45, 0.7);
  animation: quran-spin 1s linear infinite;
}

@keyframes quran-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Add highlighted ayah effect */
.ayah-wrapper.playing-ayah-audio {
  background-color: rgba(167, 126, 45, 0.1);
  border-radius: 3px;
  padding: 0.6em 2px 0 2px;
  box-shadow: 0 0 5px rgba(167, 126, 45, 0.2);
  transition: background-color 0.3s ease;
}

/* Enhance audio player styling */
.audio-player {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(253, 251, 245, 0.97);
  border-top: 1px solid rgba(167, 126, 45, 0.3);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  padding: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  z-index: 50; /* Above the book view container */
}

.play-pause-button, .stop-button {
  background-color: rgba(253, 251, 245, 0.95);
  border-radius: 50%;
  padding: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(167, 126, 45, 0.2);
  transition: all 0.2s ease;
}

.play-pause-button:hover, .stop-button:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
  background-color: rgba(253, 251, 245, 1);
}

/* Controls styling */
.go-button {
  margin-left: 0.5rem;
  padding: 0.35rem 0.75rem;
  color: white;
  border-radius: 0.25rem;
  background-color: #8a672a;
  border: 1px solid #6e5222;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.go-button:hover:not(:disabled) {
  background-color: #6e5222;
}

.go-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.audio-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.35rem 0.75rem;
  color: white;
  border-radius: 0.25rem;
  background-color: #8a672a;
  border: 1px solid #6e5222;
  transition: background-color 0.2s ease;
  white-space: nowrap;
}

.audio-button:hover:not(:disabled) {
  background-color: #6e5222;
}

.audio-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Add these additional styles at the bottom */

/* Loading and error messages should be centered on the full page */
.loading-message, .error-message, .no-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  width: 100%;
  padding: 2rem;
  text-align: center;
}

/* Make control groups more responsive */
.control-group {
  margin-bottom: 1rem;
}

@media (min-width: 768px) {
  .control-group {
    margin-bottom: 0;
  }
}

/* Full width background ensures the pattern extends across the entire viewport */
.book-view-container::before {
  content: "";
  position: fixed;
  top: 4rem; /* Match the header height */
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #f3eee1;
  background-image: url("data:image/svg+xml,%3Csvg width='52' height='26' viewBox='0 0 52 26' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23a77e2d' fill-opacity='0.05'%3E%3Cpath d='M10 10c0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6h2c0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4v2c-3.314 0-6-2.686-6-6 0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6zm25.464-1.95l8.486 8.486-1.414 1.414-8.486-8.486 1.414-1.414z' /%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  z-index: -1;
}

/* Improved styling for the bottom navigation buttons container */
.flex.justify-center.gap-4.mt-6.mb-4 {
  margin: 1rem 0 3rem; /* Add bottom margin for spacing */
  padding: 0;
}

/* Add extra bottom padding when audio player is active */
.audio-player + .flex.justify-center.gap-4.mt-6.mb-4 {
  margin-bottom: calc(env(safe-area-inset-bottom, 0) + 5rem);
}

/* Ensure footer doesn't overlap with content */
.app-footer {
  z-index: 10;
}

/* Screen reader only text for better accessibility */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style> 