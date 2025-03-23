<template>
  <div class="audio-controls-container">
    <!-- Simple Controls -->
    <div v-if="simplified && audioPlayer" class="audio-controls-simple">
      <div class="flex space-x-2">
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
    
    <!-- Listen to Full Surah Button -->
    <div v-if="showListenButton && !isPlayingFullSurah" class="listen-surah-container">
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
    
    <!-- Full Controls -->
    <div v-if="!simplified && audioPlayer && !audioPlayer.paused" class="audio-controls-full">
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
    
    <!-- Floating Audio Controls -->
    <div v-if="floating && audioPlayer" class="floating-audio-controls">
      <div class="floating-controls-content">
        <div class="flex items-center space-x-3">
          <button @click="stopAudio" class="audio-control-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
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
        </div>
        
        <div class="audio-progress-wrapper">
          <div class="audio-time">{{ formatTime(audioProgress) }}</div>
          
          <div class="audio-progress-container" @click="seekAudio">
            <div class="audio-progress-bar" :style="{ width: `${progressPercentage}%` }"></div>
          </div>
          
          <div class="audio-time">{{ formatTime(audioDuration) }}</div>
        </div>
        
        <div class="now-playing-info">
          <span v-if="currentSurah">{{ currentSurah.name }} - {{ $t('quran.surah') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AudioControls',
  props: {
    audioPlayer: {
      type: Object,
      default: null
    },
    simplified: {
      type: Boolean,
      default: false
    },
    floating: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    isPlayingFullSurah: {
      type: Boolean,
      default: false
    },
    downloadingSurahAudio: {
      type: Boolean,
      default: false
    },
    paused: {
      type: Boolean,
      default: false
    },
    audioProgress: {
      type: Number,
      default: 0
    },
    audioDuration: {
      type: Number,
      default: 0
    },
    currentSurah: {
      type: Object,
      default: null
    },
    showListenButton: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    togglePause() {
      this.$emit('toggle-pause')
    },
    
    stopAudio() {
      this.$emit('stop-audio')
    },
    
    listenToFullSurah() {
      this.$emit('listen-to-full-surah')
    },
    
    seekAudio(event) {
      this.$emit('seek-audio', event)
    },
    
    formatTime(seconds) {
      if (!seconds || isNaN(seconds)) return '0:00'
      
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = Math.floor(seconds % 60)
      
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
    }
  },
  computed: {
    progressPercentage() {
      if (!this.audioDuration || this.audioDuration === 0) return 0;
      return (this.audioProgress / this.audioDuration) * 100;
    }
  }
}
</script>

<style scoped>
.audio-button {
  @apply px-4 py-2 bg-indigo-600 text-white rounded-lg flex items-center justify-center hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-indigo-600 transition-colors;
}

.audio-controls-full {
  @apply flex items-center space-x-2 bg-gray-100 rounded-lg p-2;
}

.audio-control-button {
  @apply p-2 bg-indigo-600 text-white rounded-full hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors;
}

.audio-control-button.play-pause {
  @apply h-10 w-10 flex items-center justify-center;
}

.audio-time {
  @apply text-sm text-gray-600 font-mono;
}

.audio-progress-container {
  @apply flex-1 h-2 bg-gray-300 rounded-full cursor-pointer;
}

.audio-progress-bar {
  @apply h-2 bg-indigo-600 rounded-full transition-all duration-100;
}

.floating-audio-controls {
  @apply fixed bottom-0 left-0 w-full bg-white shadow-lg border-t border-gray-200 p-3 z-50;
}

.floating-controls-content {
  @apply max-w-4xl mx-auto flex flex-col md:flex-row md:items-center space-y-2 md:space-y-0 md:space-x-4;
}

.audio-progress-wrapper {
  @apply flex-1 flex items-center space-x-2;
}

.now-playing-info {
  @apply text-sm text-gray-600 font-medium truncate;
}
</style> 