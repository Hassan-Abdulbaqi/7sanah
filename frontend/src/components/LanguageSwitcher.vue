<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n();
const isOpen = ref(false);

// Available languages with language codes instead of country codes
const languages = [
  { code: 'en', name: 'English', flag: '🇬🇧', dir: 'ltr', langCode: 'EN' },
  { code: 'ar', name: 'العربية', flag: '🇸🇦', dir: 'ltr', langCode: 'AR' },
  { code: 'ku', name: 'کوردی', flag: '🇮🇶', dir: 'rtl', langCode: 'KU' },
  { code: 'fa', name: 'فارسی', flag: '🇮🇷', dir: 'rtl', langCode: 'FA' }
];

// Current language
const currentLanguage = computed(() => {
  return languages.find(lang => lang.code === locale.value) || languages[0];
});

// Handle document click to close dropdown
function handleClickOutside(event) {
  const dropdown = document.getElementById('language-dropdown');
  const button = document.getElementById('language-button');
  
  if (isOpen.value && dropdown && button) {
    if (!dropdown.contains(event.target) && !button.contains(event.target)) {
      isOpen.value = false;
    }
  }
}

// Toggle dropdown
function toggleDropdown() {
  isOpen.value = !isOpen.value;
}

// Change language
function changeLanguage(langCode) {
  // Update locale
  locale.value = langCode;
  
  // Store in localStorage
  localStorage.setItem('language', langCode);
  
  // Get language direction
  const lang = languages.find(l => l.code === langCode);
  if (lang) {
    // Set document direction
    document.documentElement.dir = lang.dir;
    document.documentElement.lang = langCode;
  }
  
  // Close dropdown
  isOpen.value = false;
}

// Set initial document direction
onMounted(() => {
  document.documentElement.dir = currentLanguage.value.dir;
  document.documentElement.lang = locale.value;
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div class="relative inline-block text-left">
    <button 
      id="language-button"
      type="button" 
      @click="toggleDropdown"
      class="inline-flex justify-center items-center px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-md hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500"
    >
      <span class="mr-1">{{ currentLanguage.langCode }}</span>
      <span class="hidden md:inline">{{ currentLanguage.name }}</span>
      <svg class="w-5 h-5 ml-2 -mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>

    <div 
      v-show="isOpen"
      id="language-dropdown"
      class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="language-button"
      tabindex="-1"
    >
      <div class="py-1" role="none">
        <a 
          v-for="lang in languages" 
          :key="lang.code"
          href="#"
          @click.prevent="changeLanguage(lang.code)"
          :class="[
            'block px-4 py-2 text-sm hover:bg-gray-100',
            lang.code === locale ? 'bg-gray-100 text-gray-900' : 'text-gray-700'
          ]"
          role="menuitem"
          tabindex="-1"
        >
          <div class="flex items-center">
            <span class="mr-2 w-8 text-center">{{ lang.langCode }}</span>
            <span>{{ lang.name }}</span>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Add any additional styling here */
</style> 