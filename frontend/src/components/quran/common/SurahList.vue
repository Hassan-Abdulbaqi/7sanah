<template>
  <div class="surah-selection">
    <h3 class="font-medium mb-2">{{ $t('quran.selectSurah') }}</h3>
    
    <!-- Surah search -->
    <div class="surah-search-container mb-3">
      <input 
        type="text" 
        v-model="searchQuery" 
        class="surah-search-input" 
        :placeholder="$t('quran.searchSurah') || 'Search surah...'"
        @input="filterSurahs"
      />
      <button 
        v-if="searchQuery" 
        @click="clearSearch" 
        class="clear-search-button"
        aria-label="Clear search"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
    
    <!-- Surah buttons grid -->
    <div class="surah-buttons-grid">
      <button 
        v-for="surah in filteredSurahs" 
        :key="surah.number" 
        @click="selectSurah(surah.number)"
        :class="['surah-button', { active: selectedSurah === surah.number }]"
        :disabled="loading"
      >
        <span class="surah-number">{{ surah.number }}</span>
        <div class="arabic-text-container">
          <span class="surah-name-arabic" lang="ar">{{ surah.name }}</span>
        </div>
        <span class="surah-name">{{ surah.englishName }}</span>
      </button>
    </div>
    
    <!-- No results message -->
    <div v-if="filteredSurahs.length === 0 && searchQuery" class="no-results-message">
      {{ $t('quran.noSurahResults') || 'No surahs found matching your search.' }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'SurahList',
  props: {
    surahs: {
      type: Array,
      required: true
    },
    selectedSurah: {
      type: [Number, String],
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      searchQuery: '',
      filteredSurahs: [],
      // Pre-normalized surah names for faster searching
      normalizedSurahNames: []
    }
  },
  watch: {
    surahs: {
      immediate: true,
      handler(newSurahs) {
        this.filteredSurahs = newSurahs || []
        
        // Pre-normalize all surah names for faster searching
        if (newSurahs && newSurahs.length > 0) {
          this.normalizedSurahNames = newSurahs.map(surah => ({
            number: surah.number,
            normalizedName: this.normalizeArabicText(surah.name),
            // Also store a version without "سورة" prefix for more flexible matching
            normalizedNameNoPrefix: this.normalizeArabicText(surah.name.replace(/^سورة\s+/i, ''))
          }))
        }
      }
    }
  },
  methods: {
    selectSurah(surahNumber) {
      this.$emit('select-surah', surahNumber)
    },
    
    // Enhanced Arabic text normalization
    normalizeArabicText(text) {
      if (!text) return '';
      
      // First remove ALL possible diacritical marks in Arabic
      let normalized = text
        // Remove harakat (fatha, damma, kasra, etc.)
        .replace(/[\u064B-\u0652]/g, '')
        // Remove tatweel (stretching character)
        .replace(/\u0640/g, '')
        // Remove other diacritics and special marks
        .replace(/[\u0653-\u0655\u0670\u06D6-\u06ED]/g, '')
        // Remove zero-width joiner and non-joiner
        .replace(/[\u200C\u200D]/g, '');
      
      // Normalize Arabic letters that may appear in different forms
      normalized = normalized
        // Normalize alifs
        .replace(/[\u0622\u0623\u0625\u0671\u0672\u0673\u0675]/g, '\u0627')
        // Normalize yaa and alif maqsura
        .replace(/\u0649/g, '\u064A')
        // Normalize taa marbouta to haa
        .replace(/\u0629/g, '\u0647')
        // Normalize various forms of hamza
        .replace(/[\u0624\u0626]/g, '\u0621');
      
      return normalized;
    },
    
    // Enhanced search for Arabic text
    searchArabicText(query, surah) {
      // Normalize the query
      const normalizedQuery = this.normalizeArabicText(query);
      
      // Get pre-normalized name for this surah
      const surahInfo = this.normalizedSurahNames.find(s => s.number === surah.number);
      if (!surahInfo) return false;
      
      // Check if the normalized query matches the normalized surah name
      if (surahInfo.normalizedName.includes(normalizedQuery)) {
        return true;
      }
      
      // Check if query might be just the surah name without "سورة" prefix
      if (surahInfo.normalizedNameNoPrefix.includes(normalizedQuery)) {
        return true;
      }
      
      // Additional check: If query is very short (1-2 chars), be more lenient
      if (normalizedQuery.length <= 2) {
        // For short queries, look for exact character matches but don't require sequence
        return [...normalizedQuery].every(char => 
          surahInfo.normalizedName.includes(char) || 
          surahInfo.normalizedNameNoPrefix.includes(char)
        );
      }
      
      return false;
    },
    
    filterSurahs() {
      if (!this.searchQuery.trim()) {
        this.filteredSurahs = this.surahs
        return
      }
      
      const query = this.searchQuery.toLowerCase().trim()
      
      // Check if the search query contains Arabic characters
      const containsArabic = /[\u0600-\u06FF]/.test(query)
      
      this.filteredSurahs = this.surahs.filter(surah => {
        // Search in English name
        const englishMatch = surah.englishName.toLowerCase().includes(query)
        
        // Search in surah number
        const numberMatch = surah.number.toString() === query
        
        // Search in English translation if available
        const translationMatch = surah.englishNameTranslation && 
          surah.englishNameTranslation.toLowerCase().includes(query)
        
        // Enhanced Arabic matching
        let arabicMatch = false
        
        if (containsArabic) {
          // Use the enhanced Arabic search method
          arabicMatch = this.searchArabicText(query, surah)
        } else {
          // For non-Arabic queries, try simple matching against the original name
          arabicMatch = surah.name.includes(query)
        }
        
        return englishMatch || numberMatch || arabicMatch || translationMatch
      })
    },
    
    clearSearch() {
      this.searchQuery = ''
      this.filteredSurahs = this.surahs
    }
  }
}
</script>

<style scoped>
.surah-buttons-grid {
  @apply grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-2;
}

.surah-button {
  @apply flex flex-col items-center justify-center p-3 bg-white border border-gray-200 rounded-lg hover:bg-indigo-50 hover:border-indigo-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm transition-colors;
  min-height: 90px;
}

.surah-button.active {
  @apply bg-indigo-100 border-indigo-400;
}

.surah-number {
  @apply text-indigo-600 font-bold mb-1;
}

.arabic-text-container {
  @apply w-full text-center;
}

.surah-name-arabic {
  @apply text-gray-800 font-medium mb-1 inline-block;
  font-family: var(--font-family-quran);
  font-size: 1rem;
  line-height: 1.4;
  text-align: center;
  direction: rtl;
}

.surah-name {
  @apply text-gray-700 text-center;
  font-size: 0.8rem;
  line-height: 1.2;
}

.surah-search-container {
  @apply relative;
}

.surah-search-input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm;
}

.clear-search-button {
  @apply absolute right-2 top-2 text-gray-400 hover:text-gray-600 focus:outline-none;
}

.no-results-message {
  @apply text-center text-gray-500 mt-4 py-6;
}
</style> 