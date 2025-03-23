<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n();
const isOpen = ref(false);
const dropdownRef = ref(null);
const buttonRef = ref(null);

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
  if (!dropdownRef.value || !buttonRef.value) return;
  
  if (isOpen.value && 
      !dropdownRef.value.contains(event.target) && 
      !buttonRef.value.contains(event.target)) {
    isOpen.value = false;
  }
}

// Toggle dropdown
function toggleDropdown(event) {
  // Prevent event from bubbling up to parent elements
  event.stopPropagation();
  isOpen.value = !isOpen.value;
}

// Change language
function changeLanguage(langCode, event) {
  // Prevent event from bubbling
  if (event) event.stopPropagation();
  
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
  <div class="relative inline-block text-left language-dropdown-container">
    <button 
      ref="buttonRef"
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
      ref="dropdownRef"
      class="dropdown-menu origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
      role="menu"
      aria-orientation="vertical"
      tabindex="-1"
    >
      <div class="py-1" role="none">
        <a 
          v-for="lang in languages" 
          :key="lang.code"
          href="#"
          @click.prevent="(e) => changeLanguage(lang.code, e)"
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
.language-dropdown-container {
  position: relative;
  display: inline-flex;
}

.dropdown-menu {
  z-index: 50;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
}

/* Desktop adjustments */
@media (min-width: 769px) {
  .dropdown-menu {
    min-width: 180px;
    position: absolute;
    top: calc(100% + 5px);
    right: 0;
  }
}

/* Mobile adjustments */
@media (max-width: 768px) {
  .mobile-language .dropdown-menu {
    position: absolute;
    right: 0;
    left: auto;
    width: 100%;
    max-width: 200px;
  }
}
</style> 