<script setup>
import { ref, computed, watch, defineProps, defineEmits, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { store } from '../store';

const { t } = useI18n();

const props = defineProps({
  khatmahs: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['select-khatmah']);

const searchQuery = ref('');
const searchFocused = ref(false);
const currentPage = ref(1);
const pageSize = ref(9);

// Computed property for filtered khatmahs
const filteredKhatmahs = computed(() => {
  if (!searchQuery.value.trim()) {
    return props.khatmahs;
  }
  
  const query = searchQuery.value.toLowerCase();
  return props.khatmahs.filter(khatmah => {
    // Search in khatmah name
    if (khatmah.name.toLowerCase().includes(query)) {
      return true;
    }
    
    // Search in participants
    if (khatmah.participants && khatmah.participants.some(p => 
      p.name.toLowerCase().includes(query)
    )) {
      return true;
    }
    
    return false;
  });
});

// Computed property for my created khatmahs
const myCreatedKhatmahs = computed(() => {
  return store.getMyCreatedKhatmahs();
});

// Computed property for total pages
const totalPages = computed(() => {
  return Math.ceil(store.pagination.count / pageSize.value);
});

// Computed property for page numbers to display
const pageNumbers = computed(() => {
  const pages = [];
  const maxVisiblePages = 5;
  
  if (totalPages.value <= maxVisiblePages) {
    // If we have fewer pages than the max, show all pages
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i);
    }
  } else {
    // Always show first page
    pages.push(1);
    
    // Calculate start and end of the middle section
    let start = Math.max(2, currentPage.value - 1);
    let end = Math.min(totalPages.value - 1, currentPage.value + 1);
    
    // Adjust if we're at the beginning or end
    if (currentPage.value <= 2) {
      end = Math.min(totalPages.value - 1, 4);
    } else if (currentPage.value >= totalPages.value - 1) {
      start = Math.max(2, totalPages.value - 3);
    }
    
    // Add ellipsis if needed
    if (start > 2) {
      pages.push('...');
    }
    
    // Add middle pages
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    
    // Add ellipsis if needed
    if (end < totalPages.value - 1) {
      pages.push('...');
    }
    
    // Always show last page
    if (totalPages.value > 1) {
      pages.push(totalPages.value);
    }
  }
  
  return pages;
});

function selectKhatmah(khatmahId) {
  emit('select-khatmah', khatmahId);
}

function clearSearch() {
  searchQuery.value = '';
}

function focusSearch() {
  searchFocused.value = true;
}

function blurSearch() {
  searchFocused.value = false;
}

async function changePage(page) {
  if (page === '...' || page === currentPage.value) {
    return;
  }
  
  currentPage.value = page;
  await store.fetchKhatmahs(page, pageSize.value);
}

async function goToNextPage() {
  if (currentPage.value < totalPages.value) {
    await changePage(currentPage.value + 1);
  }
}

async function goToPreviousPage() {
  if (currentPage.value > 1) {
    await changePage(currentPage.value - 1);
  }
}

// Handle keyboard shortcuts
function handleKeyDown(event) {
  // Ctrl+K or Cmd+K to focus search
  if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
    event.preventDefault();
    document.getElementById('khatmah-search').focus();
  }
  
  // Escape to clear search when focused
  if (event.key === 'Escape' && searchFocused.value) {
    clearSearch();
    document.getElementById('khatmah-search').blur();
  }
}

// Add event listeners on mount and remove on unmount
onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});

// Watch for search query changes and reset to page 1
watch(searchQuery, async () => {
  if (currentPage.value !== 1) {
    currentPage.value = 1;
    await store.fetchKhatmahs(1, pageSize.value);
  }
});

