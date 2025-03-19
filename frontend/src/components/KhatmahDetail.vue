<script setup>
import { ref, onMounted, watch, defineProps, defineEmits, onUnmounted, watchEffect } from 'vue';
import { useI18n } from 'vue-i18n';
import { store } from '../store';
import JuzReader from './JuzReader.vue';

const { t } = useI18n();

const props = defineProps({
  khatmahId: {
    type: String,
    required: true
  }
});

const emit = defineEmits([
  'edit-khatmah',
  'select-khatmah',
  'khatmah-created',
  'khatmah-updated',
  'cancel'
]);

const participantName = ref('');
const nameError = ref('');
const selectedJuz = ref(null);
const juzError = ref('');
const readingJuz = ref(null);
const showMyParticipations = ref(false);
const linkCopied = ref(false);
const copyTimeout = ref(null);
// New state to track if user is reading a Juz
const isReadingJuz = ref(false);
const currentReadingJuz = ref(null);
const currentAssignmentId = ref(null);
// New state for share modal
const showShareModal = ref(false);

// New function to safely get the base URL
function getBaseUrl() {
  return typeof window !== 'undefined' ? window.location.origin : '';
}

// Load khatmah data when component mounts or khatmahId changes
watch(() => props.khatmahId, fetchKhatmah, { immediate: true });

async function fetchKhatmah() {
  if (props.khatmahId) {
    await store.fetchKhatmah(props.khatmahId);
  }
}

async function joinKhatmah() {
  // Validate name if required
  if (store.currentKhatmah.require_name && !participantName.value.trim()) {
    nameError.value = t('khatmahDetail.nameError');
    return;
  }
  
  nameError.value = '';
  
  // Join the khatmah
  await store.joinKhatmah(props.khatmahId, participantName.value.trim() || null);
}

async function assignJuz(juzNumber) {
  // Check if user has joined
  if (!store.currentParticipant) {
    juzError.value = t('khatmahDetail.joinFirst');
    return;
  }
  
  // Check if juz is already assigned
  if (isJuzAssigned(juzNumber) && !isMyJuz(juzNumber)) {
    juzError.value = t('khatmahDetail.juzAlreadyAssigned');
    return;
  }
  
  juzError.value = '';
  
  // Assign the juz
  await store.assignJuz(props.khatmahId, juzNumber);
}

// Function to handle clicking on a juz
async function handleJuzClick(juzNumber) {
  // Clear any previous errors
  juzError.value = '';
  
  // Check if user has joined
  if (!store.currentParticipant) {
    juzError.value = t('khatmahDetail.joinFirst');
    return;
  }
  
  // Check if juz is already assigned to someone else
  if (isJuzAssigned(juzNumber) && !isMyJuz(juzNumber)) {
    juzError.value = t('khatmahDetail.juzAlreadyAssigned');
    return;
  }
  
  // If it's my juz, open the reader
  if (isMyJuz(juzNumber)) {
    const assignment = getJuzAssignment(juzNumber);
    if (assignment) {
      // Set the current reading Juz and assignment ID
      currentReadingJuz.value = juzNumber;
      currentAssignmentId.value = assignment.id;
      isReadingJuz.value = true;
    }
  } else {
    // If not assigned, assign it to me
    await assignJuz(juzNumber);
  }
}

// Function to handle going back from Juz reader to Khatmah detail
function handleBackToKhatmah() {
  isReadingJuz.value = false;
  currentReadingJuz.value = null;
  currentAssignmentId.value = null;
}

// Function to handle marking a Juz as completed from the Juz reader
function handleMarkCompleted() {
  isReadingJuz.value = false;
  currentReadingJuz.value = null;
  currentAssignmentId.value = null;
  // Refresh the khatmah data to show updated completion status
  fetchKhatmah();
}

async function toggleComplete(assignmentId) {
  await store.toggleJuzComplete(assignmentId, props.khatmahId);
}

