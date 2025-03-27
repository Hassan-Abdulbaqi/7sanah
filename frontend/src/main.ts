import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import './style.css'
import App from './App.vue'
import router from './router'
import messages from './locales/index.js'
import { clickOutside } from './directives/clickOutside.js'

// Get the stored language from localStorage or use Arabic
const getStoredLanguage = (): string => {
  const storedLang = localStorage.getItem('language')
  return storedLang && ['en', 'ar', 'ku', 'fa'].includes(storedLang) 
    ? storedLang 
    : 'ar'
}

// Create i18n instance
const i18n = createI18n({
  legacy: false, // Use Composition API
  locale: getStoredLanguage(),
  fallbackLocale: 'ar',
  messages,
  pluralizationRules: {
    /**
     * @param choice {number} a choice index given by the input to $tc: `$tc('path.to.rule', choiceIndex)`
     * @param choicesLength {number} an overall amount of available choices
     * @returns a final choice index to select plural word by
     */
    'ar': function(choice: number, _choicesLength: number): number {
      // Arabic has different plural forms
      if (choice === 0) {
        return 0;
      }
      if (choice === 1) {
        return 0;
      }
      if (choice === 2) {
        return 1;
      }
      if (choice >= 3 && choice <= 10) {
        return 1;
      }
      return 1;
    },
    'ku': function(choice: number, _choicesLength: number): number {
      // Kurdish follows similar rules to Arabic
      return choice === 1 ? 0 : 1;
    },
    'fa': function(choice: number, _choicesLength: number): number {
      // Persian has simple pluralization
      return choice > 1 ? 1 : 0;
    }
  }
})

// Create the app
const app = createApp(App)

// Register the click-outside directive
app.directive('clickOutside', clickOutside)

// Create notification service on the app
app.config.globalProperties.$notification = {
  info: (message: any) => console.info('[Info]', message),
  success: (message: any) => console.log('[Success]', message),
  warning: (message: any) => console.warn('[Warning]', message),
  error: (message: any) => console.error('[Error]', message)
}

// Use plugins
app.use(i18n)
app.use(router)

// After all plugins are added, mount the app
app.mount('#app')

// Export the i18n instance for use in other files
export { i18n }
