<template>
  <div class="search-bar-container mb-4">
    <h3 class="font-medium mb-2">{{ $t('quran.searchQuran') }}</h3>
    <div class="search-input-group">
      <input 
        type="text" 
        v-model="searchKeyword" 
        :placeholder="$t('quran.searchPlaceholder')" 
        class="search-input"
        @keyup.enter="performSearch"
      />
      <div class="search-options-row">
        <div class="search-select-container">
          <select v-model="searchSurah" class="search-select">
            <option value="all">{{ $t('quran.allSurahs') }}</option>
            <option v-for="surah in surahs" :key="surah.number" :value="surah.number">
              {{ surah.number }} - {{ surah.englishName }}
            </option>
          </select>
        </div>

        <div class="search-select-container">
          <select v-model="searchEdition" class="search-select">
            <option value="ar">{{ $t('quran.arabicText') }}</option>
            <optgroup v-for="(translations, lang) in groupedTranslations" :key="lang" :label="getLanguageName(lang)">
              <option v-for="translation in translations" :key="translation.identifier" :value="translation.identifier">
                {{ translation.name }}
              </option>
            </optgroup>
          </select>
        </div>

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
        @click="jumpToSearchResult(match)"
      >
        <div class="search-result-header">
          <span class="surah-name">{{ match.surah.englishName }}</span>
          <span class="verse-number">{{ $t('quran.verse') }} {{ match.numberInSurah }}</span>
          <span v-if="match.edition && match.edition.type" class="edition-type">[{{ match.edition.type }}]</span>
        </div>
        <p class="search-result-text" v-html="highlightSearchTerm(match.text)"></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuranSearch',
  props: {
    surahs: {
      type: Array,
      required: true
    },
    groupedTranslations: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      searchKeyword: '',
      searchSurah: 'all',
      searchEdition: 'ar',
      searchResults: [],
      searchCount: 0,
      searchLoading: false,
      searchError: null
    }
  },
  methods: {
    getLanguageName(langCode) {
      // Emit an event to parent to get language name
      return this.$emit('get-language-name', langCode)
    },
    
    async performSearch() {
      if (!this.searchKeyword) return
      
      this.searchLoading = true
      this.searchResults = []
      this.searchCount = 0
      this.searchError = null
      
      try {
        let apiUrl = `http://api.alquran.cloud/v1/search/${encodeURIComponent(this.searchKeyword)}/${this.searchEdition}`
        
        // If a specific surah is selected, append it to the URL
        if (this.searchSurah !== 'all') {
          apiUrl += `/${this.searchSurah}`
        }
        
        const response = await fetch(apiUrl)
        const data = await response.json()
        
        if (data.code === 200) {
          this.searchResults = data.data.matches
          this.searchCount = data.data.count
        } else {
          this.searchError = data.status
        }
      } catch (error) {
        console.error('Error searching Quran:', error)
        this.searchError = this.$t('quran.searchError')
      } finally {
        this.searchLoading = false
      }
    },
    
    highlightSearchTerm(text) {
      if (!this.searchKeyword || !text) return text
      
      // Simple case-insensitive highlighting
      const regex = new RegExp(`(${this.searchKeyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi')
      return text.replace(regex, '<span class="search-highlight">$1</span>')
    },
    
    jumpToSearchResult(match) {
      // Emit an event to the parent component to handle navigation
      this.$emit('jump-to-search-result', match)
    }
  }
}
</script>

<style scoped>
.search-input-group {
  @apply flex flex-col space-y-2;
}

.search-input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent;
}

.search-options-row {
  @apply flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2;
}

.search-select-container {
  @apply flex-1;
}

.search-select {
  @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent;
}

.search-button {
  @apply px-4 py-2 bg-indigo-600 text-white rounded-lg flex items-center justify-center hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-indigo-600;
}

.search-results-container {
  @apply border border-gray-200 rounded-lg overflow-hidden;
}

.search-result-item {
  @apply px-4 py-3 border-b border-gray-200 last:border-b-0 hover:bg-gray-50 cursor-pointer;
}

.search-result-header {
  @apply flex flex-wrap items-center justify-between mb-1;
}

.surah-name {
  @apply font-medium text-indigo-600;
}

.verse-number {
  @apply text-sm text-gray-500;
}

.edition-type {
  @apply text-xs text-gray-400 ml-2;
}

.search-result-text {
  @apply text-gray-700;
}

.search-highlight {
  @apply bg-yellow-200 font-medium px-1 rounded;
}
</style> 