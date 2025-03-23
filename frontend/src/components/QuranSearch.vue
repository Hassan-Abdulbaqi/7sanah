<template>
  <div class="quran-search">
    <h1 class="text-2xl font-bold text-center mb-6">{{ $t('quran.search') }}</h1>
    
    <!-- Search Bar for Quran Text -->
    <div class="search-bar-container mb-4">
      <h3 class="font-medium mb-2">{{ $t('quran.searchQuran') }}</h3>
      <div class="search-input-group">
        <input 
          type="text" 
          v-model="searchKeyword" 
          :placeholder="$t('quran.searchPlaceholder')" 
          class="search-input"
          :dir="inputDirection"
          @keyup.enter="performSearch"
        />
        <div class="search-options-row">
          <button 
            @click="performSearch" 
            class="search-button"
            :disabled="searchLoading || !searchKeyword"
          >
            <span v-if="searchLoading">
              <svg class="animate-spin h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ $t('quran.searching') }}
            </span>
            <span v-else>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
              </svg>
              {{ $t('quran.search') }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Search Results -->
    <div v-if="searchResults.length > 0" class="search-results mb-4">
      <h3 class="font-medium mb-2">{{ $t('quran.searchResults', { count: searchCount }) }}</h3>
      <div class="search-results-container">
        <div 
          v-for="(match, index) in searchResults" 
          :key="index" 
          class="search-result-item"
          @click="goToVerse(match)"
        >
          <div class="search-result-header">
            <span class="surah-name">{{ match.surah.englishName }}</span>
            <span class="verse-number">{{ $t('quran.verse') }} {{ match.verse_key }}</span>
          </div>
          <!-- Display search results using the words array for accurate highlighting -->
          <p 
            class="search-result-text" 
            :dir="getTextDirection(match.text)"
            :lang="isArabicText(match.text) ? 'ar' : match.edition?.language || 'en'"
          >
            <template v-if="match.words && match.words.length > 0 && match.words.some(w => w.text && typeof w.text === 'string')">
              <!-- Add verse number if present at the end -->
              <template v-for="(word, wordIndex) in match.words">
                <span 
                  v-if="word.char_type !== 'end'"
                  :key="wordIndex"
                  :class="{
                    'highlight-match': word.highlight === true, 
                    'quran-word': true
                  }"
                >
                  {{ word.text || '' }}
                </span>
                <span 
                  v-else
                  :key="`end-${wordIndex}`"
                  class="verse-number-inline"
                >
                  {{ word.text || '' }}
                </span>
              </template>
            </template>
            <template v-else>
              <span v-html="formatQuranText(match.text, match.verse_key)"></span>
            </template>
          </p>
        </div>
      </div>
      
      <!-- Load More button -->
      <div v-if="hasMoreResults" class="flex justify-center mt-4">
        <button 
          @click="loadMoreResults" 
          class="load-more-button"
          :disabled="loadingMore"
        >
          <span v-if="loadingMore">
            <svg class="animate-spin h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ $t('quran.loadingMore') }}
          </span>
          <span v-else>
            {{ $t('quran.loadMore') }}
          </span>
        </button>
      </div>
    </div>

    <!-- No Results Message -->
    <div v-else-if="searchPerformed && !searchLoading" class="no-results">
      <p>{{ $t('quran.noSearchResults') }}</p>
    </div>

    <!-- Loading State -->
    <div class="loading-spinner" v-if="searchLoading">
      <svg class="animate-spin h-8 w-8" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <p class="mt-2">{{ $t('quran.loading') }}</p>
    </div>

    <!-- Error Message -->
    <div class="error-message" v-if="searchError">
      <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <p>{{ searchError }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuranSearch',
  data() {
    return {
      searchKeyword: '',
      searchResults: [],
      searchCount: 0,
      searchLoading: false,
      searchError: null,
      searchPerformed: false,
      surahs: [],
      translations: [],
      groupedTranslations: {},
      hasMoreResults: false,
      loadingMore: false,
      // Pagination
      currentPage: 1,
      pageSize: 50,
      totalResults: 0
    };
  },
  async created() {
    await Promise.all([
      this.loadSurahs(),
      this.loadTranslations()
    ]);
  },
  methods: {
    async loadSurahs() {
      try {
        const response = await fetch('http://api.alquran.cloud/v1/surah');
        const data = await response.json();
        if (data.code === 200 && data.data) {
          this.surahs = data.data;
        }
      } catch (error) {
        console.error('Error loading surahs:', error);
      }
    },

    async loadTranslations() {
      try {
        // Only get text format translations, no tafsir
        const response = await fetch('http://api.alquran.cloud/v1/edition?format=text&type=translation');
        const data = await response.json();
        
        if (data.code === 200 && data.data) {
          this.translations = data.data;
          
          // Group translations by language
          this.groupedTranslations = this.translations.reduce((acc, translation) => {
            const lang = translation.language;
            if (!acc[lang]) {
              acc[lang] = [];
            }
            acc[lang].push(translation);
            return acc;
          }, {});
        }
      } catch (error) {
        console.error('Error loading translations:', error);
      }
    },

    getLanguageName(code) {
      const languageNames = {
        'en': 'English',
        'ar': 'Arabic',
        'IQ': 'Iraqi Arabic',
        'fr': 'French',
        'es': 'Spanish',
        'id': 'Indonesian',
        'tr': 'Turkish',
        'ur': 'Urdu',
        'ru': 'Russian',
        'fa': 'Persian',
        'de': 'German',
        'hi': 'Hindi',
        'bn': 'Bengali',
        'ms': 'Malay',
        'zh': 'Chinese',
        'sw': 'Swahili',
        'nl': 'Dutch',
        'bs': 'Bosnian',
        'it': 'Italian',
        'th': 'Thai',
        'ku': 'Kurdish',
        'pt': 'Portuguese',
        'ja': 'Japanese',
        'my': 'Myanmar',
        'ko': 'Korean',
        'tg': 'Tajik',
        'tt': 'Tatar',
        'uz': 'Uzbek',
      };
      
      return languageNames[code] || code;
    },

    async performSearch() {
      if (!this.searchKeyword.trim()) {
        return;
      }
      
      this.searchLoading = true;
      this.searchError = null;
      this.searchResults = [];
      this.searchCount = 0;
      this.searchPerformed = true;
      this.currentPage = 1;
      this.totalResults = 0;
      this.hasMoreResults = false;
      
      // Build the search query - using Quran.com API v4
      const query = this.searchKeyword.trim();
      
      // Construct the API URL with English language parameter
      let apiUrl = `https://api.quran.com/api/v4/search?q=${encodeURIComponent(query)}&size=${this.pageSize}&page=${this.currentPage}&language=en`;
      
      console.log(`Searching the Quran using Quran.com API: ${apiUrl}`);
      
      try {
        const response = await fetch(apiUrl);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Get the text response first to check if it's valid JSON
        const responseText = await response.text();
        
        // Check if the response is empty or not valid JSON
        if (!responseText || responseText.trim() === '') {
          throw new Error('Empty response received from API');
        }
        
        // Try parsing the JSON
        let data;
        try {
          data = JSON.parse(responseText);
        } catch (jsonError) {
          console.error('Invalid JSON response:', responseText);
          throw new Error('Invalid JSON response from API');
        }
        
        if (data && data.search && data.search.results) {
          // Extract and format results from the new API
          const results = data.search.results.map(result => {
            // Ensure we properly preserve the API's word highlighting information
            const processedWords = result.words?.map(word => {
              return { ...word }; // Create a shallow copy to preserve all properties including highlight
            }) || [];
            
            // Transform the result to match our component's expected format
            return {
              number: result.verse_key.replace(":", "_"), // Use as unique identifier
              numberInSurah: parseInt(result.verse_key.split(':')[1]),
              surah: {
                number: parseInt(result.verse_key.split(':')[0]),
                englishName: result.verse_key.split(':')[0], // We'll enhance this later
                name: result.verse_key.split(':')[0]
              },
              text: result.text,
              edition: {
                identifier: 'en', // Always use English
                language: 'en',
                name: this.getLanguageName('en'),
                type: 'translation'
              },
              // Add Quran.com specific fields
              verse_key: result.verse_key,
              words: processedWords, // Use our processed words array that preserves highlight property
              highlighted: result.highlighted
            };
          });
          
          // Apply our improved highlighting
          this.manuallyHighlightResults(results);
          
          this.searchResults = results;
          this.totalResults = data.search.total_results || results.length;
          this.searchCount = results.length;
          
          // Check if there are more results to load
          this.hasMoreResults = this.searchResults.length < this.totalResults;
          
          // If we have results, try to get the proper surah names
          if (results.length > 0 && this.surahs.length > 0) {
            results.forEach(result => {
              const surahNumber = parseInt(result.verse_key.split(':')[0]);
              const surah = this.surahs.find(s => s.number === surahNumber);
              if (surah) {
                result.surah.englishName = surah.englishName;
                result.surah.name = surah.name;
              }
            });
          }
          
          if (results.length === 0) {
            this.$notification?.info?.(this.$t('quran.noSearchResults'));
          }
        } else {
          throw new Error('Invalid response format from API');
        }
      } catch (error) {
        console.error('Error searching Quran:', error);
        this.searchError = error.message || this.$t('quran.searchError');
      } finally {
        this.searchLoading = false;
      }
    },
    
    async loadMoreResults() {
      if (this.hasMoreResults && !this.loadingMore) {
        this.loadingMore = true;
        
        // Increment page number
        this.currentPage++;
        
        // Build the search query - using Quran.com API v4
        const query = this.searchKeyword.trim();
        
        // Construct the API URL with English language parameter
        let apiUrl = `https://api.quran.com/api/v4/search?q=${encodeURIComponent(query)}&size=${this.pageSize}&page=${this.currentPage}&language=en`;
        
        console.log(`Loading more results using Quran.com API: ${apiUrl}`);
        
        try {
          const response = await fetch(apiUrl);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
          // Get the text response first to check if it's valid JSON
          const responseText = await response.text();
          
          // Check if the response is empty or not valid JSON
          if (!responseText || responseText.trim() === '') {
            throw new Error('Empty response received from API');
          }
          
          // Try parsing the JSON
          let data;
          try {
            data = JSON.parse(responseText);
          } catch (jsonError) {
            console.error('Invalid JSON response:', responseText);
            throw new Error('Invalid JSON response from API');
          }
          
          if (data && data.search && data.search.results) {
            // Extract and format results from the new API
            const results = data.search.results.map(result => {
              // Ensure we properly preserve the API's word highlighting information
              const processedWords = result.words?.map(word => {
                return { ...word }; // Create a shallow copy to preserve all properties including highlight
              }) || [];
              
              // Transform the result to match our component's expected format
              return {
                number: result.verse_key.replace(":", "_"), // Use as unique identifier
                numberInSurah: parseInt(result.verse_key.split(':')[1]),
                surah: {
                  number: parseInt(result.verse_key.split(':')[0]),
                  englishName: result.verse_key.split(':')[0], // We'll enhance this later
                  name: result.verse_key.split(':')[0]
                },
                text: result.text,
                edition: {
                  identifier: 'en', // Always use English
                  language: 'en',
                  name: this.getLanguageName('en'),
                  type: 'translation'
                },
                // Add Quran.com specific fields
                verse_key: result.verse_key,
                words: processedWords, // Use our processed words array that preserves highlight property
                highlighted: result.highlighted
              };
            });
            
            // Apply our improved highlighting to the new results
            this.manuallyHighlightResults(results);
            
            // Append the new results to the existing ones
            this.searchResults = [...this.searchResults, ...results];
            this.searchCount = this.searchResults.length;
            
            // Check if there are more results to load
            this.hasMoreResults = this.searchResults.length < this.totalResults;
            
            // If we have results, try to get the proper surah names
            if (results.length > 0 && this.surahs.length > 0) {
              results.forEach(result => {
                const surahNumber = parseInt(result.verse_key.split(':')[0]);
                const surah = this.surahs.find(s => s.number === surahNumber);
                if (surah) {
                  result.surah.englishName = surah.englishName;
                  result.surah.name = surah.name;
                }
              });
            }
          } else {
            throw new Error('Invalid response format from API');
          }
        } catch (error) {
          console.error('Error loading more results:', error);
          this.searchError = error.message || this.$t('quran.searchError');
        } finally {
          this.loadingMore = false;
        }
      }
    },
    
    goToVerse(match) {
      // Parse the verse_key to get surah number and verse number
      const verseKey = match.verse_key || '';
      
      try {
        // Check if verseKey is valid
        if (!verseKey || !verseKey.includes(':')) {
          console.error('Invalid verse key format:', verseKey);
          this.$notification?.error?.(this.$t('quran.invalidVerseKey'));
          return;
        }
        
        const [surahStr, verseStr] = verseKey.split(':');
        const surahNumber = parseInt(surahStr);
        const verseNumber = parseInt(verseStr);
        
        // Validate the parsed numbers
        if (isNaN(surahNumber) || isNaN(verseNumber) || surahNumber <= 0 || verseNumber <= 0) {
          console.error('Invalid surah or verse number:', surahNumber, verseNumber);
          this.$notification?.error?.(this.$t('quran.invalidVerseNumber'));
          return;
        }
        
        // Emit an event that can be handled by parent component to navigate
        this.$emit('navigate-to-verse', {
          surah: surahNumber,
          verse: verseNumber,
          edition: match.edition ? match.edition.identifier : null
        });
      } catch (error) {
        console.error('Error navigating to verse:', error);
        this.$notification?.error?.(this.$t('quran.navigationError'));
      }
    },
    
    highlightSearchTerm(text) {
      if (!text) return text;
      
      // Find the matching result for this text
      let matchingResult = null;
      if (this.searchResults && this.searchResults.length > 0) {
        matchingResult = this.searchResults.find(m => m.text === text);
      }
      
      // If we have a match with words array and at least one word has highlight property from the API
      if (matchingResult && matchingResult.words && Array.isArray(matchingResult.words) && 
          matchingResult.words.some(w => 'highlight' in w)) {
        // Use the API's highlight property to mark highlighted words
        return matchingResult.words.map(word => {
          if (word.highlight) {
            return `<span class="highlight-match">${word.text || ''}</span>`;
          }
          return word.text || '';
        }).join(' ');
      }
      
      // Otherwise do our own highlighting
      if (!this.searchKeyword) return text;
      
      try {
        // Escape special regex characters
        const escapedKeyword = this.searchKeyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        
        // Create a regular expression to find the keyword (case insensitive)
        const regex = new RegExp(`(${escapedKeyword})`, 'gi');
        
        // Replace matches with highlighted spans, preserving the original text
        return text.replace(regex, '<span class="highlight-match">$1</span>');
      } catch (error) {
        console.error('Error highlighting search term:', error);
        return text;
      }
    },
    
    // Determine if text is primarily Arabic
    isArabicText(text) {
      // Check if the text contains Arabic characters
      return /[\u0600-\u06FF]/.test(text);
    },
    
    // Get the appropriate direction for text display
    getTextDirection(text) {
      return this.isArabicText(text) ? 'rtl' : 'ltr';
    },

    formatQuranText(text, verse_key) {
      if (!text) return '';
      
      // First try our regular highlighting
      const highlighted = this.highlightSearchTerm(text);
      
      // If it's Arabic text, we need to ensure proper spacing
      if (this.isArabicText(text)) {
        // Remove verse numbers at the end of ayahs (they often appear as ١٦٣, etc.)
        const cleanedText = highlighted.replace(/[٠-٩]+$/, '');
        
        // Check if the text appears to be missing spaces (running together)
        const spacesCount = (text.match(/\s/g) || []).length;
        const textLength = text.length;
        
        if (spacesCount < textLength / 20) { // Less than 1 space per 20 characters
          // Use a regex to add spans after certain characters that typically
          // mark word boundaries in Arabic Quranic text
          return cleanedText.replace(/([\u0627\u0628\u062A-\u063A\u0641-\u064A])/g, '$1<span class="letter-spacing"></span>');
        }
        
        return cleanedText;
      }
      
      return highlighted;
    },

    // Improved manually add highlighting function that will be reused
    manuallyHighlightResults(results) {
      if (!results || results.length === 0 || !this.searchKeyword) return;
      
      // For Arabic text, we need to be smart about diacritics and normalization
      let escapedKeyword = this.searchKeyword.trim();
      let isArabic = this.isArabicText(escapedKeyword);
      
      // Escape special regex characters
      escapedKeyword = escapedKeyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      
      // If it's Arabic, make a more flexible regex that can match with/without diacritics
      let regexPattern;
      if (isArabic) {
        // Create a pattern that's more flexible with Arabic diacritics
        regexPattern = escapedKeyword.split('').map(char => {
          // Base Arabic characters
          if (/[\u0600-\u061F\u0640-\u064A]/.test(char)) {
            return char + '[\\u064B-\\u065F\\u0670]*'; // Allow optional diacritics after each character
          }
          return char;
        }).join('');
      } else {
        regexPattern = escapedKeyword;
      }
      
      // Create the regex with the appropriate pattern
      const regex = new RegExp(regexPattern, 'gi');
      
      // Process each result
      results.forEach(result => {
        if (result.words && Array.isArray(result.words)) {
          // Check if this result needs highlighting (doesn't already have it)
          if (!result.words.some(word => word.highlight === true)) {
            // For Arabic, we might need to check the full text
            if (isArabic && result.text) {
              // If the full text matches but individual words don't, try to identify the right word
              if (regex.test(result.text)) {
                // Find the most likely word to highlight
                const words = result.words.filter(w => w.char_type !== 'end');
                let highlightedAny = false;
                
                for (const word of words) {
                  if (word.text && typeof word.text === 'string') {
                    // Reset regex before testing
                    regex.lastIndex = 0;
                    if (regex.test(word.text)) {
                      word.highlight = true;
                      highlightedAny = true;
                    }
                  }
                }
                
                // If no matches found, highlight the word that seems most similar
                if (!highlightedAny && words.length > 0) {
                  // Simple approach - find the word with the most character overlap
                  const keyword = this.searchKeyword.replace(/[\u064B-\u065F\u0670]/g, ''); // Remove diacritics
                  let bestMatch = null;
                  let bestScore = 0;
                  
                  for (const word of words) {
                    if (word.text && typeof word.text === 'string') {
                      const cleanWord = word.text.replace(/[\u064B-\u065F\u0670]/g, ''); // Remove diacritics
                      let score = 0;
                      for (let i = 0; i < keyword.length; i++) {
                        if (cleanWord.includes(keyword[i])) score++;
                      }
                      if (score > bestScore) {
                        bestScore = score;
                        bestMatch = word;
                      }
                    }
                  }
                  
                  if (bestMatch && bestScore > keyword.length / 2) {
                    bestMatch.highlight = true;
                  }
                }
              }
            } else {
              // Non-Arabic - just do the simple check
              result.words.forEach(word => {
                if (word.text && typeof word.text === 'string') {
                  // Reset regex before testing
                  regex.lastIndex = 0;
                  if (regex.test(word.text)) {
                    word.highlight = true;
                  }
                }
              });
            }
          }
        }
      });
    }
  },
  computed: {
    // Compute the text direction for the search input based on the current keyword
    inputDirection() {
      return this.isArabicText(this.searchKeyword) ? 'rtl' : 'ltr';
    }
  }
};
</script>

