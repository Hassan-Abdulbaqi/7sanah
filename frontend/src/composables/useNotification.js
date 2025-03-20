import { getCurrentInstance } from 'vue';

/**
 * Composable for using the notification system
 * This provides a consistent way to show notifications from any component
 */
export function useNotification() {
  // Get the current component instance
  const instance = getCurrentInstance();
  
  // For Vue 3, we can access global properties through the app context
  const globalNotification = instance ? instance.appContext.config.globalProperties.$notification : null;
  
  // If notification service is not found, log a warning and provide fallback
  if (!globalNotification) {
    console.warn('Notification service not found. Notifications will be logged to console instead.');
  }
  
  return {
    /**
     * Show an info notification
     * @param {string} message - The message to display
     * @param {number} timeout - How long to show the notification (ms)
     */
    info(message, timeout = 5000) {
      if (globalNotification) {
        globalNotification.info(message, timeout);
      } else {
        console.info('[Notification]', message);
      }
    },
    
    /**
     * Show a success notification
     * @param {string} message - The message to display
     * @param {number} timeout - How long to show the notification (ms)
     */
    success(message, timeout = 5000) {
      if (globalNotification) {
        globalNotification.success(message, timeout);
      } else {
        console.log('[Success]', message);
      }
    },
    
    /**
     * Show a warning notification
     * @param {string} message - The message to display
     * @param {number} timeout - How long to show the notification (ms)
     */
    warning(message, timeout = 5000) {
      if (globalNotification) {
        globalNotification.warning(message, timeout);
      } else {
        console.warn('[Warning]', message);
      }
    },
    
    /**
     * Show an error notification
     * @param {string} message - The message to display
     * @param {number} timeout - How long to show the notification (ms)
     */
    error(message, timeout = 5000) {
      if (globalNotification) {
        globalNotification.error(message, timeout);
      } else {
        console.error('[Error]', message);
      }
    },
    
    /**
     * Remove all current notifications
     */
    clearAll() {
      if (globalNotification && globalNotification.clearAll) {
        globalNotification.clearAll();
      }
    }
  };
} 