import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// Log for debugging

// Helper function for detecting shared URLs
function isDirectKhatmahAccess(path: string): boolean {
  return path.startsWith('/khatmah/') && path.length > 9;
}

// If this is a direct khatmah access, log it clearly
if (typeof window !== 'undefined' && isDirectKhatmahAccess(window.location.pathname)) {
  console.log(
    '%c why the hell are you here?',
    'background: #10b981; color: white; padding: 6px 12px; border-radius: 4px; font-size: 14px; font-weight: bold;'
  );
  console.log(
    '%cKhatmah ID: ' + window.location.pathname.split('/').pop(),
    'background: #f3f4f6; color: #1f2937; padding: 4px 8px; border-radius: 4px; font-size: 12px;'
  );
}

// Create router instance 
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: App,
      meta: { mode: 'home', transitionName: 'fade' }
    },
    {
      path: '/khatmah/:id',
      name: 'khatmah-detail',
      component: App,
      meta: { mode: 'khatmah-detail', transitionName: 'fade' },
      beforeEnter: (to, _from, next) => {
        console.log('⭐ DIRECT URL: Khatmah detail route activated with ID:', to.params.id)
        // Add metadata to be used by the App component
        to.meta.khatmahId = to.params.id
        next()
      }
    },
    {
      path: '/khatmah',
      name: 'khatmah',
      component: App,
      meta: { mode: 'khatmah-list', transitionName: 'fade' }
    },
    {
      path: '/calendar',
      name: 'calendar',
      component: App,
      meta: { mode: 'calendar', transitionName: 'fade' }
    },
    {
      path: '/qibla',
      name: 'qibla',
      component: App,
      meta: { mode: 'qibla', transitionName: 'fade' }
    },
    {
      path: '/prayer-times',
      name: 'prayer-times',
      component: App,
      meta: { mode: 'prayer-times', transitionName: 'fade' }
    },
    {
      path: '/age-calculator',
      name: 'age-calculator',
      component: App,
      meta: { mode: 'age-calculator', transitionName: 'fade' }
    },
    {
      path: '/tasbeeh',
      name: 'tasbeeh',
      component: App,
      meta: { mode: 'tasbeeh', transitionName: 'fade' }
    },
    {
      path: '/quran',
      name: 'quran',
      component: App,
      meta: { mode: 'quran', transitionName: 'fade' }
    },
    {
      path: '/quran/book',
      name: 'quran-book',
      component: App,
      meta: { mode: 'quran-book', transitionName: 'fade' }
    },
    {
      path: '/quran-search',
      name: 'quran-search',
      component: App,
      meta: { mode: 'quran-search', transitionName: 'fade' }
    },
    {
      path: '/about',
      name: 'about',
      component: App,
      meta: { mode: 'about', transitionName: 'fade' }
    },
    // Wildcard route for 404
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      redirect: '/'
    }
  ],
  // Add scroll behavior for better UX during transitions
  scrollBehavior(_to, _from, savedPosition) {
    // If the user uses back/forward navigation, restore the position
    if (savedPosition) {
      return new Promise((resolve) => {
        // Add a small delay to account for the transition
        setTimeout(() => {
          resolve(savedPosition)
        }, 350) // Slightly longer than our transition time
      })
    } else {
      // For new navigation, scroll to top with a small delay for transition
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({ top: 0, behavior: 'smooth' })
        }, 350)
      })
    }
  }
})

// Log every navigation for debugging
router.beforeEach((_to, _from, next) => {
  // Allow transitions to play out
  document.body.classList.add('page-transitioning')
  
  next()
})

// After navigation is complete
router.afterEach(() => {
  // Small delay to match our CSS transitions
  setTimeout(() => {
    document.body.classList.remove('page-transitioning')
  }, 300)
})

// Handle navigation errors
router.onError((error) => {
  console.error('🛑 Router error:', error)
  document.body.classList.remove('page-transitioning')
})

export default router 