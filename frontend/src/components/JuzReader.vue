<script setup>
import { ref, onMounted, watch, defineProps, defineEmits, computed } from 'vue';
import { store } from '../store';

const props = defineProps({
  khatmahId: {
    type: String,
    required: true
  },
  juzNumber: {
    type: Number,
    required: true
  },
  assignmentId: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['back-to-khatmah', 'mark-completed']);

const juzText = ref('');
const ayahs = ref([]);
const loading = ref(true);
const error = ref(null);
const currentSurah = ref('');
const showTranslation = ref(false);
const pageFormat = ref(false);
// Bookmark related state
const bookmarkPosition = ref(null);
const showBookmarkNotification = ref(false);

// Computed property to get unique surahs in this juz
const uniqueSurahs = computed(() => {
  if (!ayahs.value.length) return [];
  
  const surahs = [];
  const surahNumbers = new Set();
  
  for (const ayah of ayahs.value) {
    if (!surahNumbers.has(ayah.surah.number)) {
      surahNumbers.add(ayah.surah.number);
      surahs.push({
        name: ayah.surah.name,
        number: ayah.surah.number
      });
    }
  }
  
  return surahs;
});

// Function to check if a surah should display Bismillah
// All surahs except Surah At-Tawbah (9) should have Bismillah
function shouldDisplayBismillah(surahNumber) {
  return surahNumber !== 9; // Surah At-Tawbah (9) doesn't have Bismillah
}

// Function to extract Bismillah from the first ayah if needed
function extractBismillah(ayahText) {
  if (!ayahText) return 'بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ';
  
  // Always return the standard Bismillah text for consistency
  return 'بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ';
}

// Function to remove Bismillah from ayah text if it's included
function cleanAyahText(ayahText, surahNumber, ayahNumberInSurah) {
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
}

// Load bookmark when component mounts
onMounted(() => {
  loadBookmark();
});

// Fetch the Juz text when component mounts or juzNumber changes
watch(() => props.juzNumber, fetchJuzText, { immediate: true });

async function fetchJuzText() {
  loading.value = true;
  error.value = null;
  
  try {
    // Use the direct Quran API as the primary method
    const apiUrl = `https://api.alquran.cloud/v1/juz/${props.juzNumber}/quran-uthmani`;
    
    const response = await fetch(apiUrl);
    
    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    if (data.code !== 200 || !data.data || !data.data.ayahs) {
      throw new Error('Invalid response from API');
    }
    
    // Process the ayahs
    ayahs.value = data.data.ayahs;
    
    // Format the text
    let formattedText = `# Juz ${props.juzNumber}\n\n`;
    
    // Group ayahs by surah
    let currentSurahName = null;
    for (const ayah of ayahs.value) {
      const surahName = ayah.surah.name;
      const surahNumber = ayah.surah.number;
      
      // Add surah header when changing to a new surah
      if (currentSurahName !== surahName) {
        currentSurahName = surahName;
        formattedText += `\n## ${surahName}\n\n`;
        
       
      }
      
      // Add the ayah text (clean it if needed)
      const cleanedText = cleanAyahText(ayah.text, surahNumber, ayah.numberInSurah);
      formattedText += `${cleanedText} (${ayah.numberInSurah})\n\n`;
    }
    
    juzText.value = formattedText;
    
    // Set the initial current surah
    if (ayahs.value.length > 0) {
      currentSurah.value = ayahs.value[0].surah.name;
      
      // Check if we have a bookmark and scroll to it
      if (bookmarkPosition.value) {
        setTimeout(() => {
          scrollToAyah(bookmarkPosition.value.ayahNumber);
        }, 1000); // Give time for the content to render
      }
    }
    
    loading.value = false;
  } catch (err) {
    console.error('Error fetching Juz text from direct API:', err);
    // Try our backend API as fallback
    tryBackendAPI();
  }
}

// Fallback function to fetch Juz text from our backend API
async function tryBackendAPI() {
  try {
    const response = await fetch(`/api/juz/${props.juzNumber}/text/`);
    
    if (!response.ok) {
      // Try to get error details from the response
      let errorDetails = '';
      try {
        const errorData = await response.json();
        errorDetails = errorData.error || errorData.detail || '';
      } catch (e) {
        // If we can't parse the JSON, use the status text
        errorDetails = response.statusText;
      }
      
      throw new Error(`Failed to fetch Juz text from backend: ${errorDetails}`);
    }
    
    // Try to parse the JSON response
    let data;
    try {
      data = await response.json();
    } catch (e) {
      console.error('Error parsing JSON response:', e);
      throw new Error('Invalid response format from server');
    }
    
    // Check if the data is valid
    if (!data || (data.error && !data.ayahs)) {
      throw new Error(data.error || 'Invalid response from server');
    }
    
    juzText.value = data.text || '';
    ayahs.value = data.ayahs || [];
    
    // Set the initial current surah if there are ayahs
    if (ayahs.value.length > 0) {
      currentSurah.value = ayahs.value[0].surah.name;
    } else {
      // If no ayahs are available, try the CORS proxy
      await tryCorsProxy();
    }
    
    loading.value = false;
  } catch (err) {
    console.error('Backend API also failed:', err);
    // Try with CORS proxy
    await tryCorsProxy();
  }
}

// Try using a CORS proxy if direct API and backend API both fail
async function tryCorsProxy() {
  try {
    const corsProxy = 'https://cors-anywhere.herokuapp.com/';
    const apiUrl = `https://api.alquran.cloud/v1/juz/${props.juzNumber}/quran-uthmani`;
    
    const response = await fetch(`${corsProxy}${apiUrl}`, {
      headers: {
        'Origin': window.location.origin,
        'X-Requested-With': 'XMLHttpRequest'
      }
    });
    
    if (!response.ok) {
      throw new Error(`CORS proxy request failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    if (data.code !== 200 || !data.data || !data.data.ayahs) {
      throw new Error('Invalid response from CORS proxy API');
    }
    
    // Process the ayahs
    ayahs.value = data.data.ayahs;
    
    // Format the text
    let formattedText = `# Juz ${props.juzNumber}\n\n`;
    
    // Group ayahs by surah
    let currentSurahName = null;
    for (const ayah of ayahs.value) {
      const surahName = ayah.surah.name;
      const surahNumber = ayah.surah.number;
      
      // Add surah header when changing to a new surah
      if (currentSurahName !== surahName) {
        currentSurahName = surahName;
        formattedText += `\n## ${surahName}\n\n`;
        
        // Add Bismillah after surah header except for Surah At-Tawbah
      
      }
      
      // Add the ayah text (clean it if needed)
      const cleanedText = cleanAyahText(ayah.text, surahNumber, ayah.numberInSurah);
      formattedText += `${cleanedText} (${ayah.numberInSurah})\n\n`;
    }
    
    juzText.value = formattedText;
    
    // Set the initial current surah
    if (ayahs.value.length > 0) {
      currentSurah.value = ayahs.value[0].surah.name;
    }
    
    // Clear any error
    error.value = null;
    loading.value = false;
  } catch (err) {
    console.error('CORS proxy also failed:', err);
    // Update the error message
    error.value = `All API methods failed: ${err.message}. Please try the static content option.`;
    loading.value = false;
  }
}

// Fallback function to fetch Juz text directly from the Quran API
async function fetchFallbackJuzText() {
  // This is now the same as our primary method, so just call fetchJuzText again
  await fetchJuzText();
}

async function markAsCompleted() {
  try {
    await store.toggleJuzComplete(props.assignmentId, props.khatmahId);
    emit('mark-completed');
  } catch (err) {
    console.error('Error marking Juz as completed:', err);
    store.error = 'Failed to mark Juz as completed';
  }
}

function goBackToKhatmah() {
  emit('back-to-khatmah');
}

function toggleTranslation() {
  showTranslation.value = !showTranslation.value;
}

function scrollToSurah(surahName) {
  currentSurah.value = surahName;
  const element = document.getElementById(`surah-${surahName}`);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function navigateToJuz(juzNumber) {
  // This will trigger the parent component to change the juz
  emit('back-to-khatmah');
  
  // We need to wait for the parent component to update before we can navigate to the new juz
  setTimeout(() => {
    const juzElement = document.querySelector(`[data-juz="${juzNumber}"]`);
    if (juzElement) {
      juzElement.click();
    }
  }, 100);
}

function useStaticFallback() {
  loading.value = true;
  error.value = null;
  
  // Create a static fallback text with basic information
  setTimeout(() => {
    // Clear ayahs array since we're using static content
    ayahs.value = [];
    
    // Create a static fallback text with basic information
    juzText.value = `
      <div class="text-center">
        <h1 class="text-3xl mb-4">Juz ${props.juzNumber}</h1>
        <p class="text-gray-500 text-sm mb-8">Static fallback content</p>
        
        <div class="mb-8">
          <h2 class="text-2xl font-bold">Example Surah</h2>
          <p class="font-arabic text-2xl mt-4 mb-4">بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ</p>
          <p class="text-gray-600 mt-2">This is a placeholder for Juz ${props.juzNumber}.</p>
        </div>
        
        <div class="bg-yellow-50 p-4 rounded-lg text-yellow-700 mb-8 max-w-lg mx-auto">
          <p>This is a placeholder for Juz ${props.juzNumber}. For the actual Quranic text, please try again later when the API service is available.</p>
          <p class="mt-2">You can still mark this Juz as completed to continue with your Khatmah progress.</p>
        </div>
      </div>
    `;
    
    loading.value = false;
  }, 500); // Small delay to show loading indicator
}

// Bookmark functions
function saveBookmark(ayahNumber) {
  // Create a bookmark object with all necessary information
  const bookmark = {
    khatmahId: props.khatmahId,
    juzNumber: props.juzNumber,
    ayahNumber: ayahNumber,
    timestamp: new Date().toISOString(),
    surahName: ayahs.value.find(a => a.number === ayahNumber)?.surah.name || '',
    ayahNumberInSurah: ayahs.value.find(a => a.number === ayahNumber)?.numberInSurah || 0
  };
  
  // Save to localStorage
  localStorage.setItem(`quran-khatmah-bookmark-${props.khatmahId}-${props.juzNumber}`, JSON.stringify(bookmark));
  
  // Update the bookmark position
  bookmarkPosition.value = bookmark;
  
  // Show notification
  showBookmarkNotification.value = true;
  setTimeout(() => {
    showBookmarkNotification.value = false;
  }, 3000);
}

function loadBookmark() {
  try {
    // Try to load bookmark from localStorage
    const savedBookmark = localStorage.getItem(`quran-khatmah-bookmark-${props.khatmahId}-${props.juzNumber}`);
    
    if (savedBookmark) {
      bookmarkPosition.value = JSON.parse(savedBookmark);
      
      // If we have ayahs loaded and a bookmark, scroll to the bookmarked ayah
      if (ayahs.value.length > 0 && bookmarkPosition.value) {
        setTimeout(() => {
          scrollToAyah(bookmarkPosition.value.ayahNumber);
        }, 1000); // Give time for the content to render
      }
    }
  } catch (err) {
    console.error('Error loading bookmark:', err);
  }
}

function scrollToAyah(ayahNumber) {
  const ayahElement = document.getElementById(`ayah-${ayahNumber}`);
  if (ayahElement) {
    // Scroll to the ayah with a smooth animation
    ayahElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Highlight the ayah briefly
    ayahElement.classList.add('bookmark-highlight');
    
    // If we're in page format, make sure the bookmark button is visible
    if (pageFormat.value) {
      const bookmarkButton = ayahElement.querySelector('.bookmark-inline-button');
      if (bookmarkButton) {
        bookmarkButton.style.display = 'block';
      }
    }
    
    // Remove the highlight after a delay
    setTimeout(() => {
      ayahElement.classList.remove('bookmark-highlight');
      
      // If we're in page format, hide the bookmark button again after a delay
      if (pageFormat.value) {
        const bookmarkButton = ayahElement.querySelector('.bookmark-inline-button');
        if (bookmarkButton && !bookmarkButton.classList.contains('active')) {
          bookmarkButton.style.display = '';
        }
      }
    }, 3000);
  }
}

function clearBookmark() {
  localStorage.removeItem(`quran-khatmah-bookmark-${props.khatmahId}-${props.juzNumber}`);
  bookmarkPosition.value = null;
  
  // Show notification
  showBookmarkNotification.value = true;
  setTimeout(() => {
    showBookmarkNotification.value = false;
  }, 3000);
}
</script>

<template>
  <div class="juz-reader">
    <!-- Header with back button and navigation -->
    <div class="flex items-center justify-between mb-6">
      <button 
        @click="goBackToKhatmah" 
        class="flex items-center text-emerald-600 hover:text-emerald-700 transition-colors"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
        </svg>
        Back to Khatmah
      </button>
      
      <div class="flex items-center space-x-4">
        <button 
          v-if="props.juzNumber > 1"
          @click="navigateToJuz(props.juzNumber - 1)"
          class="text-emerald-600 hover:text-emerald-700 transition-colors"
          title="Previous Juz"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <div class="flex items-center">
          <img src="../assets/7sanah_logo.png" alt="7sanah Logo" class="h-8 w-auto mr-2" />
          <div class="text-lg font-semibold text-gray-800">
            Juz {{ props.juzNumber }}
          </div>
        </div>
        
        <button 
          v-if="props.juzNumber < 30"
          @click="navigateToJuz(props.juzNumber + 1)"
          class="text-emerald-600 hover:text-emerald-700 transition-colors"
          title="Next Juz"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-500"></div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="bg-red-50 text-red-700 p-4 rounded-lg mb-6">
      <p class="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        {{ error }}
      </p>
      <div class="mt-4 flex flex-wrap gap-2">
        <button 
          @click="fetchJuzText" 
          class="px-4 py-2 bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors"
        >
          Try Again
        </button>
        <button 
          @click="tryBackendAPI" 
          class="px-4 py-2 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors"
        >
          Try Backend API
        </button>
        <button 
          @click="tryCorsProxy" 
          class="px-4 py-2 bg-yellow-100 text-yellow-700 rounded-md hover:bg-yellow-200 transition-colors"
        >
          Try CORS Proxy
        </button>
        <button 
          @click="useStaticFallback" 
          class="px-4 py-2 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors"
        >
          Use Static Content
        </button>
      </div>
    </div>
    
    <!-- Juz content -->
    <div v-else class="mb-8">
      <!-- Quran text display -->
      <div class="bg-white rounded-xl shadow-md p-6 mb-6 border border-gray-100">
        <!-- Bismillah header - removing static version -->
        <div class="text-center mb-8">
          <h2 class="text-2xl font-semibold">Juz {{ props.juzNumber }}</h2>
        </div>
        
        <!-- Bookmark notification -->
        <div 
          v-if="showBookmarkNotification" 
          class="fixed top-4 right-4 bg-emerald-100 text-emerald-800 px-4 py-3 rounded-lg shadow-md z-50 transition-opacity duration-300"
        >
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
            </svg>
            <span>{{ bookmarkPosition ? 'Bookmark saved!' : 'Bookmark cleared!' }}</span>
          </div>
        </div>
        
        <!-- Bookmark info -->
        <div v-if="bookmarkPosition && ayahs.length > 0" class="mb-6 bg-blue-50 p-4 rounded-lg">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
              </svg>
              <span class="text-blue-800">
                Bookmarked at: {{ bookmarkPosition.surahName }} - Ayah {{ bookmarkPosition.ayahNumberInSurah }}
              </span>
            </div>
            <div class="flex space-x-2">
              <button 
                @click="scrollToAyah(bookmarkPosition.ayahNumber)"
                class="text-xs px-3 py-1 bg-blue-200 text-blue-800 rounded-md hover:bg-blue-300 transition-colors"
              >
                Go to Bookmark
              </button>
              <button 
                @click="clearBookmark"
                class="text-xs px-3 py-1 bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors"
              >
                Clear Bookmark
              </button>
            </div>
          </div>
        </div>
        
        <!-- Surah navigation -->
        <div v-if="ayahs.length > 0" class="mb-6">
          <div class="flex flex-wrap gap-2 justify-center">
            <button 
              v-for="surah in uniqueSurahs" 
              :key="surah.number"
              @click="scrollToSurah(surah.name)"
              class="px-3 py-1 text-sm rounded-full transition-colors"
              :class="currentSurah === surah.name ? 'bg-emerald-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            >
              {{ surah.name }}
            </button>
          </div>
        </div>
        
        <!-- Display format toggle -->
        <div v-if="ayahs.length > 0" class="mb-6 flex justify-center">
          <div class="inline-flex rounded-md shadow-sm" role="group">
            <button
              @click="pageFormat = false"
              type="button"
              class="px-4 py-2 text-sm font-medium rounded-l-lg focus:z-10 focus:ring-2 focus:ring-emerald-500 transition-colors"
              :class="!pageFormat ? 'bg-emerald-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            >
              <span class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
                Line Format
              </span>
            </button>
            <button
              @click="pageFormat = true"
              type="button"
              class="px-4 py-2 text-sm font-medium rounded-r-lg focus:z-10 focus:ring-2 focus:ring-emerald-500 transition-colors"
              :class="pageFormat ? 'bg-emerald-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            >
              <span class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
                Page Format
              </span>
            </button>
          </div>
        </div>
        
        <!-- Ayahs display -->
        <div v-if="ayahs.length > 0" class="quran-content">
          <!-- Line-by-line format -->
          <div v-if="!pageFormat">
            <div v-for="(ayah, index) in ayahs" :key="ayah.number">
              <!-- Surah header when changing to a new surah -->
              <div 
                v-if="index === 0 || ayahs[index-1].surah.name !== ayah.surah.name" 
                class="surah-header mb-6 mt-8"
                :id="`surah-${ayah.surah.name}`"
              >
                <h2 class="text-2xl font-bold text-center mb-2">{{ ayah.surah.name }}</h2>
                <div class="h-0.5 bg-emerald-100 w-24 mx-auto"></div>
                
                <!-- Display Bismillah after surah header except for Surah At-Tawbah -->
                <div v-if="shouldDisplayBismillah(ayah.surah.number)" class="text-center mt-4 mb-6">
                  <p class="font-arabic text-2xl">
                    {{ extractBismillah(ayahs.find(a => a.surah.number === ayah.surah.number && a.numberInSurah === 1)?.text) }}
                  </p>
                </div>
              </div>
              
              <!-- Ayah text -->
              <div 
                :id="`ayah-${ayah.number}`"
                class="ayah mb-4 pb-4 border-b border-gray-100"
                :class="{ 'bookmark-active': bookmarkPosition && bookmarkPosition.ayahNumber === ayah.number }"
              >
                <div class="flex justify-between items-start mb-2">
                  <button 
                    @click="saveBookmark(ayah.number)"
                    class="bookmark-button text-gray-400 hover:text-emerald-600 transition-colors"
                    :class="{ 'text-emerald-600': bookmarkPosition && bookmarkPosition.ayahNumber === ayah.number }"
                    title="Bookmark this ayah"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
                    </svg>
                  </button>
                  <p class="text-right font-arabic text-2xl leading-loose">
                    <!-- Only show cleaned text without bismillah since it's shown in the surah header -->
                    {{ cleanAyahText(ayah.text, ayah.surah.number, ayah.numberInSurah) }}
                  </p>
                </div>
                <div class="flex justify-between items-center text-sm text-gray-500">
                  <span>Ayah {{ ayah.numberInSurah }}</span>
                  <span>{{ ayah.surah.name }} ({{ ayah.surah.number }})</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Page format -->
          <div v-else>
            <div v-for="(surah, surahIndex) in uniqueSurahs" :key="surah.number">
              <!-- Surah header -->
              <div 
                class="surah-header mb-6 mt-8"
                :id="`surah-${surah.name}`"
              >
                <h2 class="text-2xl font-bold text-center mb-2">{{ surah.name }}</h2>
                <div class="h-0.5 bg-emerald-100 w-24 mx-auto"></div>
                
                <!-- Display Bismillah after surah header except for Surah At-Tawbah -->
                <div v-if="shouldDisplayBismillah(surah.number)" class="text-center mt-4 mb-6">
                  <p class="font-arabic text-2xl">
                    {{ extractBismillah(ayahs.find(a => a.surah.number === surah.number && a.numberInSurah === 1)?.text) }}
                  </p>
                </div>
              </div>
              
              <!-- Surah content in page format -->
              <div class="page-format mb-8 pb-4">
                <div class="text-container text-right font-arabic text-2xl">
                  <span 
                    v-for="ayah in ayahs.filter(a => a.surah.number === surah.number)" 
                    :key="ayah.number"
                    :id="`ayah-${ayah.number}`"
                    class="ayah-inline"
                    :class="{ 'bookmark-active-inline': bookmarkPosition && bookmarkPosition.ayahNumber === ayah.number }"
                  >
                    <span class="ayah-text">
                      <!-- Only show cleaned text without bismillah since it's shown in the surah header -->
                      {{ cleanAyahText(ayah.text, ayah.surah.number, ayah.numberInSurah) }}
                    </span>
                    <span class="ayah-number">﴿{{ ayah.numberInSurah }}﴾</span>
                    <button 
                      @click.stop.prevent="saveBookmark(ayah.number)"
                      class="bookmark-inline-button"
                      :class="{ 'active': bookmarkPosition && bookmarkPosition.ayahNumber === ayah.number }"
                      title="Bookmark this ayah"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
                      </svg>
                    </button>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Fallback to formatted text if ayahs are not available -->
        <div v-else class="juz-content prose prose-emerald max-w-none">
          <div v-html="juzText.replace(/\n/g, '<br>')"></div>
        </div>
      </div>
      
      <!-- Progress indicator -->
      <div class="bg-white rounded-xl shadow-md p-4 mb-6 border border-gray-100">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-500">
            Reading Juz {{ props.juzNumber }} of 30
          </div>
          <div class="flex items-center">
            <div class="w-32 bg-gray-200 rounded-full h-2.5 mr-2">
              <div class="bg-emerald-600 h-2.5 rounded-full" :style="{ width: `${(props.juzNumber / 30) * 100}%` }"></div>
            </div>
            <span class="text-sm text-gray-500">{{ Math.round((props.juzNumber / 30) * 100) }}%</span>
          </div>
        </div>
      </div>
      
      <!-- Mark as completed button -->
      <div class="flex justify-center">
        <button 
          @click="markAsCompleted" 
          class="px-6 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-medium rounded-lg shadow-sm hover:from-emerald-700 hover:to-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-colors"
        >
          Mark as Completed
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quran-content {
  direction: rtl;
}

.font-arabic {
  font-family: 'Scheherazade New', 'Traditional Arabic', 'Amiri', serif;
}

.ayah {
  position: relative;
}

.ayah:hover {
  background-color: rgba(16, 185, 129, 0.05);
  border-radius: 0.5rem;
  padding: 0.5rem;
  margin: -0.5rem;
}

/* Page format styles */
.page-format {
  text-align: justify;
  padding: 1rem;
  border-radius: 0.5rem;
  line-height: 2.2;
  word-spacing: 0.1em;
}

.page-format .text-container {
  text-align: justify;
  white-space: normal;
  word-wrap: break-word;
  text-align-last: right;
  overflow-wrap: break-word;
  hyphens: auto;
}

.ayah-inline {
  position: relative;
  display: inline;
  padding: 0 0.05em;
  margin: 0;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
  white-space: normal;
}

.ayah-text {
  position: relative;
  z-index: 1;
  white-space: normal;
  word-wrap: break-word;
}

.ayah-inline:hover {
  background-color: rgba(16, 185, 129, 0.05);
}

.ayah-number {
  font-size: 0.75em;
  color: #10b981;
  margin: 0 0.1em;
  position: relative;
  z-index: 1;
  display: inline-block;
}

/* Bookmark styles */
.bookmark-button {
  flex-shrink: 0;
  margin-top: 0.5rem;
}

.bookmark-active {
  background-color: rgba(16, 185, 129, 0.05);
  border-left: 3px solid #10b981;
  padding-left: 0.5rem;
}

.bookmark-highlight {
  animation: highlight-pulse 3s ease-in-out;
}

/* Different highlight animations for line and page formats */
.ayah.bookmark-highlight {
  position: relative;
}

.ayah.bookmark-highlight::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(16, 185, 129, 0.1);
  border-radius: 0.5rem;
  animation: highlight-pulse 3s ease-in-out;
  z-index: 0;
}

.ayah-inline.bookmark-highlight {
  animation: highlight-pulse-inline 3s ease-in-out;
}

@keyframes highlight-pulse {
  0% { background-color: rgba(16, 185, 129, 0.05); }
  50% { background-color: rgba(16, 185, 129, 0.2); }
  100% { background-color: rgba(16, 185, 129, 0.05); }
}

@keyframes highlight-pulse-inline {
  0% { background-color: rgba(16, 185, 129, 0.1); box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1); }
  50% { background-color: rgba(16, 185, 129, 0.3); box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2); }
  100% { background-color: rgba(16, 185, 129, 0.1); box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1); }
}

.bookmark-active-inline {
  background-color: rgba(16, 185, 129, 0.1);
  border-radius: 0.25rem;
  padding: 0.25rem;
}

.bookmark-inline-button {
  display: none;
  position: absolute;
  top: -0.8rem;
  right: 0.1rem;
  z-index: 10;
  background-color: white;
  border-radius: 50%;
  padding: 0.15rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  color: #d1d5db;
  transition: color 0.2s, transform 0.2s;
}

.bookmark-inline-button.active {
  display: block;
  color: #10b981;
}

.ayah-inline:hover {
  background-color: rgba(16, 185, 129, 0.05);
  border-radius: 0.25rem;
  padding: 0 0.05em;
}

.ayah-inline:hover .bookmark-inline-button {
  display: block;
  transform: scale(1.1);
}

.bookmark-inline-button:hover {
  color: #10b981;
  transform: scale(1.2);
}
</style> 