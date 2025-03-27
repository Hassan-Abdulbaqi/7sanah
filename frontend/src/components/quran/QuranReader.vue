<template>
  <div class="quran-reader light-mode">
    <h1 class="text-2xl font-bold text-center mb-6">{{ $t('quran.title') }}</h1>
    
    <!-- Advanced Search Button -->
    <div class="flex justify-center mb-4">
      <router-link to="/quran-search" class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
        </svg>
        {{ $t('quran.advancedSearch') }}
      </router-link>
    </div>
    
    <div class="quran-container">
      <!-- View Mode Switcher -->
      <div class="view-mode-switcher mb-4">
        <div class="flex justify-center space-x-2">
          <button 
            @click="viewMode = 'surah'" 
            :class="['view-mode-button', { active: viewMode === 'surah' }]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
            </svg>
            {{ $t('quran.surahView') }}
          </button>
          <router-link 
            to="/quran/book"
            :class="['view-mode-button', { active: $route.path.includes('/quran/book') }]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
            </svg>
            {{ $t('quran.bookView') }}
          </router-link>
        </div>
      </div>

      <!-- Surah View Content -->
      <div v-if="viewMode === 'surah'">
        <!-- Toggle button for surah list when a surah is selected -->
        <div v-if="selectedSurah && surahListCollapsed" class="flex justify-center mb-4">
          <button 
            @click="surahListCollapsed = false" 
            class="inline-flex items-center px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
            {{ $t('quran.showSurahList') || 'Show Surah List' }}
          </button>
        </div>
        
        <!-- Surah Selection and Audio Controls - Hide when a surah is selected and list is collapsed -->
        <div v-if="!selectedSurah || !surahListCollapsed">
          <!-- Collapse button when surah is selected -->
          <div v-if="selectedSurah" class="flex justify-center mb-4">
            <button 
              @click="surahListCollapsed = true" 
              class="inline-flex items-center px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clip-rule="evenodd" />
              </svg>
              {{ $t('quran.hideSurahList') || 'Hide Surah List' }}
            </button>
          </div>
          
          <!-- Surah List Component -->
          <SurahList 
            :surahs="surahs" 
            :selected-surah="selectedSurah" 
            :loading="loading"
            @select-surah="onSelectSurah"
          />
        </div>
        
        <!-- Loading State -->
        <div v-if="loading" class="loading-message">
          <svg class="animate-spin h-10 w-10 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p>{{ $t('common.loading') }}</p>
        </div>
        
        <!-- Error State -->
        <div v-else-if="error" class="error-message">
          <svg class="h-10 w-10 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <p>{{ error }}</p>
        </div>
        
        <!-- Surah Content -->
        <div 
          v-else-if="!loading && !error && selectedSurah && currentSurah" 
          :class="['surah-content', { 'surah-content-expanded': surahListCollapsed }]"
        >
          <SurahContentView 
            :current-surah="currentSurah"
            :expanded="surahListCollapsed"
            :grouped-translations="groupedTranslations"
            :grouped-reciters="groupedReciters"
            :loading-translations="loadingTranslations"
            :loading-reciters="loadingReciters"
            :is-playing-full-surah="isPlayingFullSurah"
            :downloading-surah-audio="downloadingSurahAudio"
            :paused="paused"
            :audio-player="audioPlayer"
            :audio-progress="audioProgress"
            :audio-duration="audioDuration"
            :loading-verse-audio="loadingVerseAudio"
            :current-playing-verse="currentPlayingVerse"
            :highlighted-ayah="highlightedAyah"
            @get-language-name="getLanguageName"
            @load-more-verses="loadMoreVerses"
            @load-more-verses-completed="loadMoreVersesCompleted"
            @load-all-remaining-verses="loadAllRemainingVerses"
            @load-all-remaining-verses-completed="loadAllRemainingVersesCompleted"
            @listen-to-full-surah="listenToFullSurah"
            @stop-audio="stopAudio"
            @toggle-pause="togglePause"
            @seek-audio="seekAudio"
            @toggle-verse-audio="toggleVerseAudio"
          />
        </div>
        
        <!-- No Surah Selected -->
        <div class="no-selection" v-if="!loading && !error && !selectedSurah">
          <p class="text-center text-gray-500">{{ $t('quran.selectSurahPrompt') }}</p>
        </div>
      </div>

      <!-- Book View Content will be implemented next -->
      <div v-if="viewMode === 'book'" class="book-view">
        <BookView 
          :grouped-translations="groupedTranslations"
          :languages="languages"
        />
      </div>
    </div>
  </div>
  
  <!-- Floating Audio Controls -->
  <AudioControls 
    v-if="audioPlayer"
    :audio-player="audioPlayer"
    :paused="paused"
    :audio-progress="audioProgress"
    :audio-duration="audioDuration"
    :current-surah="currentSurah"
    :current-playing-verse="currentPlayingVerse"
    :floating="true"
    :show-listen-button="false"
    @toggle-pause="togglePause"
    @stop-audio="stopAudio"
    @seek-audio="seekAudio"
  />
