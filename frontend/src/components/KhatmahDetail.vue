<script setup>
import { ref, onMounted, watch, onUnmounted, watchEffect } from 'vue';
import { useI18n } from 'vue-i18n';
import { store } from '../store';
import { useRouter } from 'vue-router';
import axios from 'axios';
import JuzReader from './JuzReader.vue'; // Add JuzReader import

const { t } = useI18n();
const router = useRouter();

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
  'cancel',
  'navigate-to-surah',
  'navigate-to-juz'
]);

const participantName = ref('');
const nameError = ref('');
const selectedJuz = ref(null);
const juzError = ref('');
const showMyParticipations = ref(false);
const linkCopied = ref(false);
const copyTimeout = ref(null);
// New state for share modal
const showShareModal = ref(false);
// State for participations from local storage
const myParticipations = ref([]);
// Add new state for confirmation dialogs
const showJuzConfirmation = ref(false);
const confirmingJuzNumber = ref(null);
const showSurahConfirmation = ref(false);
const confirmingSurahNumber = ref(null);
// Add state for Surahs data
const surahs = ref([]);
const loadingSurahs = ref(false);
const surahsError = ref(null);
// Add search state variables
const searchQuery = ref('');
const filteredSurahs = ref([]);
const normalizedSurahNames = ref([]);

// Add missing reactive properties
const isReadingJuz = ref(false);
const currentReadingJuz = ref(null);
const currentAssignmentId = ref(null);

// Enhanced profanity filter lists with common variations
const englishProfanityList = [
  'fuck', 'fuk', 'fck', 'f*ck', 'f**k', 'fucc', 'phuck', 'phuk',
  'shit', 'sh*t', 'sh1t', 'shiit', 'shyt',
  'ass', '@ss', 'a$$', 'azz',
  'bitch', 'b*tch', 'b1tch', 'biatch', 'bytch',
  'dick', 'd*ck', 'd1ck', 'dicc', 'dik',
  'pussy', 'pu$$y', 'puss', 'p*ssy',
  'cock', 'c*ck', 'coc', 'c0ck',
  'whore', 'wh*re', 'h0e', 'hoe',
  'bastard', 'b@stard', 'b*stard',
  'cunt', 'kunt', 'c*nt',
  'damn', 'd*mn', 'dammn',
  'piss', 'p*ss', 'p1ss',
  'slut', 'sl*t', '$lut',
  'tits', 't*ts', 't1ts'
];

const arabicProfanityList = [
  // Existing MSA profanity
  'كس', 'ك س', 'كـس', 'كــس', 'كسس', 'كص', 'كز',
  'طيز', 'طـيـز', 'طي ز', 'طيظ', 'تيز',
  'زب', 'ز ب', 'زبب', 'زبر', 'ذب', 'زبي',
  'شرموط', 'شرمو ط', 'شـرمـوط', 'شرموت',
  'عرص', 'عـرص', 'ع ر ص', 'عرس',
  'خول', 'خـول', 'خ و ل', 'خوول',
  'منيك', 'منـيـك', 'م ن ي ك', 'منيوك',
  'قحبة', 'قحـبة', 'ق ح ب ة', 'قحبه',
  'عاهرة', 'عـاهـرة', 'ع ا ه ر ة',
  'شرموطة', 'شرموطه', 'شـرمـوطـة',
  'منيوك', 'منـيـوك', 'م ن ي و ك',
  'متناك', 'متـنـاك', 'م ت ن ا ك',
  'خنزير', 'خـنـزيـر', 'خ ن ز ي ر',
  'كلب', 'كـلـب', 'ك ل ب',

  // Iraqi dialect profanity and variations
  'عير', 'ع ي ر', 'عـيـر', 'عيرر',
  'خرة', 'خره', 'خ ر ه', 'خـرة',
  'كواد', 'كـواد', 'ك و ا د', 'كوواد',
  'منيوج', 'منيوك', 'م ن ي و ج', 'منـيـوج',
  'عيوره', 'عيورة', 'ع ي و ر ه', 'عـيـوره',
  'جحش', 'ج ح ش', 'جـحـش', 'جحشش',
  'خايس', 'خ ا ي س', 'خـايـس', 'خايسس',
  'دياث', 'د ي ا ث', 'ديـاث', 'دياثث',
  'عرص', 'ع ر ص', 'عـرص', 'عرصص',
  'كحبة', 'ك ح ب ة', 'كحـبـة', 'كحبه',
  'مخنث', 'م خ ن ث', 'مـخـنـث', 'مخنثث',
  'معرص', 'م ع ر ص', 'مـعـرص', 'معرصص',
  'منيوك', 'م ن ي و ك', 'مـنـيـوك', 'منيوكك',
  'ديوث', 'د ي و ث', 'ديـوث', 'ديوثث',
  
  // Iraqi slang variations
  'كحاب', 'ك ح ا ب', 'كـحـاب',
  'عواهر', 'ع و ا ه ر', 'عـواهـر',
  'شراميط', 'ش ر ا م ي ط', 'شـرامـيـط',
  'منايك', 'م ن ا ي ك', 'مـنـايـك',
  'عيور', 'ع ي و ر', 'عـيـور',
  'زنديق', 'ز ن د ي ق', 'زنـديـق',
  'فاجر', 'ف ا ج ر', 'فـاجـر',
  'منجوس', 'م ن ج و س', 'مـنـجـوس',
  'نجس', 'ن ج س', 'نـجـس',
  'وصخ', 'و ص خ', 'وصـخ',
  'قواد', 'ق و ا د', 'قـواد',
  'دنكة', 'د ن ك ة', 'دنـكـة',
  'خنزيرة', 'خ ن ز ي ر ة', 'خنـزيـرة',
  'جلب', 'ج ل ب', 'جـلـب',
  
  // Common Iraqi insults and their variations
  'حيوان', 'ح ي و ا ن', 'حـيـوان',
  'بهيمة', 'ب ه ي م ة', 'بهـيـمة',
  'حمار', 'ح م ا ر', 'حـمـار',
  'خايب', 'خ ا ي ب', 'خـايـب',
  'سافل', 'س ا ف ل', 'سـافـل',
  'واطي', 'و ا ط ي', 'واطـي',
  'نذل', 'ن ذ ل', 'نـذل',
  'دعبل', 'د ع ب ل', 'دعـبـل',
  'مطي', 'م ط ي', 'مـطـي',
  'بزون', 'ب ز و ن', 'بـزون',
  'كلاوي', 'ك ل ا و ي', 'كـلاوي',
  'مقيد', 'م ق ي د', 'مـقـيـد',
  'مصخم', 'م ص خ م', 'مـصـخـم'
];

