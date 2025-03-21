<template>
  <div class="tasbeeh-container">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">{{ $t('features.tasbeeh.title') }}</h2>
    
    <div class="tasbeeh-card">
      <div class="tasbeeh-selection">
        <label for="tasbeeh-select" class="block text-sm font-medium text-gray-700 mb-2">
          {{ $t('features.tasbeeh.selectTasbeeh') }}
        </label>
        <select 
          id="tasbeeh-select" 
          v-model="selectedTasbeeh" 
          class="w-full p-2 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
          @change="handleTasbeehChange"
        >
          <option 
            v-for="tasbeeh in tasbeehs" 
            :key="tasbeeh.id" 
            :value="tasbeeh.id"
          >
            {{ tasbeeh.name[$i18n.locale] || tasbeeh.name.en }} 
            <template v-if="!tasbeeh.isFreeMode">({{ tasbeeh.count }})</template>
            <template v-else>(∞)</template>
          </option>
        </select>
      </div>

      <div class="tasbeeh-info my-4">
        <p v-if="!isTasbeehFreeMode" class="text-center text-lg font-arabic">{{ currentTasbeeh.phrase }}</p>
        <p v-if="!isTasbeehFreeMode" class="text-center text-sm text-gray-600 mt-2">{{ currentTasbeeh.translation }}</p>
        
        <p v-if="isTasbeehFreeMode" class="text-center text-lg font-arabic my-4">
          {{ $t('features.tasbeeh.freeMode.description') }}
        </p>
        
        <!-- Current phrase to be recited (specifically for multi-part tasbeeh) -->
        <div v-if="!isTasbeehFreeMode && currentTasbeeh.parts && currentTasbeeh.parts.length > 0" class="current-phrase-container mt-4">
          <p class="text-center font-bold text-emerald-600">{{ $t('features.tasbeeh.currentPhrase') }}:</p>
          <p class="text-center text-xl font-arabic mt-2 current-phrase">{{ currentPart.arabic }}</p>
          <p class="text-center text-sm text-gray-600 mt-1">{{ currentPart.translation }}</p>
          
          <div class="flex items-center justify-center mt-3">
            <div class="part-progress-container">
              <div 
                v-for="(part, index) in currentTasbeeh.parts" 
                :key="index"
                :class="['part-indicator', { 'active': index === currentPart.partIndex }]"
              >
                {{ index + 1 }}
              </div>
            </div>
          </div>
          
          <p class="text-center text-sm text-emerald-700 mt-2">
            {{ currentPart.partProgress }} / {{ currentPart.count }}
          </p>
        </div>
        
        <div class="flex justify-between items-center mt-4">
          <span v-if="!isTasbeehFreeMode" class="text-sm text-gray-500">{{ $t('features.tasbeeh.target') }}: {{ currentTasbeeh.count }}</span>
          <span v-else class="text-sm text-gray-500">{{ $t('features.tasbeeh.target') }}: ∞</span>
          
          <span class="text-sm text-gray-500">{{ $t('features.tasbeeh.remaining') }}: {{ remainingCount }}</span>
        </div>
        
        <!-- Free mode counter info -->
        <div v-if="isTasbeehFreeMode" class="text-center mt-3">
          <p class="text-sm text-emerald-700">
            {{ $t('features.tasbeeh.freeMode.cycles') }}: {{ Math.floor(counter / 100) }}
          </p>
          <p class="text-sm text-emerald-700">
            {{ $t('features.tasbeeh.freeMode.current') }}: {{ counter % 100 }} / 100
          </p>
        </div>
      </div>

      <div class="counter-display">
        <div class="counter-circle" :style="progressStyle">
          <span class="counter-number">{{ counter }}</span>
        </div>
      </div>
      
      <!-- Completion message - shown when tasbeeh is completed -->
      <div 
        v-if="isCompleted" 
        class="completion-message"
        :class="{ 'animate-in': isCompleted }"
      >
        <p class="acceptance-prayer font-arabic">تَقَبَّلَ اللهُ</p>
        <p class="acceptance-translation">{{ $t('features.tasbeeh.acceptanceMessage') }}</p>
      </div>

      <div class="counter-controls">
        <button 
          @click="incrementCounter"
          class="increment-btn"
          :disabled="!isTasbeehFreeMode && counter >= currentTasbeeh.count"
        >
          <span class="btn-text">{{ $t('features.tasbeeh.increment') }}</span>
        </button>
        <button 
          @click="resetCounter"
          class="reset-btn"
        >
          <span class="btn-text">{{ $t('features.tasbeeh.reset') }}</span>
        </button>
      </div>

      <div class="vibration-setting mt-4">
        <label class="inline-flex items-center">
          <input type="checkbox" v-model="vibrationEnabled" class="form-checkbox h-5 w-5 text-emerald-600">
          <span class="ml-2 text-gray-700">{{ $t('features.tasbeeh.vibration') }}</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TasbeehCounter',
  data() {
    return {
      counter: 0,
      selectedTasbeeh: 'tasbih-fatima',
      vibrationEnabled: true,
      isFreeMode: false,
      tasbeehs: [
        {
          id: 'tasbih-fatima',
          name: {
            en: 'Tasbeeh Al-Zahra',
            ar: 'تسبيح الزهراء'
          },
          phrase: 'سبحان الله (33) الحمد لله (33) الله أكبر (34)',
          translation: 'SubhanAllah (33) Alhamdulillah (33) Allahu Akbar (34)',
          count: 100,
          parts: [
            {
              arabic: 'سبحان الله',
              translation: 'Glory be to Allah',
              count: 33
            },
            {
              arabic: 'الحمد لله',
              translation: 'Praise be to Allah',
              count: 33
            },
            {
              arabic: 'الله أكبر',
              translation: 'Allah is Greater',
              count: 34
            }
          ]
        },
        {
          id: 'subhanallah',
          name: {
            en: 'SubhanAllah',
            ar: 'سبحان الله'
          },
          phrase: 'سبحان الله',
          translation: 'Glory be to Allah',
          count: 33
        },
        {
          id: 'alhamdulillah',
          name: {
            en: 'Alhamdulillah',
            ar: 'الحمد لله'
          },
          phrase: 'الحمد لله',
          translation: 'Praise be to Allah',
          count: 33
        },
        {
          id: 'allahuakbar',
          name: {
            en: 'Allahu Akbar',
            ar: 'الله أكبر'
          },
          phrase: 'الله أكبر',
          translation: 'Allah is Greater',
          count: 34
        },
        {
          id: 'istighfar',
          name: {
            en: 'Istighfar',
            ar: 'استغفار'
          },
          phrase: 'أستغفر الله',
          translation: 'I seek forgiveness from Allah',
          count: 100
        },
        {
          id: 'hawqala',
          name: {
            en: 'Hawqala',
            ar: 'حوقلة'
          },
          phrase: 'لا حول ولا قوة إلا بالله',
          translation: 'There is no power nor strength except from Allah',
          count: 100
        },
        {
          id: 'free-mode',
          name: {
            en: 'Free Mode',
            ar: 'وضع حر'
          },
          phrase: '',
          translation: '',
          count: Infinity,
          isFreeMode: true
        }
      ]
    }
  },
  computed: {
    currentTasbeeh() {
      return this.tasbeehs.find(t => t.id === this.selectedTasbeeh) || this.tasbeehs[0]
    },
    isTasbeehFreeMode() {
      return this.currentTasbeeh.isFreeMode === true
    },
    localizedTasbeehName() {
      const locale = this.$i18n.locale;
      return this.currentTasbeeh.name[locale] || this.currentTasbeeh.name.en;
    },
    displayedCount() {
      return this.isTasbeehFreeMode ? this.counter : Math.min(this.counter, this.currentTasbeeh.count);
    },
    remainingCount() {
      if (this.isTasbeehFreeMode) {
        return '∞';
      }
      return this.currentTasbeeh.count - this.counter;
    },
    isCompleted() {
      if (this.isTasbeehFreeMode) {
        return false;
      }
      return this.counter >= this.currentTasbeeh.count;
    },
    progressStyle() {
      if (this.isTasbeehFreeMode) {
        // For free mode, use a repeating progress that cycles every 100 counts
        const cycleProgress = (this.counter % 100) / 100 * 100;
        return {
          background: `conic-gradient(var(--primary-color) ${cycleProgress}%, var(--card-bg) 0)`
        }
      }
      
      const progress = Math.min(this.counter / this.currentTasbeeh.count * 100, 100);
      return {
        background: `conic-gradient(var(--primary-color) ${progress}%, var(--card-bg) 0)`
      }
    },
    currentPart() {
      // For tasbeeh with multiple parts (like Tasbeeh Al-Zahra)
      if (this.currentTasbeeh.parts && this.currentTasbeeh.parts.length > 0) {
        const parts = this.currentTasbeeh.parts;
        let currentCount = 0;
        
        // Find which part we're currently in based on completed counts
        for (let i = 0; i < parts.length; i++) {
          currentCount += parts[i].count;
          
          // If we haven't reached this part's total count yet, this is our current part
          if (this.counter < currentCount) {
            return {
              ...parts[i],
              partIndex: i,
              partStartCount: currentCount - parts[i].count,
              partEndCount: currentCount - 1,
              partProgress: this.counter - (currentCount - parts[i].count) + 1,
              totalPartsCount: parts.length
            };
          }
        }
        
        // If we've exceeded all counts, return the last part
        const lastPart = parts[parts.length - 1];
        return {
          ...lastPart,
          partIndex: parts.length - 1,
          partStartCount: currentCount - lastPart.count,
          partEndCount: currentCount - 1,
          partProgress: lastPart.count,
          totalPartsCount: parts.length
        };
      }
      
      // For single-part tasbeeh or free mode, return a default object
      return {
        arabic: this.currentTasbeeh.phrase,
        translation: this.currentTasbeeh.translation,
        count: this.isTasbeehFreeMode ? Infinity : this.currentTasbeeh.count,
        partIndex: 0,
        partStartCount: 0,
        partEndCount: this.isTasbeehFreeMode ? Infinity : this.currentTasbeeh.count - 1,
        partProgress: this.counter + 1,
        totalPartsCount: 1
      }
    },
    localStorageKey() {
      return `tasbeeh_counter_${this.selectedTasbeeh}`;
    }
  },
  created() {
    // Check if vibration setting is saved in localStorage
    const savedVibrationSetting = localStorage.getItem('tasbeeh_vibration_enabled');
    if (savedVibrationSetting !== null) {
      this.vibrationEnabled = savedVibrationSetting === 'true';
    }
    
    // Load the counter value from localStorage
    this.loadFromLocalStorage();
  },
  watch: {
    selectedTasbeeh() {
      this.loadFromLocalStorage();
    },
    vibrationEnabled() {
      // Save vibration setting when it changes
      localStorage.setItem('tasbeeh_vibration_enabled', this.vibrationEnabled);
    }
  },
  methods: {
    handleTasbeehChange() {
      // When tasbeeh type changes, load the correct progress from localStorage
      this.loadFromLocalStorage();
    },
    incrementCounter() {
      if (this.isTasbeehFreeMode || this.counter < this.currentTasbeeh.count) {
        // Store current part info before incrementing
        const prevPart = this.currentPart.partIndex;
        
        // Increment the counter
        this.counter++;
        
        // Save to local storage
        this.saveToLocalStorage();
        
        // Get new part info
        const newPart = this.currentPart.partIndex;
        
        // Vibrate if enabled and available
        if (this.vibrationEnabled && 'vibrate' in navigator) {
          // Short vibration for every count
          navigator.vibrate(20);
          
          // Part transition vibration (for multi-part tasbeeh)
          if (!this.isTasbeehFreeMode && this.currentTasbeeh.parts && prevPart !== newPart) {
            // Special vibration when transitioning between parts
            setTimeout(() => navigator.vibrate([50, 30, 50]), 100);
          }
          
          // Additional vibration at completion
          if (!this.isTasbeehFreeMode && this.counter === this.currentTasbeeh.count) {
            setTimeout(() => navigator.vibrate([100, 50, 100]), 200);
          }
          
          // For free mode, special vibration at every 100 counts
          if (this.isTasbeehFreeMode && this.counter % 100 === 0) {
            setTimeout(() => navigator.vibrate([100, 50, 100]), 200);
          }
        }
      }
    },
    resetCounter() {
      this.counter = 0;
      this.saveToLocalStorage();
    },
    saveToLocalStorage() {
      try {
        localStorage.setItem(this.localStorageKey, JSON.stringify({
          counter: this.counter,
          timestamp: new Date().getTime()
        }));
      } catch (e) {
        console.error('Failed to save tasbeeh state to localStorage:', e);
      }
    },
    loadFromLocalStorage() {
      try {
        const savedData = localStorage.getItem(this.localStorageKey);
        if (savedData) {
          const data = JSON.parse(savedData);
          this.counter = data.counter || 0;
          
          // Handle case where we're loading regular tasbeeh that was completed
          if (!this.isTasbeehFreeMode && this.counter > this.currentTasbeeh.count) {
            this.counter = this.currentTasbeeh.count;
          }
        } else {
          this.counter = 0;
        }
      } catch (e) {
        console.error('Failed to load tasbeeh state from localStorage:', e);
        this.counter = 0;
      }
    }
  }
}
</script>