</template>

<script>
import SurahList from './common/SurahList.vue'
import SurahContentView from './views/SurahContentView.vue'
import AudioControls from './common/AudioControls.vue'
import BookView from './views/BookView.vue'

export default {
  name: 'QuranReader',
  components: {
    SurahList,
    SurahContentView,
    AudioControls,
    BookView
  },
  data() {
    return {
      surahs: [],
      selectedSurah: null,
      currentSurah: null,
      translations: [],
      reciters: [],
      languages: {},
      groupedTranslations: {},
      groupedReciters: {},
      loading: false,
      loadingTranslations: false,
      loadingReciters: false,
      error: null,
      loadingVerseAudio: null,
      isPlayingFullSurah: false,
      paused: false,
      downloadingSurahAudio: false,
      audioPlayer: null,
      viewMode: 'surah',
      currentPage: 1,
      jumpToPage: 1,
      loadingPage: false,
      pageError: null,
      currentPageData: null,
      pageTranslation: [],
      currentPageInfo: '',
      isPlayingPageAudio: false,
      downloadingPageAudio: false,
      highlightedAyah: null,
      pageAyahsAudio: [],
      audioProgress: 0,
      audioDuration: 0,
      audioUpdateInterval: null,
      surahListCollapsed: false,
      audioStopped: true,
      currentPlayingVerse: null,
      audioQueue: [],
      currentAudioIndex: 0,
      currentAudioRequestId: null,
      _isStoppingAudio: false
    }
  },
  async created() {
    try {
      this.loading = true
      
      // Check for navigation data in localStorage
      let targetSurah = null
      let targetVerse = null
      let targetEdition = null
      
      try {
        const navigationData = localStorage.getItem('quranNavigationTarget')
        if (navigationData) {
          const navTarget = JSON.parse(navigationData)
          
          // Check if the data is fresh (less than 10 seconds old)
          const timestamp = navTarget.timestamp || 0
          const isDataFresh = (new Date().getTime() - timestamp) < 10000 // 10 seconds
          
          if (isDataFresh) {
            targetSurah = navTarget.surah
            targetVerse = navTarget.verse
            targetEdition = navTarget.edition
            
            // Clear the data so we don't reuse it on next load
            localStorage.removeItem('quranNavigationTarget')
            
            // Set the highlighted ayah immediately if verse exists
            if (targetVerse) {
              this.highlightedAyah = parseInt(targetVerse)
            }
          } else {
            localStorage.removeItem('quranNavigationTarget')
          }
        } else {
          // Check URL query parameters as fallback
          const urlParams = new URLSearchParams(window.location.search)
          if (urlParams.has('surah')) {
            targetSurah = parseInt(urlParams.get('surah'))
            
            if (urlParams.has('verse')) {
              targetVerse = parseInt(urlParams.get('verse'))
              this.highlightedAyah = targetVerse
            }
          }
        }
      } catch (e) {
        console.error('Error parsing navigation data:', e)
      }
      
      // Fetch surahs
      const surahsResponse = await fetch('https://api.alquran.cloud/v1/surah')
      const surahsData = await surahsResponse.json()
      
      if (surahsData.code === 200) {
        this.surahs = surahsData.data
      } else {
        this.error = surahsData.status
      }
      
      // Fetch editions
      await this.fetchEditions()
      
      // If we have navigation data, navigate to the specified surah
      if (targetSurah) {
        console.log(`Auto-selecting surah ${targetSurah} from navigation data`)
        this.selectedSurah = parseInt(targetSurah)
        
        if (targetEdition) {
          this.selectedTranslation = targetEdition
        }
        
        try {
          // Load the surah
          await this.loadSurah()
          
          // After the surah is loaded, scroll to the verse if specified
          if (targetVerse) {
            setTimeout(() => {
              try {
                // Make sure the verse is highlighted
                this.highlightedAyah = parseInt(targetVerse)
                
                // Scroll to the verse
                this.scrollToVerse(parseInt(targetVerse))
              } catch (scrollError) {
                console.error('Error scrolling to verse:', scrollError)
              }
            }, 500)
          }
        } catch (loadError) {
          console.error('Error loading surah:', loadError)
          this.error = this.$t('quran.loadingError')
        }
      }
      
    } catch (error) {
      console.error('Error initializing Quran reader:', error)
      this.error = this.$t('quran.networkError')
    } finally {
      this.loading = false
    }
  },
  watch: {
    viewMode(newMode) {
      if (newMode === 'book' && !this.currentPageData) {
        // Load the first page when switching to book view for the first time
        this.loadPage()
      }
    }
  },
  methods: {
    // Helper method to get language name from code
    getLanguageName(langCode) {
      return this.languages[langCode] || langCode.toUpperCase()
    },
    
    async fetchEditions() {
      try {
        this.loadingTranslations = true
        this.loadingReciters = true
        
        // Use the specified API endpoint to get all editions
        const response = await fetch('https://api.alquran.cloud/v1/edition')
        const data = await response.json()
        
        if (data.code === 200) {
          // Extract languages from the editions data
          const languageMap = {}
          const allLanguages = new Set()
          
          data.data.forEach(edition => {
            if (edition.language) {
              allLanguages.add(edition.language)
            }
          })
          
          // Create a placeholder map of language codes to names
          Array.from(allLanguages).forEach(langCode => {
            languageMap[langCode] = langCode.toUpperCase()
          })
          
          this.languages = languageMap
          
          // Filter and organize editions
          const translations = data.data.filter(edition => edition.format === 'text' && edition.type === 'translation')
          const reciters = data.data.filter(edition => edition.format === 'audio')
          
          this.translations = translations
          this.reciters = reciters
          
          // Group translations by language
          const groupedTranslations = {}
          translations.forEach(translation => {
            const langCode = translation.language
            if (!groupedTranslations[langCode]) {
              groupedTranslations[langCode] = []
            }
            groupedTranslations[langCode].push(translation)
          })
          
          // Group reciters by language
          const groupedReciters = {}
          reciters.forEach(reciter => {
            const langCode = reciter.language
            if (!groupedReciters[langCode]) {
              groupedReciters[langCode] = []
            }
            groupedReciters[langCode].push(reciter)
          })
          
          // Sort languages alphabetically
          this.groupedTranslations = Object.keys(groupedTranslations)
            .sort((a, b) => {
              const langA = this.getLanguageName(a)
              const langB = this.getLanguageName(b)
              return langA.localeCompare(langB)
            })
            .reduce((obj, key) => {
              obj[key] = groupedTranslations[key]
              return obj
            }, {})
            
          this.groupedReciters = Object.keys(groupedReciters)
            .sort((a, b) => {
              const langA = this.getLanguageName(a)
              const langB = this.getLanguageName(b)
              return langA.localeCompare(langB)
            })
            .reduce((obj, key) => {
              obj[key] = groupedReciters[key]
              return obj
            }, {})
        }
      } catch (error) {
        console.error('Error fetching editions:', error)
      } finally {
        this.loadingTranslations = false
        this.loadingReciters = false
      }
    },
    
    async loadSurah() {
      // Check if a surah is selected
      if (!this.selectedSurah) {
        console.error('No surah selected')
        return
      }
      
      try {
        // Start loading state
        this.loading = true
        this.error = null
        
        // First, stop any playing audio completely and wait for cleanup
        // This needs to happen before any other operations
        this.stopAudio()
        
        // Wait a short moment to ensure audio cleanup is complete
        await new Promise(resolve => setTimeout(resolve, 50))
        
        // Clear any existing surah data
        this.currentSurah = null
        
        console.log(`Loading surah ${this.selectedSurah} with highlighting for verse ${this.highlightedAyah || 'none'}`)
        
        // Fetch the surah data from the API
        const response = await fetch(`https://api.alquran.cloud/v1/surah/${this.selectedSurah}/quran-uthmani`)
        const data = await response.json()
        
        if (data.code === 200) {
          // Set the current surah
          this.currentSurah = data.data
          
          // If this is the first time loading, collapse the surah list for better readability
          if (!this.surahListCollapsed) {
            this.surahListCollapsed = true
          }
          
          // Force a reactivity update for the highlighted verse in case it was set before the surah loaded
          if (this.highlightedAyah) {
            console.log(`Highlighting ayah ${this.highlightedAyah} after surah load`)
            // Use a temporary variable to force Vue to detect the change
            const ayahToHighlight = this.highlightedAyah
            this.highlightedAyah = null
            
            // Short delay to ensure component updates
            setTimeout(() => {
              this.highlightedAyah = ayahToHighlight
            }, 100)
          }
        } else {
          this.error = data.status || this.$t('quran.loadingError')
        }
      } catch (error) {
        console.error('Error loading surah:', error)
        this.error = this.$t('quran.networkError')
      } finally {
        this.loading = false
      }
    },
    
    onSelectSurah(surahNumber) {
      // Make sure audio is completely stopped before switching surahs
      if (this.audioPlayer || this.isPlayingFullSurah || this.currentPlayingVerse) {
        this.stopAudio();
        
        // Give a small delay to ensure audio cleanup is complete before loading the new surah
        setTimeout(() => {
          this.selectedSurah = surahNumber;
          this.loadSurah();
        }, 100);
      } else {
        // No audio playing, can switch immediately
        this.selectedSurah = surahNumber;
        this.loadSurah();
      }
    },
    
    loadMoreVerses(chunkSize) {
      // This method will be called when the "Load More" button is clicked
      // The actual loading is now handled by the SurahContentView component
      console.log(`Loading more verses requested with chunk size ${chunkSize}`)
    },
    
    loadMoreVersesCompleted(loadedCount) {
      console.log(`Loading more verses completed. Now displaying ${loadedCount} verses.`)
    },
    
    loadAllRemainingVerses() {
      // This method will be called when the "Load All" button is clicked
      // The actual loading is now handled by the SurahContentView component
      console.log('Loading all remaining verses')
    },
    
    loadAllRemainingVersesCompleted() {
      console.log('All verses loaded successfully.')
    },
    
    jumpToSearchResult(match) {
      if (match && match.surah) {
        // Set the selected surah
        this.selectedSurah = match.surah.number
        
        // Load the surah content
        this.loadSurah().then(() => {
          // After the surah is loaded, highlight and scroll to the verse
          setTimeout(() => {
            if (match.numberInSurah) {
              this.highlightedAyah = match.numberInSurah
              
              // Use the existing scrollToVerse method
              this.scrollToVerse(match.numberInSurah)
            }
          }, 500)
        })
      }
    },
    
    // Audio methods
    toggleVerseAudio({ verseNumberInSurah, verseNumber, reciter }) {
      // If this verse is already playing, toggle pause/play
      if (this.currentPlayingVerse === verseNumberInSurah) {
        this.togglePause();
        return;
      }
      
      // We need to ensure audio is fully stopped before creating a new audio player
      // First, mark that we're loading a new verse
      const targetVerseNumber = verseNumberInSurah;
      const targetGlobalVerseNumber = verseNumber;
      const targetReciter = reciter || 'ar.alafasy';
      
      // Set loading state before stopping current audio
      this.loadingVerseAudio = targetVerseNumber;
      
      // Stop any currently playing audio and wait for the cleanup to complete
      this.stopAudio();
      
      // Use setTimeout to ensure the audio cleanup is complete before starting new audio
      setTimeout(() => {
        // Now create a new audio player
        this.currentPlayingVerse = targetVerseNumber;
        this.audioStopped = false;
        this.audioPlayer = new Audio();
        
        // Set up event listeners
        this.audioPlayer.addEventListener('ended', () => {
          // When single verse ends, stop playback instead of continuing
          console.log('Audio ended normally, cleaning up');
          this.currentPlayingVerse = null;  // Clear the current playing verse first
          this.audioStopped = true;  // Mark as stopped before cleanup
          
          // Use setTimeout to ensure this happens after the event processing is complete
          setTimeout(() => {
            this.stopAudio();
          }, 0);
        });
        
        this.audioPlayer.addEventListener('error', (error) => {
          // Check if the error is happening during normal cleanup
          if (this.audioStopped) {
            console.log('Error event occurred during cleanup, ignoring');
            return;
          }
          
          console.error('Error playing audio:', error.target?.error || 'Unknown error');
          this.currentPlayingVerse = null;  // Clear the current playing verse first
          this.audioStopped = true;  // Mark as stopped before cleanup
          
          // Use setTimeout to ensure this happens after the event processing is complete
          setTimeout(() => {
            this.stopAudio();
          }, 0);
        });
        
        this.audioPlayer.addEventListener('canplay', () => {
          this.loadingVerseAudio = null;
          this.startProgressTracking();
          
          // Store a local reference to the current audio player
          const currentPlayer = this.audioPlayer;
          const currentRequestId = this.currentAudioRequestId;
          
          // Check if player still exists before attempting to play
          if (currentPlayer && !this.audioStopped) {
            currentPlayer.play().catch(err => {
              console.error('Error starting playback:', err);
              
              // Only stop audio if this is still the current player and request
              if (this.audioPlayer === currentPlayer && this.currentAudioRequestId === currentRequestId && !this.audioStopped) {
                this.stopAudio();
              }
            });
            this.paused = false;
          }
          
          // Scroll to the verse once audio starts playing
          this.scrollToVerse(targetVerseNumber);
        });
        
        // Store a reference to this audio request
        const requestId = `${targetGlobalVerseNumber}-${Date.now()}`;
        this.currentAudioRequestId = requestId;
        
        // Fetch the ayah audio URL from the API
        fetch(`https://api.alquran.cloud/v1/ayah/${targetGlobalVerseNumber}/${targetReciter}`)
          .then(response => response.json())
          .then(data => {
            // Check if this is still the current request and if the player exists
            if (this.currentAudioRequestId !== requestId || !this.audioPlayer || this.audioStopped) {
              console.log('Audio request completed but player was stopped, ignoring result');
              return;
            }
            
            if (data.code === 200 && data.data && data.data.audio) {
              try {
                // Double check we still want to play before setting the source
                if (this.audioStopped || !this.audioPlayer) {
                  console.log('Audio load aborted because playback was stopped');
                  return;
                }
                
                // Use a try-catch block for setting the audio source
                try {
                  // Set the source to the audio URL provided by the API
                  this.audioPlayer.src = data.data.audio;
                  
                  // Load the audio (inside a try-catch to handle any loading errors)
                  try {
                    this.audioPlayer.load();
                  } catch (loadError) {
                    console.error('Error loading audio:', loadError);
                    this.stopAudio();
                  }
                } catch (srcError) {
                  console.error('Error setting audio source:', srcError);
                  this.stopAudio();
                }
              } catch (error) {
                console.error('Error setting audio source:', error);
                this.stopAudio();
              }
            } else {
              console.error('Error fetching audio URL:', data);
              this.stopAudio();
            }
          })
          .catch(error => {
            console.error('Error fetching audio data:', error);
            
            // Only call stopAudio if this is still the current audio request
            if (this.currentAudioRequestId === requestId) {
              this.stopAudio();
            }
          });
      }, 50); // Small delay to ensure previous audio is fully cleaned up
    },
    
    // Method to scroll to a specific verse
    scrollToVerse(verseNumberInSurah) {
      if (!verseNumberInSurah) return;
      
      this.$nextTick(() => {
        setTimeout(() => {
          try {
            const verseElement = document.getElementById(`verse-${verseNumberInSurah}`);
            if (verseElement) {
              verseElement.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
              });
              
              // Add a temporary highlight effect
              verseElement.classList.add('verse-highlight-animation');
              setTimeout(() => {
                verseElement.classList.remove('verse-highlight-animation');
              }, 2000);
            }
          } catch (error) {
            console.error('Error scrolling to verse:', error);
          }
        }, 100); // Small delay to ensure DOM is updated
      });
    },
    
    listenToFullSurah(reciter) {
      if (!this.currentSurah || this.downloadingSurahAudio) return;
      
      // If already playing full surah, toggle pause
      if (this.isPlayingFullSurah) {
        this.togglePause();
        return;
      }
      
      // Stop any currently playing audio
      this.stopAudio();
      
      this.downloadingSurahAudio = true;
      this.isPlayingFullSurah = true;
      this.audioStopped = false;
      
      console.log(`Setting up to play full surah: ${this.currentSurah.englishName} (${this.currentSurah.numberOfAyahs} verses)`);
      
      // Default reciter to Alafasy if not specified
      const reciterToUse = reciter || 'ar.alafasy';
      console.log(`Using reciter: ${reciterToUse}`);
      
      // Clear the audio queue
      this.audioQueue = [];
      this.currentAudioIndex = 0;
      
      // Prepare audio queue for all verses in the surah
      if (this.currentSurah.ayahs && Array.isArray(this.currentSurah.ayahs)) {
        // Sort verses by their numberInSurah to ensure correct order
        const sortedVerses = [...this.currentSurah.ayahs].sort((a, b) => 
          a.numberInSurah - b.numberInSurah
        );
        
        console.log(`Adding ${sortedVerses.length} verses to the queue`);
        
        sortedVerses.forEach(verse => {
          this.audioQueue.push({
            verseNumberInSurah: verse.numberInSurah,
            verseNumber: verse.number,
            reciter: reciterToUse
          });
        });
      } else {
        // Fallback method if ayahs array is not available
        console.log(`Using fallback method to build queue based on numberOfAyahs: ${this.currentSurah.numberOfAyahs}`);
        
        for (let i = 1; i <= this.currentSurah.numberOfAyahs; i++) {
          // Find the verse with this number
          const verse = this.currentSurah.ayahs ? 
                      this.currentSurah.ayahs.find(v => v.numberInSurah === i) : 
                      null;
          
          if (verse) {
            this.audioQueue.push({
              verseNumberInSurah: verse.numberInSurah,
              verseNumber: verse.number,
              reciter: reciterToUse
            });
          } else {
            // If we can't find the verse object, we need to construct our best guess
            // The verse number is usually surahNumber * 1000 + verseNumberInSurah
            // This is a rough estimate and may not always be accurate
            const estimatedVerseNumber = this.currentSurah.number * 1000 + i;
            
            console.log(`Estimated verse number for ${this.currentSurah.number}:${i} is ${estimatedVerseNumber}`);
            
            this.audioQueue.push({
              verseNumberInSurah: i,
              verseNumber: estimatedVerseNumber,
              reciter: reciterToUse
            });
          }
        }
      }
      
      console.log(`Final queue has ${this.audioQueue.length} verses`);
      
      // Start playing the first audio in the queue
      this.downloadingSurahAudio = false;
      if (this.audioQueue.length > 0) {
        this.playNextInQueue();
      } else {
        console.error('No verses found to play');
        this.stopAudio();
      }
    },
    
    playNextInQueue() {
      console.log(`Playing next in queue. Index: ${this.currentAudioIndex}, Queue length: ${this.audioQueue.length}`);
      
      if (this.audioQueue.length === 0 || this.currentAudioIndex >= this.audioQueue.length) {
        // No more audio to play, clean up
        console.log('End of queue reached, stopping audio');
        this.stopAudio();
        return;
      }
      
      const currentItem = this.audioQueue[this.currentAudioIndex];
      console.log(`Current item to play: Verse #${currentItem.verseNumberInSurah} (${currentItem.verseNumber}) with reciter ${currentItem.reciter}`);
      
      this.currentPlayingVerse = currentItem.verseNumberInSurah;
      
      // Scroll to the current verse
      this.scrollToVerse(currentItem.verseNumberInSurah);
      
      // Set loading state
      this.loadingVerseAudio = currentItem.verseNumberInSurah;

      // Clean up old audio player if it exists
      if (this.audioPlayer) {
        const oldAudio = this.audioPlayer;
        
        // Remove event listeners from old player
        oldAudio.onended = null;
        oldAudio.onerror = null;
        oldAudio.oncanplay = null;
        
        try {
          oldAudio.pause();
          oldAudio.src = '';
        } catch (e) {
          console.error('Error cleaning up previous audio:', e);
        }
      }
      
      // Create new audio player
      this.audioPlayer = new Audio();
      
      // Use a direct reference to this for clarity
      const self = this;
      
      // Setup event listeners with bind to ensure correct context
      this.audioPlayer.onended = function() {
        console.log(`Verse #${currentItem.verseNumberInSurah} finished playing, moving to next`);
        self.currentAudioIndex++;
        
        // Use setTimeout to ensure this happens after event processing is complete
        setTimeout(() => {
          if (!self.audioStopped) {
            self.playNextInQueue();
          }
        }, 0);
      };
      
      this.audioPlayer.onerror = function(event) {
        // Check if the error is happening during normal cleanup
        if (self.audioStopped) {
          console.log(`Error event occurred during cleanup for verse #${currentItem.verseNumberInSurah}, ignoring`);
          return;
        }
        
        console.error(`Error playing audio for verse #${currentItem.verseNumberInSurah}:`, 
          event.target?.error?.message || event.target?.error || 'Unknown error');
          
        // Skip to next on error
        self.currentAudioIndex++;
        
        // Use setTimeout to ensure this happens after event processing is complete
        setTimeout(() => {
          if (!self.audioStopped) {
            self.playNextInQueue();
          }
        }, 0);
      };
      
      this.audioPlayer.oncanplay = function() {
        console.log(`Audio for verse #${currentItem.verseNumberInSurah} is ready to play`);
        self.loadingVerseAudio = null;
        self.startProgressTracking();
        
        // Store reference to current player and request
        const currentPlayer = self.audioPlayer;
        const currentAudioIndex = self.currentAudioIndex;
        
        // Only try to play if player still exists and we're still on this item
        if (currentPlayer && !self.audioStopped && self.currentAudioIndex === currentAudioIndex) {
          currentPlayer.play()
            .catch(error => {
              console.error(`Error starting playback for verse #${currentItem.verseNumberInSurah}:`, error);
              
              // Only proceed to next if this is still the current player and index and not stopped
              if (self.audioPlayer === currentPlayer && self.currentAudioIndex === currentAudioIndex && !self.audioStopped) {
                self.currentAudioIndex++;
                
                // Use setTimeout to ensure this happens after event processing is complete
                setTimeout(() => {
                  if (!self.audioStopped) {
                    self.playNextInQueue();
                  }
                }, 0);
              }
            });
          
          self.paused = false;
        }
      };
      
      // API endpoint format: https://api.alquran.cloud/v1/ayah/{ayah_number}/{edition}
      console.log(`Fetching audio for verse #${currentItem.verseNumberInSurah} from API...`);
      fetch(`https://api.alquran.cloud/v1/ayah/${currentItem.verseNumber}/${currentItem.reciter}`)
        .then(response => response.json())
        .then(data => {
          // Ensure we still want to play this verse (in case user stopped playback)
          if (!this.audioPlayer || this.audioStopped) {
            console.log('Audio request completed but playback was stopped, ignoring result');
            return;
          }
          
          if (data.code === 200 && data.data && data.data.audio) {
            console.log(`Received audio URL for verse #${currentItem.verseNumberInSurah}:`, data.data.audio);
            
            // Double check we still want to play before setting the source
            if (this.audioStopped || !this.audioPlayer) {
              console.log('Audio load aborted because playback was stopped');
              return;
            }
            
            // Use a try-catch block for setting the audio source
            try {
              // Set the source to the audio URL provided by the API
              this.audioPlayer.src = data.data.audio;
              
              // Load the audio (inside a try-catch to handle any loading errors)
              try {
                this.audioPlayer.load();
              } catch (loadError) {
                console.error(`Error loading audio for verse #${currentItem.verseNumberInSurah}:`, loadError);
                // Skip to next on error
                this.currentAudioIndex++;
                this.playNextInQueue();
              }
            } catch (srcError) {
              console.error(`Error setting audio source for verse #${currentItem.verseNumberInSurah}:`, srcError);
              // Skip to next on error
              this.currentAudioIndex++;
              this.playNextInQueue();
            }
          } else {
            console.error(`Error fetching audio URL for verse #${currentItem.verseNumberInSurah}:`, data);
            // Skip to next on error
            this.currentAudioIndex++;
            this.playNextInQueue();
          }
        })
        .catch(error => {
          console.error(`Network error fetching audio for verse #${currentItem.verseNumberInSurah}:`, error);
          // Skip to next on error
          this.currentAudioIndex++;
          this.playNextInQueue();
        });
        
      // Preload next audio if available
      if (this.currentAudioIndex + 1 < this.audioQueue.length) {
        const nextItem = this.audioQueue[this.currentAudioIndex + 1];
        
        // Use setTimeout to delay preloading slightly to prioritize current audio
        setTimeout(() => {
          // Make sure we're still playing the current verse
          if (this.audioStopped) return;
          
          const preloadAudio = new Audio();
          preloadAudio.preload = 'auto';
          
          console.log(`Preloading next verse #${nextItem.verseNumberInSurah}`);
          fetch(`https://api.alquran.cloud/v1/ayah/${nextItem.verseNumber}/${nextItem.reciter}`)
            .then(response => response.json())
            .then(data => {
              if (data.code === 200 && data.data && data.data.audio) {
                preloadAudio.src = data.data.audio;
              }
            })
            .catch(error => {
              console.error(`Error preloading next verse #${nextItem.verseNumberInSurah}:`, error);
            });
        }, 500);
      }
    },
    
    stopAudio() {
      // Prevent multiple rapid calls to stopAudio
      if (this._isStoppingAudio) {
        console.log('Already stopping audio, ignoring duplicate call');
        return;
      }
      
      this._isStoppingAudio = true;
      console.log('Stopping all audio playback and cleaning up resources');
      
      // Set stopped flag first to prevent any new operations on the player
      this.audioStopped = true;
      
      // Clear current audio request ID to prevent race conditions
      this.currentAudioRequestId = null;
      
      // Store the current player reference
      const playerToCleanup = this.audioPlayer;
      
      // Immediately set audioPlayer to null to prevent access while it's being cleaned up
      this.audioPlayer = null;
      
      // Reset states first
      this.isPlayingFullSurah = false;
      this.loadingVerseAudio = null;
      this.highlightedAyah = null;
      this.currentPlayingVerse = null;
      this.paused = false;
      
      // Stop audio progress tracking
      this.stopProgressTracking();
      
      // Clean up the audio player if it exists
      if (playerToCleanup) {
        try {
          // Remove all event listeners before doing anything else to prevent errors during cleanup
          const eventTypes = ['ended', 'error', 'canplay', 'play', 'pause', 'timeupdate', 'loadedmetadata'];
          
          // First method: try to use removeEventListener with null handler (modern browsers)
          try {
            eventTypes.forEach(type => {
              playerToCleanup.removeEventListener(type, null);
            });
          } catch (e) {
            console.log('Could not use generic event removal, removing specific listeners');
          }
          
          // Second method: explicitly set listeners to null
          playerToCleanup.onended = null;
          playerToCleanup.onerror = null;
          playerToCleanup.oncanplay = null;
          playerToCleanup.onplay = null;
          playerToCleanup.onpause = null;
          playerToCleanup.ontimeupdate = null;
          playerToCleanup.onloadedmetadata = null;
          
          // Try to stop playback
          playerToCleanup.pause();
          
          try {
            playerToCleanup.currentTime = 0;
          } catch (e) {
            // Ignore currentTime errors that might happen if the media is not ready
          }
          
          // Set src to empty string first to cancel any pending loads
          try {
            playerToCleanup.src = '';
          } catch (e) {
            console.error('Error clearing audio source:', e);
          }
          
          // Properly clean up all event listeners
          try {
            if (playerToCleanup.parentNode) {
              const clone = playerToCleanup.cloneNode(false);
              playerToCleanup.parentNode.replaceChild(clone, playerToCleanup);
            }
          } catch (e) {
            console.error('Error cleaning up audio element DOM references:', e);
          }
        } catch (error) {
          console.error('Error cleaning up audio player:', error);
        }
      }
      
      // Clear the audio queue
      this.audioQueue = [];
      this.currentAudioIndex = 0;
      
      // Reset stopping flag after a small delay to ensure complete cleanup
      setTimeout(() => {
        this._isStoppingAudio = false;
      }, 200);
    },
    
    togglePause() {
      if (!this.audioPlayer) return;
      
      if (this.audioPlayer.paused) {
        this.audioPlayer.play();
        this.paused = false;
      } else {
        this.audioPlayer.pause();
        this.paused = true;
      }
    },
    
    seekAudio(event) {
      if (!this.audioPlayer || !this.audioDuration) return;
      
      const container = event.currentTarget;
      const clickPosition = event.clientX - container.getBoundingClientRect().left;
      const containerWidth = container.clientWidth;
      const seekPercentage = clickPosition / containerWidth;
      
      this.audioPlayer.currentTime = seekPercentage * this.audioDuration;
    },
    
    // Audio progress tracking
    startProgressTracking() {
      // Clear any existing interval
      if (this.audioUpdateInterval) {
        clearInterval(this.audioUpdateInterval);
      }
      
      // Update progress every 100ms
      this.audioUpdateInterval = setInterval(() => {
        if (this.audioPlayer && !this.audioPlayer.paused) {
          this.audioProgress = this.audioPlayer.currentTime;
          this.audioDuration = this.audioPlayer.duration || 0;
        }
      }, 100);
      
      this.audioStopped = false;
    },
    
    stopProgressTracking() {
      if (this.audioUpdateInterval) {
        clearInterval(this.audioUpdateInterval);
        this.audioUpdateInterval = null;
      }
      
      // Reset progress
      this.audioProgress = 0;
      this.audioDuration = 0;
    },
    
    loadPage() {
      // This method will be implemented in the next phase
      console.log(`Loading page ${this.currentPage}`)
    }
  },
  mounted() {
    // Listen for the custom event for verse navigation
    window.addEventListener('quran-navigation', this.handleQuranNavigation = (event) => {
      if (event.detail) {
        const { surah, verse } = event.detail;
        console.log(`Received navigation event for surah ${surah}${verse ? `, verse ${verse}` : ', no specific verse'}`);
        
        if (surah) {
          // Set the selected surah
          this.selectedSurah = parseInt(surah);
          
          // If there's a specific verse, highlight it
          if (verse) {
            // Set the highlighted verse
            this.highlightedAyah = parseInt(verse);
          } else {
            // Just navigate to the surah without highlighting a specific ayah
            this.highlightedAyah = null;
            // Ensure surah list is collapsed for better UI experience
            this.surahListCollapsed = true;
          }
          
          // Load the surah content
          this.loadSurah().then(() => {
            console.log(`Surah ${surah} loaded${verse ? `, navigating to verse ${verse}` : ''}`);
            
            // Double check that the verse is highlighted after surah is loaded (if applicable)
            if (verse) {
              setTimeout(() => {
                if (this.highlightedAyah !== parseInt(verse)) {
                  console.log(`Re-setting highlighted ayah to ${verse} after delay`);
                  this.highlightedAyah = parseInt(verse);
                  
                  // Scroll to the verse
                  this.scrollToVerse(parseInt(verse));
                }
              }, 800); // Give more time for everything to load
            }
          });
        }
      }
    });
  },
  beforeUnmount() {
    // Clean up the event listener
    window.removeEventListener('quran-navigation', this.handleQuranNavigation);
    
    // Clean up any audio resources
    this.stopAudio();
  }
}
</script>