// Initial fetch with pagination
onMounted(async () => {
  await store.fetchKhatmahs(currentPage.value, pageSize.value);
});
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-8 text-gray-800 flex items-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-2 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
        <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z" />
      </svg>
      {{ t('khatmahList.title') }}
    </h2>
    
    <!-- Search Bar -->
    <div class="relative mb-6">
      <div class="flex items-center bg-white rounded-lg border border-gray-300 focus-within:ring-2 focus-within:ring-emerald-500 focus-within:border-emerald-500 transition-colors">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
          </svg>
        </div>
        <input
          id="khatmah-search"
          v-model="searchQuery"
          type="text"
          class="block w-full pl-10 pr-10 py-3 rounded-lg focus:outline-none"
          :placeholder="t('khatmahList.search')"
          @focus="focusSearch"
          @blur="blurSearch"
        />
        <div v-if="searchQuery" class="absolute inset-y-0 right-0 pr-3 flex items-center">
          <button 
            @click="clearSearch" 
            class="text-gray-400 hover:text-gray-600 focus:outline-none"
            aria-label="Clear search"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        <div v-else class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-xs text-gray-400">
          <span class="hidden sm:inline">Ctrl+K</span>
        </div>
      </div>
    </div>
    
    <!-- My Created Khatmahs Section -->
    <div v-if="myCreatedKhatmahs.length > 0" class="mb-8">
      <h3 class="text-lg font-semibold mb-4 text-gray-800 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-600" viewBox="0 0 20 20" fill="currentColor">
          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
        </svg>
        {{ t('khatmahList.myCreatedKhatmahs') }}
      </h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="khatmah in myCreatedKhatmahs" 
          :key="khatmah.id"
          class="bg-blue-50 border border-blue-100 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer"
          @click="selectKhatmah(khatmah.id)"
        >
          <div class="p-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-semibold text-gray-800">{{ khatmah.name }}</h3>
              <span class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">{{ t('khatmahList.creator') }}</span>
            </div>
            <div class="flex items-center justify-between text-sm text-gray-500">
              <div>{{ t('khatmahList.created') }}: {{ new Date(khatmah.created_at).toLocaleDateString() }}</div>
              <div v-if="khatmah.is_private" class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                {{ t('khatmahList.private') }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Search Results Info -->
    <div class="flex justify-between items-center mb-4">
      <div>
        <span class="text-sm text-gray-500">
          {{ filteredKhatmahs.length }} 
          {{ filteredKhatmahs.length === 1 
            ? t('khatmahList.participants', 1) 
            : t('khatmahList.participants', filteredKhatmahs.length) }}
          <span v-if="searchQuery"> for "{{ searchQuery }}"</span>
          <span v-if="!searchQuery"> (page {{ currentPage }} of {{ totalPages }})</span>
        </span>
      </div>
      <div v-if="searchQuery" class="text-sm">
        <button 
          @click="clearSearch" 
          class="text-emerald-600 hover:text-emerald-700 focus:outline-none"
        >
          {{ t('khatmahList.clearSearch') }}
        </button>
      </div>
    </div>
    
    <!-- No Results Message -->
    <div v-if="filteredKhatmahs.length === 0" class="bg-gray-50 rounded-lg p-8 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-2">{{ t('khatmahList.noKhatmahs') }}</h3>
      <p class="text-gray-500 mb-4">
        {{ searchQuery 
          ? `${t('khatmahList.noKhatmahsMatch')} "${searchQuery}"`
          : t('khatmahList.noKhatmahsAvailable') 
        }}
      </p>
      <button 
        v-if="searchQuery"
        @click="clearSearch" 
        class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
      >
        {{ t('khatmahList.clearSearch') }}
      </button>
    </div>
    
    <!-- Khatmah List -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="khatmah in filteredKhatmahs" 
        :key="khatmah.id"
        class="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer"
        @click="selectKhatmah(khatmah.id)"
      >
        <div v-if="khatmah.image_url" class="h-32 overflow-hidden">
          <img :src="khatmah.image_url" :alt="khatmah.name" class="w-full h-full object-cover" />
        </div>
        <div class="p-4">
          <h3 class="font-semibold text-gray-800 mb-2">{{ khatmah.name }}</h3>
          
          <div class="flex flex-wrap gap-2 mb-2">
            <div class="text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
              </svg>
              {{ khatmah.participant_count }} 
              {{ khatmah.participant_count === 1 
                ? t('khatmahList.participants', 1) 
                : t('khatmahList.participants', khatmah.participant_count) }}
            </div>
            
            <div class="text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
              </svg>
              {{ khatmah.completed_juz_count }}/30 {{ t('khatmahList.completed') }}
            </div>
            
            <div v-if="store.isKhatmahCreator(khatmah.id)" class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
              {{ t('khatmahList.creator') }}
            </div>
          </div>
          
          <div class="flex justify-between items-center text-sm text-gray-500">
            <div>{{ t('khatmahList.created') }}: {{ new Date(khatmah.created_at).toLocaleDateString() }}</div>
            <div v-if="khatmah.end_date" class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ t('khatmahList.ends') }}: {{ new Date(khatmah.end_date).toLocaleDateString() }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Pagination -->
    <div v-if="!searchQuery && totalPages > 1" class="mt-8 flex justify-center">
      <nav class="flex items-center space-x-1">
        <!-- Previous Page Button -->
        <button 
          @click="goToPreviousPage" 
          class="px-3 py-2 rounded-md text-sm font-medium"
          :class="currentPage > 1 
            ? 'text-gray-700 hover:bg-gray-100' 
            : 'text-gray-400 cursor-not-allowed'"
          :disabled="currentPage <= 1"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <!-- Page Numbers -->
        <template v-for="(page, index) in pageNumbers" :key="index">
          <button 
            v-if="page !== '...'"
            @click="changePage(page)" 
            class="px-3 py-2 rounded-md text-sm font-medium"
            :class="page === currentPage 
              ? 'bg-emerald-600 text-white' 
              : 'text-gray-700 hover:bg-gray-100'"
          >
            {{ page }}
          </button>
          <span 
            v-else
            class="px-2 py-2 text-gray-500"
          >
            ...
          </span>
        </template>
        
        <!-- Next Page Button -->
        <button 
          @click="goToNextPage" 
          class="px-3 py-2 rounded-md text-sm font-medium"
          :class="currentPage < totalPages 
            ? 'text-gray-700 hover:bg-gray-100' 
            : 'text-gray-400 cursor-not-allowed'"
          :disabled="currentPage >= totalPages"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </nav>
    </div>
  </div>
</template> 