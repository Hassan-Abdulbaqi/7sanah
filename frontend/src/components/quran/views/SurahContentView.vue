<template>
  <div>
    <!-- Surah Header -->
    <div class="surah-header">
      <h2 class="arabic-title">{{ currentSurah.name }}</h2>
      <h3 class="english-title">{{ currentSurah.englishName }} - {{ currentSurah.englishNameTranslation }}</h3>
      <p class="ayah-count">{{ currentSurah.numberOfAyahs }} {{ $t('quran.ayah') }}</p>
      
      <!-- Bismillah except for Surah 9 -->
      <div class="bismillah" v-if="shouldDisplayBismillah(currentSurah.number)">
        {{ extractBismillah(currentSurah.ayahs && currentSurah.ayahs.length > 0 ? currentSurah.ayahs[0].text : '') }}
      </div>
      
      <!-- Audio Controls and Settings -->
      <div class="surah-actions mt-3">
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2 sm:gap-3">
          <!-- Language Selection -->
          <div>
            <label class="block mb-1 text-xs sm:text-sm font-medium">{{ $t('quran.selectLanguage') }}</label>
            <select v-model="selectedTranslation" @change="onTranslationChange" class="select-input" :disabled="loadingTranslations">
              <option v-if="loadingTranslations" value="">{{ $t('quran.loading') }}</option>
              <optgroup v-for="(translations, lang) in groupedTranslations" :key="lang" :label="getLanguageName(lang)">
                <option v-for="translation in translations" :key="translation.identifier" :value="translation.identifier">
                  {{ translation.name }}
                </option>
              </optgroup>
            </select>
          </div>
          
          <!-- Reciter Selection -->
          <div>
            <label class="block mb-1 text-xs sm:text-sm font-medium">{{ $t('quran.selectReciter') }}</label>
            <select v-model="selectedReciter" @change="onReciterChange" class="select-input" :disabled="loadingReciters">
              <option v-if="loadingReciters" value="">{{ $t('quran.loading') }}</option>
              <optgroup v-for="(reciters, lang) in groupedReciters" :key="lang" :label="getLanguageName(lang)">
                <option v-for="reciter in reciters" :key="reciter.identifier" :value="reciter.identifier">
                  {{ reciter.name }}
                </option>
              </optgroup>
            </select>
          </div>
          
          <!-- Listen to Surah Button -->
          <div class="flex items-end sm:col-span-2 md:col-span-1">
            <button 
              @click="listenToFullSurah" 
              class="listen-surah-button w-full"
              :disabled="downloadingSurahAudio || isPlayingFullSurah"
              v-if="showListenButton"
            >
              <svg v-if="downloadingSurahAudio" class="animate-spin h-4 w-4 mr-1 sm:h-5 sm:w-5 sm:mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 sm:h-5 sm:w-5 sm:mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
              </svg>
              {{ downloadingSurahAudio ? $t('quran.loading') : $t('quran.listenToSurah') || 'Listen to Surah' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Verses with lazy loading -->
    <div 
      :class="['verses', { 'verses-when-collapsed': expanded, 'verses-container-expanded': expanded }]"
      ref="versesContainer" 
      @scroll="handleScroll"
    >
      <div 
        v-for="verse in displayedVerses" 
        :key="verse.number"
        :id="`verse-${verse.numberInSurah}`"
        :class="[
          'verse-container mb-3 rounded-lg',
          {
            'bg-gray-50': verse.numberInSurah % 2 === 0,
            'bg-white': verse.numberInSurah % 2 !== 0,
            'playing-ayah-audio': (currentPlayingVerse === verse.numberInSurah) || (loadingVerseAudio === verse.numberInSurah)
          }
        ]"
      >
        <div class="verse-number">{{ verse.numberInSurah }}</div>
        
        <div class="arabic-text">{{ cleanAyahText(verse.text, currentSurah.number, verse.numberInSurah) }}</div>
        
        <div v-if="translatedVerses[verse.number]" class="translation-text">
          {{ translatedVerses[verse.number] }}
        </div>
        
        <div class="verse-footer">
          <div class="verse-actions">
            <button 
              @click="toggleVerseAudio(verse.numberInSurah, verse.number)"
              class="verse-action-button"
              :class="{ 'active': currentPlayingVerse === verse.numberInSurah }"
              :disabled="loadingVerseAudio !== null && loadingVerseAudio !== verse.numberInSurah"
            >
              <svg v-if="loadingVerseAudio === verse.numberInSurah" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else-if="currentPlayingVerse === verse.numberInSurah && !paused" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <svg v-else-if="currentPlayingVerse === verse.numberInSurah && paused" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Loading more indicator -->
      <div v-if="isLoadingMore" class="text-center py-3">
        <button 
          @click="loadMoreChunk" 
          class="load-more-button mb-2 px-4 py-2 sm:px-6 sm:py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-medium transition-colors shadow-sm flex items-center justify-center mx-auto"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 sm:h-5 sm:w-5 sm:mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clip-rule="evenodd" />
          </svg>
          {{ $t('quran.loadMoreVerses') || 'تحميل المزيد من الآيات' }}
        </button>
        
        <!-- Load all button -->
        <button 
          @click="loadAllRemainingVerses" 
          class="load-all-button px-3 py-1.5 sm:px-4 sm:py-2 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 rounded-md text-sm font-medium transition-colors"
        >
          {{ $t('quran.loadAllVerses') || 'تحميل جميع الآيات دفعة واحدة' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SurahContentView',
  props: {
    currentSurah: {
      type: Object,
      required: true
    },
    expanded: {
      type: Boolean,
      default: false
    },
    groupedTranslations: {
      type: Object,
      required: true
    },
    groupedReciters: {
      type: Object,
      required: true
    },
    loadingTranslations: {
      type: Boolean,
      default: false
    },
    loadingReciters: {
      type: Boolean,
      default: false
    },
    isPlayingFullSurah: {
      type: Boolean,
      default: false
    },
    downloadingSurahAudio: {
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
    loadingVerseAudio: {
      type: Number,
      default: null
    },
    currentPlayingVerse: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      selectedTranslation: 'en.asad',
      selectedReciter: 'ar.alafasy',
      translatedVerses: {},
      displayedVerses: [],
      isLoadingMore: false,
      verseChunkSize: 20,
      initialChunkSize: 10,
      largeVerseThreshold: 100,
      loadingChunks: false,
      scrollThreshold: 300,
      prefetchThreshold: 500,
      loadThreshold: 300,
      isLargeSurah: false,
      highlightedAyah: null,
      _scrollDebounceTimer: null,
      _prefetchTimer: null,
      _shouldPrefetch: false,
      _loadAttempts: 0,
      backupLoadTimer: null,
      showListenButton: true
    }
  },
  watch: {
    currentSurah: {
      handler(newSurah) {
        if (newSurah) {
          // Reset displayed verses and load initial chunk
          this.displayedVerses = []
          this.translatedVerses = {}
          this.isLargeSurah = newSurah.ayahs && newSurah.ayahs.length > this.largeVerseThreshold
          this.loadInitialVerses()
          this.loadTranslation()
        }
      },
      immediate: true,
      deep: true
    }
  },
  created() {
    // Load user preferences from localStorage
    this.loadUserPreferences();
  },
  methods: {
    // Function to check if a surah should display Bismillah
    // All surahs except Surah At-Tawbah (9) should have Bismillah
    shouldDisplayBismillah(surahNumber) {
      return surahNumber !== 9; // Surah At-Tawbah (9) doesn't have Bismillah
    },
    
    // Function to extract Bismillah from the first ayah if needed
    extractBismillah(ayahText) {
      if (!ayahText) return 'بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ';
      
      // Always return the standard Bismillah text for consistency
      return 'بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ';
    },
    
    // Function to remove Bismillah from ayah text if it's included
    cleanAyahText(ayahText, surahNumber, ayahNumberInSurah) {
      // Only process the first ayah of each surah (except for Surah Al-Fatiha and At-Tawbah)
      if (ayahNumberInSurah === 1 && surahNumber !== 1 && surahNumber !== 9) {
        // Find where the Bismillah ends by checking for space or special character after it
        // Try 38 characters, then 39, then 40 if needed
        
        let cleanedText = '';
        // Start with standard length of 38-39 characters
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
    
    getLanguageName(langCode) {
      this.$emit('get-language-name', langCode)
    },
    
    onTranslationChange() {
      this.loadTranslation();
      this.saveUserPreferences();
    },
    
    onReciterChange() {
      this.saveUserPreferences();
    },
    
    saveUserPreferences() {
      // Save user preferences to localStorage
      try {
        const preferences = {
          selectedTranslation: this.selectedTranslation,
          selectedReciter: this.selectedReciter,
          timestamp: new Date().getTime()
        };
        localStorage.setItem('quranUserPreferences', JSON.stringify(preferences));
        console.log('User preferences saved:', preferences);
      } catch (error) {
        console.error('Error saving user preferences:', error);
      }
    },
    
    listenToFullSurah() {
      this.$emit('listen-to-full-surah', this.selectedReciter);
    },
    
    stopAudio() {
      this.$emit('stop-audio')
    },
    
    togglePause() {
      this.$emit('toggle-pause')
    },
    
    seekAudio(event) {
      this.$emit('seek-audio', event)
    },
    
    toggleVerseAudio(verseNumberInSurah, verseNumber) {
      this.$emit('toggle-verse-audio', {
        verseNumberInSurah,
        verseNumber,
        reciter: this.selectedReciter
      })
    },
    
    handleScroll(event) {
      if (!this.currentSurah) return;
      
      // Check if we have more verses to load
      const hasMoreVersesToLoad = this.displayedVerses && 
                               this.currentSurah.ayahs && 
                               this.displayedVerses.length < this.currentSurah.ayahs.length;
      
      // If no more verses to load, reset loading state and exit
      if (!hasMoreVersesToLoad) {
        if (this.isLoadingMore) {
          this.isLoadingMore = false;
          this.loadingChunks = false;
        }
        return;
      }
      
      // Ignore scroll events if we're already loading
      if (this.loadingChunks) return;
      
      const container = event.target;
      const scrollHeight = container.scrollHeight;
      const scrollTop = container.scrollTop;
      const clientHeight = container.clientHeight;
      
      // Calculate the distance from the bottom
      const distanceFromBottom = scrollHeight - scrollTop - clientHeight;
      
      // Force detection of very small containers
      const isNearBottom = distanceFromBottom < this.loadThreshold || 
                        (scrollHeight <= clientHeight * 1.5 && scrollTop > 0);
      
      // If we've reached near the bottom and have more verses to load, show the load more button
      if (isNearBottom) {
        this.isLoadingMore = true;
      }
    },
    
    loadInitialVerses() {
      if (!this.currentSurah || !this.currentSurah.ayahs || !Array.isArray(this.currentSurah.ayahs)) {
        return
      }
      
      // Determine appropriate initial chunk size for the surah
      let initialSize = this.verseChunkSize
      
      if (this.isLargeSurah) {
        // For very large surahs, use smaller initial chunk but load more later
        if (this.currentSurah.ayahs.length > 200) {
          initialSize = Math.min(initialSize, 20)
        }
      } else {
        initialSize = this.verseChunkSize // Use regular chunk size for normal surahs
      }
      
      // If the surah is small enough, load all verses at once
      if (this.currentSurah.ayahs.length <= initialSize) {
        this.displayedVerses = this.currentSurah.ayahs
        this.isLoadingMore = false
        this.loadingChunks = false
        return
      }
      
      // Load first chunk immediately without delay for better UX
      this.displayedVerses = this.currentSurah.ayahs.slice(0, initialSize)
      
      // If there are more verses, set up loading indicator and prepare to load more
      if (initialSize < this.currentSurah.ayahs.length) {
        this.isLoadingMore = true
        
        // Schedule loading of next chunk after a short delay
        setTimeout(() => {
          if (this.isLoadingMore) {  // Double-check we still need to load more
            this.$emit('load-more-verses', this.verseChunkSize)
          }
        }, 100)
        
        // Set up a backup mechanism that loads all verses if lazy loading is stuck
        this.setupAutoLoadBackup()
      } else {
        // All verses are loaded, make sure loading state is reset
        this.isLoadingMore = false
        this.loadingChunks = false
      }
    },
    
    // Setup a backup mechanism to load all verses if scrolling doesn't work
    setupAutoLoadBackup() {
      // Clear any existing backup timer
      if (this.backupLoadTimer) {
        clearTimeout(this.backupLoadTimer)
      }
      
      // We don't need a backup timer anymore since loading is manual
      // but we'll keep a minimal implementation for compatibility
      this._loadAttempts = 0
    },
    
    loadAllRemainingVerses() {
      if (!this.currentSurah || !this.currentSurah.ayahs) return;
      
      this.loadingChunks = true;
      
      // Add all remaining verses to the displayed verses
      this.displayedVerses = [...this.currentSurah.ayahs];
      
      // Reset loading states
      this.isLoadingMore = false;
      this.loadingChunks = false;
      
      // Emit event for parent component
      this.$emit('load-all-remaining-verses-completed');
    },
    
    async loadTranslation() {
      if (!this.currentSurah?.number || !this.selectedTranslation) return
      
      // Set a flag to show that translations are loading
      const loadingMessage = this.$t('quran.loadingTranslations');
      const tempTranslations = {};
      
      try {
        // Create a temporary loading message for each verse
        if (this.currentSurah && this.currentSurah.ayahs) {
          this.currentSurah.ayahs.forEach(ayah => {
            tempTranslations[ayah.numberInSurah] = loadingMessage;
          });
          
          // Set these temporary translations first so the UI isn't empty
          this.translatedVerses = {...tempTranslations};
        }
        
        // Then load the actual translations in the background
        const response = await fetch(`http://api.alquran.cloud/v1/surah/${this.currentSurah.number}/${this.selectedTranslation}`)
        const data = await response.json()
        
        if (data.code === 200) {
          // Create a mapping of verse number to translation
          const translations = {}
          data.data.ayahs.forEach(ayah => {
            translations[ayah.numberInSurah] = ayah.text
          })
          
          // Update the translations gradually to avoid UI freezes with large suras
          if (this.isLargeSurah && Object.keys(translations).length > 100) {
            // For large suras, update translations in batches
            const batchSize = 30;
            const keys = Object.keys(translations);
            
            // Create a function to update translations in batches
            const updateBatch = (startIdx) => {
              const endIdx = Math.min(startIdx + batchSize, keys.length);
              const currentBatch = {};
              
              for (let i = startIdx; i < endIdx; i++) {
                const key = keys[i];
                currentBatch[key] = translations[key];
              }
              
              // Update the current batch
              this.translatedVerses = {...this.translatedVerses, ...currentBatch};
              
              // Schedule next batch if needed
              if (endIdx < keys.length) {
                setTimeout(() => updateBatch(endIdx), 10);
              }
            };
            
            // Start the batch updates
            updateBatch(0);
          } else {
            // For smaller suras, update all at once
            this.translatedVerses = translations;
          }
        }
      } catch (error) {
        console.error('Error fetching translation:', error)
      }
    },
    
    formatTime(seconds) {
      if (!seconds || isNaN(seconds)) return '0:00'
      
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = Math.floor(seconds % 60)
      
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
    },
    
    loadMoreChunk() {
      if (!this.currentSurah || !this.currentSurah.ayahs) return;
      
      this.loadingChunks = true;
      
      // Calculate the next chunk of verses to load
      const currentCount = this.displayedVerses.length;
      const totalVerses = this.currentSurah.ayahs.length;
      
      if (currentCount >= totalVerses) {
        // All verses are loaded
        this.isLoadingMore = false;
        this.loadingChunks = false;
        return;
      }
      
      // Calculate end index for next chunk
      const endIndex = Math.min(currentCount + this.verseChunkSize, totalVerses);
      
      // Get the next chunk of verses
      const nextChunk = this.currentSurah.ayahs.slice(currentCount, endIndex);
      
      // Add the new verses to the displayed verses
      this.displayedVerses = [...this.displayedVerses, ...nextChunk];
      
      // Check if we have loaded all verses
      if (this.displayedVerses.length >= totalVerses) {
        this.isLoadingMore = false;
      }
      
      this.loadingChunks = false;
      
      // Emit event for parent component
      this.$emit('load-more-verses-completed', this.displayedVerses.length);
    },
    
    loadUserPreferences() {
      try {
        const savedPreferences = localStorage.getItem('quranUserPreferences');
        if (savedPreferences) {
          const preferences = JSON.parse(savedPreferences);
          
          // Check if preferences are still valid (not too old)
          const now = new Date().getTime();
          const oneMonthInMs = 30 * 24 * 60 * 60 * 1000;
          
          if (preferences.timestamp && (now - preferences.timestamp) < oneMonthInMs) {
            // Apply saved preferences
            if (preferences.selectedTranslation) {
              this.selectedTranslation = preferences.selectedTranslation;
            }
            
            if (preferences.selectedReciter) {
              this.selectedReciter = preferences.selectedReciter;
            }
            
            console.log('Loaded user preferences:', preferences);
          } else {
            // Preferences are too old, remove them
            localStorage.removeItem('quranUserPreferences');
          }
        }
      } catch (error) {
        console.error('Error loading user preferences:', error);
      }
    }
  }
}
</script>

<style scoped>
.surah-header {
  @apply bg-white p-3 sm:p-4 border border-gray-200 rounded-lg mb-3 text-center;
}

.arabic-title {
  @apply text-2xl font-bold mb-1;
  font-family: 'Scheherazade New', serif;
}

.english-title {
  @apply text-lg font-semibold text-gray-700 mb-1;
}

.ayah-count {
  @apply text-sm text-gray-500 mb-2;
}

.bismillah {
  @apply text-xl mb-3 text-center font-semibold;
  font-family: 'Scheherazade New', serif;
}

.select-input {
  @apply w-full px-2 py-1.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent;
}

.listen-surah-button {
  @apply px-3 py-1.5 bg-indigo-600 text-white rounded-lg flex items-center justify-center hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-indigo-600 transition-colors;
}

.verses {
  @apply bg-white border border-gray-200 rounded-lg overflow-y-auto mt-2 p-2 sm:p-4;
  max-height: 65vh;
  scroll-behavior: smooth;
}

.verses-when-collapsed {
  max-height: 75vh;
}

.verses-container-expanded {
  @apply mt-0;
}

.verse-container {
  @apply px-2 py-3 relative overflow-hidden border-b border-gray-200 last:border-b-0;
}

.verse-number {
  @apply absolute top-3 right-2 w-6 h-6 flex items-center justify-center bg-indigo-100 text-indigo-700 font-bold rounded-full text-xs;
}

.arabic-text {
  @apply text-xl mb-2 leading-loose text-right;
  font-family: 'Scheherazade New', serif;
  padding-right: 2rem;
}

.translation-text {
  @apply text-gray-700 leading-relaxed text-sm sm:text-base;
}

.verse-footer {
  @apply mt-2 flex justify-between items-center;
}

.verse-actions {
  @apply flex space-x-1;
}

.verse-action-button {
  @apply p-1.5 bg-gray-100 text-gray-700 rounded-full hover:bg-indigo-100 hover:text-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors;
}

.verse-action-button.active {
  @apply bg-indigo-500 text-white hover:bg-indigo-600;
}

.highlighted {
  @apply bg-indigo-50;
}

.playing-ayah-audio {
  @apply bg-indigo-100 border-l-4 border-indigo-400;
}

.load-more-button {
  @apply transition-all duration-200 text-sm;
}

.load-more-button:hover {
  @apply transform scale-105;
}

.load-all-button {
  @apply transition-all duration-200 text-xs sm:text-sm;
}

.load-all-button:hover {
  @apply transform scale-105;
}

.verse-highlight-animation {
  animation: verse-highlight 2s ease-in-out;
}

@keyframes verse-highlight {
  0% {
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
  }
  50% {
    box-shadow: 0 0 0 6px rgba(99, 102, 241, 0.4);
  }
  100% {
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0);
  }
}

/* Media queries for responsive design */
@media (max-width: 640px) {
  .surah-actions .grid {
    @apply gap-2;
  }
  
  .verses {
    max-height: 70vh;
    @apply px-1 py-2;
  }
  
  .arabic-title {
    @apply text-xl;
  }
  
  .english-title {
    @apply text-base;
  }
  
  .bismillah {
    @apply text-lg mb-2;
  }
  
  .verse-container {
    @apply mx-0 px-2 py-2;
  }
  
  .arabic-text {
    @apply text-lg;
    padding-right: 1.75rem;
  }
  
  .translation-text {
    @apply text-xs leading-relaxed;
  }
  
  .verse-number {
    @apply w-5 h-5 text-xs top-2 right-1;
  }
  
  .verse-action-button {
    @apply p-1;
  }
}

@media (min-width: 640px) {
  .verse-container {
    @apply px-3 py-3;
  }
}

@media (min-width: 768px) {
  .verse-container {
    @apply px-4 py-4;
  }
}
</style> 