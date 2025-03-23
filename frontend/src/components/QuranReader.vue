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
        <div v-if="!selectedSurah || !surahListCollapsed" class="surah-selection">
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
            <!-- Surah Header -->
            <div class="surah-header">
              <h2 class="arabic-title">{{ currentSurah.name }}</h2>
              <h3 class="english-title">{{ currentSurah.englishName }} - {{ currentSurah.englishNameTranslation }}</h3>
              <p class="ayah-count">{{ currentSurah.numberOfAyahs }} {{ $t('quran.ayah') }}</p>
              
              <!-- Bismillah except for Surah 9 -->
              <div class="bismillah" v-if="currentSurah.number !== 9">
                {{ $t('quran.bismillah') }}
              </div>
              
              <!-- Audio Controls and Settings -->
              <div class="surah-actions mt-4">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <!-- Language Selection -->
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
                  
                  <!-- Reciter Selection -->
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
                  
                  <!-- Listen to Surah Button -->
                  <div class="flex items-end">
                    <button 
                      @click="listenToFullSurah" 
                      class="listen-surah-button w-full"
                      :disabled="downloadingSurahAudio || isPlayingFullSurah"
                    >
                      <svg v-if="downloadingSurahAudio" class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
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
              :class="['verses', { 'verses-when-collapsed': surahListCollapsed, 'verses-container-expanded': surahListCollapsed }]"
              ref="versesContainer" 
              @scroll="handleScroll"
            >
              <div 
                v-for="verse in displayedVerses" 
                :key="verse.number"
                class="verse"
                :id="`verse-${verse.number}`"
                :class="{ 
                  'highlighted': highlightedAyah === verse.number,
                  'playing-ayah-audio': loadingVerseAudio === verse.number && !isPartiallyLoaded
                }"
              >
                <div class="verse-number">{{ verse.numberInSurah }}</div>
                
                <div class="arabic-text">{{ verse.text }}</div>
                
                <div v-if="translatedVerses[verse.number]" class="translation-text">
                  {{ translatedVerses[verse.number] }}
                </div>
                
                <div class="verse-footer">
                  <div class="verse-actions">
                    <button 
                      @click="toggleVerseAudio(verse.numberInSurah)"
                      class="verse-action-button"
                      :class="{ 'active': currentPlayingVerse === verse.numberInSurah }"
                      :disabled="loadingVerseAudio !== null"
                    >
                      <svg v-if="currentPlayingVerse === verse.numberInSurah && !paused" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- Loading more indicator -->
              <div v-if="isLoadingMore" class="text-center py-4">
                <div class="inline-block animate-spin rounded-full h-5 w-5 border-2 border-indigo-600 border-t-transparent"></div>
                <p class="text-sm text-gray-600 mt-2">{{ $t('quran.loadingMore') || 'جارٍ تحميل المزيد من الآيات...' }}</p>
                
                <!-- Manual load button as a fallback -->
                <button 
                  @click="loadAllRemainingVerses" 
                  class="load-all-button mt-3 px-4 py-2 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 rounded-md text-sm font-medium transition-colors"
                >
                  {{ $t('quran.loadAllVerses') || 'تحميل جميع الآيات دفعة واحدة' }}
                </button>
              </div>
            </div>
            
            <!-- Audio Controls (separate from verses) -->
            <div v-if="audioPlayer && !audioPlayer.paused" class="audio-controls">
              <button @click="stopAudio" class="audio-control-button">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd" />
                </svg>
              </button>
              
              <button @click="togglePause" class="audio-control-button play-pause">
                <svg v-if="paused" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </button>
              
              <div class="audio-time">{{ formatTime(audioProgress) }}</div>
              <div class="audio-progress-container" @click="seekAudio">
                <div class="audio-progress-bar" :style="{ width: `${(audioProgress / audioDuration) * 100}%` }"></div>
              </div>
              <div class="audio-time">{{ formatTime(audioDuration) }}</div>
            </div>
          </div>
          
          <!-- No Surah Selected -->
          <div class="no-selection" v-if="!loading && !error && !selectedSurah">
            <p class="text-center text-gray-500">{{ $t('quran.selectSurahPrompt') }}</p>
          </div>
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
          <!-- Surah Header -->
          <div class="surah-header">
            <h2 class="arabic-title">{{ currentSurah.name }}</h2>
            <h3 class="english-title">{{ currentSurah.englishName }} - {{ currentSurah.englishNameTranslation }}</h3>
            <p class="ayah-count">{{ currentSurah.numberOfAyahs }} {{ $t('quran.ayah') }}</p>
            
            <!-- Bismillah except for Surah 9 -->
            <div class="bismillah" v-if="currentSurah.number !== 9">
              {{ $t('quran.bismillah') }}
            </div>
            
            <!-- Audio Controls and Settings -->
            <div class="surah-actions mt-4">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                <!-- Language Selection -->
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
                
                <!-- Reciter Selection -->
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
                
                <!-- Listen to Surah Button -->
                <div class="flex items-end">
                  <button 
                    @click="listenToFullSurah" 
                    class="listen-surah-button w-full"
                    :disabled="downloadingSurahAudio || isPlayingFullSurah"
                  >
                    <svg v-if="downloadingSurahAudio" class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
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
            :class="['verses', { 'verses-when-collapsed': surahListCollapsed, 'verses-container-expanded': surahListCollapsed }]"
            ref="versesContainer" 
            @scroll="handleScroll"
          >
            <div 
              v-for="verse in displayedVerses" 
              :key="verse.number"
              class="verse"
              :id="`verse-${verse.number}`"
              :class="{ 
                'highlighted': highlightedAyah === verse.number,
                'playing-ayah-audio': loadingVerseAudio === verse.number && !isPartiallyLoaded
              }"
            >
              <div class="verse-number">{{ verse.numberInSurah }}</div>
              
              <div class="arabic-text">{{ verse.text }}</div>
              
              <div v-if="translatedVerses[verse.number]" class="translation-text">
                {{ translatedVerses[verse.number] }}
              </div>
              
              <div class="verse-footer">
                <div class="verse-actions">
                  <button 
                    @click="toggleVerseAudio(verse.numberInSurah)"
                    class="verse-action-button"
                    :class="{ 'active': currentPlayingVerse === verse.numberInSurah }"
                    :disabled="loadingVerseAudio !== null"
                  >
                    <svg v-if="currentPlayingVerse === verse.numberInSurah && !paused" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Loading more indicator -->
            <div v-if="isLoadingMore" class="text-center py-4">
              <div class="inline-block animate-spin rounded-full h-5 w-5 border-2 border-indigo-600 border-t-transparent"></div>
              <p class="text-sm text-gray-600 mt-2">{{ $t('quran.loadingMore') || 'جارٍ تحميل المزيد من الآيات...' }}</p>
              
              <!-- Manual load button as a fallback -->
              <button 
                @click="loadAllRemainingVerses" 
                class="load-all-button mt-3 px-4 py-2 bg-indigo-100 hover:bg-indigo-200 text-indigo-700 rounded-md text-sm font-medium transition-colors"
              >
                {{ $t('quran.loadAllVerses') || 'تحميل جميع الآيات دفعة واحدة' }}
              </button>
            </div>
          </div>
          
          <!-- Audio Controls (separate from verses) -->
          <div v-if="audioPlayer && !audioPlayer.paused" class="audio-controls">
            <button @click="stopAudio" class="audio-control-button">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd" />
              </svg>
            </button>
            
            <button @click="togglePause" class="audio-control-button play-pause">
              <svg v-if="paused" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </button>
            
            <div class="audio-time">{{ formatTime(audioProgress) }}</div>
            <div class="audio-progress-container" @click="seekAudio">
              <div class="audio-progress-bar" :style="{ width: `${(audioProgress / audioDuration) * 100}%` }"></div>
            </div>
            <div class="audio-time">{{ formatTime(audioDuration) }}</div>
          </div>
        </div>
        
        <!-- No Surah Selected -->
        <div class="no-selection" v-if="!loading && !error && !selectedSurah">
          <p class="text-center text-gray-500">{{ $t('quran.selectSurahPrompt') }}</p>
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
  
  <!-- Floating Audio Controls Bar - fixed at bottom of screen -->
  <div v-if="audioPlayer && !audioPlayer.paused" class="floating-audio-controls">
    <div class="audio-controls-container">
      <button @click="stopAudio" class="audio-control-button">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd" />
        </svg>
      </button>
      
      <button @click="togglePause" class="audio-control-button play-pause">
        <svg v-if="paused" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
      </button>
      
      <div class="audio-progress-wrapper">
        <div class="audio-time">{{ formatTime(audioProgress) }}</div>
        <div class="audio-progress-container" @click="seekAudio">
          <div class="audio-progress-bar" :style="{ width: `${(audioProgress / audioDuration) * 100}%` }"></div>
        </div>
        <div class="audio-time">{{ formatTime(audioDuration) }}</div>
      </div>
      
      <div class="now-playing-info">
        <span v-if="currentSurah">{{ currentSurah.name }} - {{ $t('quran.surah') }}</span>
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
      selectedSurah: '',
      currentSurah: null,
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
      loadThreshold: 300, // Distance from bottom to trigger loading more verses
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
      searchError: null,
      _loadAttempts: 0,
      // Surah list collapse state
      surahListCollapsed: false,
      backupLoadTimer: null
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
            
            console.log('Found navigation target in localStorage:', navTarget)
          } else {
            console.log('Found navigation data but it was stale, ignoring')
            localStorage.removeItem('quranNavigationTarget')
          }
        } else {
          // Check URL query parameters as fallback
          const urlParams = new URLSearchParams(window.location.search)
          if (urlParams.has('surah') && urlParams.has('verse')) {
            targetSurah = parseInt(urlParams.get('surah'))
            targetVerse = parseInt(urlParams.get('verse'))
            console.log('Found navigation target in URL params:', { surah: targetSurah, verse: targetVerse })
          }
        }
      } catch (e) {
        console.error('Error parsing navigation data:', e)
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
        console.log('Navigating to surah:', targetSurah, 'verse:', targetVerse)
        this.selectedSurah = targetSurah
        if (targetEdition) {
          this.selectedTranslation = targetEdition
        }
        
        try {
          // Load the surah
          await this.loadSurah()
          
          // After the surah is loaded, find and scroll to the verse
          // Use setTimeout to ensure the DOM is fully updated after loadSurah completes
          setTimeout(() => {
            try {
              console.log('Looking for verse element:', targetVerse)
              // Use our helper method to find the verse element
              const verseElement = this.findVerseElement(targetVerse)
              
              if (verseElement) {
                console.log('Found verse element, scrolling to it')
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
                console.log('Verse element not found immediately, trying to load more verses')
                // The verse might not be loaded yet if it's in a large surah with lazy loading
                this.loadVersesUntilFound(targetVerse)
              }
            } catch (scrollError) {
              console.error('Error scrolling to verse:', scrollError)
            }
          }, 500) // Giving it a little more time to ensure DOM updates
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
        
        // Auto-collapse the surah list when loading a new surah
        this.surahListCollapsed = true;
        
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
      if (!this.currentSurah || !this.currentSurah.ayahs || !Array.isArray(this.currentSurah.ayahs)) {
        console.error('Cannot load initial verses: Invalid surah data')
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
        console.log(`Loading all ${this.currentSurah.ayahs.length} verses at once (small surah)`)
        this.displayedVerses = this.currentSurah.ayahs
        this.isLoadingMore = false
        this.loadingChunks = false
        
        // Tag all verse elements with proper IDs
        setTimeout(() => {
          this.tagVerseElementsWithIds(0, this.currentSurah.ayahs.length - 1)
          this.checkAndResetLoadingState()
        }, 100)
        
        return
      }
      
      console.log(`Loading initial ${initialSize} verses of ${this.currentSurah.ayahs.length} total verses`)
      
      // Load first chunk immediately without delay for better UX
      this.displayedVerses = this.currentSurah.ayahs.slice(0, initialSize)
      
      // Tag the loaded verse elements with IDs
      setTimeout(() => {
        this.tagVerseElementsWithIds(0, initialSize - 1)
      }, 100)
      
      // If there are more verses, set up loading indicator and prepare to load more
      if (initialSize < this.currentSurah.ayahs.length) {
        this.isLoadingMore = true
        
        // Schedule loading of next chunk after a short delay
        setTimeout(() => {
          if (this.isLoadingMore) {  // Double-check we still need to load more
            this.loadMoreVerses(this.verseChunkSize)
              .then(() => {
                // After loading more verses, check if we need to reset loading state
                this.checkAndResetLoadingState()
              })
              .catch(error => {
                console.error('Error loading more verses:', error)
                this.isLoadingMore = false
                this.loadingChunks = false
              })
          }
        }, 100)
        
        // Set up a backup mechanism that loads all verses if lazy loading is stuck
        this.setupAutoLoadBackup()
      } else {
        // All verses are loaded, make sure loading state is reset
        this.isLoadingMore = false
        this.loadingChunks = false
        this.checkAndResetLoadingState()
      }
    },
    
    // Setup a backup mechanism to load all verses if scrolling doesn't work
    setupAutoLoadBackup() {
      // Clear any previous backup timer
      if (this.backupLoadTimer) {
        clearTimeout(this.backupLoadTimer)
      }
      
      // Set a timer that will load all verses if scrolling hasn't triggered loading after a delay
      this.backupLoadTimer = setTimeout(() => {
        // Check if we still have verses to load but lazy loading appears stuck
        if (this.displayedVerses && 
            this.currentSurah?.ayahs &&
            this.displayedVerses.length < this.currentSurah.ayahs.length &&
            this.displayedVerses.length < 50) { // Only for cases when very few verses have loaded
          
          console.log('Backup solution: Loading all remaining verses since lazy loading appears stuck');
          
          // Force loading of all remaining verses
          this.loadAllRemainingVerses()
        }
      }, 10000) // Wait 10 seconds before activating backup
    },
    
    // Method to force load all remaining verses if lazy loading isn't working
    loadAllRemainingVerses() {
      // Only proceed if we actually have a surah and verses to load
      if (!this.currentSurah?.ayahs || !Array.isArray(this.currentSurah.ayahs)) {
        console.error('Cannot load all verses: Invalid surah data');
        return Promise.resolve('Invalid surah data');
      }
      
      // Ensure displayedVerses is initialized
      if (!this.displayedVerses || !Array.isArray(this.displayedVerses)) {
        this.displayedVerses = [];
      }
      
      // If all verses are already loaded, do nothing
      if (this.displayedVerses.length >= this.currentSurah.ayahs.length) {
        console.log('All verses already loaded, nothing to do');
        this.isLoadingMore = false;
        this.loadingChunks = false;
        return Promise.resolve('All verses already loaded');
      }
      
      return new Promise((resolve, reject) => {
        try {
          console.log(`Loading all remaining verses (${this.currentSurah.ayahs.length - this.displayedVerses.length} verses)`);
          
          // Set loading state
          this.loadingChunks = true;
          this.isLoadingMore = true;
          
          // For large surahs, load in chunks to prevent UI freezing
          if (this.currentSurah.ayahs.length > 200) {
            // Load in chunks of 50 verses with small delays between
            this.loadInProgressiveChunks(resolve, reject, null, 50);
          } else {
            // For smaller surahs, load all at once
            // Directly load all verses
            this.displayedVerses = [...this.currentSurah.ayahs];
            
            // Reset loading state
            this.loadingChunks = false;
            this.isLoadingMore = false;
            
            // Tag all verse elements
            setTimeout(() => {
              this.tagVerseElementsWithIds(0, this.currentSurah.ayahs.length - 1);
            }, 100);
            
            resolve('All verses loaded successfully');
          }
        } catch (error) {
          console.error('Error loading all verses:', error);
          this.loadingChunks = false;
          this.isLoadingMore = false;
          reject(error);
        }
      });
    },
    
    // Load verses in progressive chunks to prevent UI freezing for large surahs
    loadInProgressiveChunks(resolve, reject, startIndex = null, chunkSize = 50) {
      try {
        // Start loading from the current displayedVerses length
        const currentIndex = startIndex !== null ? startIndex : this.displayedVerses.length;
        
        // If we've loaded all verses, we're done
        if (currentIndex >= this.currentSurah.ayahs.length) {
          console.log('Finished loading all verses in progressive chunks');
          this.loadingChunks = false;
          this.isLoadingMore = false;
          resolve('All verses loaded successfully');
          return;
        }
        
        // Calculate the end index for this chunk
        const endIndex = Math.min(currentIndex + chunkSize, this.currentSurah.ayahs.length);
        console.log(`Loading progressive chunk from ${currentIndex} to ${endIndex}`);
        
        // Get the next chunk of verses
        const nextChunk = this.currentSurah.ayahs.slice(currentIndex, endIndex);
        
        // Add to displayed verses
        this.displayedVerses = [...this.displayedVerses, ...nextChunk];
        
        // Tag the new verse elements
        setTimeout(() => {
          this.tagVerseElementsWithIds(currentIndex, endIndex - 1);
          
          // Recursively load the next chunk after a short delay
          setTimeout(() => {
            this.loadInProgressiveChunks(resolve, reject, endIndex, chunkSize);
          }, 100);
        }, 50);
      } catch (error) {
        console.error('Error loading verses in progressive chunks:', error);
        this.loadingChunks = false;
        this.isLoadingMore = false;
        reject(error);
      }
    },
    
    loadMoreVerses(chunkSize = null, targetVerseNumber = null) {
      // Check for valid state in a more robust way
      if (this.loadingChunks) {
        console.log('Already loading chunks, skipping new request')
        return Promise.resolve('Already loading chunks')
      }
      
      if (!this.currentSurah) {
        console.error('No current surah loaded, cannot load more verses')
        return Promise.resolve('No surah loaded')
      }
      
      if (!this.currentSurah.ayahs || !Array.isArray(this.currentSurah.ayahs)) {
        console.error('Current surah has no valid ayahs array')
        return Promise.resolve('No valid ayahs array')
      }

      return new Promise((resolve, reject) => {
        this.loadingChunks = true
        this.isLoadingMore = true
        
        // Determine start index for next chunk
        const startIndex = this.displayedVerses?.length || 0
        
        // Debug information to help diagnose issues
        console.log('LoadMoreVerses current state:', {
          startIndex,
          totalAyahs: this.currentSurah.ayahs.length,
          displayedVersesLength: this.displayedVerses?.length || 0,
          displayedVersesValid: Array.isArray(this.displayedVerses)
        });
        
        // If all verses are already loaded, do nothing
        if (startIndex >= this.currentSurah.ayahs.length) {
          console.log('All verses already loaded, resetting loading state')
          this.isLoadingMore = false
          this.loadingChunks = false
          resolve('All verses already loaded')
          return
        }
        
        // Use provided chunkSize or default to verseChunkSize
        let actualChunkSize = chunkSize || this.verseChunkSize
        
        // Calculate end index for next chunk
        const endIndex = Math.min(startIndex + actualChunkSize, this.currentSurah.ayahs.length)
        
        console.log(`Loading verses ${startIndex+1} to ${endIndex} of ${this.currentSurah.ayahs.length} (chunk size: ${actualChunkSize})`)
        
        // Force the loading indicator to be visible before loading verses
        this.$nextTick(() => {
          // Use setTimeout to ensure the UI updates before heavy processing
          setTimeout(() => {
            try {
              // Verify the arrays are valid
              if (!Array.isArray(this.currentSurah.ayahs)) {
                throw new Error('currentSurah.ayahs is not an array');
              }
              
              // Add next chunk of verses to displayed verses
              const nextChunk = this.currentSurah.ayahs.slice(startIndex, endIndex)
              
              if (!nextChunk || nextChunk.length === 0) {
                console.error('Failed to get next chunk of verses', {
                  startIndex,
                  endIndex,
                  currentSurahLength: this.currentSurah.ayahs.length
                });
                throw new Error('Failed to get next chunk of verses');
              }
              
              console.log(`Successfully sliced ${nextChunk.length} verses from ayahs array`);
              
              // Initialize displayedVerses if it's undefined
              if (!this.displayedVerses || !Array.isArray(this.displayedVerses)) {
                console.log('Initializing displayedVerses as empty array');
                this.displayedVerses = []
              }
              
              // Update displayed verses with defensive copy
              const updatedVerses = [...this.displayedVerses, ...nextChunk];
              console.log(`Preparing to update displayedVerses from ${this.displayedVerses.length} to ${updatedVerses.length} verses`);
              
              // Directly assign the new array
              this.displayedVerses = updatedVerses;
              
              console.log(`DisplayedVerses updated to ${this.displayedVerses.length} verses`);
              
              // Wait for next tick to ensure Vue updates the DOM
              this.$nextTick(() => {
                // Verify the update happened
                console.log(`After nextTick, displayedVerses has ${this.displayedVerses.length} verses`);
                
                // Tag the new verse elements with IDs
                this.tagVerseElementsWithIds(startIndex, endIndex - 1)
                
                // Resolve the promise after a small delay to ensure the DOM has updated
                setTimeout(() => {
                  // Reset loading states only after DOM has updated
                  this.loadingChunks = false
                  // Only set isLoadingMore to false if we've loaded all verses
                  this.isLoadingMore = endIndex < this.currentSurah.ayahs.length
                  
                  console.log(`Loading complete. isLoadingMore: ${this.isLoadingMore}, loadingChunks: ${this.loadingChunks}`);
                  
                  resolve({
                    startIndex,
                    endIndex,
                    loadedCount: nextChunk.length,
                    totalLoaded: this.displayedVerses.length,
                    total: this.currentSurah.ayahs.length
                  })
                }, 100)
              })
            } catch (error) {
              console.error('Error loading verse chunk:', error)
              
              // Reset the loading state so we can try again
              this.loadingChunks = false
              
              // Don't reset isLoadingMore immediately to avoid UI flicker
              setTimeout(() => {
                if (this.loadingChunks === false) {
                  this.isLoadingMore = false
                }
              }, 1000) // Give time for potential retries
              
              reject(error)
            }
          }, 50) // Short delay to ensure loading indicator appears
        })
      })
    },
    
    // Method to tag verse elements with proper IDs for easier finding
    tagVerseElementsWithIds(startIndex, endIndex) {
      console.log(`Tagging verse elements with IDs from index ${startIndex} to ${endIndex}`)
      
      if (!this.displayedVerses || !Array.isArray(this.displayedVerses)) {
        console.warn('No displayed verses to tag')
        return
      }
      
      try {
        // First try to identify verse elements by their class and position
        const verseContainers = document.querySelectorAll('.verse, .ayah, .quran-verse, .verse-container')
        if (verseContainers.length > 0) {
          // This assumes the verses are in the same order in the DOM as they are in displayedVerses
          for (let i = startIndex; i <= endIndex && i < this.displayedVerses.length; i++) {
            if (i < verseContainers.length) {
              const verse = this.displayedVerses[i]
              const verseNumber = verse.numberInSurah || (verse.number ? parseInt(verse.number.split('_')[1]) : null)
              
              if (verseNumber) {
                // Add ID and data attributes to verse container
                const container = verseContainers[i]
                
                // Only add if it doesn't already have an ID
                if (!container.id) {
                  container.id = `verse-${verseNumber}`
                }
                
                // Add data attributes for easier finding
                container.setAttribute('data-verse-number', verseNumber)
                container.setAttribute('data-surah', this.selectedSurah)
                container.setAttribute('data-verse-index', i)
                
                // Add a specific class for verification
                container.classList.add('tagged-verse')
                
                // Also tag any verse number elements within the container
                const numberElements = container.querySelectorAll('.verse-number, .ayah-number')
                numberElements.forEach(numEl => {
                  numEl.setAttribute('data-verse-number', verseNumber)
                })
                
                console.log(`Tagged verse element with ID verse-${verseNumber}`)
              }
            }
          }
        }
        
        // Also try to find verse elements by their content
        for (let i = startIndex; i <= endIndex && i < this.displayedVerses.length; i++) {
          const verse = this.displayedVerses[i]
          const verseNumber = verse.numberInSurah || (verse.number ? parseInt(verse.number.split('_')[1]) : null)
          
          if (verseNumber && verse.text) {
            // Look for elements containing the verse text
            const textSnippet = verse.text.substring(0, Math.min(30, verse.text.length))
            
            // Use XPath to find elements containing this text more efficiently
            const xpathResult = document.evaluate(
              `//*[contains(text(), "${textSnippet.replace(/"/g, '\\"')}")]`,
              document,
              null,
              XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
              null
            )
            
            for (let j = 0; j < xpathResult.snapshotLength; j++) {
              const textElement = xpathResult.snapshotItem(j)
              const container = textElement.closest('.verse') || textElement.closest('.ayah') || 
                               textElement.closest('.verse-container') || textElement.parentElement
              
              if (container && !container.id) {
                container.id = `verse-${verseNumber}`
                container.setAttribute('data-verse-number', verseNumber)
                container.setAttribute('data-surah', this.selectedSurah)
                container.setAttribute('data-verse-index', i)
                container.classList.add('tagged-verse')
                
                console.log(`Tagged verse element with ID verse-${verseNumber} via text content`)
              }
            }
          }
        }
      } catch (error) {
        console.error('Error tagging verse elements:', error)
      }
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
      // Don't handle scroll events when no current surah
      if (!this.currentSurah) return;
      
      // Check if we have more verses to load
      const hasMoreVersesToLoad = this.displayedVerses && 
                                 this.currentSurah.ayahs && 
                                 this.displayedVerses.length < this.currentSurah.ayahs.length;
      
      // If no more verses to load, reset loading state and exit
      if (!hasMoreVersesToLoad) {
        if (this.isLoadingMore) {
          console.log('All verses loaded, resetting loading indicators');
          this.isLoadingMore = false;
          this.loadingChunks = false;
        }
        return;
      }
      
      // Ignore scroll events if we're already loading
      if (this.loadingChunks) {
        console.log('Already loading chunks, ignoring scroll event');
        return;
      }
      
      const container = event.target;
      const scrollHeight = container.scrollHeight;
      const scrollTop = container.scrollTop;
      const clientHeight = container.clientHeight;
      
      // Calculate the distance from the bottom
      const distanceFromBottom = scrollHeight - scrollTop - clientHeight;
      
      // Force detection of very small containers
      const isNearBottom = distanceFromBottom < this.loadThreshold || 
                          (scrollHeight <= clientHeight * 1.5 && scrollTop > 0);
      
      // Log detailed scrolling info for debugging
      console.log(`Scroll event - distanceFromBottom: ${distanceFromBottom}px, threshold: ${this.loadThreshold}px, isNearBottom: ${isNearBottom}`);
      console.log(`Container metrics - scrollHeight: ${scrollHeight}px, scrollTop: ${scrollTop}px, clientHeight: ${clientHeight}px`);
      console.log(`Displayed verses: ${this.displayedVerses?.length || 0}/${this.currentSurah.ayahs?.length || 0}`);
      
      // If we've reached near the bottom and have more verses to load
      if (isNearBottom) {
        console.log('Bottom threshold reached, loading more verses...');
        
        // Load more verses when scrolling near the bottom
        this.loadMoreVerses()
          .then((result) => {
            console.log('Loaded more verses successfully:', result);
            
            // Check if we need to load even more (for small screens)
            setTimeout(() => {
              // Get updated container dimensions after new content has rendered
              const newScrollHeight = container.scrollHeight;
              const newClientHeight = container.clientHeight;
              const stillHasMoreToLoad = this.displayedVerses?.length < this.currentSurah.ayahs?.length;
              
              // If the container isn't scrollable yet (or barely scrollable) and we have more to load
              if (stillHasMoreToLoad && (newScrollHeight <= newClientHeight * 1.2)) {
                console.log('Container needs more content, loading additional verses...');
                this.loadMoreVerses();
              }
            }, 300);
          })
          .catch(error => {
            console.error('Error loading more verses on scroll:', error);
            
            // Reset loading state after error
            setTimeout(() => {
              if (this.loadingChunks) {
                console.log('Resetting stuck loading state after error');
                this.loadingChunks = false;
                this.isLoadingMore = false;
              }
            }, 3000);
            
            // Try again after a delay if it failed
            setTimeout(() => {
              // Only retry if we're not already loading and still have more to load
              if (!this.loadingChunks && this.displayedVerses?.length < this.currentSurah.ayahs?.length) {
                console.log('Retrying verse loading after previous failure');
                this.loadMoreVerses();
              }
            }, 5000);
          });
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
          
          // Use more robust error handling for fetching
          const response = await fetch(`http://api.alquran.cloud/v1/surah/${this.selectedSurah}/${this.selectedReciter}`)
            .catch(error => {
              console.error(`Network error fetching surah data: ${error.message}`);
              throw new Error(`Network error: ${error.message}`);
            });
          
          if (!response.ok) {
            console.error(`API returned error status: ${response.status}`);
            throw new Error(`API error: ${response.status}`);
          }
          
          const data = await response.json()
            .catch(error => {
              console.error(`Error parsing API response: ${error.message}`);
              throw new Error(`Invalid API response: ${error.message}`);
            });
          
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
                console.log(`Playing full surah audio from URL provided by API: ${fullSurahAudio}`)
                
                // Create audio with progressive loading for full surah
                this.audioPlayer = new Audio()
                
                // Start tracking progress for controls visibility immediately
                this.startProgressTracking()
                
                // Set up event listeners for progressive loading
                this.audioPlayer.addEventListener('canplay', () => {
                  console.log('Full surah audio has buffered enough to begin playback')
                  // Start playing as soon as we have enough data
                  this.audioPlayer.play().catch(error => {
                    console.error('Error starting full surah playback:', error)
                    // If there's an error starting playback, fall back to verse-by-verse
                    this.$notification.warning(this.$t('quran.tryingVerseByVerse'))
                    this.playVerseByVerseWithData(data.data.ayahs)
                  })
                  this.isPlayingFullSurah = true
                  this.paused = false
                  
                  // Set current playing verse to first verse of surah
                  this.currentPlayingVerse = 1
                  
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
                
                // Set a timeout to fall back if loading takes too long
                const loadingTimeout = setTimeout(() => {
                  if (this.downloadingSurahAudio) {
                    console.warn('Loading full surah audio timed out, falling back to verse-by-verse')
                    this.$notification.warning(this.$t('quran.tryingVerseByVerse'))
                    if (this.audioPlayer) {
                      this.audioPlayer.removeAttribute('src')
                      this.audioPlayer.load()
                    }
                    this.downloadingSurahAudio = false
                    this.playVerseByVerseWithData(data.data.ayahs)
                  }
                }, 8000) // 8 second timeout
                
                // Start loading the audio (will trigger canplay when ready)
                this.audioPlayer.preload = 'auto'
                this.audioPlayer.src = fullSurahAudio
                // Show loading indication while waiting for canplay event
                this.downloadingSurahAudio = true
                
                // Clean up the timeout if audio loads or errors out
                this.audioPlayer.addEventListener('canplay', () => {
                  clearTimeout(loadingTimeout)
                }, { once: true })
                
                this.audioPlayer.addEventListener('error', () => {
                  clearTimeout(loadingTimeout)
                }, { once: true })
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
            this.currentPlayingVerse = ayahs[index].numberInSurah // Set current playing verse
            
            // Scroll to the verse being played
            const verseElement = document.getElementById(`verse-${ayahs[index].number}`)
            if (verseElement) {
              verseElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
              verseElement.classList.add('loading-ayah-audio')
            }
            
            // Get the audio URL from the ayah data
            if (ayahs[index].audio) {
              console.log(`Playing verse ${index + 1} from audio URL provided by API: ${ayahs[index].audio}`)
              
              // Check if the URL contains Islamic.network CDN which might have CORS issues
              const isIslamicNetworkCDN = ayahs[index].audio.includes('islamic.network') || 
                                         ayahs[index].audio.includes('cdn.alquran.cloud');
              
              if (isIslamicNetworkCDN) {
                console.log(`Using direct audio element for Islamic.network CDN to avoid CORS issues`);
                // Try to use preloaded audio if available
                if (preloadedAudio[index]) {
                  try {
                    this.audioPlayer = await preloadedAudio[index];
                    console.log(`Using preloaded audio for verse ${index + 1}`);
                    if (verseElement) {
                      verseElement.classList.remove('loading-ayah-audio');
                      verseElement.classList.add('playing-ayah-audio');
                    }
                    // Start tracking progress for controls visibility
                    this.startProgressTracking();
                  } catch (error) {
                    console.warn(`Preloaded audio failed, creating direct audio for verse ${index + 1}`);
                    // Create direct audio player for Islamic.network CDN
                    this.audioPlayer = new Audio(ayahs[index].audio);
                    
                    // Add event listeners
                    this.audioPlayer.addEventListener('canplay', () => {
                      if (verseElement) {
                        verseElement.classList.remove('loading-ayah-audio');
                        verseElement.classList.add('playing-ayah-audio');
                      }
                    });
                    
                    this.audioPlayer.load();
                    this.audioPlayer.play().catch(error => {
                      console.error(`Error starting direct playback: ${error}`);
                    });
                    // Start tracking progress for controls visibility
                    this.startProgressTracking();
                  }
                } else {
                  // No preloaded audio, create a direct audio player
                  this.audioPlayer = new Audio(ayahs[index].audio);
                  
                  // Add event listeners
                  this.audioPlayer.addEventListener('canplay', () => {
                    if (verseElement) {
                      verseElement.classList.remove('loading-ayah-audio');
                      verseElement.classList.add('playing-ayah-audio');
                    }
                  });
                  
                  this.audioPlayer.load();
                  this.audioPlayer.play().catch(error => {
                    console.error(`Error starting direct playback: ${error}`);
                  });
                  // Start tracking progress for controls visibility
                  this.startProgressTracking();
                }
              } else {
                // For other sources, use progressive loading
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
                    // Start tracking progress for controls visibility
                    this.startProgressTracking();
                  } catch (error) {
                    // If preloaded audio fails, create a new one
                    console.warn(`Preloaded audio failed, creating new audio for verse ${index + 1}`)
                    this.createProgressiveAudioPlayer(ayahs[index].audio, verseElement)
                    // Start tracking progress for controls visibility
                    this.startProgressTracking();
                  }
                } else {
                  // No preloaded audio, create a new one with progressive loading
                  this.createProgressiveAudioPlayer(ayahs[index].audio, verseElement)
                  // Start tracking progress for controls visibility
                  this.startProgressTracking();
                }
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
      
      // Start tracking progress for controls visibility immediately
      this.startProgressTracking();
      
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
        
        // Start tracking progress for controls visibility immediately
        this.startProgressTracking();
        
        // Use a small chunk approach for mp3 files
        const response = await fetch(audioUrl, {
          headers: {
            'Range': 'bytes=0-65536' // Request just the first chunk
          },
          mode: 'cors' // Try with CORS mode first
        }).catch(error => {
          console.log('CORS request failed, falling back to direct audio playback:', error);
          return null;
        });
        
        if (!response || !response.ok) {
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
        // Fetch the complete file in the background, with fallback
        const fullResponse = await fetch(audioUrl, {
          mode: 'cors' // Try with CORS mode first 
        }).catch(error => {
          console.log('CORS request failed for full audio, falling back to direct audio element:', error);
          return null;
        });
        
        // If CORS fetch failed or the initial playback is complete, handle accordingly
        if (!fullResponse || !this.audioPlayer || this.audioPlayer.ended) {
          if (!fullResponse) {
            // If CORS fetch failed, just continue with the initial audio element
            console.log('Continuing with initial audio element as fallback');
          }
          return;
        }
        
        const fullAudioBlob = await fullResponse.blob();
        
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
      
      // Get the verse number in surah (not the combined ID)
      let verseNumberInSurah = match.numberInSurah;
      
      // If we have a string ID like "3_40", extract the verse number
      if (typeof match.number === 'string' && match.number.includes('_')) {
        verseNumberInSurah = parseInt(match.number.split('_')[1]);
      }
      
      console.log('Jumping to search result:', match.surah.number, 'verse:', verseNumberInSurah);
      
      // Load the surah
      this.loadSurah().then(() => {
        // Wait for the surah to load then scroll to the verse
        setTimeout(() => {
          try {
            // Use our helper method to find the verse
            const verseElement = this.findVerseElement(verseNumberInSurah);
            
            if (verseElement) {
              console.log('Found verse element, scrolling to it');
              // Highlight the verse
              this.highlightedAyah = verseNumberInSurah;
              
              // Scroll to the verse
              verseElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
              
              // Add a temporary highlight effect
              verseElement.classList.add('search-highlight');
              setTimeout(() => {
                verseElement.classList.remove('search-highlight');
              }, 3000);
            } else {
              console.log('Verse element not found immediately, trying to load more verses');
              // The verse might not be loaded yet
              this.loadVersesUntilFound(verseNumberInSurah);
            }
          } catch (error) {
            console.error('Error scrolling to search result verse:', error);
          }
        }, 500); // Give enough time for the DOM to update
      });
    },
    
    async loadVersesUntilFound(verseNumber) {
      // Convert string ID to number if it's in the format "surah_verse"
      let verseNumberInSurah = verseNumber
      
      // Check if verseNumber contains an underscore (format: surah_verse)
      if (typeof verseNumber === 'string' && verseNumber.includes('_')) {
        verseNumberInSurah = parseInt(verseNumber.split('_')[1])
      }
      
      // Parse to ensure we have a number
      verseNumberInSurah = parseInt(verseNumberInSurah)
      
      console.log(`Trying to find verse ${verseNumberInSurah} in surah ${this.selectedSurah}`)
      
      // If no current surah, wait for it to load first
      if (!this.currentSurah) {
        console.log('Waiting for surah to load before finding verse')
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Check again after delay
        if (!this.currentSurah) {
          console.error('Cannot find verse: Surah failed to load')
          this.$notification?.warning?.(this.$t('quran.surahLoadingFailed'))
          return
        }
      }
      
      // If no ayahs or verse number is invalid, return
      if (!this.currentSurah.ayahs || !Array.isArray(this.currentSurah.ayahs) || isNaN(verseNumberInSurah)) {
        console.error('Cannot find verse: Invalid surah ayahs or verse number')
        return
      }
      
      // Verify the verse number is within range for this surah
      if (verseNumberInSurah > this.currentSurah.numberOfAyahs) {
        console.error(`Verse number ${verseNumberInSurah} is out of range for surah ${this.selectedSurah} (max ${this.currentSurah.numberOfAyahs})`)
        return
      }
      
      // First try to find the verse in already loaded verses
      const verseElement = this.findVerseElement(verseNumberInSurah)
      if (verseElement) {
        // Found it! Scroll to it
        this.scrollToVerseElement(verseElement, verseNumberInSurah)
        return
      }
      
      // If not found, let's try a more systematic approach to loading
      console.log(`Verse ${verseNumberInSurah} not found in already loaded verses (${this.displayedVerses?.length || 0} of ${this.currentSurah.ayahs.length}). Loading more...`)
      
      try {
        // Show loading notification
        this.$notification?.info?.(this.$t('quran.navigatingToVerse', { verse: verseNumberInSurah }) || `Navigating to verse ${verseNumberInSurah}...`)
        
        // Make sure displayedVerses is initialized
        if (!this.displayedVerses || !Array.isArray(this.displayedVerses)) {
          this.displayedVerses = []
        }
        
        // Run our debug function to understand the DOM structure
        const domInfo = this.debugVerseElementStructure()
        console.log('DOM structure analysis:', domInfo)
        
        // Check if the target verse is already loaded in the displayedVerses array
        const verseExists = this.displayedVerses.some(v => 
          v.numberInSurah === verseNumberInSurah || 
          parseInt(v.numberInSurah) === verseNumberInSurah
        )
        
        if (verseExists) {
          console.log(`Verse ${verseNumberInSurah} is loaded in the data but not found in DOM. Trying direct text search...`)
          
          // Direct DOM text content search for the verse number
          // This is a more aggressive approach that looks for the verse number in the text content
          
          // First ensure all verses are loaded
          if (this.displayedVerses.length < this.currentSurah.ayahs.length) {
            console.log(`Loading all verses to ensure verse ${verseNumberInSurah} is in the DOM`)
            const remainingVerses = this.currentSurah.ayahs.length - this.displayedVerses.length
            await this.loadMoreVerses(remainingVerses)
            await new Promise(resolve => setTimeout(resolve, 300)) // Wait for DOM updates
            
            // Check if we need to reset loading state
            this.checkAndResetLoadingState()
          }
          
          // Get the specific verse data
          const targetVerse = this.displayedVerses.find(v => 
            v.numberInSurah === verseNumberInSurah || 
            parseInt(v.numberInSurah) === verseNumberInSurah
          )
          
          if (targetVerse) {
            // Aggressive approach: search for text content that contains unique parts of the verse text
            const verseTexts = document.querySelectorAll('.verse-text, .ayah-text, .verse-content, .arabic-text')
            let matchedElement = null
            
            for (const textElement of verseTexts) {
              // Simple match for verse number in text
              if (textElement.textContent.includes(`{${verseNumberInSurah}}`) || 
                  textElement.textContent.includes(`﴿${verseNumberInSurah}﴾`) ||
                  textElement.textContent.includes(`(${verseNumberInSurah})`) ||
                  textElement.textContent.includes(`[${verseNumberInSurah}]`)) {
                
                console.log(`Found verse ${verseNumberInSurah} by verse number markers in text`)
                matchedElement = textElement.closest('.verse') || textElement.closest('.ayah') || textElement.parentElement
                break
              }
              
              // If we have actual text to match, try that
              if (targetVerse.text && targetVerse.text.length > 10) {
                // Take a distinctive snippet of the verse text to search for
                // Use the first 15-20 chars, which should be distinctive enough
                const snippetLength = Math.min(20, targetVerse.text.length)
                const textSnippet = targetVerse.text.substring(0, snippetLength)
                
                if (textElement.textContent.includes(textSnippet)) {
                  console.log(`Found verse ${verseNumberInSurah} by matching text snippet: "${textSnippet}"`)
                  matchedElement = textElement.closest('.verse') || textElement.closest('.ayah') || textElement.parentElement
                  break
                }
              }
            }
            
            if (matchedElement) {
              this.scrollToVerseElement(matchedElement, verseNumberInSurah)
              return
            }
          }
        }
        
        // If we still haven't found the verse, load more content systematically
        // Calculate how many verses we need to load to reach the target
        const versesNeeded = Math.max(0, verseNumberInSurah - this.displayedVerses.length)
        
        // First attempt: Load exactly what we need plus a buffer for context
        const loadSize = versesNeeded + 10 // Add buffer for context
        console.log(`Loading approximately ${loadSize} verses to reach verse ${verseNumberInSurah}`)
        
        try {
          await this.loadMoreVerses(loadSize, verseNumberInSurah)
          await new Promise(resolve => setTimeout(resolve, 300)) // Wait for DOM updates
          
          // Check if we need to reset loading state
          this.checkAndResetLoadingState()
        } catch (loadError) {
          console.warn('Error during initial verse loading:', loadError)
          // Continue despite errors - we'll try other approaches
        }
        
        // Check if we found it
        let element = this.findVerseElement(verseNumberInSurah)
        if (element) {
          console.log(`Found verse ${verseNumberInSurah} after targeted loading`)
          this.scrollToVerseElement(element, verseNumberInSurah)
          return
        }
        
        // If the displayedVerses array hasn't been properly initialized yet, wait a bit and retry
        if (!this.displayedVerses || this.displayedVerses.length === 0) {
          console.log('Waiting for verse display initialization...')
          await new Promise(resolve => setTimeout(resolve, 1000))
          
          // Check one more time after wait
          element = this.findVerseElement(verseNumberInSurah)
          if (element) {
            console.log(`Found verse ${verseNumberInSurah} after waiting for initialization`)
            this.scrollToVerseElement(element, verseNumberInSurah)
            return
          }
        }
        
        // If we still don't have all verses loaded, load in larger chunks
        if (!this.displayedVerses || this.displayedVerses.length < this.currentSurah.ayahs.length) {
          console.log(`Still didn't find verse ${verseNumberInSurah}. Loading remaining verses in chunks...`)
          
          // Try loading in chunks until we find it or load everything
          const maxChunks = 5 // Prevent infinite loops
          let attempts = 0
          let chunkSize = 50 // Start with medium-sized chunks
          
          while (attempts < maxChunks && this.displayedVerses.length < this.currentSurah.ayahs.length) {
            attempts++
            console.log(`Attempt ${attempts}: Loading ${chunkSize} more verses...`)
            
            try {
              await this.loadMoreVerses(chunkSize)
              await new Promise(resolve => setTimeout(resolve, 200)) // Wait for DOM updates
            } catch (loadError) {
              console.warn(`Error during chunk loading attempt ${attempts}:`, loadError)
              // Pause briefly before next attempt
              await new Promise(resolve => setTimeout(resolve, 500))
            }
            
            // Check if we found it after this chunk
            element = this.findVerseElement(verseNumberInSurah)
            if (element) {
              console.log(`Found verse ${verseNumberInSurah} on attempt ${attempts}`)
              this.scrollToVerseElement(element, verseNumberInSurah)
              return
            }
            
            // Increase chunk size for next attempt
            chunkSize = Math.min(chunkSize * 2, 200) // Double size but cap at 200
            
            // Check if we need to reset loading state
            this.checkAndResetLoadingState()
          }
          
          // If still not found, load all remaining verses at once
          if (!element && this.displayedVerses.length < this.currentSurah.ayahs.length) {
            console.log(`Final attempt: Loading all remaining verses (${this.currentSurah.ayahs.length - this.displayedVerses.length})`)
            
            try {
              const remaining = this.currentSurah.ayahs.length - this.displayedVerses.length
              await this.loadMoreVerses(remaining)
              await new Promise(resolve => setTimeout(resolve, 500)) // Longer wait for more DOM updates
              
              // Ensure loading state is reset after loading all verses
              this.checkAndResetLoadingState()
            } catch (loadError) {
              console.warn('Error during final verse loading attempt:', loadError)
            }
            
            // Final check
            element = this.findVerseElement(verseNumberInSurah)
            if (element) {
              console.log(`Found verse ${verseNumberInSurah} after loading all verses`)
              this.scrollToVerseElement(element, verseNumberInSurah)
              return
            }
          }
        }
        
        // Last resort: Try to estimate the position within the container by verse index
        if (this.displayedVerses && this.displayedVerses.length > 0) {
          console.log(`Last resort: Approximating position of verse ${verseNumberInSurah} based on index`)
          
          // Find the index of our target verse in the displayed verses
          const verseIndex = this.displayedVerses.findIndex(v => 
            v.numberInSurah === verseNumberInSurah || 
            parseInt(v.numberInSurah) === verseNumberInSurah
          )
          
          if (verseIndex >= 0) {
            console.log(`Found verse at index ${verseIndex} out of ${this.displayedVerses.length} total verses`)
            
            // Calculate the approximate position in the container
            const container = document.querySelector('.quran-container')
            if (container) {
              const containerHeight = container.scrollHeight
              const approximateScrollPosition = (containerHeight * verseIndex) / this.displayedVerses.length
              
              console.log(`Scrolling to approximate position: ${approximateScrollPosition}px of ${containerHeight}px total`)
              container.scrollTop = approximateScrollPosition
              
              // Show a notification
              this.$notification?.info?.(this.$t('quran.approximateVersePosition') || 
                `Scrolled to approximate position of verse ${verseNumberInSurah}`)
              
              // Ensure loading state is reset
              this.checkAndResetLoadingState()
              return
            }
          }
        }
        
        // If we still couldn't find it after loading all verses
        console.error(`Could not find verse ${verseNumberInSurah} after loading all ${this.displayedVerses.length} verses`)
        this.$notification?.warning?.(this.$t('quran.verseLoadingFailed') || 'Could not locate the verse')
        
        // Always ensure loading state is reset
        this.checkAndResetLoadingState()
        
        // As a fallback, try to at least navigate to the beginning of the surah
        const surahElement = document.querySelector('.quran-surah-container')
        if (surahElement) {
          surahElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
          this.$notification?.info?.(this.$t('quran.navigatedToSurahStart') || 'Navigated to the beginning of the surah')
        }
      } catch (error) {
        console.error('Error while searching for verse:', error)
        this.$notification?.error?.(this.$t('quran.loadingError') || 'Error loading verse')
        
        // Ensure loading state is reset even on error
        this.checkAndResetLoadingState()
      }
    },
    
    // Helper function to scroll to a verse element
    scrollToVerseElement(element, verseNumber) {
      if (!element) return
      
      // Set the highlighted verse
      this.highlightedAyah = verseNumber
      
      // Scroll to the verse
      element.scrollIntoView({ behavior: 'smooth', block: 'center' })
      
      // Add highlight effect
      element.classList.add('search-highlight')
      setTimeout(() => {
        element.classList.remove('search-highlight')
        this.highlightedAyah = null // Clear the highlight after the animation
        
        // Check and reset loading state after scrolling
        this.checkAndResetLoadingState()
      }, 3000)
      
      // Immediately check if we need to reset loading state
      this.checkAndResetLoadingState()
    },
    
    // Helper method to find a verse element by verse number in surah
    findVerseElement(verseNumberInSurah) {
      console.log('Looking for verse with number in surah:', verseNumberInSurah)
      
      if (!verseNumberInSurah || isNaN(parseInt(verseNumberInSurah))) {
        console.error(`Invalid verse number: ${verseNumberInSurah}`)
        return null
      }
      
      // Convert to number to ensure consistent comparisons
      const verseNum = parseInt(verseNumberInSurah)
      
      // Try different possible ID formats
      let element
      
      // Try direct verse number format (verse-123)
      element = document.getElementById(`verse-${verseNum}`)
      if (element) {
        console.log(`Found verse element with ID verse-${verseNum}`)
        return element
      }
      
      // Try verse number in surah format (verse-surah_verse)
      if (this.selectedSurah) {
        element = document.getElementById(`verse-${this.selectedSurah}_${verseNum}`)
        if (element) {
          console.log(`Found verse element with ID verse-${this.selectedSurah}_${verseNum}`)
          return element
        }
      }
      
      // Try composite verse ID format (some implementations use verse-surah-verse)
      if (this.selectedSurah) {
        element = document.getElementById(`verse-${this.selectedSurah}-${verseNum}`)
        if (element) {
          console.log(`Found verse element with ID verse-${this.selectedSurah}-${verseNum}`)
          return element
        }
      }
      
      // Try page-verse format
      element = document.getElementById(`page-verse-${verseNum}`)
      if (element) {
        console.log(`Found verse element with ID page-verse-${verseNum}`)
        return element
      }
      
      // Try data attribute selector (most reliable)
      const verseElementsByData = document.querySelectorAll(`[data-verse-number="${verseNum}"]`)
      if (verseElementsByData.length > 0) {
        console.log(`Found verse element with data-verse-number=${verseNum}`)
        return verseElementsByData[0]
      }
      
      // Try data-surah and data-ayah attributes (common in Quran apps)
      if (this.selectedSurah) {
        const verseElementsBySurahAyah = document.querySelectorAll(`[data-surah="${this.selectedSurah}"][data-ayah="${verseNum}"]`)
        if (verseElementsBySurahAyah.length > 0) {
          console.log(`Found verse element with data-surah=${this.selectedSurah} and data-ayah=${verseNum}`)
          return verseElementsBySurahAyah[0]
        }
      }
      
      // Try verse classes with specific patterns
      const likelyClasses = [
        `.verse-${verseNum}`,
        `.ayah-${verseNum}`,
        `.verse-num-${verseNum}`,
        `.ayah-num-${verseNum}`,
        `.quran-verse[data-number="${verseNum}"]`,
        `.quran-ayah[data-number="${verseNum}"]`
      ]
      
      for (const selector of likelyClasses) {
        const elements = document.querySelectorAll(selector)
        if (elements.length > 0) {
          console.log(`Found verse element with selector ${selector}`)
          return elements[0]
        }
      }
      
      // Try looking for the span that contains the verse number
      const verseNumSpans = document.querySelectorAll('.verse-number')
      for (const span of verseNumSpans) {
        if (span.textContent && span.textContent.trim().includes(`${verseNum}`)) {
          console.log(`Found verse element via verse number text: ${verseNum}`)
          return span.closest('.verse') || span.closest('.ayah') || span.parentElement
        }
      }
      
      // Most aggressive search: look for any element that might contain the verse
      // This is a last resort as it can be less accurate
      try {
        // Look for elements that have:
        // 1. IDs containing the verse number
        // 2. Attribute values containing the verse number (e.g., data-* attributes)
        // 3. Class names that might indicate a verse with this number
        
        // First, check for any elements with IDs containing the verse number
        const elementsWithIDs = document.querySelectorAll(`[id*="${verseNum}"]`)
        for (const el of elementsWithIDs) {
          // Check if the ID contains words like 'verse', 'ayah'
          if (el.id.toLowerCase().includes('verse') || el.id.toLowerCase().includes('ayah')) {
            console.log(`Found possible verse element with ID containing ${verseNum}: ${el.id}`)
            return el
          }
        }
        
        // Actually look directly in displayed verses for the right verse
        if (this.displayedVerses && Array.isArray(this.displayedVerses)) {
          const verseIndex = this.displayedVerses.findIndex(verse => 
            verse.numberInSurah === verseNum || 
            verse.number === verseNum || 
            verse.number === `${this.selectedSurah}:${verseNum}` ||
            verse.number === `${this.selectedSurah}_${verseNum}`
          )
          
          if (verseIndex >= 0) {
            console.log(`Found verse at index ${verseIndex} in displayedVerses array`)
            // Try to find it in the DOM based on position
            
            // Look for verse containers
            const verseContainers = document.querySelectorAll('.verse, .ayah, .quran-verse, .verse-container')
            if (verseContainers.length > 0 && verseIndex < verseContainers.length) {
              console.log(`Found verse element by position in DOM (index ${verseIndex})`)
              return verseContainers[verseIndex]
            }
          }
        }
      } catch (error) {
        console.error('Error in aggressive verse element search:', error)
      }
      
      // If all else fails, log what we tried
      console.warn(`Could not find verse element for verse ${verseNum} in DOM with any method`)
      return null
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
    
    // Set up event listeners for navigation events
    setupNavigationListener() {
      // Add listener for the custom quran-navigation event
      this.handleQuranNavigationEvent = (event) => {
        const { surah, verse, edition } = event.detail
        console.log('Received quran-navigation event:', event.detail)
        
        if (surah && verse) {
          // If the surah is already loaded, just navigate to the verse
          if (this.currentSurah && this.selectedSurah === surah) {
            console.log('Surah already loaded, navigating to verse:', verse)
            this.loadVersesUntilFound(verse)
          } else {
            // Otherwise, need to load the surah first
            console.log('Loading surah', surah, 'before navigating to verse', verse)
            this.selectedSurah = surah
            if (edition) {
              this.selectedTranslation = edition
            }
            
            // Wait for surah to load, then navigate to verse
            this.loadSurah()
              .then(() => {
                setTimeout(() => {
                  this.loadVersesUntilFound(verse)
                }, 500)
              })
              .catch(error => {
                console.error('Error loading surah before verse navigation:', error)
                this.$notification?.error?.(this.$t('quran.surahLoadingFailed'))
              })
          }
        }
      }
      
      // Register the event listener
      window.addEventListener('quran-navigation', this.handleQuranNavigationEvent)
    },
    
    // Clean up event listeners
    cleanupNavigationListener() {
      if (this.handleQuranNavigationEvent) {
        window.removeEventListener('quran-navigation', this.handleQuranNavigationEvent)
      }
    },
    
    // Set up infinite scroll
    setupInfiniteScroll() {
      // Find the scroll container
      if (this.$el && typeof this.$el.querySelector === 'function') {
        this.scrollContainer = this.$el.querySelector('.quran-container')
        
        if (this.scrollContainer) {
          this.scrollContainer.addEventListener('scroll', this.handleScroll)
        } else {
          console.warn('Scroll container not found. Infinite scroll may not work correctly.')
        }
      } else {
        console.warn('Component not fully mounted yet, cannot setup infinite scroll')
      }
    },
    
    // Clean up infinite scroll
    cleanupInfiniteScroll() {
      if (this.scrollContainer) {
        this.scrollContainer.removeEventListener('scroll', this.handleScroll)
      }
    },

    // Add a debugging method to help us understand the DOM structure
    debugVerseElementStructure() {
      console.log('=== DEBUG: Examining DOM structure for verse elements ===')
      
      // Look for common verse containers
      const containers = document.querySelectorAll('.verse, .ayah, .quran-verse, .verse-container')
      console.log(`Found ${containers.length} possible verse containers:`)
      
      if (containers.length > 0) {
        // Check the first few containers to understand structure
        for (let i = 0; i < Math.min(3, containers.length); i++) {
          const el = containers[i]
          console.log(`Container ${i}:`, {
            tag: el.tagName,
            id: el.id,
            classes: Array.from(el.classList),
            attributes: Array.from(el.attributes).map(attr => `${attr.name}="${attr.value}"`),
            children: Array.from(el.children).map(child => ({
              tag: child.tagName,
              classes: Array.from(child.classList),
              id: child.id
            }))
          })
        }
      } else {
        console.log('No standard verse containers found. Looking for verse elements by other patterns...')
      }
      
      // Check what attributes are used on elements that might be verses
      const allElements = document.querySelectorAll('.quran-container *')
      const idPatterns = new Set()
      const classPatterns = new Set()
      const dataAttributes = new Set()
      
      allElements.forEach(el => {
        if (el.id && (el.id.includes('verse') || el.id.includes('ayah'))) {
          idPatterns.add(el.id)
        }
        
        el.classList.forEach(cls => {
          if (cls.includes('verse') || cls.includes('ayah')) {
            classPatterns.add(cls)
          }
        })
        
        Array.from(el.attributes).forEach(attr => {
          if (attr.name.startsWith('data-')) {
            dataAttributes.add(`${attr.name}="${attr.value}"`)
          }
        })
      })
      
      console.log('ID patterns found:', Array.from(idPatterns).slice(0, 5))
      console.log('Class patterns found:', Array.from(classPatterns).slice(0, 5))
      console.log('Data attributes found:', Array.from(dataAttributes).slice(0, 5))
      
      // Look specifically for verse numbers
      const verseNumberElements = document.querySelectorAll('.verse-number, .ayah-number')
      console.log(`Found ${verseNumberElements.length} verse number elements`)
      if (verseNumberElements.length > 0) {
        const sample = verseNumberElements[0]
        console.log('Sample verse number element:', {
          tag: sample.tagName,
          text: sample.textContent,
          parent: sample.parentElement ? {
            tag: sample.parentElement.tagName,
            id: sample.parentElement.id,
            classes: Array.from(sample.parentElement.classList)
          } : 'none'
        })
      }
      
      console.log('=== END DEBUG ===')
      
      // Return the findings to help improve the findVerseElement method
      return {
        containerCount: containers.length,
        idPatterns: Array.from(idPatterns),
        classPatterns: Array.from(classPatterns),
        dataAttributes: Array.from(dataAttributes),
        verseNumberElements: verseNumberElements.length
      }
    },
    
    // Helper method to check and reset loading state if all verses are loaded
    checkAndResetLoadingState() {
      if (this.currentSurah && this.displayedVerses && 
          this.displayedVerses.length >= this.currentSurah.ayahs.length &&
          (this.isLoadingMore || this.loadingChunks)) {
        
        console.log('All verses are loaded, resetting loading states')
        this.isLoadingMore = false
        this.loadingChunks = false
        
        // Hide any loading indicators in the UI
        const loadingIndicators = document.querySelectorAll('.loading-indicator, .loading-more')
        loadingIndicators.forEach(el => {
          el.style.display = 'none'
        })
      }
    }
  },
  mounted() {
    // Add event listener for custom navigation events
    this.setupNavigationListener()
    
    // Initialize infinite scroll after the DOM is fully rendered
    this.$nextTick(() => {
      this.setupInfiniteScroll()
    })
    
    // Check loading state initially
    this.checkAndResetLoadingState()
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
    
    // Clear any timers
    if (this._scrollEndTimer) {
      clearTimeout(this._scrollEndTimer)
      this._scrollEndTimer = null
    }
    
    // Clean up event listeners when component is destroyed
    this.cleanupNavigationListener()
    this.cleanupInfiniteScroll()
  },
  
  // Add updated lifecycle hook to check loading state after component updates
  updated() {
    // Ensure loading state is consistent with actual data
    this.checkAndResetLoadingState()
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

.loading-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: var(--primary-color);
}

.loading-message svg {
  margin-bottom: 1rem;
}

.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 2rem 0;
}

.error-message svg {
  margin-bottom: 1rem;
}

.surah-content {
  position: relative;
}

.surah-content.surah-content-expanded .verses {
  max-height: none;
}

.surah-content.surah-content-expanded .verses-when-collapsed {
  max-height: 200px;
}

.surah-content.surah-content-expanded .verses-container-expanded {
  max-height: none;
}

.verse-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.verse-actions {
  display: flex;
  gap: 0.5rem;
}

.verse-action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.verse-action-button:hover {
  background-color: var(--primary-hover);
}

.verse-action-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.verse-action-button.active {
  background-color: var(--primary-hover);
}

.audio-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1rem;
}

.audio-control-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.audio-control-button:hover {
  background-color: var(--primary-hover);
}

.audio-control-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.audio-control-button.play-pause {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  background-color: var(--primary-color);
  color: white;
  font-size: 0.875rem;
  transition: background-color 0.2s ease;
}

.audio-control-button.play-pause:hover {
  background-color: var(--primary-hover);
}

.audio-control-button.play-pause:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.audio-control-button.play-pause.active {
  background-color: var(--primary-hover);
}

.audio-time {
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-align: center;
  margin-top: 0.5rem;
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

.surah-actions {
  border-top: 1px solid #e5e7eb;
  padding-top: 1rem;
  margin-top: 1rem;
}

.listen-surah-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4f46e5;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: background-color 0.2s;
  height: 38px;
}

.listen-surah-button:hover:not(:disabled) {
  background-color: #4338ca;
}

.listen-surah-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.surah-content-container {
  position: relative;
}

.surah-content-container.expanded .verses {
  max-height: none;
}

.surah-content-container.expanded .verses-when-collapsed {
  max-height: 200px;
}

.surah-content-container.expanded .verses-container-expanded {
  max-height: none;
}

.show-list-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4f46e5;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: background-color 0.2s;
  height: 38px;
}

.show-list-button:hover:not(:disabled) {
  background-color: #4338ca;
}

.show-list-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.surah-content {
  position: relative;
}

.surah-content.fullscreen .verses {
  max-height: none;
}

.surah-content.fullscreen .verses-when-collapsed {
  max-height: 200px;
}

.surah-content.fullscreen .verses-container-expanded {
  max-height: none;
}

.sticky-audio-controls {
  position: sticky;
  top: 0;
  background-color: var(--card-bg);
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.audio-now-playing {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.audio-controls-buttons {
  display: flex;
  gap: 0.5rem;
}

.control-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4f46e5;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: background-color 0.2s;
  height: 38px;
}

.control-button:hover:not(:disabled) {
  background-color: #4338ca;
}

.control-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.now-playing-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.now-playing-surah {
  font-size: 1rem;
  font-weight: bold;
}

.retry-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4f46e5;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: background-color 0.2s;
  height: 38px;
}

.retry-button:hover:not(:disabled) {
  background-color: #4338ca;
}

.retry-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Loading more indicator styling */
.text-center.py-4 {
  background-color: rgba(245, 247, 250, 0.8);
  border-top: 1px solid #e5e7eb;
  margin-top: 1rem;
  padding: 1rem 0;
  border-radius: 0 0 0.5rem 0.5rem;
}

.text-center.py-4 .animate-spin {
  height: 1.5rem;
  width: 1.5rem;
  border-width: 3px;
}

.text-center.py-4 p {
  font-weight: 500;
  color: #4f46e5;
  margin-top: 0.5rem;
}

/* Load all verses button styling */
.load-all-button {
  display: block;
  margin: 1rem auto 0;
  background-color: #4f46e5;
  color: white;
  font-weight: 600;
  padding: 0.5rem 1.25rem;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.load-all-button:hover {
  background-color: #4338ca;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.load-all-button:active {
  transform: translateY(0);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Floating audio controls */
.floating-audio-controls {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  background-color: rgba(250, 250, 250, 0.95);
  border-top: 1px solid #e5e7eb;
  box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.1), 0 -2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.3s ease;
  padding: 0.75rem 1rem;
  backdrop-filter: blur(8px);
}

.audio-controls-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  gap: 0.75rem;
}

.audio-progress-wrapper {
  display: flex;
  align-items: center;
  flex: 1;
  gap: 0.5rem;
  margin: 0 0.5rem;
}

.audio-progress-container {
  flex: 1;
  height: 6px;
  background-color: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
  cursor: pointer;
  margin: 0 0.5rem;
}

.audio-progress-bar {
  height: 100%;
  background-color: #4f46e5;
  transition: width 0.1s linear;
}

.audio-time {
  font-size: 0.75rem;
  color: #4b5563;
  min-width: 2.5rem;
  text-align: center;
}

.audio-control-button {
  border-radius: 50%;
  width: 2.25rem;
  height: 2.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4f46e5;
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.audio-control-button:hover {
  background-color: #4338ca;
}

.now-playing-info {
  font-size: 0.875rem;
  color: #4b5563;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
  text-align: right;
}

@media (max-width: 640px) {
  .audio-controls-container {
    flex-wrap: wrap;
  }
  
  .now-playing-info {
    display: none;
  }
  
  .audio-progress-wrapper {
    width: 100%;
    order: 3;
    margin-top: 0.5rem;
  }
}
</style> 