// Common character substitutions
const charSubstitutions = {
  'a': ['@', '4', 'α', 'а', 'λ', 'Д'],
  'b': ['8', '6', 'ь', 'в'],
  'e': ['3', '€', 'е', 'ε'],
  'i': ['1', '!', '|', 'і', 'ι'],
  'l': ['1', '|', 'і', 'ι'],
  'o': ['0', 'θ', 'о', 'σ'],
  's': ['5', '$', 'ѕ', 'š'],
  't': ['7', '+', 'т'],
  'u': ['υ', 'μ', 'у'],
  'v': ['\\/', 'ν'],
  'w': ['ω', 'ш', 'щ'],
  'x': ['×', 'х'],
  'y': ['¥', 'γ', 'у', 'ү'],
  'z': ['2', 'ζ', 'з'],
  // Add Arabic character substitutions common in Iraqi typing
  'ك': ['گ', 'ݣ', 'ڭ', 'ک', 'ڪ', '؟', '&'],
  'ج': ['چ', 'ج', 'ڃ', 'ڄ'],
  'ع': ['ع', 'غ', 'ڠ'],
  'ح': ['ح', '7', '₇', '७', '៧', 'ዕ'],
  'ق': ['ڨ', 'ڧ', 'ف'],
  'ط': ['ظ', 'ط', 'ض'],
  'ص': ['ض', 'ص', 'س'],
  'ة': ['ه', 'ت', '؟', '?', '6', '٦']
};