<style scoped>
.quran-search {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-bar-container {
  margin-bottom: 20px;
}

.search-input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background-color: var(--input-bg);
  color: var(--text-color);
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  border-color: var(--primary-color);
  outline: none;
}

/* Add RTL support for the input field */
[dir="rtl"] .search-input {
  text-align: right;
}

.search-options-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  align-items: center;
}

.search-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
  min-width: 120px;
  width: 100%;
}

.search-button:hover {
  background-color: var(--primary-hover);
}

.search-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.search-results {
  margin-top: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: var(--card-bg);
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
}

.search-results-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 500px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.search-result-item {
  display: flex;
  flex-direction: column;
  background-color: var(--bg-light);
  border-radius: 0.5rem;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid var(--border-color);
}

.search-result-item:hover {
  background-color: var(--hover-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.search-result-header {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.search-result-header .surah-name {
  font-weight: 500;
  margin-right: 10px;
  color: var(--primary-color);
}

.search-result-header .verse-number {
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.search-result-text {
  line-height: 1.6;
  color: var(--text-secondary);
  font-size: 0.95rem;
  overflow-wrap: break-word;
  word-break: break-word;
  max-height: 150px;
  overflow-y: auto;
  direction: auto; /* Automatically adjust direction based on content */
}

/* RTL-specific styles for Arabic text */
.search-result-text[dir="rtl"] {
  text-align: right;
  font-size: 1.2rem; /* Larger for Arabic text */
  line-height: 2;
  font-family: "Scheherazade New", "Amiri", "Traditional Arabic", sans-serif;
  padding: 10px 5px;
  letter-spacing: 0.01em;
  word-spacing: 0.15em;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: var(--text-secondary);
}

.error-message {
  margin: 1rem 0;
}

.no-results {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
  background-color: var(--card-bg);
  border-radius: 0.5rem;
  border: 1px solid var(--border-color);
}

.highlight-match {
  background-color: rgba(var(--primary-color-rgb), 0.15);
  color: var(--primary-color);
  padding: 0 3px;
  border-radius: 4px;
  font-weight: 500;
  display: inline-block; /* Helps with RTL text highlighting */
  position: relative;
}

/* Enhanced Arabic highlight styles */
[dir="rtl"] .highlight-match {
  color: var(--primary-color);
  background-color: rgba(var(--primary-color-rgb), 0.15);
  padding: 0 3px;
  border-radius: 4px;
  font-weight: bold;
  /* Slightly increase size for better readability of highlighted Arabic */
  font-size: 1.05em;
}

/* For Arabic text in word-by-word display */
[dir="rtl"] .search-result-text span {
  margin-left: 4px;
  margin-right: 0;
}

[dir="ltr"] .search-result-text span {
  margin-right: 4px;
  margin-left: 0;
}

/* Last word in sequence doesn't need a margin */
.search-result-text span:last-child {
  margin-right: 0;
  margin-left: 0;
}

.load-more-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  background-color: var(--secondary-bg);
  color: var(--text-color);
  font-size: 0.875rem;
  transition: all 0.2s ease;
  border: 1px solid var(--border-color);
}

.load-more-button:hover {
  background-color: var(--hover-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.load-more-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Media query for smaller screens */
@media (max-width: 640px) {
  .search-button {
    width: 100%;
  }
}

.quran-word {
  display: inline-block;
  margin: 0 2px;
}

/* Help space out Arabic characters when no spaces are provided */
.arabic-spacing {
  display: inline-block;
  width: 0.05em;
  height: 1em;
}

/* Apply special styling for Arabic text with poor spacing */
[dir="rtl"] .search-result-text {
  letter-spacing: 0.03em;
  word-spacing: 0.1em;
}

.letter-spacing {
  display: inline-block;
  width: 0.02em;
}

.verse-number-inline {
  font-size: 0.8em;
  color: var(--text-secondary);
  vertical-align: super;
  margin-right: 0.5em;
  font-weight: normal;
  opacity: 0.8;
}
</style> 