function isJuzAssigned(juzNumber) {
  if (!store.currentKhatmah) return false;
  return store.currentKhatmah.assignments.some(a => a.juz_number === juzNumber);
}

function getJuzAssignment(juzNumber) {
  if (!store.currentKhatmah) return null;
  return store.currentKhatmah.assignments.find(a => a.juz_number === juzNumber);
}

function isMyJuz(juzNumber) {
  if (!store.currentParticipant || !store.currentKhatmah) return false;
  const assignment = getJuzAssignment(juzNumber);
  return assignment && assignment.participant === store.currentParticipant.id;
}

function getCompletionPercentage() {
  if (!store.currentKhatmah) return 0;
  const completedCount = store.currentKhatmah.assignments.filter(a => a.completed).length;
  return (completedCount / 30) * 100;
}

function getParticipantName(participantId) {
  if (!store.currentKhatmah) return '';
  const participant = store.currentKhatmah.participants.find(p => p.id === participantId);
  return participant ? participant.name : '';
}

function getParticipantJuzCount(participantId) {
  if (!store.currentKhatmah) return 0;
  return store.currentKhatmah.assignments.filter(a => a.participant === participantId).length;
}

function getParticipantCompletedJuzCount(participantId) {
  if (!store.currentKhatmah) return 0;
  return store.currentKhatmah.assignments.filter(a => a.participant === participantId && a.completed).length;
}

function editKhatmah() {
  emit('edit-khatmah', props.khatmahId);
}

function toggleMyParticipations() {
  showMyParticipations.value = !showMyParticipations.value;
}

function switchParticipation(participationId) {
  store.switchParticipation(participationId);
  fetchKhatmah();
}

function leaveKhatmah(participationId) {
  if (confirm(t('khatmahDetail.leaveConfirm'))) {
    store.leaveKhatmah(participationId);
    fetchKhatmah();
  }
}

function openShareModal() {
  showShareModal.value = true;
}

function closeShareModal() {
  showShareModal.value = false;
}

function copyKhatmahLink() {
  const baseUrl = getBaseUrl();
  const khatmahUrl = `${baseUrl}/khatmah/${props.khatmahId}`;
  
  // Copy to clipboard
  if (typeof navigator !== 'undefined' && navigator.clipboard) {
    navigator.clipboard.writeText(khatmahUrl)
      .then(() => {
        linkCopied.value = true;
        
        // Reset the copied state after 2 seconds
        copyTimeout.value = setTimeout(() => {
          linkCopied.value = false;
        }, 2000);
      })
      .catch(err => {
        console.error('Failed to copy link: ', err);
        store.error = t('khatmahDetail.copyError');
      });
  }
}

function shareToSocialMedia(platform) {
  const baseUrl = getBaseUrl();
  const khatmahUrl = `${baseUrl}/khatmah/${props.khatmahId}`;
  const khatmahName = store.currentKhatmah.name;
  const shareText = t('khatmahDetail.shareText', { name: khatmahName });
  
  let shareUrl = '';
  
  switch(platform) {
    case 'facebook':
      shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(khatmahUrl)}&quote=${encodeURIComponent(shareText)}`;
      break;
    case 'twitter':
      shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(khatmahUrl)}`;
      break;
    case 'whatsapp':
      shareUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(shareText + ' ' + khatmahUrl)}`;
      break;
    case 'telegram':
      shareUrl = `https://t.me/share/url?url=${encodeURIComponent(khatmahUrl)}&text=${encodeURIComponent(shareText)}`;
      break;
    case 'email':
      shareUrl = `mailto:?subject=${encodeURIComponent(t('khatmahDetail.emailSubject', { name: khatmahName }))}&body=${encodeURIComponent(shareText + '\n\n' + khatmahUrl)}`;
      break;
    default:
      return;
  }
  
  // Open share URL in a new window
  if (typeof window !== 'undefined') {
    window.open(shareUrl, '_blank');
  }
}

