<template>
  <div class="audio-controls-container">
    <!-- Floating Audio Controls -->
    <div v-if="audioPlayer" class="floating-audio-controls">
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
          <span v-if="currentSurah && currentPlayingVerse" class="now-playing-text">
            <span class="audio-time-display mr-2">{{ formatTime(audioProgress) }}</span>
            <span class="surah-name mr-1">{{ currentSurah.name }}</span> - 
            <span class="ayah-number ml-1">{{ $t('quran.ayah') }} {{ currentPlayingVerse }}</span>
          </span>
          <span v-else-if="currentSurah" class="now-playing-text">
            <span class="audio-time-display mr-2">{{ formatTime(audioProgress) }}</span>
            <span class="surah-name">{{ currentSurah.name }}</span>
          </span>
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
    currentPlayingVerse: {
      type: Number,
      default: null
    }
  },
  methods: {
    togglePause() {
      this.$emit('toggle-pause')
    },
    
    stopAudio() {
      this.$emit('stop-audio')
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

.now-playing-text {
  @apply inline-flex items-center;
}

.audio-time-display {
  @apply text-sm font-mono;
}

.surah-name {
  @apply text-sm font-medium;
}

.ayah-number {
  @apply text-sm font-mono;
}
</style> 