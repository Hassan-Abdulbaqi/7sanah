import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import './style.css'
import App from './App.vue'
import router from './router'
import messages from './locales'
import { clickOutside } from './directives/clickOutside'

// Log initial URL and route for debugging
console.log('------------------------')
console.log('Application starting...')
console.log('Initial URL:', window.location.href)
console.log('Initial pathname:', window.location.pathname)
console.log('------------------------')

// Get the browser language or use English as fallback
const getBrowserLanguage = () => {
  const browserLang = navigator.language.split('-')[0]
  return ['en', 'ar', 'ku', 'fa'].includes(browserLang) ? browserLang : 'en'
}

// Get the stored language from localStorage or use browser language
const getStoredLanguage = () => {
  const storedLang = localStorage.getItem('language')
  return storedLang && ['en', 'ar', 'ku', 'fa'].includes(storedLang) 
    ? storedLang 
    : getBrowserLanguage()
}

// Create i18n instance
const i18n = createI18n({
  legacy: false, // Use Composition API
  locale: getStoredLanguage(),
  fallbackLocale: 'en',
  messages,
  pluralizationRules: {
    /**
     * @param choice {number} a choice index given by the input to $tc: `$tc('path.to.rule', choiceIndex)`
     * @param choicesLength {number} an overall amount of available choices
     * @returns a final choice index to select plural word by
     */
    'ar': function(choice, choicesLength) {
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
    'ku': function(choice, choicesLength) {
      // Kurdish follows similar rules to Arabic
      return choice === 1 ? 0 : 1;
    },
    'fa': function(choice, choicesLength) {
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
  info: (message) => console.info('[Info]', message),
  success: (message) => console.log('[Success]', message),
  warning: (message) => console.warn('[Warning]', message),
  error: (message) => console.error('[Error]', message)
}

// Use plugins
app.use(i18n)
app.use(router)

// Log the current route for debugging
console.log('Current route:', window.location.pathname)

// After all plugins are added, mount the app
app.mount('#app')

// Export the i18n instance for use in other files
export { i18n }