<style scoped lang="postcss">
.quran-reader {
  @apply max-w-6xl mx-auto p-4;
}

.quran-container {
  @apply bg-gray-50 dark:bg-gray-100 rounded-lg p-4 shadow-sm;
}

.view-mode-button {
  @apply flex items-center px-4 py-2 rounded-lg bg-white border border-gray-300 text-gray-700 hover:bg-gray-100 transition-colors;
}

.view-mode-button.active {
  @apply bg-indigo-500 text-white border-indigo-500 hover:bg-indigo-600;
}

.loading-message {
  @apply flex flex-col items-center justify-center py-12 text-gray-500 space-y-4;
}

.error-message {
  @apply flex flex-col items-center justify-center py-12 text-red-500 space-y-4;
}

.surah-content {
  @apply transition-all duration-300 ease-in-out;
}

.surah-content-expanded {
  @apply mt-4;
}

.book-view {
  @apply min-h-[60vh] bg-white rounded-lg border border-gray-200;
}

.light-mode {
  color-scheme: light;
  --tw-bg-opacity: 1;
  background-color: rgba(255, 255, 255, var(--tw-bg-opacity));
  --tw-text-opacity: 1;
  color: rgba(31, 41, 55, var(--tw-text-opacity));
}

.light-mode .verse-container,
.light-mode .surah-header,
.light-mode .verses {
  --tw-bg-opacity: 1;
  background-color: rgba(255, 255, 255, var(--tw-bg-opacity));
  border-color: rgba(229, 231, 235, var(--tw-border-opacity));
}
</style>