<style scoped>
.tasbeeh-container {
  max-width: 600px;
  margin: 0 auto;
}

.tasbeeh-card {
  background-color: var(--card-bg);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.font-arabic {
  font-family: 'Scheherazade New', 'Amiri', serif;
  font-size: 1.5rem;
  line-height: 1.7;
}

.current-phrase-container {
  padding: 1rem;
  background-color: rgba(16, 185, 129, 0.05);
  border-radius: 12px;
  border: 1px dashed var(--primary-color);
}

.current-phrase {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-color);
}

.completion-message {
  background-color: rgba(16, 185, 129, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  text-align: center;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.5s ease;
}

.completion-message.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.acceptance-prayer {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.acceptance-translation {
  color: var(--text-secondary);
  font-style: italic;
}

.part-progress-container {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  margin: 0.5rem 0;
}

.part-indicator {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--hover-color);
  color: var(--text-color);
  font-weight: bold;
  transition: all 0.3s ease;
}

.part-indicator.active {
  background-color: var(--primary-color);
  color: white;
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
}

.counter-display {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
}

.counter-circle {
  position: relative;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1), inset 0 0 15px rgba(0, 0, 0, 0.1);
}

.counter-circle::before {
  content: '';
  position: absolute;
  width: 160px;
  height: 160px;
  border-radius: 50%;
  background-color: var(--card-bg);
  z-index: 0;
}

.counter-number {
  position: relative;
  z-index: 1;
  font-size: 3rem;
  font-weight: bold;
  color: var(--primary-color);
}

.counter-controls {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.increment-btn, .reset-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.increment-btn {
  background-color: var(--primary-color);
  color: white;
}

.increment-btn:hover:not(:disabled) {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
}

.increment-btn:disabled {
  background-color: var(--text-secondary);
  cursor: not-allowed;
}

.reset-btn {
  background-color: var(--hover-color);
  color: var(--text-color);
}

.reset-btn:hover {
  background-color: var(--border-color);
}

.btn-text {
  font-size: 1rem;
}

@media (max-width: 640px) {
  .tasbeeh-card {
    padding: 1.5rem;
  }
  
  .counter-circle {
    width: 150px;
    height: 150px;
  }
  
  .counter-circle::before {
    width: 130px;
    height: 130px;
  }
  
  .counter-number {
    font-size: 2.5rem;
  }
}
</style> 