// Clean up any timeouts when component is unmounted
onUnmounted(() => {
  if (copyTimeout.value) {
    clearTimeout(copyTimeout.value);
  }
});
</script>

<template>
  <!-- Juz Reader View -->
  <div v-if="isReadingJuz && currentReadingJuz && currentAssignmentId">
    <JuzReader 
      :khatmah-id="khatmahId"
      :juz-number="currentReadingJuz" 
      :assignment-id="currentAssignmentId"
      @back-to-khatmah="handleBackToKhatmah"
      @mark-completed="handleMarkCompleted"
    />
  </div>
  
  <!-- Khatmah Detail View -->
  <div v-else>
    <!-- Loading State -->
    <div v-if="!store.currentKhatmah" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-500"></div>
    </div>
    
    <!-- Khatmah Content -->
    <div v-else>
      <!-- Khatmah Image (if available) -->
      <div v-if="store.currentKhatmah.image_url" class="mb-6">
        <div class="rounded-xl overflow-hidden shadow-sm border border-gray-100">
          <img 
            :src="store.currentKhatmah.image_url" 
            :alt="store.currentKhatmah.name" 
            class="w-full h-48 md:h-64 object-cover"
          />
        </div>
      </div>
      
      <!-- Improved header layout with better horizontal space usage -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 items-center">
        <!-- Khatmah Title and Info - Takes 2/3 of space on desktop -->
        <div class="md:col-span-2">
          <div class="flex items-center">
            <h2 class="text-2xl font-bold text-gray-800 mb-2 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-2 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
              </svg>
              {{ store.currentKhatmah.name }}
              
              <!-- Creator Badge -->
              <span 
                v-if="store.isKhatmahCreator(props.khatmahId)" 
                class="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full"
              >
                {{ t('khatmahDetail.creator') }}
              </span>
            </h2>
          </div>
          
          <div class="flex flex-wrap gap-4 mb-2">
            <p class="text-gray-500 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ t('khatmahDetail.createdOn') }}: {{ new Date(store.currentKhatmah.created_at).toLocaleDateString() }}
            </p>
            
            <p v-if="store.currentKhatmah.end_date" class="text-gray-500 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              {{ t('khatmahDetail.endDate') }}: {{ new Date(store.currentKhatmah.end_date).toLocaleDateString() }}
            </p>
            
            <p v-if="store.currentKhatmah.is_private" class="text-gray-500 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              {{ t('khatmahDetail.privateKhatmah') }}
            </p>
          </div>
          
          <!-- Action Buttons -->
          <div class="flex flex-wrap gap-2 mt-4">
            <!-- Edit Button (only for creator) -->
            <button 
              v-if="store.isKhatmahCreator(props.khatmahId)" 
              @click="editKhatmah"
              class="flex items-center px-3 py-1.5 bg-blue-50 text-blue-700 rounded-md hover:bg-blue-100 transition-colors text-sm"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
              {{ t('khatmahDetail.editKhatmah') }}
            </button>
            
            <!-- Share Button -->
            <button 
              @click="openShareModal"
              class="flex items-center px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-md hover:bg-emerald-100 transition-colors text-sm"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z" />
              </svg>
              {{ t('khatmahDetail.share') }}
            </button>
            
            <!-- My Participations Button -->
            <button 
              @click="toggleMyParticipations"
              class="flex items-center px-3 py-1.5 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors text-sm"
              :class="{ 'bg-gray-200': showMyParticipations }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
              </svg>
              {{ t('khatmahDetail.myParticipations') }}
            </button>
          </div>
        </div>
        
        <!-- Completion Status - Takes 1/3 of space on desktop -->
        <div class="bg-white rounded-xl shadow-sm p-4 border border-gray-100">
          <h3 class="text-lg font-semibold mb-3 text-gray-800 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            {{ t('khatmahDetail.completed') }}
          </h3>
          
          <div class="flex items-center justify-between">
            <div class="text-2xl font-bold text-emerald-600">
              {{ store.currentKhatmah.assignments.filter(a => a.completed).length }}/30
            </div>
            
            <div class="relative h-10 w-10">
              <svg class="w-10 h-10 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="#E2E8F0"
                  stroke-width="3"
                  stroke-dasharray="100, 100"
                />
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="#10B981"
                  stroke-width="3"
                  stroke-dasharray="100, 100"
                  :stroke-dasharray="`${getCompletionPercentage()}, 100`"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center text-xs font-medium">
                {{ store.currentKhatmah.assignments.filter(a => a.completed).length }}/30 {{ t('khatmahDetail.juz') }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Join Khatmah Form (if not joined) -->
      <div v-if="!store.currentParticipant" class="bg-white rounded-xl shadow-sm p-6 mb-8 border border-gray-100">
        <h3 class="text-xl font-semibold mb-4 text-gray-800">{{ t('khatmahDetail.joinKhatmah') }}</h3>
        
        <form @submit.prevent="joinKhatmah" class="flex flex-col md:flex-row gap-4">
          <div v-if="store.currentKhatmah.require_name" class="flex-grow relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
              </svg>
            </div>
            <input
              v-model="participantName"
              type="text"
              class="block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
              :placeholder="t('khatmahDetail.enterName')"
            />
            <p v-if="nameError" class="mt-2 text-sm text-red-600 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              {{ nameError }}
            </p>
          </div>
          
          <div v-else class="flex-grow">
            <p class="text-gray-500 mb-2">{{ t('khatmahDetail.joinAnonymously') }}</p>
          </div>
          
          <button
            type="submit"
            class="px-6 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-medium rounded-lg shadow-sm hover:from-emerald-700 hover:to-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-colors"
          >
            {{ t('khatmahDetail.joinButton') }}
          </button>
        </form>
      </div>
      
      <!-- Participant Info (if joined) -->
      <div v-else class="bg-white rounded-xl shadow-sm p-6 mb-8 border border-gray-100">
        <div class="flex items-center mb-4">
          <div class="bg-emerald-100 rounded-full p-2 mr-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-800">{{ t('khatmahDetail.joinedAs') }}: <span class="text-emerald-600">{{ store.currentParticipant.name }}</span></h3>
            <p class="text-sm text-gray-500">{{ t('khatmahDetail.clickUnassigned') }}</p>
            <p class="text-sm text-gray-500 mt-1">{{ t('khatmahDetail.clickAssigned') }}</p>
          </div>
        </div>
        
        <p v-if="juzError" class="mt-2 mb-4 text-sm text-red-600 bg-red-50 p-2 rounded-md flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          {{ juzError }}
        </p>
      </div>
      
      <!-- Juz Grid -->
      <div class="mb-8">
        <h3 class="text-xl font-semibold mb-6 text-gray-800 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
            <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
          </svg>
          {{ t('khatmahDetail.juzAssignments') }}
        </h3>
        
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-6 gap-4">
          <div 
            v-for="juz in 30" 
            :key="juz"
            :data-juz="juz"
            class="relative border rounded-lg overflow-hidden shadow-sm cursor-pointer transform transition-all duration-300"
            :class="{
              'bg-white border-gray-200 hover:border-emerald-300 hover:shadow-md': !isJuzAssigned(juz) && store.currentParticipant,
              'bg-emerald-50 border-emerald-200': isJuzAssigned(juz) && !getJuzAssignment(juz)?.completed,
              'bg-emerald-100 border-emerald-300': isJuzAssigned(juz) && getJuzAssignment(juz)?.completed,
              'scale-105': readingJuz === juz,
              'opacity-60 cursor-not-allowed': isJuzAssigned(juz) && !isMyJuz(juz),
              'hover:shadow-md': store.currentParticipant
            }"
            @click="handleJuzClick(juz)"
          >
            <div 
              v-if="isJuzAssigned(juz)" 
              class="h-1 bg-gradient-to-r from-emerald-500 to-teal-500"
              :class="{ 'bg-gradient-to-r from-emerald-600 to-teal-600': getJuzAssignment(juz)?.completed }"
            ></div>
            <div v-else class="h-1 bg-gray-100"></div>
            
            <div class="p-3">
              <div class="font-bold text-center mb-1">{{ t('khatmahDetail.juzNumber', { number: juz }) }}</div>
              
              <div v-if="isJuzAssigned(juz)" class="text-center">
                <div class="text-xs mb-2 truncate" :title="getJuzAssignment(juz).participant_name">
                  {{ getJuzAssignment(juz).participant_name }}
                </div>
                
                <div v-if="isMyJuz(juz)" class="mt-2">
                  <button 
                    @click.stop="handleJuzClick(juz)"
                    class="w-full text-xs px-2 py-1 rounded-md transition-colors bg-blue-500 hover:bg-blue-600 text-white mb-1"
                  >
                    {{ t('khatmahDetail.readJuz') }}
                  </button>
                  <button 
                    @click.stop="toggleComplete(getJuzAssignment(juz).id)"
                    class="w-full text-xs px-2 py-1 rounded-md transition-colors"
                    :class="{
                      'bg-emerald-500 hover:bg-emerald-600 text-white': !getJuzAssignment(juz).completed,
                      'bg-red-500 hover:bg-red-600 text-white': getJuzAssignment(juz).completed
                    }"
                  >
                    {{ getJuzAssignment(juz).completed ? t('khatmahDetail.markIncomplete') : t('khatmahDetail.markComplete') }}
                  </button>
                </div>
                
                <div v-else class="mt-2 text-xs">
                  <span 
                    class="inline-block px-2 py-1 rounded-md"
                    :class="{
                      'bg-emerald-100 text-emerald-800': !getJuzAssignment(juz).completed,
                      'bg-emerald-200 text-emerald-800': getJuzAssignment(juz).completed
                    }"
                  >
                    {{ getJuzAssignment(juz).completed ? t('khatmahDetail.completed') : t('khatmahDetail.inProgress') }}
                  </span>
                </div>
              </div>
              
              <div v-else class="text-center mt-2">
                <span class="text-xs text-gray-500 block py-1">
                  {{ store.currentParticipant ? t('khatmahDetail.clickToSelect') : t('khatmahDetail.notAssigned') }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Participants List -->
      <div class="mb-8">
        <h3 class="text-xl font-semibold mb-6 text-gray-800 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
          </svg>
          {{ t('khatmahDetail.participants', { count: store.currentKhatmah.participants.length }) }}
        </h3>
        
        <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
          <ul class="divide-y divide-gray-100">
            <li 
              v-for="participant in store.currentKhatmah.participants" 
              :key="participant.id"
              class="p-4 hover:bg-gray-50 transition-colors"
            >
              <div class="flex justify-between items-center">
                <div class="flex items-center">
                  <div class="bg-emerald-100 rounded-full p-2 mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                    </svg>
                  </div>
                  <div>
                    <span class="font-medium text-gray-800">{{ participant.name }}</span>
                    <span 
                      v-if="store.currentParticipant && participant.id === store.currentParticipant.id" 
                      class="ml-2 text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full"
                    >
                      {{ t('khatmahDetail.you') }}
                    </span>
                  </div>
                </div>
                <div class="flex items-center">
                  <div class="text-sm text-gray-500 mr-4">
                    {{ t('khatmahDetail.joined') }}: {{ new Date(participant.created_at).toLocaleDateString() }}
                  </div>
                  <div class="text-sm bg-gray-100 text-gray-800 px-2 py-1 rounded-md">
                    {{ getParticipantJuzCount(participant.id) }} {{ t('khatmahDetail.juz') }}
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Share Modal -->
  <div 
    v-if="showShareModal" 
    id="share-modal"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
  >
    <div 
      id="share-modal-content"
      class="bg-white rounded-xl shadow-xl max-w-md w-full p-6 transform transition-all"
    >
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-semibold text-gray-800">Share Khatmah</h3>
        <button 
          @click="closeShareModal"
          class="text-gray-500 hover:text-gray-700 focus:outline-none"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <p class="text-gray-600 mb-6">
        Share this Khatmah with others to invite them to join the Quran reading journey.
      </p>
      
      <!-- Social Media Sharing Options -->
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-6">
        <!-- Facebook -->
        <button 
          @click="shareToSocialMedia('facebook')"
          class="flex flex-col items-center justify-center p-4 rounded-lg bg-blue-50 hover:bg-blue-100 transition-colors"
        >
          <svg class="h-8 w-8 text-blue-600 mb-2" viewBox="0 0 24 24" fill="currentColor">
            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
          </svg>
          <span class="text-sm font-medium text-gray-700">Facebook</span>
        </button>
        
        <!-- Twitter (now X) -->
        <button 
          @click="shareToSocialMedia('twitter')"
          class="flex flex-col items-center justify-center p-4 rounded-lg bg-black hover:bg-gray-900 transition-colors"
        >
          <svg class="h-8 w-8 text-white mb-2" viewBox="0 0 24 24" fill="currentColor">
            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
          </svg>
          <span class="text-sm font-medium text-white">X</span>
        </button>
        
        <!-- WhatsApp -->
        <button 
          @click="shareToSocialMedia('whatsapp')"
          class="flex flex-col items-center justify-center p-4 rounded-lg bg-green-50 hover:bg-green-100 transition-colors"
        >
          <svg class="h-8 w-8 text-green-500 mb-2" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.198.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.5-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.272-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
          </svg>
          <span class="text-sm font-medium text-gray-700">WhatsApp</span>
        </button>
        
        <!-- Telegram -->
        <button 
          @click="shareToSocialMedia('telegram')"
          class="flex flex-col items-center justify-center p-4 rounded-lg bg-blue-50 hover:bg-blue-100 transition-colors"
        >
          <svg class="h-8 w-8 text-blue-500 mb-2" viewBox="0 0 24 24" fill="currentColor">
            <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.347.372.198.27.149.444.198.642.048.99L12.434 12l4.962 2.478c.348.174.498.822.348 1.194-.196L19.5 12l-1.194-5.724zM12.002.42l-1.194 5.724L12 7.56l-2.406-1.2L8.998 4.2l4.806-2.4z"/>
          </svg>
          <span class="text-sm font-medium text-gray-700">Telegram</span>
        </button>
        
        <!-- Email -->
        <button 
          @click="shareToSocialMedia('email')"
          class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-600 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          <span class="text-sm font-medium text-gray-700">Email</span>
        </button>
      </div>
      
      <!-- Copy Link Section -->
      <div class="mt-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">Khatmah Link</label>
        <div class="flex">
          <div class="flex-grow relative">
            <input 
              type="text" 
              readonly 
              :value="`${getBaseUrl()}/khatmah/${props.khatmahId}`"
              class="block w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            />
          </div>
          <button
            @click="copyKhatmahLink"
            class="flex items-center justify-center px-4 py-3 bg-blue-600 text-white rounded-r-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
            :class="{ 'bg-green-600 hover:bg-green-700': linkCopied }"
          >
            <svg v-if="!linkCopied" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
              <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            <span class="ml-1">{{ linkCopied ? 'Copied!' : 'Copy' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reading-animation {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    opacity: 0.7;
  }
  50% {
    transform: scale(1.05);
    opacity: 1;
  }
  100% {
    transform: scale(0.95);
    opacity: 0.7;
  }
}

/* Modal Animation */
#share-modal-content {
  animation: modal-appear 0.3s ease-out;
}

@keyframes modal-appear {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style> 