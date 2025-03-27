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
const selectedImage = ref(null);
const imagePreview = ref('');
const khatmahType = ref('juz'); // Default to juz-based khatmah

function handleImageChange(event) {
  const file = event.target.files[0];
  if (file) {
    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      alert(t('createKhatmah.imageSizeError'));
      event.target.value = '';
      return;
    }
    
    if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
      alert(t('createKhatmah.imageTypeError'));
      event.target.value = '';
      return;
    }
    
    selectedImage.value = file;
    imagePreview.value = URL.createObjectURL(file);
  } else {
    selectedImage.value = null;
    imagePreview.value = '';
  }
}

async function createKhatmah() {
  // Validate
  if (!khatmahName.value.trim()) {
    nameError.value = t('createKhatmah.nameError');
    return;
  }
  
  nameError.value = '';
  
  // Prepare form data for multipart/form-data
  const formData = new FormData();
  formData.append('name', khatmahName.value);
  formData.append('is_private', isPrivate.value);
  formData.append('require_name', requireName.value);
  formData.append('khatmah_type', khatmahType.value);
  
  if (hasEndDate.value && endDate.value) {
    formData.append('end_date', endDate.value);
  }
  
  if (selectedImage.value) {
    formData.append('image', selectedImage.value);
  }
  
  // Create khatmah
  const newKhatmah = await store.createKhatmah(formData);
  
  if (newKhatmah) {
    // Reset form
    khatmahName.value = '';
    isPrivate.value = false;
    requireName.value = true;
    hasEndDate.value = false;
    endDate.value = '';
    selectedImage.value = null;
    imagePreview.value = '';
    khatmahType.value = 'juz';
    
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
          
          <!-- Khatmah Type -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('createKhatmah.typeLabel') }}</label>
            <div class="mt-2 flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-6">
              <div class="flex items-center">
                <input 
                  id="juzType" 
                  v-model="khatmahType" 
                  type="radio" 
                  value="juz"
                  class="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300"
                />
                <label for="juzType" class="ml-2 block text-sm text-gray-700">
                  {{ t('createKhatmah.juzTypeLabel') }}
                </label>
                <div class="ml-2 text-xs bg-emerald-100 text-emerald-800 py-0.5 px-2 rounded-full">
                  30 {{ t('createKhatmah.parts') }}
                </div>
              </div>
              
              <div class="flex items-center">
                <input 
                  id="surahType" 
                  v-model="khatmahType" 
                  type="radio" 
                  value="surah"
                  class="h-4 w-4 text-emerald-600 focus:ring-emerald-500 border-gray-300"
                />
                <label for="surahType" class="ml-2 block text-sm text-gray-700">
                  {{ t('createKhatmah.surahTypeLabel') }}
                </label>
                <div class="ml-2 text-xs bg-blue-100 text-blue-800 py-0.5 px-2 rounded-full">
                  114 {{ t('createKhatmah.surahs') }}
                </div>
              </div>
            </div>
            <p class="mt-2 text-xs text-gray-500">
              {{ t('createKhatmah.typeHelp') }}
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
          
          <!-- Image Upload -->
          <div class="mb-6">
            <label for="imageUpload" class="block text-sm font-medium text-gray-700 mb-2">{{ t('createKhatmah.imageLabel') }}</label>
            <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-emerald-500 transition-colors">
              <div class="space-y-1 text-center">
                <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                  <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <div class="flex text-sm text-gray-600">
                  <label for="imageUpload" class="relative cursor-pointer bg-white rounded-md font-medium text-emerald-600 hover:text-emerald-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-emerald-500">
                    <span>{{ t('createKhatmah.uploadImage') }}</span>
                    <input 
                      id="imageUpload" 
                      type="file" 
                      @change="handleImageChange" 
                      accept="image/jpeg,image/png,image/gif"
                      class="sr-only"
                    />
                  </label>
                  <p class="pl-1">{{ t('createKhatmah.dragAndDrop') }}</p>
                </div>
                <p class="text-xs text-gray-500">
                  {{ t('createKhatmah.imageHelp') }}
                </p>
              </div>
            </div>
            
            <!-- Image Preview -->
            <div v-if="imagePreview" class="mt-3">
              <div class="relative border rounded-lg overflow-hidden">
                <img :src="imagePreview" alt="Khatmah image preview" class="w-full h-40 object-cover" />
                <button 
                  @click="selectedImage = null; imagePreview = ''" 
                  class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
                  type="button"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
                <div class="bg-gray-50 px-3 py-2 text-xs text-gray-500">{{ t('createKhatmah.imagePreview') }}</div>
              </div>
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