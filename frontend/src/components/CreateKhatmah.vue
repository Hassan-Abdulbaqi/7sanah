<script setup>
import { ref, defineEmits } from 'vue';
import { useI18n } from 'vue-i18n';
import { store } from '../store';

const { t } = useI18n();
const emit = defineEmits(['khatmah-created', 'cancel']);
const khatmahName = ref('');
const nameError = ref('');
const isPrivate = ref(false);
const requireName = ref(true);
const hasEndDate = ref(false);
const endDate = ref('');
const imageUrl = ref('');
const imagePreview = ref('');

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

async function createKhatmah() {
  // Validate
  if (!khatmahName.value.trim()) {
    nameError.value = t('createKhatmah.nameError');
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
  
  // Create khatmah
  const newKhatmah = await store.createKhatmah(khatmahData);
  
  if (newKhatmah) {
    // Reset form
    khatmahName.value = '';
    isPrivate.value = false;
    requireName.value = true;
    hasEndDate.value = false;
    endDate.value = '';
    imageUrl.value = '';
    imagePreview.value = '';
    
    // Emit event with created khatmah
    emit('khatmah-created', newKhatmah);
  }
}

function cancel() {
  emit('cancel');
}
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-8 text-gray-800 flex items-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mr-2 text-emerald-600" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
      </svg>
      {{ t('createKhatmah.title') }}
    </h2>
    
    <div class="max-w-2xl mx-auto">
      <div class="bg-white rounded-xl shadow-sm p-8 border border-gray-100">
        <div class="mb-8 text-center">
          <div class="inline-flex items-center justify-center mb-4">
            <img src="../assets/7sanah_logo.png" alt="7sanah Logo" class="h-16 w-auto" />
          </div>
          <p class="text-gray-600">{{ t('createKhatmah.subtitle') }}</p>
        </div>
        
        <form @submit.prevent="createKhatmah">
          <!-- Khatmah Name -->
          <div class="mb-6">
            <label for="khatmahName" class="block text-sm font-medium text-gray-700 mb-2">{{ t('createKhatmah.nameLabel') }}*</label>
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
                :placeholder="t('createKhatmah.namePlaceholder')"
              />
            </div>
            <p v-if="nameError" class="mt-2 text-sm text-red-600 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              {{ nameError }}
            </p>
            <p class="mt-2 text-xs text-gray-500">
              {{ t('createKhatmah.nameHelp') }}
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
                {{ t('createKhatmah.privateLabel') }}
              </label>
            </div>
            <p class="mt-1 text-xs text-gray-500 ml-6">
              {{ t('createKhatmah.privateHelp') }}
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
                {{ t('createKhatmah.requireNameLabel') }}
              </label>
            </div>
            <p class="mt-1 text-xs text-gray-500 ml-6">
              {{ t('createKhatmah.requireNameHelp') }}
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
                {{ t('createKhatmah.endDateLabel') }}
              </label>
            </div>
            
            <div v-if="hasEndDate" class="mt-3 ml-6">
              <label for="endDate" class="block text-sm font-medium text-gray-700 mb-1">{{ t('createKhatmah.endDateInput') }}</label>
              <input
                id="endDate"
                v-model="endDate"
                type="date"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 sm:text-sm"
                :min="new Date().toISOString().split('T')[0]"
              />
              <p class="mt-1 text-xs text-gray-500">
                {{ t('createKhatmah.endDateHelp') }}
              </p>
            </div>
          </div>
          
          <!-- Image URL Option -->
          <div class="mb-6">
            <label for="imageUrl" class="block text-sm font-medium text-gray-700 mb-2">{{ t('createKhatmah.imageLabel') }}</label>
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
                :placeholder="t('createKhatmah.imagePlaceholder')"
              />
            </div>
            <p class="mt-1 text-xs text-gray-500">
              {{ t('createKhatmah.imageHelp') }}
            </p>
            
            <!-- Image Preview -->
            <div v-if="imagePreview" class="mt-3 border rounded-lg overflow-hidden">
              <img :src="imagePreview" alt="Khatmah image preview" class="w-full h-40 object-cover" />
              <div class="bg-gray-50 px-3 py-2 text-xs text-gray-500">{{ t('createKhatmah.imagePreview') }}</div>
            </div>
          </div>
          
          <div class="flex justify-between mt-6">
            <button
              type="button"
              @click="cancel"
              class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors"
            >
              {{ t('createKhatmah.cancel') }}
            </button>
            
            <button
              type="submit"
              class="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
            >
              {{ t('createKhatmah.create') }}
            </button>
          </div>
        </form>
      </div>
      
      <div class="mt-8 bg-emerald-50 rounded-lg p-4 border border-emerald-100">
        <h3 class="font-medium text-emerald-800 mb-2 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
          {{ t('createKhatmah.whatIsKhatmahTitle') }}
        </h3>
        <p class="text-sm text-emerald-700">
          {{ t('createKhatmah.whatIsKhatmahText') }}
        </p>
      </div>
    </div>
  </div>
</template> 