// Function to normalize text by removing common obfuscation techniques
function normalizeText(text) {
  if (!text) return '';
  
  // Convert to lowercase
  let normalized = text.toLowerCase();
  
  // Remove all diacritics
  normalized = normalized.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  
  // Enhanced special character handling
  // Replace all special characters and symbols with empty string
  normalized = normalized.replace(/[!@#$%^&*()_+\-=\[\]{};:'",.<>?~`؟]/g, '');
  
  // Remove common separators and special characters
  normalized = normalized.replace(/[\s_\-.,*'"´`~!@#$%^&\+=\[\]{}()|\\]/g, '');
  
  // Replace common character substitutions
  Object.entries(charSubstitutions).forEach(([char, substitutions]) => {
    const pattern = new RegExp(`[${substitutions.join('')}]`, 'g');
    normalized = normalized.replace(pattern, char);
  });
  
  // Handle zero-width characters and other invisible characters
  normalized = normalized.replace(/[\u200B-\u200D\uFEFF]/g, '');
  
  // Handle Arabic-specific normalizations
  normalized = normalized
    // Normalize different forms of Alef
    .replace(/[أإآا]/g, 'ا')
    // Normalize different forms of Yaa
    .replace(/[ىي]/g, 'ي')
    // Normalize different forms of Taa Marbouta
    .replace(/[ة]/g, 'ه')
    // Normalize different forms of Hamza
    .replace(/[ؤئء]/g, 'ء')
    // Iraqi-specific character normalizations
    .replace(/[گڭک]/g, 'ك')
    .replace(/[چڃڄ]/g, 'ج')
    .replace(/[غڠ]/g, 'ع')
    .replace(/[ڨڧ]/g, 'ق')
    .replace(/[ظض]/g, 'ط')
    .replace(/ض/g, 'ص');
  
  // Remove any remaining non-alphanumeric characters
  normalized = normalized.replace(/[^\p{L}\p{N}]/gu, '');
  
  return normalized;
}

// Function to check if a string contains a profanity pattern
function containsProfanity(text, profanityList) {
  const normalizedText = normalizeText(text);
  
  // Check exact matches and common variations
  return profanityList.some(word => {
    const normalizedWord = normalizeText(word);
    
    // Check if the word exists as is
    if (normalizedText.includes(normalizedWord)) return true;
    
    // Check for l33t speak variations (if not already caught by normalizeText)
    const l33tPattern = word
      .split('')
      .map(char => {
        const substitutions = charSubstitutions[char.toLowerCase()] || [char];
        return `[${char}${substitutions.join('')}]`;
      })
      .join('[\\s_\\-.*!@#$%^&()+=\\[\\]{}|\\\\]*');
    
    const regex = new RegExp(l33tPattern, 'i');
    return regex.test(text);
  });
}

// Function to validate name
function validateName(name) {
  if (!name || !name.trim()) {
    return { isValid: false, error: t('khatmahDetail.nameError') || 'Name is required' };
  }

  // Check English profanity with enhanced detection
  if (containsProfanity(name, englishProfanityList)) {
    return { 
      isValid: false, 
      error: t('khatmahDetail.inappropriateNameError') || 'Please use an appropriate name' 
    };
  }
  
  // Check Arabic profanity with enhanced detection
  if (containsProfanity(name, arabicProfanityList)) {
    return { 
      isValid: false, 
      error: t('khatmahDetail.inappropriateNameError') || 'Please use an appropriate name' 
    };
  }
  
  // Add additional validation rules
  if (name.length < 2) {
    return { 
      isValid: false, 
      error: t('khatmahDetail.nameTooShortError') || 'Name must be at least 2 characters long' 
    };
  }
  
  if (name.length > 50) {
    return { 
      isValid: false, 
      error: t('khatmahDetail.nameTooLongError') || 'Name must not exceed 50 characters' 
    };
  }
  
  // Enhanced character validation
  // Must contain at least one valid letter (Arabic or English)
  const hasValidLetter = /[a-zA-Zء-ي]/.test(name);
  if (!hasValidLetter) {
    return { 
      isValid: false, 
      error: t('khatmahDetail.nameInvalidCharacters') || 'Name must contain at least some letters' 
    };
  }
  
  // Check for excessive special characters or numbers
  const specialCharCount = (name.match(/[^a-zA-Zء-ي\s]/g) || []).length;
  if (specialCharCount > name.length / 3) {
    return {
      isValid: false,
      error: t('khatmahDetail.tooManySpecialChars') || 'Name contains too many special characters or numbers'
    };
  }

  return { isValid: true, error: null };
}

// New function to safely get the base URL
function getBaseUrl() {
  // Use the current origin (e.g., http://localhost:5173)
  return typeof window !== 'undefined' ? window.location.origin : '';
}

// Add a new function to get the full khatmah URL
function getKhatmahUrl() {
  if (typeof window === 'undefined') return '';
  
  // Ensure we have the correct origin with protocol
  const origin = window.location.origin; // e.g., http://localhost:5173
  
  // Return the complete absolute URL with the khatmah ID
  // This needs to be an absolute URL for sharing
  return `${origin}/khatmah/${props.khatmahId}`;
}

// Function to load participations from local storage
function loadMyParticipations() {
  if (typeof window === 'undefined') return;
  
  try {
    const participationsJson = localStorage.getItem('quran_khatmah_participants');
    if (participationsJson) {
      const participationsObj = JSON.parse(participationsJson);
      myParticipations.value = Object.values(participationsObj).map(p => ({
        id: p.id,
        name: p.name,
        khatmahId: p.khatmahId,
        khatmahName: p.khatmahName
      }));
    }
  } catch (err) {
    console.error('Error loading participations from local storage:', err);
    myParticipations.value = [];
  }
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
  if (store.currentKhatmah.require_name) {
    const validation = validateName(participantName.value);
    if (!validation.isValid) {
      nameError.value = validation.error;
      return;
    }
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
    scrollToError(); // Scroll to error
    return;
  }
  
  // Check if juz is already assigned to someone else
  if (isJuzAssigned(juzNumber) && !isMyJuz(juzNumber)) {
    juzError.value = t('khatmahDetail.juzAlreadyAssigned');
    scrollToError(); // Scroll to error
    return;
  }
  
  // If it's my juz, navigate to read it
  if (isMyJuz(juzNumber)) {
    const assignment = getJuzAssignment(juzNumber);
    if (assignment) {
      // Set the reading state
      isReadingJuz.value = true;
      currentReadingJuz.value = juzNumber;
      currentAssignmentId.value = assignment.id;
    }
  } else {
    // If not assigned, show confirmation dialog
    confirmingJuzNumber.value = juzNumber;
    showJuzConfirmation.value = true;
  }
}

// Function to confirm juz assignment
async function confirmJuzAssignment() {
  if (confirmingJuzNumber.value) {
    await assignJuz(confirmingJuzNumber.value);
    // Close the confirmation dialog
    showJuzConfirmation.value = false;
    
    // Get the assignment after assigning
    const assignment = getJuzAssignment(confirmingJuzNumber.value);
    if (assignment) {
      // Set the reading state
      isReadingJuz.value = true;
      currentReadingJuz.value = confirmingJuzNumber.value;
      currentAssignmentId.value = assignment.id;
    }
    
    confirmingJuzNumber.value = null;
  }
}

// Function to handle going back from Juz reader
function handleBackFromJuz() {
  isReadingJuz.value = false;
  currentReadingJuz.value = null;
  currentAssignmentId.value = null;
}

// Function to cancel juz assignment
function cancelJuzAssignment() {
  showJuzConfirmation.value = false;
  confirmingJuzNumber.value = null;
}

// Function to handle going back from Juz reader to Khatmah detail
function handleBackToKhatmah() {
  // No need to reset any state here as we're using navigation
}

// Function to handle marking a Juz as completed from the Juz reader
async function handleMarkCompleted() {
  // Return to the Khatmah detail view
  isReadingJuz.value = false;
  currentReadingJuz.value = null;
  currentAssignmentId.value = null;
  
  // Refresh the Khatmah data to show updated completion status
  await fetchKhatmah();
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
  
  if (store.currentKhatmah.khatmah_type === 'juz') {
    const completedCount = store.currentKhatmah.assignments.filter(a => a.completed).length;
    return (completedCount / 30) * 100;
  } else if (store.currentKhatmah.khatmah_type === 'surah') {
    const completedCount = store.currentKhatmah.surah_assignments.filter(a => a.completed).length;
    return (completedCount / 114) * 100;
  }
  
  return 0;
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

function getParticipantSurahCount(participantId) {
  if (!store.currentKhatmah) return 0;
  return store.currentKhatmah.surah_assignments.filter(a => a.participant === participantId).length;
}

function getParticipantCompletedJuzCount(participantId) {
  if (!store.currentKhatmah) return 0;
  return store.currentKhatmah.assignments.filter(a => a.participant === participantId && a.completed).length;
}

function getParticipantCompletedSurahCount(participantId) {
  if (!store.currentKhatmah) return 0;
  return store.currentKhatmah.surah_assignments.filter(a => a.participant === participantId && a.completed).length;
}

function getJuzCardClass(juzNumber) {
  if (isJuzAssigned(juzNumber)) {
    if (isMyJuz(juzNumber)) {
      if (getJuzAssignment(juzNumber).completed) {
        return 'bg-emerald-100 text-emerald-800 border border-emerald-300 hover:bg-emerald-200';
      }
      return 'bg-blue-100 text-blue-800 border border-blue-300 hover:bg-blue-200';
    }
    if (getJuzAssignment(juzNumber).completed) {
      return 'bg-green-50 text-green-800 border border-green-200 hover:bg-green-100 completed-by-other';
    }
    return 'bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 card-in-progress';
  }
  return 'bg-white text-gray-800 border border-gray-200 hover:bg-gray-50';
}

function editKhatmah() {
  // Only allow editing if the user is the creator
  if (store.isKhatmahCreator(props.khatmahId)) {
    emit('edit-khatmah', props.khatmahId);
  } else {
    // Display error message if not authorized (this can be handled by the UI as needed)
    alert(t('khatmahDetail.notAuthorized') || 'You are not authorized to edit this khatmah');
  }
}

function toggleMyParticipations() {
  showMyParticipations.value = !showMyParticipations.value;
  if (showMyParticipations.value) {
    loadMyParticipations();
  }
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

function selectKhatmah(khatmahId) {
  emit('select-khatmah', khatmahId);
}

function openShareModal() {
  showShareModal.value = true;
}

function closeShareModal() {
  showShareModal.value = false;
}

async function copyKhatmahLink() {
  const url = getKhatmahUrl();
  
  try {
    await navigator.clipboard.writeText(url);
    
    // Show success message
    linkCopied.value = true;
    
    // Clear any existing timeout
    if (copyTimeout.value) {
      clearTimeout(copyTimeout.value);
    }
    
    // Reset message after 3 seconds
    copyTimeout.value = setTimeout(() => {
      linkCopied.value = false;
    }, 3000);
    
  } catch (err) {
    console.error('Failed to copy link:', err);
  }
}

// Add the async keyword to the shareKhatmah function
async function shareKhatmah() {
  const url = getKhatmahUrl();
  const title = store.currentKhatmah?.name || 'Quran Khatmah';
  const text = t('khatmahDetail.shareMessage', { 
    name: store.currentKhatmah?.name || 'Quran Khatmah' 
  });
  
  // Use Web Share API if available (mobile devices)
  if (navigator.share) {
    try {
      await navigator.share({
        title,
        text,
        url
      });
    } catch (err) {
      console.error('Error sharing:', err);
      // Fall back to copy if share was cancelled or failed
      copyKhatmahLink();
    }
  } else {
    // Fall back to copy on desktop
    copyKhatmahLink();
  }
}

// Clean up any timeouts when component is unmounted
onUnmounted(() => {
  if (copyTimeout.value) {
    clearTimeout(copyTimeout.value);
  }
});

// Load participations when component is mounted
onMounted(() => {
  loadMyParticipations();
  fetchSurahs();
});

function toggleShareModal() {
  showShareModal.value = !showShareModal.value;
}

// Functions for Surah assignments
function isSurahAssigned(surahNumber) {
  if (!store.currentKhatmah) return false;
  return store.currentKhatmah.surah_assignments.some(a => a.surah_number === surahNumber);
}

function getSurahAssignment(surahNumber) {
  if (!store.currentKhatmah) return null;
  return store.currentKhatmah.surah_assignments.find(a => a.surah_number === surahNumber);
}

function isMySurahAssignment(surahNumber) {
  if (!store.currentParticipant || !store.currentKhatmah) return false;
  const assignment = getSurahAssignment(surahNumber);
  return assignment && assignment.participant === store.currentParticipant.id;
}

async function handleSurahClick(surahNumber) {
  // Clear any previous errors
  juzError.value = '';
  
  // Check if user has joined
  if (!store.currentParticipant) {
    juzError.value = t('khatmahDetail.joinFirst');
    scrollToError(); // Scroll to error
    return;
  }
  
  // Check if surah is already assigned to someone else
  if (isSurahAssigned(surahNumber) && !isMySurahAssignment(surahNumber)) {
    juzError.value = t('khatmahDetail.surahAlreadyAssigned');
    scrollToError(); // Scroll to error
    return;
  }
  
  // If it's my surah, navigate to read it
  if (isMySurahAssignment(surahNumber)) {
    const assignment = getSurahAssignment(surahNumber);
    if (assignment) {
      // Navigate to SurahList view for reading
      navigateToSurah(surahNumber);
    }
  } else {
    // If not assigned, show confirmation dialog
    confirmingSurahNumber.value = surahNumber;
    showSurahConfirmation.value = true;
  }
}

// Add new function to navigate to SurahList view
function navigateToSurah(surahNumber) {
  // Emit an event that can be handled by parent component to navigate
  emit('navigate-to-surah', {
    surah: surahNumber
  });
  
  // The parent component (App.vue) will handle the navigation to the Quran reader
}

// Function to confirm surah assignment
async function confirmSurahAssignment() {
  if (confirmingSurahNumber.value) {
    await store.assignSurah(props.khatmahId, confirmingSurahNumber.value);
    // Close the confirmation dialog
    showSurahConfirmation.value = false;
    
    // Navigate to SurahList view for reading after assignment
    navigateToSurah(confirmingSurahNumber.value);
    
    confirmingSurahNumber.value = null;
  }
}

// Function to cancel surah assignment
function cancelSurahAssignment() {
  showSurahConfirmation.value = false;
  confirmingSurahNumber.value = null;
}

function getSurahCardClass(surahNumber) {
  if (isSurahAssigned(surahNumber)) {
    if (isMySurahAssignment(surahNumber)) {
      if (getSurahAssignment(surahNumber).completed) {
        return 'bg-emerald-100 text-emerald-800 border border-emerald-300 hover:bg-emerald-200';
      }
      return 'bg-blue-100 text-blue-800 border border-blue-300 hover:bg-blue-200';
    }
    if (getSurahAssignment(surahNumber).completed) {
      return 'bg-green-50 text-green-800 border border-green-200 hover:bg-green-100 completed-by-other';
    }
    return 'bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 card-in-progress';
  }
  return 'bg-white text-gray-800 border border-gray-200 hover:bg-gray-50';
}

// Function to handle marking a Surah as completed
async function toggleSurahComplete(assignmentId) {
  await store.toggleSurahComplete(assignmentId, props.khatmahId);
}

// Function to handle going back from Surah reader
function handleBackFromSurah() {
  // No need to reset any state here as we're using navigation
}

// Add function to fetch Surahs data from API
async function fetchSurahs() {
  loadingSurahs.value = true;
  surahsError.value = null;
  
  try {
    const response = await axios.get('https://api.alquran.cloud/v1/surah');
    
    if (response.data && response.data.code === 200 && response.data.data) {
      surahs.value = response.data.data;
      filteredSurahs.value = response.data.data;
      
      // Pre-normalize all surah names for faster searching
      normalizedSurahNames.value = surahs.value.map(surah => ({
        number: surah.number,
        normalizedName: normalizeArabicText(surah.name),
        // Also store a version without "سورة" prefix for more flexible matching
        normalizedNameNoPrefix: normalizeArabicText(surah.name.replace(/^سورة\s+/i, ''))
      }));
    } else {
      surahsError.value = 'Invalid API response format';
    }
  } catch (error) {
    console.error('Error fetching Surahs:', error);
    surahsError.value = 'Failed to load Surahs data';
  } finally {
    loadingSurahs.value = false;
  }
}

// Arabic text normalization for search
function normalizeArabicText(text) {
  if (!text) return '';
  
  // First remove ALL possible diacritical marks in Arabic
  let normalized = text
    // Remove harakat (fatha, damma, kasra, etc.)
    .replace(/[\u064B-\u0652]/g, '')
    // Remove tatweel (stretching character)
    .replace(/\u0640/g, '')
    // Remove other diacritics and special marks
    .replace(/[\u0653-\u0655\u0670\u06D6-\u06ED]/g, '')
    // Remove zero-width joiner and non-joiner
    .replace(/[\u200C\u200D]/g, '');
  
  // Normalize Arabic letters that may appear in different forms
  normalized = normalized
    // Normalize alifs
    .replace(/[\u0622\u0623\u0625\u0671\u0672\u0673\u0675]/g, '\u0627')
    // Normalize yaa and alif maqsura
    .replace(/\u0649/g, '\u064A')
    // Normalize taa marbouta to haa
    .replace(/\u0629/g, '\u0647')
    // Normalize various forms of hamza
    .replace(/[\u0624\u0626]/g, '\u0621');
  
  return normalized;
}

// Enhanced search for Arabic text
function searchArabicText(query, surah) {
  // Normalize the query
  const normalizedQuery = normalizeArabicText(query);
  
  // Get pre-normalized name for this surah
  const surahInfo = normalizedSurahNames.value.find(s => s.number === surah.number);
  if (!surahInfo) return false;
  
  // Check if the normalized query matches the normalized surah name
  if (surahInfo.normalizedName.includes(normalizedQuery)) {
    return true;
  }
  
  // Check if query might be just the surah name without "سورة" prefix
  if (surahInfo.normalizedNameNoPrefix.includes(normalizedQuery)) {
    return true;
  }
  
  // Additional check: If query is very short (1-2 chars), be more lenient
  if (normalizedQuery.length <= 2) {
    // For short queries, look for exact character matches but don't require sequence
    return [...normalizedQuery].every(char => 
      surahInfo.normalizedName.includes(char) || 
      surahInfo.normalizedNameNoPrefix.includes(char)
    );
  }
  
  return false;
}

// Function to filter surahs based on search query
function filterSurahs() {
  if (!searchQuery.value.trim()) {
    filteredSurahs.value = surahs.value;
    return;
  }
  
  const query = searchQuery.value.toLowerCase().trim();
  
  // Check if the search query contains Arabic characters
  const containsArabic = /[\u0600-\u06FF]/.test(query);
  
  filteredSurahs.value = surahs.value.filter(surah => {
    // Search in English name
    const englishMatch = surah.englishName.toLowerCase().includes(query);
    
    // Search in surah number
    const numberMatch = surah.number.toString() === query;
    
    // Search in English translation if available
    const translationMatch = surah.englishNameTranslation && 
      surah.englishNameTranslation.toLowerCase().includes(query);
    
    // Enhanced Arabic matching
    let arabicMatch = false;
    
    if (containsArabic) {
      // Use the enhanced Arabic search method
      arabicMatch = searchArabicText(query, surah);
    } else {
      // For non-Arabic queries, try simple matching against the original name
      arabicMatch = surah.name.includes(query);
    }
    
    return englishMatch || numberMatch || arabicMatch || translationMatch;
  });
}

// Function to clear search
function clearSearch() {
  searchQuery.value = '';
  filteredSurahs.value = surahs.value;
}

//Add this new function to handle scrolling to error
function scrollToError() {
  // Wait for DOM update
  setTimeout(() => {
    const errorElement = document.querySelector('.error-message');
    if (errorElement) {
      errorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, 100);
}

// Add to existing imports
const showRemoveParticipantConfirm = ref(false);
const participantToRemove = ref(null);

// Add new function to handle participant removal
async function handleRemoveParticipant(participant) {
  participantToRemove.value = participant;
  showRemoveParticipantConfirm.value = true;
}

async function confirmRemoveParticipant() {
  if (!participantToRemove.value) return;
  
  const result = await store.removeParticipant(
    props.khatmahId,
    participantToRemove.value.id
  );
  
  if (result) {
    showRemoveParticipantConfirm.value = false;
    participantToRemove.value = null;
  }
}

function cancelRemoveParticipant() {
  showRemoveParticipantConfirm.value = false;
  participantToRemove.value = null;
}
</script>

<template>
  <div class="khatmah-detail-container">
    <!-- Juz Reader View -->
    <div v-if="isReadingJuz && currentReadingJuz && currentAssignmentId">
      <JuzReader 
        :khatmah-id="khatmahId"
        :juz-number="currentReadingJuz" 
        :assignment-id="currentAssignmentId"
        @back-to-khatmah="handleBackFromJuz"
        @mark-completed="handleMarkCompleted"
      />
    </div>
    
    <!-- My Participations View -->
    <div v-else-if="showMyParticipations" class="my-participations">
      <div class="mb-6">
        <button 
          @click="toggleMyParticipations" 
          class="flex items-center text-gray-600 hover:text-gray-800 mb-4"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
          {{ t('khatmahDetail.backToDetails') || 'Back to Khatmah Details' }}
        </button>
        
        <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-2 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
          </svg>
          {{ t('khatmahDetail.myParticipations') || 'My Participations' }}
        </h2>
      </div>
      
      <!-- No participations message -->
      <div v-if="myParticipations.length === 0" class="bg-gray-50 rounded-lg p-8 text-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">{{ t('khatmahDetail.noParticipations') || 'No Participations Found' }}</h3>
        <p class="text-gray-500 mb-4">
          {{ t('khatmahDetail.noParticipationsDescription') || 'You have not participated in any Khatmahs yet.' }}
        </p>
      </div>
      
      <!-- Participations list -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="participation in myParticipations" 
          :key="participation.id"
          class="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer"
          @click="selectKhatmah(participation.khatmahId)"
        >
          <div class="p-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-semibold text-gray-800">{{ participation.khatmahName }}</h3>
              <span 
                v-if="props.khatmahId === participation.khatmahId" 
                class="text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full"
              >
                {{ t('khatmahDetail.current') || 'Current' }}
              </span>
            </div>
            
            <div class="text-gray-800 flex items-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
              </svg>
              {{ t('khatmahDetail.joinedAs') }}: {{ participation.name }}
            </div>
            
            <div class="mt-3 flex justify-between">
              <button
                @click.stop="selectKhatmah(participation.khatmahId)"
                class="flex items-center px-2 py-1 bg-emerald-50 text-emerald-700 rounded-md hover:bg-emerald-100 transition-colors text-xs"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                  <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                </svg>
                {{ t('khatmahDetail.view') || 'View' }}
              </button>
              
              <button
                v-if="props.khatmahId !== participation.khatmahId"
                @click.stop="selectKhatmah(participation.khatmahId)"
                class="flex items-center px-2 py-1 bg-blue-50 text-blue-700 rounded-md hover:bg-blue-100 transition-colors text-xs"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
                {{ t('khatmahDetail.switch') || 'Switch' }}
              </button>
            </div>
          </div>
        </div>
      </div>
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
          <div class="rounded-xl overflow-hidden shadow-sm border border-gray-100 flex justify-center bg-gray-50 mx-auto" style="width: 300px; height: 200px;">
            <img 
              :src="store.currentKhatmah.image_url" 
              :alt="store.currentKhatmah.name" 
              class="w-full h-full object-scale-down"
              loading="lazy"
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
            
            <div class="text-sm text-gray-500 mb-2">
              <span>{{ t('khatmahDetail.khatmahId') }}: </span>
              <code class="bg-gray-100 px-2 py-1 rounded text-gray-700">{{ props.khatmahId }}</code>
              <button 
                @click="copyKhatmahLink" 
                class="ml-2 text-emerald-600 hover:text-emerald-700 focus:outline-none inline-flex items-center"
                :title="t('khatmahDetail.copyLinkToClipboard')"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
                  <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
                </svg>
                <span class="ml-1 text-xs">{{ t('khatmahDetail.copyLink') }}</span>
              </button>
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
                @click="toggleShareModal"
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
                <template v-if="store.currentKhatmah.khatmah_type === 'juz'">
                  {{ store.currentKhatmah.assignments.filter(a => a.completed).length }}/30
                </template>
                <template v-else-if="store.currentKhatmah.khatmah_type === 'surah'">
                  {{ store.currentKhatmah.surah_assignments.filter(a => a.completed).length }}/114
                </template>
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
                    :stroke-dasharray="`${getCompletionPercentage()}, 100`"
                  />
                </svg>
                <div class="absolute inset-0 flex items-center justify-center text-xs font-medium">
                  <span class="text-xxs whitespace-nowrap">
                    <template v-if="store.currentKhatmah.khatmah_type === 'juz'">
                      {{ store.currentKhatmah.assignments.filter(a => a.completed).length }}/30
                    </template>
                    <template v-else-if="store.currentKhatmah.khatmah_type === 'surah'">
                      {{ store.currentKhatmah.surah_assignments.filter(a => a.completed).length }}/114
                    </template>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Join Khatmah Form (if not joined) -->
        <div v-if="!store.currentParticipant" class="bg-white rounded-xl shadow-sm p-6 mb-8 border border-gray-100">
          <h3 class="text-xl font-semibold mb-4 text-gray-800">{{ t('khatmahDetail.joinKhatmah') }}</h3>
          
          <!-- Display error message if any -->
          <p v-if="nameError || juzError" class="error-message mb-4 text-sm text-red-600 bg-red-50 p-3 rounded-md flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            {{ nameError || juzError }}
          </p>
          
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
        </div>
        
        <!-- Global error display that's always visible regardless of join status -->
        <div v-if="juzError" class="error-message bg-red-50 border border-red-200 rounded-lg p-3 mb-6 sticky top-4 z-10">
          <p class="text-sm text-red-600 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            {{ juzError }}
          </p>
        </div>
        
        <!-- Assignment grid for Juz -->
        <template v-if="store.currentKhatmah && store.currentKhatmah.khatmah_type === 'juz'">
          <h3 class="text-xl font-semibold mb-4 text-gray-800">{{ t('khatmahDetail.juzAssignments') }}</h3>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-6 gap-3 mb-10">
            <div
              v-for="juz in 30"
              :key="`juz-${juz}`"
              :class="[
                'p-3 rounded-lg text-center cursor-pointer transition-all',
                getJuzCardClass(juz)
              ]"
              @click="handleJuzClick(juz)"
            >
              <div class="font-medium">{{ t('khatmahDetail.juzNumber', { number: juz }) }}</div>
              <div class="text-sm mt-1">
                <template v-if="getJuzAssignment(juz)">
                  <div class="text-xs font-semibold">
                    <span>{{ t('khatmahDetail.assignedTo') || 'Assigned to' }}:</span> {{ getJuzAssignment(juz).participant_name }}
                    <span v-if="isMyJuz(juz)" class="text-xs text-rose-700 font-bold">({{ t('khatmahDetail.you') }})</span>
                  </div>
                  <div v-if="getJuzAssignment(juz).completed" class="text-emerald-700 text-xs mt-1 font-medium">
                    {{ t('khatmahDetail.completed') }}
                  </div>
                  <div v-else-if="isMyJuz(juz)" class="text-blue-600 text-xs mt-1 font-medium flex flex-col">
                    <span>{{ t('khatmahDetail.clickToRead') }}</span>
                    <button 
                      class="mt-2 px-3 py-1.5 bg-emerald-100 text-emerald-700 rounded text-sm hover:bg-emerald-200 font-medium w-full"
                      @click.stop="toggleComplete(getJuzAssignment(juz).id)"
                    >
                      {{ t('khatmahDetail.markComplete') }}
                    </button>
                  </div>
                  <div v-else class="text-amber-600 text-xs mt-1 font-medium juz-in-progress">
                    {{ t('khatmahDetail.inProgress') }}
                    <span class="pulse-dot ml-1"></span>
                  </div>
                </template>
                <template v-else>
                  <div class="text-gray-500 text-xs">{{ t('khatmahDetail.notAssigned') }}</div>
                  <div v-if="store.currentParticipant" class="text-blue-600 text-xs mt-1">{{ t('khatmahDetail.clickToSelect') }}</div>
                </template>
              </div>
            </div>
          </div>
        </template>
        
        <!-- Surah Assignments -->
        <template v-else-if="store.currentKhatmah && store.currentKhatmah.khatmah_type === 'surah'">
          <h3 class="text-xl font-semibold mb-4 text-gray-800">{{ t('khatmahDetail.surahAssignments') }}</h3>
          
          <div class="surah-content-container relative border border-gray-200 rounded-xl overflow-hidden">
            <!-- Search input - Fixed at top -->
            <div class="sticky top-0 z-10 bg-white border-b border-gray-200 p-4">
              <div class="bg-gray-50 p-3 rounded-lg border border-gray-200">
                <h4 class="text-sm font-medium text-gray-700 mb-2 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  {{ t('quran.searchSurahCaption') || 'Search Surahs' }}
                </h4>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                  <input 
                    type="text" 
                    v-model="searchQuery" 
                    class="w-full pl-10 pr-10 py-3 sm:py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-base sm:text-sm" 
                    :placeholder="t('quran.searchSurah') || 'Search surah by name or number...'"
                    @input="filterSurahs"
                  />
                  <button 
                    v-if="searchQuery" 
                    @click="clearSearch" 
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 focus:outline-none"
                    aria-label="Clear search"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-4 sm:w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Scrollable content area -->
            <div class="surah-scrollable-content overflow-y-auto p-4">
              <!-- Loading state for Surahs -->
              <div v-if="loadingSurahs" class="flex justify-center items-center py-12">
                <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-500"></div>
              </div>
              
              <!-- Error state for Surahs -->
              <div v-else-if="surahsError" class="bg-red-50 p-4 rounded-lg mb-6">
                <p class="text-red-600 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                  {{ surahsError }}
                </p>
                <button 
                  @click="fetchSurahs" 
                  class="mt-2 px-3 py-1 bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors text-sm"
                >
                  {{ t('common.retry') || 'Retry' }}
                </button>
              </div>

              <!-- No results message -->
              <div v-else-if="filteredSurahs.length === 0 && searchQuery" class="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <p class="text-gray-600 font-medium">{{ t('quran.noSurahResults') || 'No surahs found matching your search.' }}</p>
                <button 
                  @click="clearSearch" 
                  class="mt-4 px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200 transition-colors inline-flex items-center"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                  {{ t('quran.clearSearch') || 'Clear search' }}
                </button>
              </div>
              
              <!-- Surah Cards -->
              <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 mb-10">
                <div
                  v-for="surah in filteredSurahs"
                  :key="`surah-${surah.number}`"
                  :class="[
                    'p-3 rounded-lg cursor-pointer transition-all relative overflow-hidden',
                    getSurahCardClass(surah.number)
                  ]"
                  @click="handleSurahClick(surah.number)"
                >
                  <!-- Surah number badge -->
                  <div class="absolute top-2 right-2 bg-gray-100 text-gray-700 rounded-full w-6 h-6 flex items-center justify-center text-xs font-medium">
                    {{ surah.number }}
                  </div>
                  
                  <!-- Surah content -->
                  <div class="text-right mt-2 mb-1">
                    <span class="text-lg font-arabic leading-tight block" :dir="'rtl'">{{ surah.name }}</span>
                  </div>
                  
                  <div class="text-sm">
                    <span class="font-medium">{{ surah.englishName }}</span>
                    <span class="text-xs text-gray-500 block">{{ surah.englishNameTranslation }}</span>
                    <span class="text-xs bg-gray-100 text-gray-700 rounded-full px-2 py-0.5 mt-1 inline-block">
                      {{ surah.numberOfAyahs }} {{ t('khatmahDetail.ayahs') || 'Ayahs' }}
                    </span>
                    <span 
                      class="text-xs ml-1 rounded-full px-2 py-0.5 mt-1 inline-block"
                      :class="surah.revelationType === 'Meccan' ? 'bg-amber-50 text-amber-800' : 'bg-emerald-50 text-emerald-800'"
                    >
                      {{ surah.revelationType }}
                    </span>
                  </div>
                  
                  <!-- Assignment info -->
                  <div class="text-sm mt-3 border-t border-gray-100 pt-2">
                    <template v-if="getSurahAssignment(surah.number)">
                      <div class="text-xs font-semibold">
                        <span>{{ t('khatmahDetail.assignedTo') || 'Assigned to' }}:</span> {{ getSurahAssignment(surah.number).participant_name }}
                        <span v-if="isMySurahAssignment(surah.number)" class="text-xs text-rose-700 font-bold">({{ t('khatmahDetail.you') }})</span>
                      </div>
                      <div v-if="getSurahAssignment(surah.number).completed" class="text-emerald-700 text-xs mt-1 font-medium">
                        {{ t('khatmahDetail.completed') }}
                      </div>
                      <div v-else-if="isMySurahAssignment(surah.number)" class="text-blue-600 text-xs mt-1 font-medium flex flex-col">
                        <span>{{ t('khatmahDetail.clickToRead') }}</span>
                        <button 
                          class="mt-2 px-3 py-1.5 bg-emerald-100 text-emerald-700 rounded text-sm hover:bg-emerald-200 font-medium w-full"
                          @click.stop="toggleSurahComplete(getSurahAssignment(surah.number).id)"
                        >
                          {{ t('khatmahDetail.markComplete') }}
                        </button>
                      </div>
                      <div v-else class="text-amber-600 text-xs mt-1 font-medium juz-in-progress">
                        {{ t('khatmahDetail.inProgress') }}
                        <span class="pulse-dot ml-1"></span>
                      </div>
                    </template>
                    <template v-else>
                      <div class="text-gray-500 text-xs">{{ t('khatmahDetail.notAssigned') }}</div>
                      <div v-if="store.currentParticipant" class="text-blue-600 text-xs mt-1">{{ t('khatmahDetail.clickToSelect') }}</div>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
        
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
                      <span 
                        v-if="store.currentKhatmah.creator && participant.id === store.currentKhatmah.creator.id"
                        class="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full"
                      >
                        {{ t('khatmahDetail.creator') }}
                      </span>
                    </div>
                  </div>
                  <div class="flex items-center space-x-4">
                    <div class="text-sm text-gray-500">
                      {{ t('khatmahDetail.joined') }}: {{ new Date(participant.created_at).toLocaleDateString() }}
                    </div>
                    <div class="text-sm bg-gray-100 text-gray-800 px-2 py-1 rounded-md">
                      <template v-if="store.currentKhatmah.khatmah_type === 'juz'">
                        {{ getParticipantJuzCount(participant.id) }} {{ getParticipantJuzCount(participant.id) >= 3 ? t('khatmahDetail.juzPlural') : t('khatmahDetail.juz') }}
                      </template>
                      <template v-else>
                        {{ getParticipantSurahCount(participant.id) }} {{ getParticipantSurahCount(participant.id) >= 3 ? t('khatmahDetail.surahPlural') : t('khatmahDetail.surah') }}
                      </template>
                    </div>
                    <!-- Add remove button for creator -->
                    <button
                      v-if="store.isKhatmahCreator(props.khatmahId) && 
                            (!store.currentKhatmah.creator || participant.id !== store.currentKhatmah.creator.id)"
                      @click="handleRemoveParticipant(participant)"
                      class="text-red-600 hover:text-red-700 focus:outline-none"
                      :title="t('khatmahDetail.removeParticipant')"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Share Modal -->
    <transition name="fade">
      <div v-if="showShareModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click.self="toggleShareModal">
        <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4 transform transition-all">
          <h3 class="text-lg font-semibold mb-4">{{ t('khatmahDetail.shareKhatmah') || 'Share Khatmah' }}</h3>
          
          <!-- QR Code section (if implemented) -->
          <div class="mb-6 text-center" v-if="false">
            <!-- Future QR code implementation -->
          </div>
          
          <div class="mb-6">
            <p class="text-gray-600 mb-2">{{ t('khatmahDetail.shareDescription') || 'Share this link with others to invite them to this Khatmah:' }}</p>
            <div class="flex items-center">
              <input 
                type="text" 
                readonly 
                :value="getKhatmahUrl()" 
                class="block w-full border border-gray-300 rounded-l-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button 
                @click="copyKhatmahLink" 
                class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-r-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 flex items-center"
              >
                <svg v-if="!linkCopied" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
                  <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <span v-if="!linkCopied">{{ t('khatmahDetail.copy') || 'Copy' }}</span>
                <span v-else>{{ t('khatmahDetail.copied') || 'Copied!' }}</span>
              </button>
            </div>
          </div>
          
          <div class="flex flex-col sm:flex-row sm:justify-between gap-2">
            <button 
              @click="shareKhatmah"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-full sm:w-auto"
            >
              {{ t('khatmahDetail.shareButton') || 'Share' }}
            </button>
            <button 
              @click="toggleShareModal"
              class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg text-sm focus:outline-none w-full sm:w-auto"
            >
              {{ t('khatmahDetail.close') || 'Close' }}
            </button>
          </div>
        </div>
      </div>
    </transition>
    
    <!-- Confirmation Dialogs -->
    <!-- Juz Confirmation Modal -->
    <div v-if="showJuzConfirmation" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full m-4">
        <h3 class="text-lg font-semibold mb-4 text-gray-800">{{ t('khatmahDetail.confirmJuzSelection') || 'Confirm Juz Selection' }}</h3>
        <p class="mb-6 text-gray-600">
          {{ t('khatmahDetail.confirmJuzSelectionText', { number: confirmingJuzNumber }) || `Are you sure you want to select Juz ${confirmingJuzNumber}?` }}
        </p>
        <div class="flex justify-end gap-3">
          <button 
            @click="cancelJuzAssignment" 
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
          >
            {{ t('common.cancel') || 'Cancel' }}
          </button>
          <button 
            @click="confirmJuzAssignment" 
            class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 transition-colors"
          >
            {{ t('common.confirm') || 'Confirm' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Surah Confirmation Modal -->
    <div v-if="showSurahConfirmation" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full m-4">
        <h3 class="text-lg font-semibold mb-4 text-gray-800">{{ t('khatmahDetail.confirmSurahSelection') || 'Confirm Surah Selection' }}</h3>
        <p class="mb-6 text-gray-600">
          {{ t('khatmahDetail.confirmSurahSelectionText', { number: confirmingSurahNumber }) || `Are you sure you want to select Surah ${confirmingSurahNumber}?` }}
        </p>
        <div class="flex justify-end gap-3">
          <button 
            @click="cancelSurahAssignment" 
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
          >
            {{ t('common.cancel') || 'Cancel' }}
          </button>
          <button 
            @click="confirmSurahAssignment" 
            class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-700 transition-colors"
          >
            {{ t('common.confirm') || 'Confirm' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Back button to return to list -->
    <div class="mt-4 text-center">
      <button 
        @click="$emit('cancel')" 
        class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
      >
        {{ t('khatmahDetail.backToList') || 'Back to List' }}
      </button>
    </div>

    <!-- Add Remove Participant Confirmation Modal -->
    <div v-if="showRemoveParticipantConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full m-4">
        <h3 class="text-lg font-semibold mb-4 text-gray-800">{{ t('khatmahDetail.confirmRemoveParticipant') || 'Remove Participant' }}</h3>
        <p class="mb-6 text-gray-600">
          {{ t('khatmahDetail.confirmRemoveParticipantText', { name: participantToRemove?.name }) || 
             `Are you sure you want to remove ${participantToRemove?.name}? This will remove all their assignments and progress.` }}
        </p>
        <div class="flex justify-end gap-3">
          <button 
            @click="cancelRemoveParticipant" 
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
          >
            {{ t('common.cancel') || 'Cancel' }}
          </button>
          <button 
            @click="confirmRemoveParticipant" 
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
          >
            {{ t('common.remove') || 'Remove' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.juz-in-progress {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-in-progress {
  animation: card-pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Style for completed cards by other participants */
.completed-by-other {
  position: relative;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-color: #86efac !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.completed-by-other:after {
  content: "✓";
  position: absolute;
  top: 8px;
  right: 8px;
  width: 16px;
  height: 16px;
  background-color: #22c55e;
  color: white;
  border-radius: 50%;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.9;
}

/* Add styles for error message to ensure visibility and scrolling */
.error-message {
  position: relative;
  z-index: 5;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-left: 3px solid #ef4444;
}

@keyframes card-pulse {
  0%, 100% {
    border-color: #fcd34d;
  }
  50% {
    border-color: #f59e0b;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

.pulse-dot {
  display: inline-block;
  height: 6px;
  width: 6px;
  background-color: #f59e0b;
  border-radius: 50%;
  animation: pulse-dot 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse-dot {
  0% {
    transform: scale(0.8);
    opacity: 0.8;
  }
  50% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(0.8);
    opacity: 0.8;
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

.text-xxs {
  font-size: 0.65rem;
  line-height: 1rem;
}

/* Arabic font styling */
.font-arabic {
  font-family: 'Traditional Arabic', 'Scheherazade New', 'Amiri', 'Noto Naskh Arabic', serif;
  font-size: 1.25rem;
  font-weight: 400;
}

/* Add these new styles at the top of your style section */
.surah-content-container {
  height: calc(100vh - 400px);
  min-height: 500px;
  max-height: 800px;
  display: flex;
  flex-direction: column;
  margin-bottom: 2rem;
  background: white;
}

.surah-scrollable-content {
  flex: 1;
  height: 100%;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.surah-scrollable-content::-webkit-scrollbar {
  width: 6px;
}

.surah-scrollable-content::-webkit-scrollbar-track {
  background: transparent;
}

.surah-scrollable-content::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}
</style> 