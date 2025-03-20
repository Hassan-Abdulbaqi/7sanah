<script setup>
import { ref, defineProps, defineEmits, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { store } from '../store';

const { t } = useI18n();

const props = defineProps({
  khatmahId: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['khatmah-updated', 'cancel']);
const khatmahName = ref('');
const nameError = ref('');
const isPrivate = ref(false);
const requireName = ref(true);
const hasEndDate = ref(false);
const endDate = ref('');
const imageUrl = ref('');
const imagePreview = ref('');
const deleteConfirmation = ref(false);

// Load khatmah data when component mounts or khatmahId changes
watch(() => props.khatmahId, loadKhatmahData, { immediate: true });

async function loadKhatmahData() {
  if (props.khatmahId) {
    // If we already have the current khatmah loaded, use it
    if (store.currentKhatmah && store.currentKhatmah.id === props.khatmahId) {
      populateForm(store.currentKhatmah);
    } else {
      // Otherwise fetch it
      const khatmah = await store.fetchKhatmah(props.khatmahId);
      if (khatmah) {
        populateForm(khatmah);
      }
    }
  }
}

function populateForm(khatmah) {
  khatmahName.value = khatmah.name;
  isPrivate.value = khatmah.is_private;
  requireName.value = khatmah.require_name;
  
  if (khatmah.end_date) {
    hasEndDate.value = true;
    // Format date to YYYY-MM-DD for input
    endDate.value = new Date(khatmah.end_date).toISOString().split('T')[0];
  } else {
    hasEndDate.value = false;
    endDate.value = '';
  }
  
  imageUrl.value = khatmah.image_url || '';
  if (imageUrl.value && isValidUrl(imageUrl.value)) {
    imagePreview.value = imageUrl.value;
  }
}

function handleImageUrlChange() {
  // Only update preview if URL is valid
  if (imageUrl.value && isValidUrl(imageUrl.value)) {
    imagePreview.value = imageUrl.value;
  } else {
    imagePreview.value = '';
  }
}

function isValidUrl(string) {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}

async function updateKhatmah() {
  // Validate
  if (!khatmahName.value.trim()) {
    nameError.value = t('editKhatmah.nameError');
    return;
  }
  
  nameError.value = '';
  
  // Prepare data
  const khatmahData = {
    name: khatmahName.value,
    is_private: isPrivate.value,
    require_name: requireName.value,
    end_date: hasEndDate.value ? endDate.value : null,
    image_url: imageUrl.value || null
  };
  
  // Update khatmah
  const updatedKhatmah = await store.updateKhatmah(props.khatmahId, khatmahData);
  
  if (updatedKhatmah) {
    emit('khatmah-updated', updatedKhatmah);
  }
}

async function deleteKhatmah() {
  if (deleteConfirmation.value) {
    const success = await store.deleteKhatmah(props.khatmahId);
    if (success) {
      emit('cancel');
    }
  } else {
    deleteConfirmation.value = true;
    // Auto-reset confirmation after 5 seconds
    setTimeout(() => {
      deleteConfirmation.value = false;
    }, 5000);
  }
}

function cancelEdit() {
  emit('cancel');
}
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-8 text-gray-800 flex items-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-2 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
      </svg>
      {{ t('editKhatmah.title') }}
    </h2>
    
    <div class="max-w-2xl mx-auto">
      <div class="bg-white rounded-xl shadow-sm p-8 border border-gray-100">
        <div class="mb-8 text-center">
          <div class="inline-flex items-center justify-center mb-4">
            <img src="../assets/7sanah_logo.png" alt="7sanah Logo" class="h-16 w-auto" />
          </div>
          <p class="text-gray-600">{{ t('editKhatmah.subtitle') }}</p>
        </div>
        
        <form @submit.prevent="updateKhatmah">
          <!-- Khatmah Name -->
          <div class="mb-6">
            <label for="khatmahName" class="block text-sm font-medium text-gray-700 mb-2">{{ t('editKhatmah.nameLabel') }}*</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 2a1 1 0 00-1 1v1a1 1 0 002 0V3a1 1 0 00-1-1zM4 4h3a3 3 0 006 0h3a2 2 0 012 2v9a2 2 0 01-2 2H4a2 2 0 01-2-2V6a2 2 0 012-2zm2.5 7a1.5 1.5 0 100-3 1.5 1.5 0 000 3zm2.45 4a2.5 2.5 0 10-4.9 0h4.9zM12 9a1 1 0 100 2h3a1 1 0 100-2h-3zm-1 4a1 1 0 011-1h2a1 1 0 110 2h-2a1 1 0 01-1-1z" clip-rule="evenodd" />
                </svg>
              </div>
              <input
                id="khatmahName"
                v-model="khatmahName"
                type="text"
                class="block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
                :placeholder="t('editKhatmah.namePlaceholder')"
              />
            </div>
            <p v-if="nameError" class="mt-2 text-sm text-red-600 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              {{ nameError }}
            </p>
          </div>
          
          <!-- Privacy Option -->
          <div class="mb-6">
            <div class="flex items-center">
              <input 
                id="isPrivate" 
                v-model="isPrivate" 
                type="checkbox" 
                class="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
              />
              <label for="isPrivate" class="ml-2 block text-sm text-gray-700">
                {{ t('editKhatmah.privateLabel') }}
              </label>
            </div>
            <p class="mt-1 text-xs text-gray-500 ml-6">
              {{ t('editKhatmah.privateHelp') }}
            </p>
          </div>
          
          <!-- Require Name Option -->
          <div class="mb-6">
            <div class="flex items-center">
              <input 
                id="requireName" 
                v-model="requireName" 
                type="checkbox" 
                class="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
              />
              <label for="requireName" class="ml-2 block text-sm text-gray-700">
                {{ t('editKhatmah.requireNameLabel') }}
              </label>
            </div>
            <p class="mt-1 text-xs text-gray-500 ml-6">
              {{ t('editKhatmah.requireNameHelp') }}
            </p>
          </div>
          
          <!-- End Date Option -->
          <div class="mb-6">
            <div class="flex items-center mb-2">
              <input 
                id="hasEndDate" 
                v-model="hasEndDate" 
                type="checkbox" 
                class="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300 rounded"
              />
              <label for="hasEndDate" class="ml-2 block text-sm text-gray-700">
                {{ t('editKhatmah.endDateLabel') }}
              </label>
            </div>
            
            <div v-if="hasEndDate" class="mt-3 ml-6">
              <label for="endDate" class="block text-sm font-medium text-gray-700 mb-1">{{ t('editKhatmah.endDateInput') }}</label>
              <input
                id="endDate"
                v-model="endDate"
                type="date"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
                :min="new Date().toISOString().split('T')[0]"
              />
              <p class="mt-1 text-xs text-gray-500">
                {{ t('editKhatmah.endDateHelp') }}
              </p>
            </div>
          </div>
          
          <!-- Image URL Option -->
          <div class="mb-6">
            <label for="imageUrl" class="block text-sm font-medium text-gray-700 mb-2">{{ t('editKhatmah.imageLabel') }}</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd" />
                </svg>
              </div>
              <input
                id="imageUrl"
                v-model="imageUrl"
                type="url"
                @input="handleImageUrlChange"
                class="block w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-colors"
                :placeholder="t('editKhatmah.imagePlaceholder')"
              />
            </div>
            <p class="mt-1 text-xs text-gray-500">
              {{ t('editKhatmah.imageHelp') }}
            </p>
            
            <!-- Image Preview -->
            <div v-if="imagePreview" class="mt-3 border rounded-lg overflow-hidden">
              <img :src="imagePreview" alt="Khatmah image preview" class="w-full h-40 object-cover" />
              <div class="bg-gray-50 px-3 py-2 text-xs text-gray-500">{{ t('editKhatmah.imagePreview') }}</div>
            </div>
          </div>
          
          <div class="flex items-center justify-between pt-4">
            <div class="flex space-x-2">
              <button
                type="button"
                @click="cancelEdit"
                class="px-4 py-2 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors"
              >
                {{ t('editKhatmah.cancelButton') }}
              </button>
              
              <button
                type="button"
                @click="deleteKhatmah"
                class="px-4 py-2 bg-red-100 text-red-700 font-medium rounded-lg hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
                :class="{ 'bg-red-600 text-white hover:bg-red-700': deleteConfirmation }"
              >
                {{ deleteConfirmation ? t('editKhatmah.confirmDeleteButton') : t('editKhatmah.deleteButton') }}
              </button>
            </div>
            
            <button
              type="submit"
              class="px-6 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-medium rounded-lg shadow-sm hover:from-emerald-700 hover:to-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-colors"
            >
              {{ t('editKhatmah.saveButton') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template> 