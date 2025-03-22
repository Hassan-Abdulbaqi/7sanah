<template>
  <div class="quran-reader">
    <h1 class="text-2xl font-bold text-center mb-6">{{ $t('quran.title') }}</h1>
    
    <!-- Direct Search Link -->
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
          <button 
            @click="viewMode = 'book'" 
            :class="['view-mode-button', { active: viewMode === 'book' }]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
            </svg>
            {{ $t('quran.bookView') }}
          </button>
        </div>
      </div>

      <!-- Surah View Content -->
      <div v-if="viewMode === 'surah'">
        <!-- Surah Selection and Audio Controls -->
        <div class="surah-selection">
          <div class="mb-4">
            <!-- Search Bar for Quran Text -->
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

            <h3 class="font-medium mb-2">{{ $t('quran.selectSurah') }}</h3>
            
            <!-- Replace dropdown with surah buttons grid -->
            <div class="surah-buttons-grid">
              <button 
                v-for="surah in surahs" 
                :key="surah.number" 
                @click="selectedSurah = surah.number; loadSurah()"
                :class="['surah-button', { active: selectedSurah === surah.number }]"
                :disabled="loading"
              >
                <span class="surah-number">{{ surah.number }}</span>
                <span class="surah-name">{{ surah.englishName }}</span>
              </button>
            </div>
            
            <!-- Audio Controls (unchanged) -->
            <div class="audio-controls mt-4" v-if="selectedSurah">
              <div v-if="!isPlayingFullSurah">
                <button 
                  @click="listenToFullSurah" 
                  class="audio-button"
                  :disabled="loading || downloadingSurahAudio"
                >
                  <span v-if="downloadingSurahAudio">
                    <svg class="animate-spin h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    {{ $t('quran.downloadingAudio') }}
                  </span>
                  <span v-else>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                    </svg>
                    {{ $t('quran.listenToSurah') }}
                  </span>
                </button>
              </div>
              <div v-else class="flex space-x-2">
                <button @click="togglePause" class="audio-button">
                  <svg v-if="paused" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                  {{ paused ? $t('quran.resumeAudio') : $t('quran.pauseAudio') }}
                </button>
                <button @click="stopAudio" class="audio-button">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd" />
                  </svg>
                  {{ $t('quran.stopAudio') }}
                </button>
              </div>
            </div>
          </div>
          
          <!-- Language and Reciter Selection (unchanged) -->
          <div class="grid grid-cols-2 gap-4 mb-4" v-if="selectedSurah">
            <div>
              <label class="block mb-1 text-sm font-medium">{{ $t('quran.selectLanguage') }}</label>
              <select v-model="selectedTranslation" @change="loadTranslation" class="select-input" :disabled="loadingTranslations">
                <option v-if="loadingTranslations" value="">{{ $t('quran.loading') }}</option>
                <optgroup v-for="(translations, lang) in groupedTranslations" :key="lang" :label="getLanguageName(lang)">
                  <option v-for="translation in translations" :key="translation.identifier" :value="translation.identifier">
                    {{ translation.name }}
                  </option>
                </optgroup>
              </select>
            </div>
            <div>
              <label class="block mb-1 text-sm font-medium">{{ $t('quran.selectReciter') }}</label>
              <select v-model="selectedReciter" class="select-input" :disabled="loadingReciters">
                <option v-if="loadingReciters" value="">{{ $t('quran.loading') }}</option>
                <optgroup v-for="(reciters, lang) in groupedReciters" :key="lang" :label="getLanguageName(lang)">
                  <option v-for="reciter in reciters" :key="reciter.identifier" :value="reciter.identifier">
                    {{ reciter.name }}
                  </option>
                </optgroup>
              </select>
            </div>
          </div>
        </div>
        
        <!-- Loading State -->
        <div class="loading-spinner" v-if="loading">
          <svg class="animate-spin h-8 w-8" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="mt-2">{{ $t('quran.loading') }}</p>
        </div>
        
        <!-- Error Message -->
        <div class="error-message" v-if="error">
          <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <p>{{ error }}</p>
          </div>
        </div>
        
        <!-- No Surah Selected -->
        <div class="no-selection" v-if="!loading && !error && !selectedSurah">
          <p class="text-center text-gray-500">{{ $t('quran.selectSurahPrompt') }}</p>
        </div>
        
        <!-- Surah Content -->
        <div v-if="!loading && !error && selectedSurah && currentSurah" class="surah-content">
          <!-- Surah Header -->
          <div class="surah-header">
            <h2 class="arabic-title">{{ currentSurah.name }}</h2>
            <h3 class="english-title">{{ currentSurah.englishName }} - {{ currentSurah.englishNameTranslation }}</h3>
            <p class="ayah-count">{{ currentSurah.numberOfAyahs }} {{ $t('quran.ayah') }}</p>
            
            <!-- Bismillah except for Surah 9 -->
            <div class="bismillah" v-if="currentSurah.number !== 9">
              {{ $t('quran.bismillah') }}
            </div>
          </div>
          
          <!-- Verses with lazy loading -->
          <div class="verses" ref="versesContainer" @scroll="handleScroll">
            <div 
              v-for="verse in displayedVerses" 
              :key="verse.number"
              class="verse"
              :id="`verse-${verse.number}`"
            >
              <div class="verse-header">
                <span class="verse-number">{{ verse.numberInSurah }}</span>
                <div class="verse-audio-controls">
                  <button 
                    @click="playVerseAudio(verse.number, verse.numberInSurah)"
                    class="verse-audio-button"
                    :disabled="loadingVerseAudio === verse.number"
                  >
                    <svg v-if="loadingVerseAudio === verse.number" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <svg v-else-if="currentPlayingVerse === verse.number" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM14.657 2.929a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071 1 1 0 01-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.828a1 1 0 011.415 0A5.983 5.983 0 0115 10a5.984 5.984 0 01-1.757 4.243 1 1 0 01-1.415-1.415A3.984 3.984 0 0013 10a3.983 3.983 0 00-1.172-2.828a1 1 0 010-1.415z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM14.657 2.929a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071a1 1 0 01-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.828a1 1 0 011.415 0A5.983 5.983 0 0115 10a5.984 5.984 0 01-1.757 4.243a1 1 0 01-1.415-1.415A3.984 3.984 0 0013 10a3.983 3.983 0 00-1.172-2.828a1 1 0 010-1.415z" clip-rule="evenodd" />
                    </svg>
                  </button>
                  <button 
                    v-if="currentPlayingVerse === verse.number" 
                    @click="toggleVerseAudio(verse.number)"
                    class="verse-audio-button ml-2"
                  >
                    <svg v-if="!paused" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
              
              <!-- Audio Progress Bar (only shown for currently playing verse) -->
              <div v-if="currentPlayingVerse === verse.number && audioDuration > 0" class="audio-progress-container">
                <div class="audio-progress-bar" :class="{'loading': verse.number === loadingVerseAudio || (currentPlayingVerse === verse.number && isPartiallyLoaded)}" @click="seekAudio($event)">
                  <div class="audio-progress-fill" :style="{ width: `${(audioProgress / audioDuration) * 100}%` }"></div>
                </div>
                <div class="audio-time">
                  {{ formatTime(audioProgress) }} / {{ formatTime(audioDuration) }}
                </div>
              </div>
              
              <!-- Verse arabic text -->
              <div class="verse-arabic" dir="rtl">
                {{ cleanAyahText(verse.text, currentSurah.number, verse.numberInSurah) }}
              </div>
              <div class="verse-translation" v-if="translatedVerses[verse.numberInSurah]">
                {{ translatedVerses[verse.numberInSurah] }}
              </div>
            </div>
            
            <!-- Loading more indicator -->
            <div v-if="isLoadingMore && currentSurah.ayahs.length > displayedVerses.length" class="loading-more">
              <svg class="animate-spin h-6 w-6 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>
                {{ $t('quran.loadingMore') }}
                <span v-if="isLargeSurah" class="text-sm opacity-70">
                  ({{ displayedVerses.length }} / {{ currentSurah.ayahs.length }} {{ $t('quran.verses') }})
                </span>
              </span>
            </div>
            
            <!-- Progress bar for large suras -->
            <div v-if="isLargeSurah && currentSurah.ayahs.length > displayedVerses.length" class="verse-loading-progress">
              <div class="progress-bar" :style="{ width: `${(displayedVerses.length / currentSurah.ayahs.length) * 100}%` }"></div>
              <div class="progress-text">{{ Math.round((displayedVerses.length / currentSurah.ayahs.length) * 100) }}%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Book View Content -->
      <div v-if="viewMode === 'book'" class="book-view">
        <div class="book-navigation mb-4">
          <div class="flex justify-between items-center">
            <div class="page-navigation">
              <button 
                @click="previousPage" 
                class="nav-button" 
                :disabled="currentPage <= 1 || loadingPage"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
              <span class="page-number">{{ $t('quran.page') }} {{ currentPage }} / 604</span>
              <button 
                @click="nextPage" 
                class="nav-button" 
                :disabled="currentPage >= 604 || loadingPage"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
            <div class="page-jump">
              <input 
                type="number" 
                v-model.number="jumpToPage" 
                min="1" 
                max="604" 
                class="page-input"
                :placeholder="$t('quran.gotoPage')"
              >
              <button @click="goToPage" class="jump-button">
                {{ $t('quran.go') }}
              </button>
            </div>
          </div>
          
          <!-- Audio Controls for Book View -->
          <div class="audio-controls-book mt-4" v-if="currentPageData && currentPageData.ayahs.length > 0">
            <div v-if="!isPlayingPageAudio">
              <button 
                @click="listenToPage" 
                class="audio-button"
                :disabled="loadingPage || downloadingPageAudio"
              >
                <span v-if="downloadingPageAudio">
                  <svg class="animate-spin h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ $t('quran.downloadingAudio') }}
                </span>
                <span v-else>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                  </svg>
                  {{ $t('quran.listenToPage') }}
                </span>
              </button>
            </div>
            <div v-else class="flex space-x-2">
              <button @click="togglePause" class="audio-button">
                <svg v-if="paused" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                {{ paused ? $t('quran.resumeAudio') : $t('quran.pauseAudio') }}
              </button>
              <button @click="stopAudio" class="audio-button">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd" />
                </svg>
                {{ $t('quran.stopAudio') }}
              </button>
            </div>
            
            <!-- Reciter Selection for Book View -->
            <div class="mt-2">
              <label class="block mb-1 text-sm font-medium">{{ $t('quran.selectReciter') }}</label>
              <select v-model="selectedReciter" class="select-input" :disabled="loadingReciters || isPlayingPageAudio">
                <option v-if="loadingReciters" value="">{{ $t('quran.loading') }}</option>
                <optgroup v-for="(reciters, lang) in groupedReciters" :key="lang" :label="getLanguageName(lang)">
                  <option v-for="reciter in reciters" :key="reciter.identifier" :value="reciter.identifier">
                    {{ reciter.name }}
                  </option>
                </optgroup>
              </select>
            </div>
          </div>
        </div>

        <!-- Page Content -->
        <div class="book-content">
          <!-- Loading State -->
          <div class="loading-spinner" v-if="loadingPage">
            <svg class="animate-spin h-8 w-8" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="mt-2">{{ $t('quran.loading') }}</p>
          </div>
          
          <!-- Error Message -->
          <div class="error-message" v-if="pageError">
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              <p>{{ pageError }}</p>
            </div>
          </div>
          
          <!-- Page Content -->
          <div v-if="!loadingPage && !pageError && currentPageData" class="page-content">
            <div class="flex justify-between mb-2 text-sm text-gray-500">
              <span>{{ currentPageInfo }}</span>
              <span>{{ $t('quran.page') }} {{ currentPage }}</span>
            </div>
            
            <div class="page-text" dir="rtl">
              <!-- Group ayahs by Surah and render with proper headers -->
              <div v-for="surahNumber in getUniquePageSurahs()" :key="`surah-group-${surahNumber}`" class="surah-group">
                <!-- Surah Header -->
                <div class="surah-header-in-page">
                  <div class="surah-name">{{ getSurahName(surahNumber) }}</div>
                  <!-- Display Bismillah from API data if this is the first ayah of the surah and it's not Surah 9 -->
                  <div v-if="isSurahFirstAyahOnPage(surahNumber) && surahNumber !== 9" class="bismillah">
                    {{ $t('quran.bismillah') }}
                  </div>
                </div>
                
                <!-- Continuous text for ayahs of this Surah -->
                <div class="continuous-quran-text">
                  <span 
                    v-for="ayah in getAyahsForSurah(surahNumber)" 
                    :key="ayah.number"
                    :id="`page-verse-${ayah.number}`"
                    :class="['ayah-text', { 'active-ayah': highlightedAyah === ayah.number }]"
                    @click="playPageVerseAudio(ayah.number, ayah.surah.number, ayah.numberInSurah)"
                  >
                    {{ cleanAyahText(ayah.text, ayah.surah.number, ayah.numberInSurah) }}
                    <span class="ayah-number">({{ ayah.numberInSurah }})</span>
                  </span>
                </div>
                
                <!-- Audio Progress Bar (only shown for currently playing verse in this surah) -->
                <div v-if="getAyahsForSurah(surahNumber).some(ayah => ayah.number === currentPlayingVerse) && audioDuration > 0" class="audio-progress-container">
                  <div class="audio-progress-bar" :class="{'loading': getAyahsForSurah(surahNumber).some(ayah => ayah.number === loadingVerseAudio) || (getAyahsForSurah(surahNumber).some(ayah => ayah.number === currentPlayingVerse) && isPartiallyLoaded)}" @click="seekAudio($event)">
                    <div class="audio-progress-fill" :style="{ width: `${(audioProgress / audioDuration) * 100}%` }"></div>
                  </div>
                  <div class="audio-time">
                    {{ formatTime(audioProgress) }} / {{ formatTime(audioDuration) }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Translation -->
            <div v-if="pageTranslation.length > 0" class="page-translation" dir="ltr">
              <div 
                v-for="ayah in pageTranslation" 
                :key="ayah.number"
                :class="['translation-verse', { 'active-translation': highlightedAyah === ayah.number }]"
              >
                <span class="verse-number">{{ ayah.numberInSurah }}:</span>
                <span class="translation-text">{{ ayah.text }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'QuranReader',
  data() {
    return {
      surahs: [],
      currentSurah: null,
      selectedSurah: '',
      selectedTranslation: 'en.asad',
      selectedReciter: 'ar.alafasy',
      translatedVerses: {},
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
      displayedVerses: [],
      isLoadingMore: false,
      verseChunkSize: 20,
      initialChunkSize: 10, // Smaller initial size for very large suras
      largeVerseThreshold: 100, // Threshold to determine "large" suras
      loadingChunks: false,
      scrollThreshold: 300, // Larger scroll threshold for earlier prefetching
      prefetchThreshold: 500, // Threshold for prefetching the next chunk
      isLargeSurah: false, // Flag to track if current surah is considered large
      currentPlayingVerse: null,
      audioProgress: 0,
      audioDuration: 0,
      audioUpdateInterval: null,
      isPartiallyLoaded: false,
      // Scroll handling optimization
      _scrollDebounceTimer: null,
      _prefetchTimer: null,
      _shouldPrefetch: false,
      // Search functionality
      searchKeyword: '',
      searchSurah: 'all',
      searchEdition: 'ar',
      searchResults: [],
      searchCount: 0,
      searchLoading: false,
      searchError: null
    }
  },
  async created() {
    try {
      this.loading = true
      
      // Check if there's navigation data from the search component
      const navigationData = localStorage.getItem('quranNavigationTarget')
      let targetSurah = null
      let targetVerse = null
      let targetEdition = null
      
      if (navigationData) {
        try {
          const parsedData = JSON.parse(navigationData)
          targetSurah = parsedData.surah
          targetVerse = parsedData.verse
          targetEdition = parsedData.edition
          
          // Clear the navigation data so it doesn't trigger again on next visit
          localStorage.removeItem('quranNavigationTarget')
        } catch (e) {
          console.error('Error parsing navigation data:', e)
        }
      }
      
      // Fetch surahs
      const surahsResponse = await fetch('http://api.alquran.cloud/v1/surah')
      const surahsData = await surahsResponse.json()
      
      if (surahsData.code === 200) {
        this.surahs = surahsData.data
      } else {
        this.error = surahsData.status
      }
      
      // Fetch editions using a single API endpoint
      await this.fetchEditions()
      
      // If we have navigation data, navigate to the specified verse
      if (targetSurah && targetVerse) {
        this.selectedSurah = targetSurah
        if (targetEdition) {
          this.selectedTranslation = targetEdition
        }
        
        // Load the surah
        await this.loadSurah()
        
        // After the surah is loaded, find and scroll to the verse
        this.$nextTick(() => {
          // Find the verse element
          const verseElement = document.getElementById(`verse-${targetVerse}`)
          if (verseElement) {
            // Highlight the verse
            this.highlightedAyah = targetVerse
            
            // Scroll to the verse
            verseElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
            
            // Add a temporary highlight effect
            verseElement.classList.add('search-highlight')
            setTimeout(() => {
              verseElement.classList.remove('search-highlight')
            }, 3000)
          } else {
            // The verse might not be loaded yet if it's in a large surah with lazy loading
            this.loadVersesUntilFound(targetVerse)
          }
        })
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
    },
    selectedTranslation() {
      // Reload translation when it changes
      if (this.viewMode === 'book' && this.currentPageData) {
        this.loadPageTranslation()
      }
    },
    currentSurah: {
      handler(newSurah) {
        if (newSurah) {
          // Reset displayed verses and load initial chunk
          this.displayedVerses = []
          this.loadInitialVerses()
        }
      },
      deep: true
    }
  },
  methods: {
    // Helper function to get MP3Quran.net reciter code
    getMp3QuranReciterCode(reciterName) {
      // Map of reciter names to their codes on MP3Quran.net
      const reciterMap = {
        'alafasy': 'mishary_alafasy',
        'abdulsamad': 'abdul_basit_murattal',
        'abdullahbasfar': 'abdullah_basfar',
        'abdurrahmaansudais': 'abdurrahmaan_sudais',
        'shaatree': 'abu_bakr_ash-shaatree',
        'ahmedajamy': 'ahmed_ibn_ali_al_ajamy',
        'hanirifai': 'hani_rifai',
        'husary': 'mahmoud_khalil_al-husary_murattal',
        'husarymujawwad': 'mahmoud_khalil_al-husary',
        'hudhaify': 'hudhaify',
        'ibrahimakhbar': 'ibrahim_akhdar',
        'mahermuaiqly': 'maher_almuaiqly',
        'muhammadayyoub': 'muhammad_ayyoub',
        'muhammadjibreel': 'muhammad_jibreel',
        'saoodshuraym': 'saood_ash-shuraym',
        'parhizgar': 'parhizgar',
        'aymanswoaid': 'ayman_sowaid'
      }
      
      return reciterMap[reciterName] || null
    },
    
    async fetchEditions() {
      try {
        this.loadingTranslations = true
        this.loadingReciters = true
        
        // Use the specified API endpoint to get all editions
        const response = await fetch('http://api.alquran.cloud/v1/edition')
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
          
          // If no reciter is selected, pre-select the default one
          if (!this.selectedReciter && this.reciters.length > 0) {
            this.selectedReciter = this.reciters.find(r => r.identifier === 'ar.alafasy')?.identifier || this.reciters[0].identifier
          }
        }
      } catch (error) {
        console.error('Error fetching editions:', error)
      } finally {
        this.loadingTranslations = false
        this.loadingReciters = false
      }
    },
    
    getLanguageName(langCode) {
      return this.languages[langCode] || langCode.toUpperCase()
    },
    
    async loadSurah() {
      if (!this.selectedSurah) {
        this.currentSurah = null;
        this.translatedVerses = {};
        this.displayedVerses = [];
        return Promise.resolve();
      }
      
      try {
        this.loading = true;
        this.error = null;
        this.stopAudio();
        this.displayedVerses = []; // Reset displayed verses
        
        const response = await fetch(`http://api.alquran.cloud/v1/surah/${this.selectedSurah}/quran-uthmani`);
        const data = await response.json();
        
        if (data.code === 200) {
          this.currentSurah = data.data;
          
          // Check if this is a large surah
          this.isLargeSurah = this.currentSurah.ayahs && 
                             this.currentSurah.ayahs.length > this.largeVerseThreshold;
          
          console.log(`Surah ${this.currentSurah.englishName} has ${this.currentSurah.ayahs.length} verses. Large Surah: ${this.isLargeSurah}`);
          
          // Load initial verses immediately
          this.loadInitialVerses();
          
          // Load translation asynchronously without waiting
          this.loadTranslation();
          
          // Set loading to false immediately after displaying initial verses
          this.loading = false;
          
          return Promise.resolve();
        } else {
          this.error = data.status;
          this.loading = false;
          return Promise.reject(new Error(data.status));
        }
      } catch (error) {
        console.error('Error fetching surah data:', error);
        this.error = this.$t('quran.networkError');
        this.loading = false;
        return Promise.reject(error);
      }
    },
    
    loadInitialVerses() {
      if (!this.currentSurah || !this.currentSurah.ayahs) return
      
      // For very large surahs (like Al-Baqarah), use an even smaller initial chunk
      let initialSize = this.initialChunkSize;
      if (this.isLargeSurah) {
        // Adjust initial size based on surah length
        if (this.currentSurah.ayahs.length > 200) {
          initialSize = 5; // For extremely large surahs, start with just 5 verses
        } else if (this.currentSurah.ayahs.length > 150) {
          initialSize = 8; // For very large surahs, start with 8 verses
        } else {
          initialSize = this.initialChunkSize; // Use default small size
        }
      } else {
        initialSize = this.verseChunkSize; // Use regular chunk size for normal surahs
      }
      
      console.log(`Loading initial ${initialSize} verses of ${this.currentSurah.ayahs.length} total verses`);
      
      // Load first chunk immediately without delay for better UX
      this.displayedVerses = this.currentSurah.ayahs.slice(0, initialSize);
      
      // If there are more verses, set up loading indicator and prepare to load more
      if (initialSize < this.currentSurah.ayahs.length) {
        this.isLoadingMore = true;
        
        // Schedule loading of next chunk after a short delay
        setTimeout(() => {
          this.isLoadingMore = false;
          this.loadMoreVerses(this.verseChunkSize);
        }, 100);
      }
    },
    
    loadMoreVerses(chunkSize = null) {
      if (this.loadingChunks || !this.currentSurah || !this.currentSurah.ayahs) return
      
      this.loadingChunks = true
      this.isLoadingMore = true
      
      // Determine start index for next chunk
      const startIndex = this.displayedVerses.length
      
      // If all verses are already loaded, do nothing
      if (startIndex >= this.currentSurah.ayahs.length) {
        this.isLoadingMore = false
        this.loadingChunks = false
        return
      }
      
      // Use provided chunkSize or default to verseChunkSize (or adjust for large surahs)
      let actualChunkSize = chunkSize || this.verseChunkSize;
      
      // For very large surahs, adjust chunk size to prevent UI freezes
      if (this.isLargeSurah && this.currentSurah.ayahs.length > 200) {
        // Use smaller chunks for very large surahs
        actualChunkSize = Math.min(actualChunkSize, 15);
      }
      
      // Calculate end index for next chunk
      const endIndex = Math.min(startIndex + actualChunkSize, this.currentSurah.ayahs.length)
      
      console.log(`Loading verses ${startIndex+1} to ${endIndex} of ${this.currentSurah.ayahs.length} (chunk size: ${actualChunkSize})`)
      
      // Minimal delay for UI responsiveness
      setTimeout(() => {
        // Add next chunk of verses to displayed verses
        const nextChunk = this.currentSurah.ayahs.slice(startIndex, endIndex)
        this.displayedVerses = [...this.displayedVerses, ...nextChunk]
        
        // Check if we should schedule next chunk loading
        if (endIndex < this.currentSurah.ayahs.length) {
          // Schedule prefetch for next chunk if we're not at the end
          this.scheduleNextChunkLoad(endIndex);
        }
        
        this.isLoadingMore = false
        this.loadingChunks = false
      }, 10) // Minimal delay just to keep UI responsive
    },
    
    scheduleNextChunkLoad(lastLoadedIndex) {
      // For very large surahs, automatically load the next chunk without waiting for scroll
      // but only do this for the first few chunks to fill the initial screen
      if (this.isLargeSurah && lastLoadedIndex < 50 && !this.loadingChunks) {
        setTimeout(() => {
          if (!this.loadingChunks && this.displayedVerses.length < this.currentSurah.ayahs.length) {
            this.loadMoreVerses();
          }
        }, 300); // Short delay before loading next chunk
      }
    },
    
    prefetchNextChunk(startIndex) {
      // This doesn't actually load the verses into the view, just prepares them
      // for faster loading when the user scrolls down
      if (startIndex >= this.currentSurah.ayahs.length) return;
      
      const prefetchSize = Math.min(this.verseChunkSize, this.currentSurah.ayahs.length - startIndex);
      console.log(`Prefetching next ${prefetchSize} verses (${startIndex+1} to ${startIndex+prefetchSize})`)
      
      // We don't need to do anything here besides triggering the API/data to load
      // The goal is to have the data ready in memory/cache when needed
    },
    
    handleScroll(event) {
      if (!this.currentSurah || this.loadingChunks) return
      
      const container = this.$refs.versesContainer
      if (!container) return
      
      // Calculate scroll position
      const scrollPosition = container.scrollTop + container.clientHeight
      const scrollHeight = container.scrollHeight
      
      // Calculate distance to bottom
      const distanceToBottom = scrollHeight - scrollPosition;
      
      // For performance, add a debounce for scroll-triggered loading
      if (!this._scrollDebounceTimer) {
        // If we've reached the loading threshold, load more verses
        if (distanceToBottom < this.scrollThreshold) {
          // Add debounce to prevent multiple rapid calls during scrolling
          this._scrollDebounceTimer = setTimeout(() => {
            this._scrollDebounceTimer = null;
            
            // Only load more if we're not already loading and there are more verses
            if (!this.loadingChunks && 
                !this.isLoadingMore && 
                this.displayedVerses.length < this.currentSurah.ayahs.length) {
              this.loadMoreVerses();
            }
          }, 100); // Short debounce delay
        }
        // If we're within prefetch threshold but not at loading threshold,
        // just mark that we should load soon but don't actually start loading
        else if (
          this.isLargeSurah && 
          !this.isLoadingMore &&
          distanceToBottom < this.prefetchThreshold && 
          this.displayedVerses.length < this.currentSurah.ayahs.length
        ) {
          // Set a flag to indicate we're approaching the end
          this._shouldPrefetch = true;
          
          // Schedule a delayed check to see if we should load more
          if (!this._prefetchTimer) {
            this._prefetchTimer = setTimeout(() => {
              this._prefetchTimer = null;
              if (this._shouldPrefetch && 
                  !this.loadingChunks && 
                  !this.isLoadingMore &&
                  this.displayedVerses.length < this.currentSurah.ayahs.length) {
                this.loadMoreVerses();
              }
              this._shouldPrefetch = false;
            }, 300);
          }
        } else {
          // If we're not near the bottom, clear the prefetch flag
          this._shouldPrefetch = false;
        }
      }
    },
    
    async loadTranslation() {
      if (!this.selectedSurah || !this.selectedTranslation) return
      
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
        const response = await fetch(`http://api.alquran.cloud/v1/surah/${this.selectedSurah}/${this.selectedTranslation}`)
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
    
    async playVerseAudio(verseNumber, verseNumberInSurah) {
      // Stop any currently playing audio
      this.stopAudio()
      
      try {
        this.loadingVerseAudio = verseNumber
        this.highlightedAyah = verseNumber
        // Reset pause state when starting new playback
        this.paused = false
        
        // Reset progress tracking
        this.audioProgress = 0
        this.audioDuration = 0
        
        // Get reciter info
        const reciter = this.reciters.find(r => r.identifier === this.selectedReciter)
        if (!reciter) {
          throw new Error('Selected reciter not found')
        }
        
        // Use the API to get the audio data for this specific ayah
        try {
          // Add loading class to the verse
          const verseElement = document.getElementById(`verse-${verseNumber}`)
          if (verseElement) {
            verseElement.classList.add('loading-ayah-audio')
          }
          
          // Fetch the surah data with the selected audio reciter
          console.log(`Fetching audio data for surah ${this.selectedSurah} ayah ${verseNumberInSurah} using ${this.selectedReciter}`)
          const response = await fetch(`http://api.alquran.cloud/v1/surah/${this.selectedSurah}/${this.selectedReciter}`)
          const data = await response.json()
          
          if (data.code === 200 && data.data && data.data.ayahs) {
            // Find the specific ayah
            const ayah = data.data.ayahs.find(a => a.numberInSurah === verseNumberInSurah)
            
            if (ayah && ayah.audio) {
              console.log(`Playing verse ${verseNumberInSurah} from audio URL provided by API`)
              // Create audio player with progressive loading
              this.audioPlayer = new Audio()
              
              // Set up event listeners
              // Start playback as soon as enough data is buffered for smooth start
              this.audioPlayer.addEventListener('canplay', () => {
                console.log('Audio has buffered enough to begin playback')
                // Start playing as soon as we have enough data
                this.audioPlayer.play().catch(error => {
                  console.error('Error starting playback:', error)
                })
                // Set this verse as the currently playing verse
                this.currentPlayingVerse = verseNumber
                this.loadingVerseAudio = null
              }, { once: true })
              
              // Continue loading the rest while playing
              this.audioPlayer.addEventListener('canplaythrough', () => {
                console.log('Audio loaded completely')
                // Remove loading class when fully loaded
                if (verseElement) {
                  verseElement.classList.remove('loading-ayah-audio')
                }
                // Set partially loaded state
                this.isPartiallyLoaded = true
                
                // Reset the partially loaded state after animation completes
                setTimeout(() => {
                  this.isPartiallyLoaded = false
                }, 3100) // Slightly longer than the animation duration (3s)
              }, { once: true })
              
              this.audioPlayer.addEventListener('playing', () => {
                console.log('Audio playback started')
                // Change visual indicator to show it's now playing
                if (verseElement) {
                  verseElement.classList.add('playing-ayah-audio')
                }
                
                // Start tracking progress
                this.startProgressTracking()
              })
              
              this.audioPlayer.addEventListener('ended', () => {
                this.loadingVerseAudio = null
                this.highlightedAyah = null
                this.currentPlayingVerse = null
                this.isPartiallyLoaded = false
                
                // Stop tracking progress
                this.stopProgressTracking()
                
                // Clean up all special classes
                if (verseElement) {
                  verseElement.classList.remove('loading-ayah-audio', 'playing-ayah-audio')
                }
              })
              
              this.audioPlayer.addEventListener('error', (error) => {
                console.error(`Error playing audio: ${error}`)
                this.loadingVerseAudio = null
                this.highlightedAyah = null
                this.currentPlayingVerse = null
                // Remove loading class
                if (verseElement) {
                  verseElement.classList.remove('loading-ayah-audio', 'playing-ayah-audio')
                }
                this.$notification.error(this.$t('quran.audioNotAvailable'))
              })
              
              // Start loading the audio (will trigger canplay when ready)
              this.audioPlayer.preload = 'auto'
              this.audioPlayer.src = ayah.audio
            } else {
              throw new Error('Audio not found for this ayah')
            }
          } else {
            throw new Error(`API error: ${data.status || 'Unknown error'}`)
          }
        } catch (error) {
          console.error(`Error fetching audio data: ${error}`)
          this.loadingVerseAudio = null
          this.highlightedAyah = null
          this.currentPlayingVerse = null
          // Remove loading class from all verses
          const verseElement = document.getElementById(`verse-${verseNumber}`)
          if (verseElement) {
            verseElement.classList.remove('loading-ayah-audio', 'playing-ayah-audio')
          }
          this.$notification.error(this.$t('quran.audioNotAvailable'))
        }
      } catch (error) {
        console.error('Error playing verse audio:', error)
        this.loadingVerseAudio = null
        this.highlightedAyah = null
        this.currentPlayingVerse = null
        // Remove loading class from all verses
        const verseElement = document.getElementById(`verse-${verseNumber}`)
        if (verseElement) {
          verseElement.classList.remove('loading-ayah-audio', 'playing-ayah-audio')
        }
        this.$notification.error(this.$t('quran.audioNotAvailable'))
      }
    },
    
    async listenToFullSurah() {
      try {
        this.stopAudio()
        this.downloadingSurahAudio = true
        
        // Get reciter info
        const reciter = this.reciters.find(r => r.identifier === this.selectedReciter)
        if (!reciter) {
          throw new Error('Selected reciter not found')
        }
        
        // Fetch the surah data with the selected audio reciter
        try {
          console.log(`Fetching audio data for surah ${this.selectedSurah} using ${this.selectedReciter}`)
          const response = await fetch(`http://api.alquran.cloud/v1/surah/${this.selectedSurah}/${this.selectedReciter}`)
          const data = await response.json()
          
          if (data.code === 200 && data.data && data.data.ayahs) {
            // For verse-by-verse reciters, we'll play the verses sequentially
            this.downloadingSurahAudio = false
            
            if (reciter.type === 'versebyverse') {
              this.$notification.info(this.$t('quran.playingVerseByVerse'))
              // Use the fetched ayahs for playback
              this.playVerseByVerseWithData(data.data.ayahs)
            } else {
              // For full surah reciters, try to play the full surah audio if available
              const firstAyah = data.data.ayahs[0]
              
              if (firstAyah && firstAyah.audioSecondary && firstAyah.audioSecondary.length > 0) {
                // Some editions provide a full surah audio in the first ayah's audioSecondary field
                const fullSurahAudio = firstAyah.audioSecondary[0]
                console.log(`Playing full surah audio from URL provided by API`)
                
                // Create audio with progressive loading for full surah
                this.audioPlayer = new Audio()
                
                // Set up event listeners for progressive loading
                this.audioPlayer.addEventListener('canplay', () => {
                  console.log('Full surah audio has buffered enough to begin playback')
                  // Start playing as soon as we have enough data
                  this.audioPlayer.play().catch(error => {
                    console.error('Error starting full surah playback:', error)
                  })
                  this.isPlayingFullSurah = true
                  this.paused = false
                  
                  // Show notification that playback has started
                  this.$notification.info(this.$t('quran.playbackStarted'))
                }, { once: true })
                
                this.audioPlayer.addEventListener('canplaythrough', () => {
                  console.log('Full surah audio loaded completely')
                  this.downloadingSurahAudio = false
                }, { once: true })
                
                this.audioPlayer.addEventListener('ended', () => {
                  this.isPlayingFullSurah = false
                })
                
                this.audioPlayer.addEventListener('error', (error) => {
                  console.error(`Error playing full surah audio: ${error}`)
                  this.$notification.warning(this.$t('quran.tryingVerseByVerse'))
                  this.playVerseByVerseWithData(data.data.ayahs)
                })
                
                // Start loading the audio (will trigger canplay when ready)
                this.audioPlayer.preload = 'auto'
                this.audioPlayer.src = fullSurahAudio
                // Show loading indication while waiting for canplay event
                this.downloadingSurahAudio = true
              } else {
                // Fall back to verse-by-verse if no full surah audio is available
                this.$notification.info(this.$t('quran.playingVerseByVerse'))
                this.playVerseByVerseWithData(data.data.ayahs)
              }
            }
          } else {
            throw new Error(`API error: ${data.status || 'Unknown error'}`)
          }
        } catch (error) {
          console.error(`Error fetching audio data: ${error}`)
          this.downloadingSurahAudio = false
          this.$notification.error(this.$t('quran.audioNotAvailable'))
        }
      } catch (error) {
        console.error('Error playing full surah audio:', error)
        this.downloadingSurahAudio = false
        this.isPlayingFullSurah = false
        this.$notification.error(this.$t('quran.audioNotAvailable'))
      }
    },
    
    async playVerseByVerseWithData(ayahs) {
      if (!ayahs || ayahs.length === 0) {
        console.error('No ayahs provided for verse-by-verse playback')
        return
      }
      
      this.isPlayingFullSurah = true
      this.paused = false
      
      // For preloading next ayahs
      const preloadedAudio = {}
      
      // Preload function to load next ayah audio
      const preloadNextAyah = async (index) => {
        // Check if we should preload the next ayah
        if (index + 1 < ayahs.length && ayahs[index + 1].audio) {
          try {
            // Check if we haven't already preloaded this ayah
            if (!preloadedAudio[index + 1]) {
              console.log(`Preloading verse ${index + 2} audio...`)
              
              // Create a new audio element with progressive loading
              const nextAudio = new Audio()
              
              // Create a promise to track when preloading is ready to play
              const preloadPromise = new Promise((resolve, reject) => {
                nextAudio.addEventListener('canplay', () => {
                  console.log(`Verse ${index + 2} audio buffered enough for playback`)
                  resolve(nextAudio)
                }, { once: true })
                
                nextAudio.addEventListener('error', (error) => {
                  console.error(`Error preloading verse ${index + 2} audio:`, error)
                  reject(error)
                }, { once: true })
              })
              
              // Start loading
              nextAudio.preload = 'auto'
              nextAudio.src = ayahs[index + 1].audio
              
              // Store in preloaded cache
              preloadedAudio[index + 1] = preloadPromise
            }
            
            // Try to preload one more in advance if possible
            if (index + 2 < ayahs.length && ayahs[index + 2].audio && !preloadedAudio[index + 2]) {
              setTimeout(() => {
                const nextNextAudio = new Audio()
                
                // Create a promise to track when preloading is ready to play
                const preloadPromise = new Promise((resolve, reject) => {
                  nextNextAudio.addEventListener('canplay', () => {
                    console.log(`Verse ${index + 3} audio buffered enough for playback`)
                    resolve(nextNextAudio)
                  }, { once: true })
                  
                  nextNextAudio.addEventListener('error', (error) => {
                    console.error(`Error preloading verse ${index + 3} audio:`, error)
                    reject(error)
                  }, { once: true })
                })
                
                // Start loading
                nextNextAudio.preload = 'auto'
                nextNextAudio.src = ayahs[index + 2].audio
                
                // Store in preloaded cache
                preloadedAudio[index + 2] = preloadPromise
              }, 1000) // Slight delay to prioritize the next verse first
            }
          } catch (error) {
            console.error(`Error during preloading:`, error)
          }
        }
      }
      
      try {
        // Play function that will recursively go through the queue
        const playNext = async (index = 0) => {
          if (index >= ayahs.length || !this.isPlayingFullSurah) {
            this.isPlayingFullSurah = false
            return
          }
          
          try {
            // Display current verse being played
            this.loadingVerseAudio = ayahs[index].number
            this.highlightedAyah = ayahs[index].number
            
            // Scroll to the verse being played
            const verseElement = document.getElementById(`verse-${ayahs[index].number}`)
            if (verseElement) {
              verseElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
              verseElement.classList.add('loading-ayah-audio')
            }
            
            // Get the audio URL from the ayah data
            if (ayahs[index].audio) {
              console.log(`Playing verse ${index + 1} from audio URL provided by API`)
              
              // Try to use preloaded audio if available
              if (preloadedAudio[index]) {
                try {
                  this.audioPlayer = await preloadedAudio[index]
                  console.log(`Using preloaded audio for verse ${index + 1}`)
                  // The audio is already buffered enough to play
                  if (verseElement) {
                    verseElement.classList.remove('loading-ayah-audio')
                    verseElement.classList.add('playing-ayah-audio')
                  }
                } catch (error) {
                  // If preloaded audio fails, create a new one
                  console.warn(`Preloaded audio failed, creating new audio for verse ${index + 1}`)
                  this.createProgressiveAudioPlayer(ayahs[index].audio, verseElement)
                }
              } else {
                // No preloaded audio, create a new one with progressive loading
                this.createProgressiveAudioPlayer(ayahs[index].audio, verseElement)
              }
              
              // Start preloading the next ayah in the background
              preloadNextAyah(index)
              
              // Set up event listeners
              this.audioPlayer.addEventListener('ended', () => {
                this.loadingVerseAudio = null
                this.highlightedAyah = null
                if (verseElement) {
                  verseElement.classList.remove('loading-ayah-audio', 'playing-ayah-audio')
                }
                if (this.isPlayingFullSurah && !this.paused) {
                  playNext(index + 1)
                }
              })
              
              this.audioPlayer.addEventListener('error', (error) => {
                console.error(`Error playing verse ${index + 1} audio: ${error}`)
                this.loadingVerseAudio = null
                this.highlightedAyah = null
                if (verseElement) {
                  verseElement.classList.remove('loading-ayah-audio', 'playing-ayah-audio')
                }
                // Skip to next verse if this one fails
                playNext(index + 1)
              })
              
              // If audio isn't already playing (from preloaded state), start it
              if (this.audioPlayer.paused) {
                try {
                  await this.audioPlayer.play()
                  if (verseElement) {
                    verseElement.classList.add('playing-ayah-audio')
                  }
                } catch (error) {
                  console.error(`Error starting playback: ${error}`)
                  this.loadingVerseAudio = null
                  this.highlightedAyah = null
                  if (verseElement) {
                    verseElement.classList.remove('loading-ayah-audio', 'playing-ayah-audio')
                  }
                  playNext(index + 1)
                }
              }
            } else {
              console.error(`No audio available for verse ${index + 1}`)
              this.loadingVerseAudio = null
              this.highlightedAyah = null
              if (verseElement) {
                verseElement.classList.remove('loading-ayah-audio', 'playing-ayah-audio')
              }
              // Skip to next verse if this one has no audio
              playNext(index + 1)
            }
          } catch (error) {
            console.error(`Error playing verse ${index + 1}:`, error)
            // Skip to next verse if this one fails
            this.loadingVerseAudio = null
            this.highlightedAyah = null
            const verseElement = document.getElementById(`verse-${ayahs[index].number}`)
            if (verseElement) {
              verseElement.classList.remove('loading-ayah-audio', 'playing-ayah-audio')
            }
            playNext(index + 1)
          }
        }
        
        // Start playing from the first ayah
        playNext(0)
        
      } catch (error) {
        console.error('Error in verse-by-verse playback:', error)
        this.isPlayingFullSurah = false
        this.loadingVerseAudio = null
        this.highlightedAyah = null
        this.$notification.error(this.$t('quran.audioNotAvailable'))
      }
    },
    
    // Helper method to create an audio player with progressive loading
    createProgressiveAudioPlayer(audioUrl, verseElement) {
      // Check if browser supports MediaSource
      if ('MediaSource' in window && audioUrl.endsWith('.mp3')) {
        this.createChunkedAudioPlayer(audioUrl, verseElement);
        return;
      }

      // Fallback to standard Audio but with aggressive settings
      this.audioPlayer = new Audio();
      
      // Set explicit buffering strategy
      this.audioPlayer.preload = 'auto';
      
      // Try to force smaller initial buffer size to start playback sooner
      if (this.audioPlayer.mozAutoplayEnabled !== undefined) {
        // Firefox specific
        this.audioPlayer.mozAutoplayEnabled = true;
      }
      
      if (this.audioPlayer.autobuffer !== undefined) {
        // Old property but might help in some browsers
        this.audioPlayer.autobuffer = true;
      }
      
      // Start load and play as soon as metadata is loaded
      this.audioPlayer.addEventListener('loadedmetadata', () => {
        console.log('Audio metadata loaded, attempting immediate playback');
        this.audioPlayer.play().catch(error => {
          console.error('Error starting playback at metadata:', error);
        });
        // Add playing indicator immediately
        if (verseElement) {
          verseElement.classList.add('playing-ayah-audio')
        }
        // Set partially loaded state
        this.isPartiallyLoaded = true
      }, { once: true });
      
      // Also try starting playback when any data is available
      this.audioPlayer.addEventListener('loadeddata', () => {
        console.log('Some audio data loaded, attempting playback');
        if (this.audioPlayer.paused) {
          this.audioPlayer.play().catch(error => {
            console.error('Error starting playback at data:', error);
          });
        }
      }, { once: true });
      
      // Backup - try playing as soon as possible
      this.audioPlayer.addEventListener('canplay', () => {
        console.log('Audio has buffered enough to begin playback');
        if (this.audioPlayer.paused) {
          this.audioPlayer.play().catch(error => {
            console.error('Error starting playback at canplay:', error);
          });
        }
      }, { once: true });
      
      // Update UI when fully loaded
      this.audioPlayer.addEventListener('canplaythrough', () => {
        console.log('Audio loaded completely')
        if (verseElement) {
          verseElement.classList.remove('loading-ayah-audio')
          verseElement.classList.add('playing-ayah-audio')
        }
        
        // Set partially loaded state
        this.isPartiallyLoaded = true
        
        // Reset after animation completes
        setTimeout(() => {
          this.isPartiallyLoaded = false
        }, 3100)
      }, { once: true });
      
      // Set source and start loading
      this.audioPlayer.src = audioUrl;
      
      // Force download to start immediately
      try {
        this.audioPlayer.load();
        
        // Try to start playback immediately (may fail, but worth trying)
        this.audioPlayer.play().catch(error => {
          console.log('Expected error with immediate play, waiting for data:', error);
          // This is expected to fail sometimes, we'll retry on events
        });
      } catch (e) {
        console.log('Expected exception with aggressive loading:', e);
      }
    },

    // Method to use for chunked streaming of MP3 files
    async createChunkedAudioPlayer(audioUrl, verseElement) {
      console.log('Creating chunked audio player for faster start');
      
      try {
        // Set partially loaded state for progressive loading visual feedback
        this.isPartiallyLoaded = true;
        
        // Create audio element
        this.audioPlayer = new Audio();
        
        // Use a small chunk approach for mp3 files
        const response = await fetch(audioUrl, {
          headers: {
            'Range': 'bytes=0-65536' // Request just the first chunk
          }
        });
        
        if (!response.ok) {
          // If range request fails, fall back to standard approach
          console.log('Range request not supported, falling back to standard audio');
          this.audioPlayer.src = audioUrl;
          this.audioPlayer.play().catch(error => {
            console.error('Error starting fallback playback:', error);
          });
          return;
        }
        
        // Get the first chunk as blob
        const initialChunk = await response.blob();
        
        // Create object URL and start playing immediately
        const objectUrl = URL.createObjectURL(initialChunk);
        this.audioPlayer.src = objectUrl;
        
        // Start playing as soon as possible
        this.audioPlayer.addEventListener('loadedmetadata', () => {
          console.log('Initial chunk metadata loaded, starting playback');
          this.audioPlayer.play().catch(error => {
            console.error('Error starting chunk playback:', error);
          });
          
          // Show playing status
          if (verseElement) {
            verseElement.classList.add('playing-ayah-audio');
          }
        }, { once: true });
        
        // Load the audio
        this.audioPlayer.load();
        
        // Start loading the rest of the file in the background
        this.loadRestOfAudio(audioUrl, verseElement);
        
      } catch (error) {
        console.error('Error with chunked playback:', error);
        // Fall back to normal method
        this.audioPlayer = new Audio(audioUrl);
        this.audioPlayer.play().catch(e => console.error('Fallback error:', e));
      }
    },

    // Load the rest of the audio file in the background
    async loadRestOfAudio(audioUrl, verseElement) {
      try {
        // Fetch the complete file in the background
        const fullResponse = await fetch(audioUrl);
        const fullAudioBlob = await fullResponse.blob();
        
        // If the initial playback is complete, don't switch
        if (!this.audioPlayer || this.audioPlayer.ended) {
          return;
        }
        
        // Store current playback position
        const currentTime = this.audioPlayer.currentTime;
        const wasPlaying = !this.audioPlayer.paused;
        const wasPaused = this.paused; // Store current pause state
        
        // Create a new audio element for the full file
        const newAudio = new Audio(URL.createObjectURL(fullAudioBlob));
        
        // Set to the same position
        newAudio.currentTime = currentTime;
        
        // When the new audio is ready, switch to it
        newAudio.addEventListener('canplay', () => {
          // Stop tracking the old audio element
          this.stopProgressTracking();
          
          // Replace the audio player
          this.audioPlayer.pause();
          this.audioPlayer = newAudio;
          
          // Continue playing if it was playing, or keep paused if it was paused
          if (wasPlaying && !wasPaused) {
            this.audioPlayer.play().catch(error => {
              console.error('Error resuming with full audio:', error);
            });
          } else if (wasPaused) {
            // Make sure the new audio stays paused if the original was paused
            this.audioPlayer.pause();
          }
          
          // Update UI
          if (verseElement) {
            verseElement.classList.remove('loading-ayah-audio');
            verseElement.classList.add('playing-ayah-audio');
          }
          
          // Resume progress tracking with the new audio element
          this.startProgressTracking();
          
          // Set partially loaded state
          this.isPartiallyLoaded = true;
          
          // Reset the partially loaded state after animation completes
          setTimeout(() => {
            this.isPartiallyLoaded = false;
          }, 3100); // Slightly longer than the animation duration (3s)
          
          console.log('Switched to full audio file');
        }, { once: true });
        
        // Load the new audio
        newAudio.load();
        
        // No need for this anymore since we use isPartiallyLoaded
        
      } catch (error) {
        console.error('Error loading rest of audio:', error);
        // Continue with the partial audio, it's better than nothing
      }
    },
    
    togglePause() {
      if (!this.audioPlayer) return
      
      if (this.paused) {
        this.audioPlayer.play().catch(error => {
          console.error('Error resuming audio:', error)
        })
        this.paused = false
      } else {
        this.audioPlayer.pause()
        this.paused = true
      }
    },
    
    stopAudio() {
      if (this.audioPlayer) {
        this.audioPlayer.pause()
        this.audioPlayer.currentTime = 0
        this.audioPlayer = null
      }
      
      // Stop progress tracking
      this.stopProgressTracking()
      
      // Reset progress values
      this.audioProgress = 0
      this.audioDuration = 0
      
      // Clear all state variables
      this.isPlayingFullSurah = false
      this.isPlayingPageAudio = false
      this.paused = false
      this.currentPlayingVerse = null
      
      // Store highlighted ayah before clearing it
      const previousHighlightedAyah = this.highlightedAyah
      
      this.loadingVerseAudio = null
      this.highlightedAyah = null
      this.downloadingSurahAudio = false
      this.downloadingPageAudio = false
      
      // Remove any loading or active classes from elements
      if (previousHighlightedAyah) {
        // Clean up any highlighted or loading ayahs in the page view
        const pageVerseElement = document.getElementById(`page-verse-${previousHighlightedAyah}`)
        if (pageVerseElement) {
          pageVerseElement.classList.remove('loading-ayah-audio')
        }
        
        // Clean up any highlighted or loading verses in the surah view
        const verseElement = document.getElementById(`verse-${previousHighlightedAyah}`)
        if (verseElement) {
          verseElement.classList.remove('loading-ayah-audio')
        }
      }
      
      // Also clean up any other loading ayahs that might be in progress
      const loadingElements = document.querySelectorAll('.loading-ayah-audio')
      loadingElements.forEach(el => {
        el.classList.remove('loading-ayah-audio')
      })
    },

    async loadPage() {
      try {
        this.loadingPage = true
        this.pageError = null
        
        // Stop any playing audio when changing pages
        this.stopAudio()
        
        // Fetch the page content
        const response = await fetch(`http://api.alquran.cloud/v1/page/${this.currentPage}/quran-uthmani`)
        const data = await response.json()
        
        if (data.code === 200) {
          this.currentPageData = data.data
          
          // Create page info text that shows what surahs are in this page
          let surahsInPage = new Set()
          data.data.ayahs.forEach(ayah => {
            if (ayah.surah) {
              surahsInPage.add(ayah.surah.number)
            }
          })
          
          const surahNames = Array.from(surahsInPage).map(surahNumber => {
            const surah = this.surahs.find(s => s.number === surahNumber)
            return surah ? surah.englishName : 'Unknown'
          }).join(', ')
          
          this.currentPageInfo = surahNames
          
          // Load translation for this page if a translation is selected
          await this.loadPageTranslation()
        } else {
          this.pageError = data.status
        }
      } catch (error) {
        console.error('Error fetching page data:', error)
        this.pageError = this.$t('quran.networkError')
      } finally {
        this.loadingPage = false
      }
    },
    
    async loadPageTranslation() {
      if (!this.selectedTranslation) {
        this.pageTranslation = []
        return
      }
      
      try {
        const response = await fetch(`http://api.alquran.cloud/v1/page/${this.currentPage}/${this.selectedTranslation}`)
        const data = await response.json()
        
        if (data.code === 200) {
          this.pageTranslation = data.data.ayahs
        } else {
          console.error('Error loading translation:', data.status)
          this.pageTranslation = []
        }
      } catch (error) {
        console.error('Error fetching page translation:', error)
        this.pageTranslation = []
      }
    },

    async previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--
        await this.loadPage()
      }
    },

    async nextPage() {
      if (this.currentPage < 604) {
        this.currentPage++
        await this.loadPage()
      }
    },

    async goToPage() {
      if (this.jumpToPage >= 1 && this.jumpToPage <= 604) {
        this.currentPage = this.jumpToPage
        await this.loadPage()
      }
    },

    getSurahName(surahNumber) {
      const surah = this.surahs.find(s => s.number === surahNumber)
      return surah ? `${surah.number}. ${surah.englishName} (${surah.name})` : 'Unknown Surah'
    },

    async listenToPage() {
      try {
        this.stopAudio()
        this.downloadingPageAudio = true
        this.highlightedAyah = null
        
        // Get reciter info
        const reciter = this.reciters.find(r => r.identifier === this.selectedReciter)
        if (!reciter) {
          throw new Error('Selected reciter not found')
        }
        
        // We'll need to fetch audio for each surah on this page
        try {
          if (!this.currentPageData || !this.currentPageData.ayahs || this.currentPageData.ayahs.length === 0) {
            throw new Error('No ayahs available on this page')
          }
          
          // Find all the surahs on this page
          const surahsOnPage = new Set()
          this.currentPageData.ayahs.forEach(ayah => {
            if (ayah.surah && ayah.surah.number) {
              surahsOnPage.add(ayah.surah.number)
            }
          })
          
          // Fetch audio data for each surah
          const pageAyahsWithAudio = []
          
          for (const surahNumber of surahsOnPage) {
            console.log(`Fetching audio data for surah ${surahNumber} using ${this.selectedReciter}`)
            const response = await fetch(`http://api.alquran.cloud/v1/surah/${surahNumber}/${this.selectedReciter}`)
            const data = await response.json()
            
            if (data.code === 200 && data.data && data.data.ayahs) {
              // Find all ayahs from this surah that are on the current page
              const pageAyahs = this.currentPageData.ayahs.filter(ayah => 
                ayah.surah && ayah.surah.number === surahNumber
              )
              
              // For each page ayah, find its audio URL from the fetched data
              pageAyahs.forEach(pageAyah => {
                const ayahWithAudio = data.data.ayahs.find(a => a.numberInSurah === pageAyah.numberInSurah)
                if (ayahWithAudio && ayahWithAudio.audio) {
                  pageAyahsWithAudio.push({
                    ...pageAyah,
                    audio: ayahWithAudio.audio
                  })
                }
              })
            }
          }
          
          // Sort the ayahs by their global number to ensure correct playback order
          this.pageAyahsAudio = pageAyahsWithAudio.sort((a, b) => a.number - b.number)
          
          this.downloadingPageAudio = false
          
          if (this.pageAyahsAudio.length > 0) {
            this.$notification.info(this.$t('quran.playingVerseByVerse'))
            this.playPageAyahsSequentially()
          } else {
            throw new Error('No audio available for ayahs on this page')
          }
        } catch (error) {
          console.error(`Error fetching page audio data: ${error}`)
          this.downloadingPageAudio = false
          this.$notification.error(this.$t('quran.audioNotAvailable'))
        }
      } catch (error) {
        console.error('Error playing page audio:', error)
        this.downloadingPageAudio = false
        this.isPlayingPageAudio = false
        this.$notification.error(this.$t('quran.audioNotAvailable'))
      }
    },
    
    async playPageAyahsSequentially(startIndex = 0) {
      if (!this.pageAyahsAudio || this.pageAyahsAudio.length === 0) {
        console.error('No ayahs with audio available for playback')
        return
      }
      
      this.isPlayingPageAudio = true
      this.paused = false
      
      // For preloading next ayahs
      const preloadedAudio = {}
      
      // Preload function to load next ayah audio
      const preloadNextAyah = async (index) => {
        // Check if we should preload the next ayah
        if (index + 1 < this.pageAyahsAudio.length && this.pageAyahsAudio[index + 1].audio) {
          try {
            // Check if we haven't already preloaded this ayah
            if (!preloadedAudio[index + 1]) {
              console.log(`Preloading page verse ${index + 2}/${this.pageAyahsAudio.length} audio...`)
              
              // Create a new audio element and start loading
              const nextAudio = new Audio()
              
              // Create a promise to track when preloading is complete
              const preloadPromise = new Promise((resolve, reject) => {
                nextAudio.addEventListener('canplaythrough', () => {
                  console.log(`Page verse ${index + 2} audio preloaded successfully`)
                  resolve(nextAudio)
                }, { once: true })
                
                nextAudio.addEventListener('error', (error) => {
                  console.error(`Error preloading page verse ${index + 2} audio:`, error)
                  reject(error)
                }, { once: true })
              })
              
              // Start loading
              nextAudio.src = this.pageAyahsAudio[index + 1].audio
              nextAudio.preload = 'auto'
              
              // Store in preloaded cache
              preloadedAudio[index + 1] = preloadPromise
            }
          } catch (error) {
            console.error(`Error during preloading:`, error)
          }
        }
      }
      
      try {
        // Play function that will recursively go through the queue
        const playNext = async (index = 0) => {
          if (index >= this.pageAyahsAudio.length || !this.isPlayingPageAudio) {
            this.isPlayingPageAudio = false
            this.highlightedAyah = null
            return
          }
          
          try {
            const currentAyah = this.pageAyahsAudio[index]
            
            // Highlight the current verse being played
            this.highlightedAyah = currentAyah.number
            
            // Scroll to the verse being played
            const verseElement = document.getElementById(`page-verse-${currentAyah.number}`)
            if (verseElement) {
              // Add loading indicator class
              verseElement.classList.add('loading-ayah-audio')
              
              // Scroll element into view with smooth scrolling
              verseElement.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center',
                inline: 'center'
              })
              
              // Show notification with current ayah number
              this.$notification.info(
                this.$t('quran.playingAyah', {
                  current: index + 1,
                  total: this.pageAyahsAudio.length
                })
              )
            }
            
            // Get the audio URL from the ayah data
            if (currentAyah.audio) {
              console.log(`Playing verse ${index + 1}/${this.pageAyahsAudio.length} (Surah ${currentAyah.surah.number}:${currentAyah.numberInSurah})`)
              
              // Try to use preloaded audio if available
              if (preloadedAudio[index]) {
                try {
                  this.audioPlayer = await preloadedAudio[index]
                  console.log(`Using preloaded audio for verse ${index + 1}`)
                } catch (error) {
                  // If preloaded audio fails, create a new one
                  console.warn(`Preloaded audio failed, creating new audio for verse ${index + 1}`)
                  this.audioPlayer = new Audio(currentAyah.audio)
                }
              } else {
                // No preloaded audio, create a new one
                this.audioPlayer = new Audio(currentAyah.audio)
              }
              
              // Start preloading the next ayah in the background
              preloadNextAyah(index)
              
              // Set up event listeners
              this.audioPlayer.addEventListener('canplaythrough', () => {
                // Remove loading class when audio is ready to play
                if (verseElement) {
                  verseElement.classList.remove('loading-ayah-audio')
                }
              }, { once: true })
              
              this.audioPlayer.addEventListener('ended', () => {
                // Play next verse when this one ends
                if (this.isPlayingPageAudio && !this.paused) {
                  playNext(index + 1)
                }
              })
              
              this.audioPlayer.addEventListener('error', (error) => {
                console.error(`Error playing verse ${index + 1} audio: ${error}`)
                // Remove loading indicator
                if (verseElement) {
                  verseElement.classList.remove('loading-ayah-audio')
                }
                // Skip to next verse if this one fails
                playNext(index + 1)
              })
              
              // Play the audio (it might already be loaded if preloaded)
              if (this.audioPlayer.readyState >= 3) {
                // Audio is already loaded, just play
                await this.audioPlayer.play()
              } else {
                // Audio isn't loaded yet, set up an event to play once loaded
                this.audioPlayer.addEventListener('canplaythrough', async () => {
                  try {
                    await this.audioPlayer.play()
                  } catch (error) {
                    console.error(`Error starting playback after load: ${error}`)
                    playNext(index + 1)
                  }
                }, { once: true })
              }
            } else {
              console.error(`No audio available for verse ${index + 1}`)
              // Remove loading indicator
              if (verseElement) {
                verseElement.classList.remove('loading-ayah-audio')
              }
              // Skip to next verse if this one has no audio
              playNext(index + 1)
            }
          } catch (error) {
            console.error(`Error playing verse ${index + 1}:`, error)
            
            // Clean up any pending loading indicators
            const currentAyah = this.pageAyahsAudio[index]
            if (currentAyah) {
              const verseElement = document.getElementById(`page-verse-${currentAyah.number}`)
              if (verseElement) {
                verseElement.classList.remove('loading-ayah-audio')
              }
            }
            
            // Skip to next verse if this one fails
            playNext(index + 1)
          }
        }
        
        // Start playing from the specified index
        playNext(startIndex)
        
      } catch (error) {
        console.error('Error in page ayahs playback:', error)
        this.isPlayingPageAudio = false
        this.highlightedAyah = null
        this.$notification.error(this.$t('quran.audioNotAvailable'))
      }
    },
    
    async playPageVerseAudio(verseNumber, surahNumber, verseNumberInSurah) {
      // Stop any currently playing audio
      this.stopAudio()
      
      try {
        this.loadingVerseAudio = verseNumber
        this.highlightedAyah = verseNumber
        
        // Reset progress tracking
        this.audioProgress = 0
        this.audioDuration = 0
        
        // Get reciter info
        const reciter = this.reciters.find(r => r.identifier === this.selectedReciter)
        if (!reciter) {
          throw new Error('Selected reciter not found')
        }
        
        // Use the API to get the audio data for this specific ayah
        try {
          // Add loading class to the verse
          const verseElement = document.getElementById(`page-verse-${verseNumber}`)
          if (verseElement) {
            verseElement.classList.add('loading-ayah-audio')
          }
          
          // Fetch the surah data with the selected audio reciter
          console.log(`Fetching audio data for surah ${surahNumber} ayah ${verseNumberInSurah} using ${this.selectedReciter}`)
          const response = await fetch(`http://api.alquran.cloud/v1/surah/${surahNumber}/${this.selectedReciter}`)
          const data = await response.json()
          
          if (data.code === 200 && data.data && data.data.ayahs) {
            // Find the specific ayah
            const ayah = data.data.ayahs.find(a => a.numberInSurah === verseNumberInSurah)
            
            // Also find adjacent ayahs for preloading
            const prevAyah = data.data.ayahs.find(a => a.numberInSurah === verseNumberInSurah - 1)
            const nextAyah = data.data.ayahs.find(a => a.numberInSurah === verseNumberInSurah + 1)
            
            if (ayah && ayah.audio) {
              console.log(`Playing verse ${verseNumberInSurah} from audio URL provided by API`)
              this.audioPlayer = new Audio(ayah.audio)
              
              // Preload adjacent ayahs
              if (nextAyah && nextAyah.audio) {
                setTimeout(() => {
                  console.log(`Preloading next ayah ${verseNumberInSurah + 1}...`)
                  const preloadNext = new Audio()
                  preloadNext.src = nextAyah.audio
                  preloadNext.preload = 'auto'
                }, 500) // Slight delay to prioritize current ayah
              }
              
              if (prevAyah && prevAyah.audio) {
                setTimeout(() => {
                  console.log(`Preloading previous ayah ${verseNumberInSurah - 1}...`)
                  const preloadPrev = new Audio()
                  preloadPrev.src = prevAyah.audio
                  preloadPrev.preload = 'auto'
                }, 1000) // Slight delay to prioritize current and next ayahs
              }
              
              // Set up event listeners
              this.audioPlayer.addEventListener('canplaythrough', () => {
                console.log('Audio loaded successfully')
                // Remove loading class and add partially loaded class
                if (verseElement) {
                  verseElement.classList.remove('loading-ayah-audio')
                }
                
                // Set partially loaded state
                this.isPartiallyLoaded = true
                
                // Reset the partially loaded state after animation completes
                setTimeout(() => {
                  this.isPartiallyLoaded = false
                }, 3100) // Slightly longer than the animation duration (3s)
              }, { once: true })
              
              this.audioPlayer.addEventListener('playing', () => {
                // Add playing class to show it's now playing
                if (verseElement) {
                  verseElement.classList.add('playing-ayah-audio')
                }
                
                // Set this verse as currently playing
                this.currentPlayingVerse = verseNumber
                
                // Start tracking progress
                this.startProgressTracking()
              })
              
              this.audioPlayer.addEventListener('ended', () => {
                this.loadingVerseAudio = null
                this.highlightedAyah = null
                this.currentPlayingVerse = null
                
                // Stop tracking progress
                this.stopProgressTracking()
                
                // Clean up all classes
                if (verseElement) {
                  verseElement.classList.remove('loading-ayah-audio', 'partially-loaded-audio', 'playing-ayah-audio')
                }
                
                // Option: automatically play next ayah after this one ends
                if (this.pageAyahsAudio && this.pageAyahsAudio.length > 0) {
                  const currentIndex = this.pageAyahsAudio.findIndex(a => a.number === verseNumber)
                  if (currentIndex !== -1 && currentIndex < this.pageAyahsAudio.length - 1) {
                    const nextPageAyah = this.pageAyahsAudio[currentIndex + 1]
                    // Uncomment to enable auto-play of next ayah:
                    // this.playPageVerseAudio(nextPageAyah.number, nextPageAyah.surah.number, nextPageAyah.numberInSurah)
                  }
                }
              })
              
              this.audioPlayer.addEventListener('error', (error) => {
                console.error(`Error playing audio: ${error}`)
                this.loadingVerseAudio = null
                this.highlightedAyah = null
                // Remove loading class
                if (verseElement) {
                  verseElement.classList.remove('loading-ayah-audio')
                }
                this.$notification.error(this.$t('quran.audioNotAvailable'))
              })
              
              // Start playing
              await this.audioPlayer.play()
            } else {
              throw new Error('Audio not found for this ayah')
            }
          } else {
            throw new Error(`API error: ${data.status || 'Unknown error'}`)
          }
        } catch (error) {
          console.error(`Error fetching audio data: ${error}`)
          this.loadingVerseAudio = null
          this.highlightedAyah = null
          // Remove loading class from all verses
          const verseElement = document.getElementById(`page-verse-${verseNumber}`)
          if (verseElement) {
            verseElement.classList.remove('loading-ayah-audio')
          }
          this.$notification.error(this.$t('quran.audioNotAvailable'))
        }
      } catch (error) {
        console.error('Error playing verse audio:', error)
        this.loadingVerseAudio = null
        this.highlightedAyah = null
        // Remove loading class from all verses
        const verseElement = document.getElementById(`page-verse-${verseNumber}`)
        if (verseElement) {
          verseElement.classList.remove('loading-ayah-audio')
        }
        this.$notification.error(this.$t('quran.audioNotAvailable'))
      }
    },

    getUniquePageSurahs() {
      if (!this.currentPageData || !this.currentPageData.ayahs || this.currentPageData.ayahs.length === 0) {
        return []
      }
      
      const surahs = new Set()
      this.currentPageData.ayahs.forEach(ayah => {
        if (ayah.surah && ayah.surah.number) {
          surahs.add(ayah.surah.number)
        }
      })
      
      return Array.from(surahs)
    },

    isSurahFirstAyahOnPage(surahNumber) {
      if (!this.currentPageData || !this.currentPageData.ayahs || this.currentPageData.ayahs.length === 0) {
        return false
      }
      
      const firstAyah = this.currentPageData.ayahs.find(ayah => ayah.surah && ayah.surah.number === surahNumber)
      return firstAyah && firstAyah.numberInSurah === 1
    },

    getAyahsForSurah(surahNumber) {
      return this.currentPageData.ayahs
        .filter(ayah => ayah.surah && ayah.surah.number === surahNumber)
        .sort((a, b) => a.numberInSurah - b.numberInSurah)
    },

    // Add new functions to handle Bismillah
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
    
    // Function to extract Bismillah from the first ayah if needed
    extractBismillah() {
      return 'بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ';
    },

    async playVerseByVerse() {
      if (!this.currentSurah || !this.currentSurah.ayahs || this.currentSurah.ayahs.length === 0) {
        return
      }
      
      try {
        // First, fetch the surah data with the selected audio reciter
        console.log(`Fetching audio data for surah ${this.selectedSurah} using ${this.selectedReciter}`)
        const response = await fetch(`http://api.alquran.cloud/v1/surah/${this.selectedSurah}/${this.selectedReciter}`)
        const data = await response.json()
        
        if (data.code === 200 && data.data && data.data.ayahs) {
          // Use the fetched ayahs with audio URLs for playback
          this.playVerseByVerseWithData(data.data.ayahs)
        } else {
          throw new Error(`API error: ${data.status || 'Unknown error'}`)
        }
      } catch (error) {
        console.error(`Error fetching audio data: ${error}`)
        this.isPlayingFullSurah = false
        this.loadingVerseAudio = null
        this.highlightedAyah = null
        this.$notification.error(this.$t('quran.audioNotAvailable'))
      }
    },

    toggleVerseAudio(verseNumber) {
      if (this.currentPlayingVerse === verseNumber) {
        this.togglePause()
      } else {
        this.currentPlayingVerse = verseNumber
        this.playVerseAudio(verseNumber, this.currentSurah.ayahs.find(ayah => ayah.numberInSurah === verseNumber).numberInSurah)
      }
    },
    
    formatTime(seconds) {
      if (isNaN(seconds) || seconds < 0) return '0:00';
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    },
    
    updateAudioProgress() {
      if (this.audioPlayer) {
        this.audioProgress = this.audioPlayer.currentTime;
        this.audioDuration = this.audioPlayer.duration;
      }
    },
    
    startProgressTracking() {
      // Clear any existing interval
      this.stopProgressTracking();
      
      // Start new interval
      this.audioUpdateInterval = setInterval(() => {
        this.updateAudioProgress();
      }, 100); // Update every 100ms for smooth progress bar
    },
    
    stopProgressTracking() {
      if (this.audioUpdateInterval) {
        clearInterval(this.audioUpdateInterval);
        this.audioUpdateInterval = null;
      }
    },

    seekAudio(event) {
      if (!this.audioPlayer || !this.audioDuration) return;
      
      const progressBar = event.currentTarget;
      const rect = progressBar.getBoundingClientRect();
      const offsetX = event.clientX - rect.left;
      const percentage = offsetX / rect.width;
      
      // Set the current time based on the click position
      this.audioPlayer.currentTime = percentage * this.audioDuration;
      
      // Update the progress immediately
      this.updateAudioProgress();
    },

    performSearch() {
      if (!this.searchKeyword.trim()) {
        return;
      }
      
      this.searchLoading = true;
      this.searchError = null;
      this.searchResults = [];
      this.searchCount = 0;
      
      // Encode search keyword with proper URI encoding to handle Arabic characters
      const encodedKeyword = encodeURIComponent(this.searchKeyword.trim());
      
      // Use the selected edition directly - 'ar' is supported by the search API
      const searchEdition = this.searchEdition;
      
      // Construct the API URL
      const apiUrl = `http://api.alquran.cloud/v1/search/${encodedKeyword}/${this.searchSurah}/${searchEdition}`;
      
      console.log(`Searching the Quran: ${apiUrl}`);
      
      fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
          if (data.code === 200 && data.data) {
            // Get all matches from the API
            this.searchResults = data.data.matches || [];
            this.searchCount = this.searchResults.length;
            
            if (this.searchResults.length === 0) {
              this.$notification.info(this.$t('quran.noSearchResults'));
            }
          } else {
            throw new Error(data.status || 'Unknown error');
          }
        })
        .catch(error => {
          console.error('Error searching Quran:', error);
          this.searchError = error.message || this.$t('quran.searchError');
          this.$notification.error(this.searchError);
        })
        .finally(() => {
          this.searchLoading = false;
        });
    },
    
    jumpToSearchResult(match) {
      // Stop any playing audio
      this.stopAudio();
      
      // Check if this is a tafsir result - we can't navigate directly to tafsir sections
      // so we'll just navigate to the verse it's referring to
      if (match.edition && match.edition.type === 'tafsir') {
        this.$notification.info(this.$t('quran.navigatingToVerse'));
      }
      
      // Set the selected surah
      this.selectedSurah = match.surah.number;
      
      // Set the translation appropriately
      if (match.edition && match.edition.identifier) {
        // If it's a tafsir, we'll set the main text to Quran instead
        if (match.edition.type === 'tafsir') {
          this.selectedTranslation = 'ar'; // Default Arabic Quran
        } else {
          this.selectedTranslation = match.edition.identifier;
        }
      }
      
      // Load the surah
      this.loadSurah().then(() => {
        // Wait for the surah to load then scroll to the verse
        this.$nextTick(() => {
          const verseElement = document.getElementById(`verse-${match.number}`);
          if (verseElement) {
            // Highlight the verse
            this.highlightedAyah = match.number;
            
            // Scroll to the verse
            verseElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Add a temporary highlight effect
            verseElement.classList.add('search-highlight');
            setTimeout(() => {
              verseElement.classList.remove('search-highlight');
            }, 3000);
          } else {
            // The verse might not be loaded yet if it's a large surah with lazy loading
            // So we need to load more verses until we find it
            this.loadVersesUntilFound(match.number);
          }
        });
      });
    },
    
    async loadVersesUntilFound(verseNumber) {
      // If the verse is not loaded yet, we need to load more verses
      if (!document.getElementById(`verse-${verseNumber}`)) {
        // Only proceed if there are more verses to load
        if (this.displayedVerses.length < this.currentSurah.ayahs.length) {
          // Load more verses
          await this.loadMoreVerses(50); // Load a larger chunk
          
          // Check again after loading
          this.$nextTick(() => {
            const verseElement = document.getElementById(`verse-${verseNumber}`);
            if (verseElement) {
              // Found the verse, scroll to it
              this.highlightedAyah = verseNumber;
              verseElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
              
              // Add highlight effect
              verseElement.classList.add('search-highlight');
              setTimeout(() => {
                verseElement.classList.remove('search-highlight');
              }, 3000);
            } else {
              // Still not found, try loading more
              this.loadVersesUntilFound(verseNumber);
            }
          });
        }
      }
    },
    
    highlightSearchTerm(text) {
      if (!this.searchKeyword || !text) return text;
      
      // First, make sure we're not dealing with tafsir (explanation) text
      const processedText = this.truncateIfTafsir(text);
      
      // Check if we're searching in Arabic text
      if (this.searchEdition === 'ar' || this.searchEdition === 'quran-uthmani' || 
          this.searchEdition === 'quran-simple' || this.searchEdition.startsWith('ar.')) {
        // For Arabic text, we need to be more careful with highlighting
        // as Arabic has connected characters that shouldn't be broken
        try {
          // Escape special regex characters
          const escapedKeyword = this.searchKeyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
          
          // Create a regular expression to find the keyword (case insensitive)
          const regex = new RegExp(`(${escapedKeyword})`, 'gi');
          
          // Replace matches with highlighted spans, preserving the original text
          return processedText.replace(regex, '<span class="highlight-match">$1</span>');
        } catch (error) {
          console.error('Error highlighting Arabic text:', error);
          return processedText; // Return processed text if there's an error
        }
      } else {
        // For non-Arabic text, use the standard approach
        // Escape special regex characters
        const escapedKeyword = this.searchKeyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        
        // Create a regular expression to find the keyword (case insensitive)
        const regex = new RegExp(`(${escapedKeyword})`, 'gi');
        
        // Replace matches with highlighted spans
        return processedText.replace(regex, '<span class="highlight-match">$1</span>');
      }
    },
    
    truncateIfTafsir(text) {
      // Tafsir (explanation) texts are typically very long
      // Quran verses are usually shorter than 400 characters
      if (text && text.length > 400) {
        // Find the nearest period, question mark, or exclamation point within the first 300 characters
        const matches = text.substring(0, 300).match(/[.?!][^\w]/g);
        if (matches && matches.length > 0) {
          // Find the last occurrence
          const lastIndex = text.substring(0, 300).lastIndexOf(matches[matches.length - 1]) + 1;
          return text.substring(0, lastIndex) + '...';
        }
        // If no proper sentence end found, just truncate at 250 characters
        return text.substring(0, 250) + '...';
      }
      return text;
    },
  },
  beforeDestroy() {
    this.stopAudio();
    
    // Clear any debounce timers
    if (this._scrollDebounceTimer) {
      clearTimeout(this._scrollDebounceTimer);
      this._scrollDebounceTimer = null;
    }
    
    if (this._prefetchTimer) {
      clearTimeout(this._prefetchTimer);
      this._prefetchTimer = null;
    }
  },

  beforeUnmount() {
    this.stopAudio()
    this.stopProgressTracking()
    
    // Clear any debounce timers
    if (this._scrollDebounceTimer) {
      clearTimeout(this._scrollDebounceTimer);
      this._scrollDebounceTimer = null;
    }
    
    if (this._prefetchTimer) {
      clearTimeout(this._prefetchTimer);
      this._prefetchTimer = null;
    }
  }
}
</script>

