<template>
  <div class="book-view-container">
    <div class="controls" v-if="navControlsVisible">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Control Group: Page Navigation -->
        <div class="control-group">
          <label for="pageInput" class="text-sm font-medium text-gray-700 mb-1">Page</label>
          <div class="page-selector flex items-center">
            <input 
              id="pageInput"
              v-model="currentPage"
              type="number" 
              class="w-20 mr-2 border rounded py-1 px-2 text-center"
              min="1" 
              :max="totalPages"
              @keyup.enter="loadPage"
            />
            <span class="text-sm text-gray-500 whitespace-nowrap">/ {{ totalPages }}</span>
            <button class="go-button" @click="loadPage" :disabled="isLoading">Go</button>
          </div>
          </div>
          
        <!-- Control Group: Text Type -->
        <div class="control-group">
          <label for="textTypeSelect" class="text-sm font-medium text-gray-700 mb-1">Display Type</label>
          <select id="textTypeSelect" v-model="selectedTextType" class="select-input" @change="loadPage">
            <option value="quran">Quran</option>
            <option value="quran-simple">Quran (Simple)</option>
            <option value="translation">Translation</option>
            <option value="quran-and-translation">Quran & Translation</option>
          </select>
        </div>
        
        <!-- Control Group: Translation -->
        <div class="control-group" v-if="showTranslationSelect">
          <label for="translationSelect" class="text-sm font-medium text-gray-700 mb-1">Translation</label>
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
          <label for="reciterSelect" class="text-sm font-medium text-gray-700 mb-1">Reciter</label>
          <div class="flex items-center">
            <select id="reciterSelect" v-model="selectedReciter" class="select-input" @change="loadPage">
              <option 
                v-for="reciter in reciters" 
                :key="reciter.id" 
                :value="reciter.id"
              >
                {{ reciter.name }}
                </option>
            </select>
            <button 
              class="audio-button" 
              @click="playPageAudio" 
              :disabled="isLoadingAudio || !pageAudiosReady || isLoading"
              aria-label="Play audio"
            >
              <span class="sr-only md:not-sr-only">Play</span>
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
      <p>Loading page {{ currentPage }}...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <button class="px-4 py-2 bg-indigo-600 text-white rounded-lg" @click="loadPage">
        Try Again
      </button>
    </div>
    
    <!-- No Page State -->
    <div v-else-if="!page" class="no-page">
      <p>No page to display. Select a page to view.</p>
      </div>
      
    <!-- Quran Content -->
    <div v-else class="quran-text-wrapper">
      <!-- Arabic Text -->
      <div v-if="showQuranText" class="quran-text-flow arabic-text">
        <template v-for="(ayah, index) in page.ayahs" :key="`arabic-${ayah.number}`">
          <template v-if="shouldAddSurahHeader(index, ayah)">
            <div class="surah-decoration">
              <div class="decoration-left"></div>
              <span class="surah-name">سورة {{ ayah.surah.name }}</span>
              <div class="decoration-right"></div>
            </div>
            <div v-if="ayah.numberInSurah === 1 && ayah.surah.number !== 1 && ayah.surah.number !== 9" class="bismillah">
              بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
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
            <span class="ayah-text">{{ ayah.text }}</span>
            <span class="ayah-number">﴿{{ ayah.numberInSurah }}﴾</span>
            <span v-if="ayah.sajda" class="sajda-mark">۩</span>
          </div>
        </template>
        </div>

      <!-- Translation Text -->
      <div v-if="showTranslation" class="mt-8">
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
              Play
              </button>
            </div>
          <div class="ayah-text">{{ ayah.translation }}</div>
          </div>
        </div>
        
      <!-- Page Number -->
        <div class="page-number">
          <div class="page-number-container">
          {{ currentPage }}
          </div>
        </div>
    
      <!-- Navigation Buttons -->
      <div class="flex justify-center gap-4 mt-4">
        <button 
          class="bottom-nav-button"
          @click="loadPreviousPage"
          :disabled="isLoading || currentPage <= 1"
        >
          Previous Page 
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        <button 
          class="bottom-nav-button"
          @click="loadNextPage"
          :disabled="isLoading || currentPage >= totalPages"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
          Next Page
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
          Playing page {{ currentPage }}
        </span>
      </div>
      <div class="flex items-center space-x-4">
        <button class="play-pause-button" @click="toggleAudioPlayPause">
          <svg v-if="audioElement && !audioElement.paused" xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-indigo-600" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-indigo-600" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
          </svg>
        </button>
        <button class="stop-button" @click="stopAudio">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-indigo-600" viewBox="0 0 20 20" fill="currentColor">
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
      if (!this.audioPlayerLocal || !this.audioPlayerLocal._playlist) return;
      
      // If not playing full page (single ayah mode), stop after one ayah
      if (!this.isPlayingFullPageLocal) {
        this.stopAnyPlayingAudio();
        return;
      }
      
      // Move to the next track
      this.audioPlayerLocal._currentTrack++;
      
      console.log(`Moving to next track: ${this.audioPlayerLocal._currentTrack} of ${this.audioPlayerLocal._playlist.length}`);
      
      if (this.audioPlayerLocal._currentTrack < this.audioPlayerLocal._playlist.length) {
        // Play the next track
        this.playCurrentTrack();
      } else {
        // Playlist finished
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
          // Filter for audio editions only
          this.reciters = data.data.map(reciter => ({
            id: reciter.identifier,
            name: reciter.englishName || reciter.name,
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
        return `${ayah.surah.name} ${ayah.numberInSurah}`;
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
  min-height: 100vh;
  min-height: 100dvh;
  width: 100vw;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f8f5e6; /* Light parchment color for the entire container */
  overflow-x: hidden;
  margin: 0;
  padding: 0;
}

.controls {
  width: 100%;
  background-color: rgba(255, 255, 255, 0.5);
  border-bottom: 1px solid #d7c89b;
  border-top: none;
  border-left: none;
  border-right: none;
  border-radius: 0;
  margin: 0 0 0.5rem 0;
  padding: 0.5rem;
}

@media (min-width: 768px) {
  .controls {
    padding: 0.75rem;
    max-width: 100%;
    margin: 0 0 1rem 0;
    background-color: transparent;
    border: none;
    border-bottom: 1px solid #d7c89b;
    border-radius: 0;
    box-shadow: none;
  }
}

.quran-text-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  margin: 0 auto;
  padding: 2.5rem 0;
  min-height: 70vh;
  background-color: #fcf9ee; /* Slightly lighter parchment color for text area */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(167, 126, 45, 0.2);
  max-width: 90%;
}

/* Ornate border */
.quran-text-wrapper::before {
  content: "";
  position: absolute;
  top: 12px;
  left: 12px;
  right: 12px;
  bottom: 12px;
  border: 1px solid rgba(167, 126, 45, 0.3);
  border-radius: 4px;
  pointer-events: none;
  background-image: 
    linear-gradient(45deg, transparent 49.5%, rgba(167, 126, 45, 0.2) 49.5%, rgba(167, 126, 45, 0.2) 50.5%, transparent 50.5%),
    linear-gradient(-45deg, transparent 49.5%, rgba(167, 126, 45, 0.2) 49.5%, rgba(167, 126, 45, 0.2) 50.5%, transparent 50.5%);
  background-size: 20px 20px;
  background-position: 0 0, 10px 0;
  background-repeat: repeat-x, repeat-x;
  background-position-y: top, top;
}

/* Add decorative border to all sides */
.quran-text-wrapper::after {
  content: "";
  position: absolute;
  top: 25px;
  left: 25px;
  right: 25px;
  bottom: 25px;
  border: 1px solid rgba(167, 126, 45, 0.15);
  border-radius: 2px;
  pointer-events: none;
  
  /* Add decorative corner elements */
  background-image: 
    /* Top-left corner */
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cpath fill='%23a77e2d' fill-opacity='0.2' d='M0,40 L40,40 L40,37 C40,16.5 23.5,0 3,0 L0,0 L0,40 Z'/%3E%3C/svg%3E"),
    /* Top-right corner */
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cpath fill='%23a77e2d' fill-opacity='0.2' d='M0,40 L40,40 L40,0 L37,0 C16.5,0 0,16.5 0,37 L0,40 Z'/%3E%3C/svg%3E"),
    /* Bottom-left corner */
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cpath fill='%23a77e2d' fill-opacity='0.2' d='M0,0 L0,3 C0,23.5 16.5,40 37,40 L40,40 L40,0 L0,0 Z'/%3E%3C/svg%3E"),
    /* Bottom-right corner */
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cpath fill='%23a77e2d' fill-opacity='0.2' d='M40,0 L0,0 L0,40 L3,40 C23.5,40 40,23.5 40,3 L40,0 Z'/%3E%3C/svg%3E");
  
  background-position: 
    top left,     /* Top-left corner */
    top right,    /* Top-right corner */
    bottom left,  /* Bottom-left corner */
    bottom right; /* Bottom-right corner */
  
  background-repeat: no-repeat;
  background-size: 40px 40px;
}

/* Corner decorations */
.quran-text-flow {
  text-align: justify;
  line-height: 2;
  white-space: normal;
  text-justify: inter-word;
  padding: 2.5rem 2rem 2rem;
  margin: 0;
  width: 100%;
  column-count: 1;
  overflow-wrap: break-word;
  direction: rtl;
  font-size: 1.25rem;
  background-color: transparent;
  position: relative;
  z-index: 1;
}

/* Inner decorative corners */
.quran-text-flow::before,
.quran-text-flow::after,
.quran-text-flow .top-left-corner,
.quran-text-flow .bottom-right-corner {
  content: "";
  position: absolute;
  width: 50px;
  height: 50px;
  background-size: contain;
  background-repeat: no-repeat;
  opacity: 0.4;
  z-index: 0;
}

/* Top-right corner decoration */
.quran-text-flow::before {
  top: 10px;
  right: 10px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%23a77e2d' d='M95,5v40c0,27.614-22.386,50-50,50H5V5H95z M85,15H15v70h30c22.091,0,40-17.909,40-40V15z'/%3E%3Cpath fill='%23a77e2d' d='M50,50c-16.569,0-30-13.431-30-30h10c0,11.046,8.954,20,20,20V50z'/%3E%3C/svg%3E");
}

/* Bottom-left corner decoration */
.quran-text-flow::after {
  bottom: 10px;
  left: 10px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%23a77e2d' d='M5,95v-40c0-27.614,22.386-50,50-50H95V95H5z M15,85H85V15H55c-22.091,0-40,17.909-40,40V85z'/%3E%3Cpath fill='%23a77e2d' d='M50,50c16.569,0,30,13.431,30,30H70c0-11.046-8.954-20-20-20V50z'/%3E%3C/svg%3E");
}

/* Add the missing corners using ::before and ::after pseudo-elements on new elements */
.quran-text-wrapper .top-left-corner {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 50px;
  height: 50px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%23a77e2d' d='M5,5v90h90V5H5z M15,15h70v70H15V15z'/%3E%3Cpath fill='%23a77e2d' d='M50,50c16.569,0,30-13.431,30-30H70c0,11.046-8.954,20-20,20V50z'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  opacity: 0.4;
  z-index: 5;
  pointer-events: none;
}

.quran-text-wrapper .bottom-right-corner {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 50px;
  height: 50px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath fill='%23a77e2d' d='M95,95H5V5h90V95z M85,15H15v70h70V15z'/%3E%3Cpath fill='%23a77e2d' d='M50,50c-16.569,0-30,13.431-30,30h10c0-11.046,8.954-20,20-20V50z'/%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  opacity: 0.4;
  z-index: 5;
  pointer-events: none;
}

/* Add decorative horizontal rule above surah name */
.surah-decoration::before {
  content: "";
  position: absolute;
  top: -10px;
  left: 30px;
  right: 30px;
  height: 5px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='5' viewBox='0 0 100 5'%3E%3Cpath fill='%23a77e2d' fill-opacity='0.3' d='M0,2.5 Q25,0 50,2.5 T100,2.5'/%3E%3C/svg%3E");
  background-repeat: repeat-x;
  background-size: 100px 5px;
  opacity: 0.6;
  z-index: 2;
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
  font-family: "QuranFont", "Traditional Arabic", serif;
  font-size: 1.25rem;
  color: #000;
  word-spacing: normal;
  white-space: normal;
}

/* Override typical paragraph behavior for this specific use case */
.quran-text-flow p {
  display: inline;
  margin: 0;
  padding: 0;
}

.ayah-wrapper {
  position: relative;
  display: inline;
  margin: 0;
  padding: 0.6em 0 0;
}

.ayah-wrapper.playing-ayah-audio {
  background-color: rgba(79, 70, 229, 0.1);
  border-radius: 3px;
  padding: 0.6em 2px 0 2px;
}

/* Media queries for responsive font sizing */
@media (max-width: 480px) {
  .quran-text-flow {
    padding: 1.5rem 1rem 1.5rem;
    font-size: 1rem;
    line-height: 1.8;
  }
  
  .arabic-text .ayah-text {
    font-size: 1rem;
  }
  
  .quran-text-wrapper {
    max-width: 95%;
    padding: 1.5rem 0;
  }
  
  .quran-text-wrapper::before,
  .quran-text-wrapper::after {
    display: none;
  }
  
  .quran-text-flow::before,
  .quran-text-flow::after {
    width: 30px;
    height: 30px;
  }
}

@media (min-width: 481px) and (max-width: 767px) {
  .quran-text-flow {
    padding: 2rem 1.25rem 1.75rem;
    font-size: 1.125rem;
    line-height: 1.9;
  }
  
  .arabic-text .ayah-text {
    font-size: 1.125rem;
  }
  
  .quran-text-wrapper {
    max-width: 95%;
  }
  
  .quran-text-flow::before,
  .quran-text-flow::after {
    width: 40px;
    height: 40px;
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .quran-text-flow {
    padding: 2.5rem 1.5rem 2rem;
    font-size: 1.375rem;
    line-height: 2;
  }
  
  .arabic-text .ayah-text {
    font-size: 1.375rem;
  }
}

@media (min-width: 1024px) {
  .quran-text-flow {
    padding: 2.5rem 2rem 2rem;
    font-size: 1.5rem;
    line-height: 2.1;
  }
  
  .arabic-text .ayah-text {
    font-size: 1.5rem;
  }
  
  .quran-text-wrapper {
    max-width: 85%;
  }
}

.nav-button {
  @apply flex items-center justify-center space-x-1 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg border border-gray-300 hover:bg-gray-200 transition-colors;
}

.page-selector {
  @apply px-3 py-2 bg-gray-50 rounded-lg border border-gray-300 flex items-center;
  max-width: 100%;
  overflow-x: auto;
}

.go-button {
  @apply ml-2 px-3 py-1 bg-indigo-500 text-white rounded-md hover:bg-indigo-600 transition-colors;
}

.control-group {
  @apply flex flex-col;
  margin-bottom: 0.5rem;
}

.select-input {
  @apply border rounded py-2 px-3 bg-white text-sm appearance-none;
  min-width: 100px;
  max-width: 200px;
  width: auto;
}

.audio-button {
  @apply ml-2 px-3 py-1.5 bg-indigo-600 text-white rounded-lg flex items-center justify-center hover:bg-indigo-700 
  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 
  disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-indigo-600 transition-colors;
}

.loading-message, .error-message, .no-page {
  @apply flex flex-col items-center justify-center py-12 space-y-4;
  flex: 1;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  padding: 2rem;
  margin: 0 auto;
  max-width: 90%;
  border: 1px solid rgba(167, 126, 45, 0.2);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.loading-message {
  @apply text-gray-500;
}

.error-message {
  @apply text-red-500;
}

.page-number {
  @apply flex justify-center items-center my-4;
}

.page-number-container {
  @apply rounded-full flex items-center justify-center text-[#a77e2d] font-quran text-xl;
  width: 3rem;
  height: 3rem;
  background-color: rgba(201, 169, 89, 0.12);
  border: 1px solid rgba(201, 169, 89, 0.3);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.07);
  position: relative;
  z-index: 10;
}

.ayah {
  @apply mb-4 leading-loose;
}

.surah-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
  padding-top: 1rem;
}

.decoration-left, .decoration-right {
  flex-grow: 1;
  height: 1px;
  margin-left: 1rem;
  margin-right: 1rem;
  background: linear-gradient(to right, rgba(167, 126, 45, 0.05), rgba(167, 126, 45, 0.3), rgba(167, 126, 45, 0.05));
}

.surah-name {
  font-size: 1.5rem;
  font-family: "QuranFont", "Traditional Arabic", serif;
  color: #a77e2d;
  letter-spacing: 0.05em;
  padding-left: 1rem;
  padding-right: 1rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.bismillah {
  text-align: center;
  font-size: 1.875rem;
  margin-bottom: 1.5rem;
  color: #a77e2d;
  font-family: "QuranFont", "Traditional Arabic", serif;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.arabic-text {
  font-size: 0;  /* Remove space between inline elements */
  text-align: justify;
  word-spacing: 0;
  padding: 0.5rem;
}

.arabic-text .ayah-text,
.arabic-text .ayah-number,
.arabic-text .sajda-mark,
.arabic-text .ayah-audio-button {
  font-size: 1.25rem; /* Restore font size for actual text */
}

.arabic-text .ayah-number {
  display: inline;
  color: #a77e2d;
  font-family: "QuranFont", "Traditional Arabic", serif;
  margin: 0 1px;
  padding: 0;
  font-size: 0.6em;
  vertical-align: middle;
  opacity: 0.7;
}

.ayah-wrapper {
  position: relative;
  display: inline;
  margin: 0;
  padding: 0.6em 0 0;
}

.arabic-text .ayah-text {
  color: #333;
  display: inline;
  letter-spacing: 0;
  margin: 0;
  padding: 0;
  font-family: "QuranFont", "Traditional Arabic", serif;
}

.sajda-mark {
  display: inline;
  color: #a03030;
  font-family: "QuranFont", "Traditional Arabic", serif;
  margin: 0 2px;
  padding: 0;
  font-size: 0.7em;
  vertical-align: middle;
}

.translation-text .ayah-header {
  @apply flex justify-between mb-1 text-sm text-gray-500;
}

.translation-text .ayah-text {
  @apply text-lg leading-relaxed;
}

/* Add Quran-specific Arabic fonts */
@font-face {
  font-family: "QuranFont";
  src: url("@/assets/fonts/ScheherazadeNew-Regular.ttf") format("truetype");
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: "QuranFont";
  src: url("@/assets/fonts/ScheherazadeNew-Bold.ttf") format("truetype");
  font-weight: bold;
  font-style: normal;
}

.font-quran {
  font-family: "QuranFont", "Traditional Arabic", serif;
}

/* Audio Controls and Styling */
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
  background-color: rgba(255, 255, 255, 0.9);
  color: #4F46E5;
  border-radius: 50%;
  border: 1px solid #d1d5db;
  cursor: pointer;
  opacity: 0.8;
  z-index: 10;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.ayah-audio-button svg {
  width: 100%;
  height: 100%;
  padding: 15%;
}

.ayah-audio-button:hover {
  transform: translateX(50%) scale(1.1);
  opacity: 1;
  background-color: rgba(255, 255, 255, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.ayah-audio-button.active {
  background-color: #4F46E5;
  color: white;
  border-color: #4F46E5;
  opacity: 1;
}

.ayah-wrapper {
  position: relative;
  display: inline;
  margin: 0;
  padding: 0.6em 0 0;
}

/* Remove the old hover rule since we want buttons always visible */
.ayah-wrapper:hover .ayah-audio-button {
  opacity: 1;
}

.ayah-audio-button-translation {
  @apply inline-flex items-center justify-center px-2 py-1 text-xs font-medium bg-gray-50 text-gray-600 rounded border border-gray-200 hover:bg-indigo-50 hover:text-indigo-600 hover:border-indigo-300 transition-colors;
}

.ayah-audio-button-translation.active {
  @apply bg-indigo-100 text-indigo-600 border-indigo-300;
}

.ayah-wrapper.playing-ayah-audio,
.ayah.playing-ayah-audio {
  @apply bg-indigo-50 px-1 rounded-md;
}

.play-button {
  @apply text-xs;
}

.stop-button, .play-pause-button {
  @apply rounded-full p-1 hover:bg-indigo-100 transition-colors;
}

/* Add specific layout for when audio controls are shown */
.audio-player {
  @apply transition-all;
}

/* Mobile responsiveness for audio controls */
@media (max-width: 640px) {
  .reciter-selector select {
    @apply text-xs py-1;
  }
  
  .play-button {
    @apply text-xs py-1 px-2;
  }
  
  .audio-player {
    @apply p-2;
  }
  
  .audio-player .play-pause-button svg,
  .audio-player .stop-button svg {
    @apply h-8 w-8;
  }
  
  .ayah-audio-button-translation {
    @apply text-xs py-0.5 px-1.5;
  }
  
  .page-selector {
    @apply flex-wrap px-2;
  }
  
  .select-input {
    min-width: 80px;
    max-width: 150px;
  }
  
  .quran-text-flow {
    @apply text-xl;
    line-height: 2.6;
  }
  
  .bottom-nav-button {
    @apply text-sm px-2 py-1;
  }
}

.bottom-nav-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  background-color: #f5f1e4;
  color: #555;
  border-radius: 0.5rem;
  border: 1px solid #d7c89b;
  transition: all 0.2s ease;
}

.bottom-nav-button:hover {
  background-color: #ebe3d0;
}

.bottom-nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.no-page {
  @apply text-center py-8 text-gray-500;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* Media queries for responsive audio button sizing */
@media (max-width: 480px) {
  .ayah-audio-button {
    width: 1.1em;
    height: 1.1em;
    top: -0.4em;
  }
  
  .ayah-wrapper {
    padding: 0.5em 0 0;
  }
  
  .ayah-wrapper.playing-ayah-audio {
    padding: 0.5em 2px 0 2px;
  }
}

@media (min-width: 768px) {
  .ayah-audio-button {
    width: 1.3em;
    height: 1.3em;
  }
}
</style> 