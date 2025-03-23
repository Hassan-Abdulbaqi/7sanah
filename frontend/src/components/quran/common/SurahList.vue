<template>
  <div class="surah-selection">
    <h3 class="font-medium mb-2">{{ $t('quran.selectSurah') }}</h3>
    
    <!-- Surah buttons grid -->
    <div class="surah-buttons-grid">
      <button 
        v-for="surah in surahs" 
        :key="surah.number" 
        @click="selectSurah(surah.number)"
        :class="['surah-button', { active: selectedSurah === surah.number }]"
        :disabled="loading"
      >
        <span class="surah-number">{{ surah.number }}</span>
        <span class="surah-name">{{ surah.englishName }}</span>
      </button>
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
  methods: {
    selectSurah(surahNumber) {
      this.$emit('select-surah', surahNumber)
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
  min-height: 70px;
}

.surah-button.active {
  @apply bg-indigo-100 border-indigo-400;
}

.surah-number {
  @apply text-indigo-600 font-bold mb-1;
}

.surah-name {
  @apply text-gray-700 text-center;
  font-size: 0.8rem;
  line-height: 1.2;
}
</style> 