<style scoped>
.quran-reader {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
}

.quran-container {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.select-input {
  width: 100%;
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background-color: var(--input-bg);
  color: var(--text-color);
  font-size: 0.875rem;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1rem;
}

.audio-button {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.audio-button:hover {
  background-color: var(--primary-hover);
}

.audio-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: var(--primary-color);
}

.error-message {
  margin: 2rem 0;
}

.no-selection {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.surah-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.arabic-title {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  font-family: 'Scheherazade New', serif;
}

.english-title {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.ayah-count {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.bismillah {
  font-family: 'Scheherazade New', serif;
  font-size: 1.5rem;
  margin: 1rem 0;
  text-align: center;
  color: var(--primary-color);
}

.verses {
  line-height: 2;
  max-height: 600px;
  overflow-y: auto;
  padding-right: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: var(--primary-color) var(--bg-light);
}

.verses::-webkit-scrollbar {
  width: 8px;
}

.verses::-webkit-scrollbar-track {
  background: var(--bg-light);
  border-radius: 4px;
}

.verses::-webkit-scrollbar-thumb {
  background-color: var(--primary-color);
  border-radius: 4px;
}

.verse {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.verse-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.verse-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background-color: var(--primary-color);
  color: white;
  border-radius: 50%;
  font-weight: bold;
  margin-right: 0.5rem;
}

.verse-audio-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  color: var(--primary-color);
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.2s;
}

.verse-audio-button:hover {
  color: var(--primary-hover);
}

.verse-audio-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.verse-audio-controls {
  display: flex;
  align-items: center;
}

.verse-arabic {
  font-family: 'Scheherazade New', serif;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  line-height: 2.2;
}

.verse-translation {
  color: var(--text-secondary);
  padding-left: 2.5rem;
  font-size: 1rem;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .quran-container {
    padding: 1rem;
  }
  
  .surah-selection {
    flex-direction: column;
  }
  
  .audio-controls {
    margin-top: 1rem;
  }
  
  .arabic-title {
    font-size: 1.5rem;
  }
  
  .verse-arabic {
    font-size: 1.25rem;
  }
  
  .verse-translation {
    padding-left: 0;
  }
}

/* Add Font for Arabic Text */
@import url('https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;700&display=swap');

optgroup {
  font-weight: bold;
  color: var(--text-secondary);
}

.select-input optgroup option {
  font-weight: normal;
  padding-left: 1rem;
}

.view-mode-switcher {
  margin-bottom: 1rem;
}

.view-mode-button {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.view-mode-button:hover {
  background-color: var(--primary-hover);
}

.view-mode-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.view-mode-button.active {
  background-color: var(--primary-hover);
}

.book-navigation {
  margin-bottom: 1rem;
}

.book-navigation button {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.book-navigation button:hover {
  background-color: var(--primary-hover);
}

.book-navigation button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.page-navigation {
  display: flex;
  align-items: center;
}

.page-navigation button {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.page-navigation button:hover {
  background-color: var(--primary-hover);
}

.page-navigation button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.page-number {
  margin: 0 1rem;
}

.page-jump {
  display: flex;
  align-items: center;
}

.page-input {
  width: 5rem;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background-color: var(--input-bg);
  color: var(--text-color);
  font-size: 0.875rem;
}

.jump-button {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.jump-button:hover {
  background-color: var(--primary-hover);
}

.jump-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.book-content {
  margin-top: 1rem;
}

.book-content .loading-spinner {
  margin-bottom: 1rem;
}

.book-content .error-message {
  margin-bottom: 1rem;
}

.book-content .page-content {
  padding: 1rem;
  background-color: var(--card-bg);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.book-content .page-text {
  line-height: 2;
}

.book-content .page-verse {
  margin-bottom: 1rem;
}

.book-content .arabic-verse {
  font-family: 'Scheherazade New', serif;
  font-size: 1.5rem;
  margin-right: 0.5rem;
}

.book-content .verse-number {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.book-content .surah-header-in-page {
  margin-bottom: 1rem;
}

.book-content .surah-name {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.book-content .bismillah {
  font-family: 'Scheherazade New', serif;
  font-size: 1.5rem;
  margin: 1rem 0;
  text-align: center;
  color: var(--primary-color);
}

.book-content .page-translation {
  margin-top: 1rem;
}

.book-content .translation-verse {
  margin-bottom: 0.5rem;
}

.book-content .translation-text {
  color: var(--text-secondary);
  padding-left: 1rem;
}

/* Surah group styles */
.surah-group {
  margin-bottom: 1.5rem;
  border-bottom: 1px dashed var(--border-color);
  padding-bottom: 1.5rem;
}

.surah-group:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

/* Continuous book view styles */
.continuous-quran-text {
  font-family: 'Scheherazade New', serif;
  font-size: 1.5rem;
  line-height: 2.5;
  text-align: justify;
  padding: 0.5rem 0;
  margin-bottom: 0.5rem;
}

.ayah-text {
  display: inline;
  position: relative;
  cursor: pointer;
  transition: background-color 0.3s ease;
  padding: 2px 0;
  border-radius: 4px;
}

.ayah-text:hover {
  background-color: rgba(var(--primary-color-rgb), 0.05);
}

.ayah-number {
  font-size: 0.75rem;
  color: var(--primary-color);
  vertical-align: super;
  margin: 0 1px;
  font-family: sans-serif;
}

.active-ayah {
  background-color: rgba(var(--primary-color-rgb), 0.1);
  border-radius: 4px;
  padding: 2px 4px;
  transition: background-color 0.3s ease;
}

.book-content .loading-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 1rem;
  border-radius: 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Add loading indicator for verse audio playback */
.loading-ayah-audio {
  position: relative;
}

.loading-ayah-audio::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(var(--primary-color-rgb), 0.1);
  border-radius: 4px;
  z-index: 1;
  animation: pulse 1.5s infinite;
}

/* Add style for actively playing audio state */
.playing-ayah-audio {
  position: relative;
  background-color: rgba(var(--primary-color-rgb), 0.05);
  border-radius: 4px;
  transition: background-color 0.3s ease;
  pointer-events: auto; /* Ensure clicks are allowed */
}

.playing-ayah-audio::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
  pointer-events: none; /* Allow clicks to pass through */
}

.playing-ayah-audio .verse-arabic,
.playing-ayah-audio .verse-translation {
  color: var(--primary-color);
}

/* Animation for partial loading progress bar */
@keyframes loading-progress {
  0% {
    width: 0%;
    opacity: 0.8;
  }
  20% {
    width: 20%;
    opacity: 0.8;
  }
  60% {
    width: 50%;
    opacity: 0.8;
  }
  100% {
    width: 70%;
    opacity: 0.5;
  }
}

@keyframes pulse {
  0% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.6;
  }
}

/* Surah buttons grid styles */
.surah-buttons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
  gap: 0.5rem;
  max-height: 300px;
  overflow-y: auto;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background-color: var(--bg-light);
}

.surah-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  transition: all 0.2s ease;
  min-height: 70px;
}

.surah-button:hover {
  background-color: var(--hover-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.surah-button.active {
  background-color: var(--primary-light);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.surah-button .surah-number {
  font-weight: bold;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.surah-button .surah-name {
  font-size: 0.75rem;
  text-align: center;
  line-height: 1.2;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Media query for smaller screens */
@media (max-width: 640px) {
  .surah-buttons-grid {
    grid-template-columns: repeat(auto-fill, minmax(70px, 1fr));
  }
  
  .surah-button {
    padding: 0.35rem;
    min-height: 60px;
  }
  
  .surah-button .surah-number {
    font-size: 0.875rem;
  }
  
  .surah-button .surah-name {
    font-size: 0.7rem;
  }
}

.loading-more {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem 0;
  color: var(--text-secondary);
}

.loading-more svg {
  margin-right: 0.5rem;
}

.audio-progress-container {
  display: flex;
  flex-direction: column;
  margin: 0.5rem 0;
  width: 100%;
}

.audio-progress-bar {
  width: 100%;
  height: 0.5rem;
  background-color: var(--bg-light);
  border-radius: 0.25rem;
  overflow: hidden;
  cursor: pointer;
  position: relative;
  margin-bottom: 0.25rem;
  border: 1px solid rgba(var(--primary-color-rgb), 0.1);
  transition: background-color 0.2s ease;
}

.audio-progress-bar:hover {
  background-color: var(--hover-color);
}

.audio-progress-fill {
  height: 100%;
  background-color: var(--primary-color);
  border-radius: 0.25rem;
  transition: width 0.1s linear;
  position: relative;
}

.audio-progress-fill::after {
  content: '';
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 0.5rem;
  height: 0.5rem;
  background-color: var(--primary-dark);
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.audio-progress-bar:hover .audio-progress-fill::after {
  opacity: 1;
}

.audio-time {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-align: right;
}

.book-view .audio-progress-container {
  margin: 0.5rem auto;
  max-width: 90%;
  background-color: rgba(var(--primary-color-rgb), 0.05);
  padding: 0.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.surah-group {
  margin-bottom: 1.5rem;
}

/* Loading indicator for audio progress bar */
.audio-progress-bar.loading::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 0;
  background: linear-gradient(90deg, rgba(var(--primary-color-rgb), 0.1), rgba(var(--primary-color-rgb), 0.3));
  animation: loading-progress 2s ease-in-out forwards;
  z-index: 1;
  pointer-events: none;
  border-radius: 0.25rem;
}

.audio-progress-bar.loading::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 3px;
  background-color: rgba(var(--primary-color-rgb), 0.5);
  animation: buffering-pulse 1.5s infinite;
  z-index: 2;
}

@keyframes buffering-pulse {
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    opacity: 0.5;
  }
}

.verse-loading-progress {
  display: flex;
  flex-direction: column;
  margin-top: 0.5rem;
  padding: 0.5rem;
  background-color: rgba(var(--primary-color-rgb), 0.05);
  border-radius: 0.5rem;
}

.progress-bar {
  height: 0.5rem;
  background-color: var(--primary-color);
  border-radius: 0.25rem;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-align: center;
  margin-top: 0.25rem;
}

.bookmark-icon,
.search-icon {
  fill: var(--primary-color);
}

.bookmark-icon,
.search-icon {
  fill: var(--primary-color);
}

.search-bar-container {
  margin-bottom: 1rem;
}

.search-input-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background-color: var(--input-bg);
  color: var(--text-color);
  font-size: 0.875rem;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  border-color: var(--primary-color);
  outline: none;
}

.search-options-row {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 0.75rem;
  align-items: center;
}

.search-select-container {
  position: relative;
  width: 100%;
}

.search-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  background-color: var(--input-bg);
  color: var(--text-color);
  font-size: 0.875rem;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1rem;
  transition: border-color 0.2s ease;
}

.search-select:focus {
  border-color: var(--primary-color);
  outline: none;
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
  max-height: 350px;
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

.search-result-header .edition-type {
  margin-left: 10px;
  font-size: 0.8em;
  color: #777;
  background-color: #f3f4f6;
  padding: 2px 6px;
  border-radius: 4px;
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

.highlight-match {
  background-color: rgba(var(--primary-color-rgb), 0.15);
  color: var(--primary-color);
  padding: 0 3px;
  border-radius: 4px;
  font-weight: 500;
  display: inline-block; /* Helps with RTL text highlighting */
}

.search-highlight {
  animation: pulse-highlight 2s ease;
}

@keyframes pulse-highlight {
  0%, 100% {
    background-color: transparent;
  }
  50% {
    background-color: rgba(var(--primary-color-rgb), 0.1);
  }
}

/* Media query for smaller screens */
@media (max-width: 640px) {
  .search-options-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .search-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .search-input {
    padding: 0.5rem;
  }
  
  .search-select {
    padding: 0.5rem;
  }
  
  .search-button {
    padding: 0.5rem;
  }
}
</style> 