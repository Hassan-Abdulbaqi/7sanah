import { reactive } from 'vue';
import axios from 'axios';

const API_URL = 'http://192.168.84.194:8000/api';
const STORAGE_KEY = 'quran_khatmah_participants';
const CREATED_KHATMAHS_KEY = 'quran_khatmah_created';
const CREATOR_TOKENS_KEY = 'quran_khatmah_creator_tokens';

// Load participants from local storage
const loadParticipantsFromStorage = () => {
  try {
    const storedData = localStorage.getItem(STORAGE_KEY);
    return storedData ? JSON.parse(storedData) : {};
  } catch (error) {
    console.error('Error loading participants from storage:', error);
    return {};
  }
};

// Save participants to local storage
const saveParticipantsToStorage = (participants) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(participants));
  } catch (error) {
    console.error('Error saving participants to storage:', error);
  }
};

// Load created khatmahs from local storage
const loadCreatedKhatmahsFromStorage = () => {
  try {
    const storedData = localStorage.getItem(CREATED_KHATMAHS_KEY);
    return storedData ? JSON.parse(storedData) : [];
  } catch (error) {
    console.error('Error loading created khatmahs from storage:', error);
    return [];
  }
};

// Save created khatmahs to local storage
const saveCreatedKhatmahsToStorage = (khatmahs) => {
  try {
    localStorage.setItem(CREATED_KHATMAHS_KEY, JSON.stringify(khatmahs));
  } catch (error) {
    console.error('Error saving created khatmahs to storage:', error);
  }
};

// Load creator tokens from local storage
const loadCreatorTokensFromStorage = () => {
  try {
    const storedData = localStorage.getItem(CREATOR_TOKENS_KEY);
    return storedData ? JSON.parse(storedData) : {};
  } catch (error) {
    console.error('Error loading creator tokens from storage:', error);
    return {};
  }
};

// Save creator tokens to local storage
const saveCreatorTokensToStorage = (tokens) => {
  try {
    localStorage.setItem(CREATOR_TOKENS_KEY, JSON.stringify(tokens));
  } catch (error) {
    console.error('Error saving creator tokens to storage:', error);
  }
};

export const store = reactive({
  khatmahs: [],
  currentKhatmah: null,
  currentParticipant: null,
  myParticipations: loadParticipantsFromStorage(),
  myCreatedKhatmahs: loadCreatedKhatmahsFromStorage(),
  creatorTokens: loadCreatorTokensFromStorage(),
  loading: false,
  error: null,
  API_URL: API_URL,
  pagination: {
    count: 0,
    next: null,
    previous: null,
    currentPage: 1
  },

  // Initialize store with migrations for existing data
  init() {
    // Migrate any existing created khatmahs to include khatmah_type
    this.migrateCreatedKhatmahs();
  },
  
  // Add missing fields to created khatmahs for compatibility
  migrateCreatedKhatmahs() {
    let needsMigration = false;
    
    this.myCreatedKhatmahs.forEach(khatmah => {
      if (!khatmah.khatmah_type) {
        khatmah.khatmah_type = 'juz'; // Default to juz type for older entries
        needsMigration = true;
      }
      
      if (khatmah.completed_juz_count === undefined) {
        khatmah.completed_juz_count = 0;
        needsMigration = true;
      }
      
      if (khatmah.completed_surah_count === undefined) {
        khatmah.completed_surah_count = 0;
        needsMigration = true;
      }
    });
    
    if (needsMigration) {
      saveCreatedKhatmahsToStorage(this.myCreatedKhatmahs);
    }
  },

  async fetchKhatmahs(page = 1, pageSize = 9) {
    this.loading = true;
    this.error = null;
    try {
      // Sanitize input parameters
      const sanitizedPage = Number.isInteger(page) && page > 0 ? page : 1;
      const sanitizedPageSize = Number.isInteger(pageSize) && pageSize > 0 && pageSize <= 100 ? pageSize : 9;
      
      const response = await axios.get(`${API_URL}/khatmahs/`, {
        params: {
          page: sanitizedPage,
          page_size: sanitizedPageSize,
          is_private: 'false' // Explicitly send as string for known value
        }
      });
      
      // Update pagination information
      this.pagination = {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        currentPage: sanitizedPage
      };
      
      // No need to filter here anymore as the server is already filtering
      this.khatmahs = response.data.results;
    } catch (error) {
      console.error('Error fetching khatmahs:', error);
      this.error = 'Failed to load khatmahs';
    } finally {
      this.loading = false;
    }
  },

  async createKhatmah(formData) {
    this.loading = true;
    this.error = null;
    try {
      const response = await axios.post(`${API_URL}/khatmahs/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      // Immediately save the creator token if present
      if (response.data.creator_token) {
        this.creatorTokens[response.data.id] = response.data.creator_token;
        saveCreatorTokensToStorage(this.creatorTokens);
      }
      
      // Only add to the list if it's not private
      if (!response.data.is_private) {
        this.khatmahs.push(response.data);
      }
      
      // Save to created khatmahs
      const khatmahData = {
        id: response.data.id,
        name: response.data.name,
        created_at: response.data.created_at,
        is_private: response.data.is_private,
        khatmah_type: response.data.khatmah_type,
        completed_juz_count: response.data.completed_juz_count || 0,
        completed_surah_count: response.data.completed_surah_count || 0,
        image: response.data.image || null
      };
      
      this.myCreatedKhatmahs.push(khatmahData);
      saveCreatedKhatmahsToStorage(this.myCreatedKhatmahs);
      
      return response.data;
    } catch (error) {
      console.error('Error creating khatmah:', error);
      this.error = 'Failed to create khatmah';
      return null;
    } finally {
      this.loading = false;
    }
  },

  async updateKhatmah(id, khatmahData) {
    this.loading = true;
    this.error = null;
    try {
      // Only use secure authentication methods
      if (this.creatorTokens[id]) {
        // Add the creator token for ownership verification (preferred method)
        khatmahData.creator_token = this.creatorTokens[id];
      }
      // Only use server-verified participant ID as fallback
      else if (this.currentParticipant && this.currentKhatmah && 
               this.currentKhatmah.creator_id === this.currentParticipant.id) {
        khatmahData.participant_id = this.currentParticipant.id;
      } else {
        this.error = 'You do not have permission to edit this khatmah';
        return null;
      }
      
      const response = await axios.put(`${API_URL}/khatmahs/${id}/`, khatmahData);
      
      // Update in the list if it exists and is not private
      const index = this.khatmahs.findIndex(k => k.id === id);
      if (index !== -1) {
        if (response.data.is_private) {
          // Remove from list if now private
          this.khatmahs.splice(index, 1);
        } else {
          // Update in list
          this.khatmahs[index] = response.data;
        }
      } else if (!response.data.is_private) {
        // Add to list if not private and not already in list
        this.khatmahs.push(response.data);
      }
      
      // Update in created khatmahs
      const createdIndex = this.myCreatedKhatmahs.findIndex(k => k.id === id);
      if (createdIndex !== -1) {
        this.myCreatedKhatmahs[createdIndex] = {
          id: response.data.id,
          name: response.data.name,
          created_at: response.data.created_at,
          is_private: response.data.is_private,
          khatmah_type: response.data.khatmah_type,
          completed_juz_count: response.data.completed_juz_count || 0,
          completed_surah_count: response.data.completed_surah_count || 0
        };
        saveCreatedKhatmahsToStorage(this.myCreatedKhatmahs);
      }
      
      // Update current khatmah if it's the one being edited
      if (this.currentKhatmah && this.currentKhatmah.id === id) {
        this.currentKhatmah = response.data;
      }
      
      return response.data;
    } catch (error) {
      console.error(`Error updating khatmah ${id}:`, error);
      
      // Capture and display more specific error messages from the API
      if (error.response && error.response.data && error.response.data.error) {
        this.error = error.response.data.error;
      } else {
        this.error = 'Failed to update khatmah';
      }
      
      return null;
    } finally {
      this.loading = false;
    }
  },

  async fetchKhatmah(id) {
    this.loading = true;
    this.error = null;
    try {
      // Validate the UUID format
      if (!this.isValidUUID(id)) {
        this.error = 'Invalid khatmah ID format';
        return null;
      }
      
      // Prepare request config with params if we have a creator token
      const requestConfig = {};
      const storedTokens = loadCreatorTokensFromStorage();
      
      // Check both store and localStorage for token
      if (this.creatorTokens[id] || (storedTokens && storedTokens[id])) {
        const token = this.creatorTokens[id] || storedTokens[id];
        
        // Validate the creator token is a UUID
        if (this.isValidUUID(token)) {
          requestConfig.params = { creator_token: token };
          // Ensure token is in store if it was only in localStorage
          this.creatorTokens[id] = token;
        } else {
          // Delete invalid token
          delete this.creatorTokens[id];
          saveCreatorTokensToStorage(this.creatorTokens);
        }
      }
      
      const response = await axios.get(`${API_URL}/khatmahs/${id}/`, requestConfig);
      this.currentKhatmah = response.data;
      
      // If the response includes a creator_token, save it
      if (response.data.creator_token) {
        this.creatorTokens[id] = response.data.creator_token;
        saveCreatorTokensToStorage(this.creatorTokens);
      }
      
      // Update myCreatedKhatmahs with latest counts if this is a created khatmah
      const createdIndex = this.myCreatedKhatmahs.findIndex(k => k.id === id);
      if (createdIndex !== -1) {
        // Update with latest counts
        this.myCreatedKhatmahs[createdIndex] = {
          ...this.myCreatedKhatmahs[createdIndex],
          completed_juz_count: response.data.completed_juz_count || 0,
          completed_surah_count: response.data.completed_surah_count || 0,
          khatmah_type: response.data.khatmah_type || this.myCreatedKhatmahs[createdIndex].khatmah_type
        };
        saveCreatedKhatmahsToStorage(this.myCreatedKhatmahs);
      }
      
      // Check if we have a saved participant for this khatmah
      if (this.myParticipations[id]) {
        // Find the participant in the current khatmah data
        const savedParticipant = this.currentKhatmah.participants.find(
          p => p.id === this.myParticipations[id].id
        );
        
        if (savedParticipant) {
          this.currentParticipant = savedParticipant;
        }
      }
      
      return response.data;
    } catch (error) {
      console.error('Error fetching khatmah:', error);
      this.error = 'Failed to load khatmah details';
      return null;
    } finally {
      this.loading = false;
    }
  },

  async joinKhatmah(khatmahId, name) {
    this.loading = true;
    this.error = null;
    try {
      // Prepare the request data
      const requestData = { name };
      
      // Add creator token if we have one for this khatmah
      if (this.creatorTokens[khatmahId]) {
        requestData.creator_token = this.creatorTokens[khatmahId];
      }
      
      const response = await axios.post(
        `${API_URL}/khatmahs/${khatmahId}/join/`, 
        requestData,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      
      this.currentParticipant = response.data;
      
      // Save to local storage
      this.myParticipations[khatmahId] = {
        id: response.data.id,
        name: response.data.name,
        khatmahId,
        khatmahName: this.currentKhatmah?.name || ''
      };
      saveParticipantsToStorage(this.myParticipations);
      
      // Refresh khatmah data
      await this.fetchKhatmah(khatmahId);
      
      return response.data;
    } catch (error) {
      console.error('Error joining khatmah:', error);
      if (error.response?.data?.error) {
        this.error = error.response.data.error;
      } else {
        this.error = 'Failed to join khatmah';
      }
      return null;
    } finally {
      this.loading = false;
    }
  },

  async assignJuz(khatmahId, juzNumber) {
    this.loading = true;
    this.error = null;
    try {
      // Make sure we have a current participant
      if (!this.currentParticipant) {
        this.error = 'You must join the khatmah first';
        return null;
      }
      
      // Validate juzNumber is within valid range (1-30)
      const sanitizedJuzNumber = Number.isInteger(Number(juzNumber)) && 
                                 juzNumber >= 1 && juzNumber <= 30 ? 
                                 juzNumber : null;
      
      if (sanitizedJuzNumber === null) {
        this.error = 'Invalid Juz number. Must be between 1 and 30.';
        return null;
      }
      
      const response = await axios.post(`${API_URL}/assignments/`, {
        khatmah: khatmahId,
        participant: this.currentParticipant.id,
        juz_number: sanitizedJuzNumber
      });
      
      // Refresh khatmah data
      await this.fetchKhatmah(khatmahId);
      
      return response.data;
    } catch (error) {
      console.error('Error assigning juz:', error);
      this.error = 'Failed to assign juz';
      return null;
    } finally {
      this.loading = false;
    }
  },

  async assignSurah(khatmahId, surahNumber) {
    this.loading = true;
    this.error = null;
    try {
      // Make sure we have a current participant
      if (!this.currentParticipant) {
        this.error = 'You must join the khatmah first';
        return null;
      }
      
      // Validate surahNumber is within valid range (1-114)
      const sanitizedSurahNumber = Number.isInteger(Number(surahNumber)) && 
                                   surahNumber >= 1 && surahNumber <= 114 ? 
                                   surahNumber : null;
      
      if (sanitizedSurahNumber === null) {
        this.error = 'Invalid Surah number. Must be between 1 and 114.';
        return null;
      }
      
      const response = await axios.post(`${API_URL}/surah-assignments/`, {
        khatmah: khatmahId,
        participant: this.currentParticipant.id,
        surah_number: sanitizedSurahNumber
      });
      
      // Refresh khatmah data
      await this.fetchKhatmah(khatmahId);
      
      return response.data;
    } catch (error) {
      console.error('Error assigning surah:', error);
      this.error = 'Failed to assign surah';
      return null;
    } finally {
      this.loading = false;
    }
  },

  async toggleJuzComplete(assignmentId, khatmahId) {
    this.loading = true;
    this.error = null;
    try {
      // Validate UUIDs
      if (!this.isValidUUID(assignmentId) || !this.isValidUUID(khatmahId)) {
        this.error = 'Invalid assignment or khatmah ID';
        return null;
      }
      
      const response = await axios.post(`${API_URL}/assignments/${assignmentId}/toggle_complete/`);
      
      // Refresh khatmah data
      await this.fetchKhatmah(khatmahId);
      
      return response.data;
    } catch (error) {
      console.error('Error toggling juz completion:', error);
      this.error = 'Failed to update juz status';
      return null;
    } finally {
      this.loading = false;
    }
  },

  async toggleSurahComplete(assignmentId, khatmahId) {
    this.loading = true;
    this.error = null;
    try {
      // Validate UUIDs
      if (!this.isValidUUID(assignmentId) || !this.isValidUUID(khatmahId)) {
        this.error = 'Invalid assignment or khatmah ID';
        return null;
      }
      
      const response = await axios.post(`${API_URL}/surah-assignments/${assignmentId}/toggle_complete/`);
      
      // Refresh khatmah data
      await this.fetchKhatmah(khatmahId);
      
      return response.data;
    } catch (error) {
      console.error('Error toggling surah completion:', error);
      this.error = 'Failed to update surah completion status';
      return null;
    } finally {
      this.loading = false;
    }
  },
  
  // Remove a participation from local storage
  removeParticipation(khatmahId) {
    if (this.myParticipations[khatmahId]) {
      delete this.myParticipations[khatmahId];
      saveParticipantsToStorage(this.myParticipations);
      
      // If we're currently viewing this khatmah, reset the current participant
      if (this.currentKhatmah && this.currentKhatmah.id === khatmahId) {
        this.currentParticipant = null;
      }
    }
  },
  
  // Get all my participations
  getMyParticipations() {
    return Object.values(this.myParticipations);
  },
  
  // Check if user is the creator of a khatmah
  isKhatmahCreator(khatmahId) {
    // Most secure: check if we have a creator token for this khatmah
    if (this.creatorTokens[khatmahId]) {
      return true;
    }
    
    // Next, check the server data (if we have a current khatmah loaded with creator info)
    if (this.currentKhatmah && this.currentKhatmah.id === khatmahId && 
        this.currentKhatmah.creator_id && this.currentParticipant) {
      return this.currentParticipant.id === this.currentKhatmah.creator_id;
    }
    
    // Do NOT trust local storage for ownership verification
    // as it can be manipulated by attackers
    return false;
  },
  
  // Get all khatmahs created by the user
  getMyCreatedKhatmahs() {
    return this.myCreatedKhatmahs;
  },
  
  // Delete a khatmah
  async deleteKhatmah(khatmahId) {
    this.loading = true;
    this.error = null;
    try {
      // Validate the UUID format
      if (!this.isValidUUID(khatmahId)) {
        this.error = 'Invalid khatmah ID format';
        return false;
      }
      
      // Add authentication parameters
      const params = {};
      
      // Only use secure authentication methods
      if (this.creatorTokens[khatmahId]) {
        // Validate the creator token is a UUID
        if (this.isValidUUID(this.creatorTokens[khatmahId])) {
          // Prefer creator token authentication (most secure)
          params.creator_token = this.creatorTokens[khatmahId];
        } else {
          console.error('Invalid creator token format stored for khatmah:', khatmahId);
          // Delete the invalid token
          delete this.creatorTokens[khatmahId];
          saveCreatorTokensToStorage(this.creatorTokens);
          this.error = 'Invalid authentication token format';
          return false;
        }
      } 
      // Only use server-verified participant ID as fallback
      else if (this.currentParticipant && this.currentKhatmah && 
               this.currentKhatmah.creator_id === this.currentParticipant.id) {
        if (this.isValidUUID(this.currentParticipant.id)) {
          params.participant_id = this.currentParticipant.id;
        } else {
          this.error = 'Invalid participant ID format';
          return false;
        }
      } else {
        this.error = 'You do not have permission to delete this khatmah';
        return false;
      }
      
      await axios.delete(`${API_URL}/khatmahs/${khatmahId}/`, { params });
      
      // Remove from lists
      this.khatmahs = this.khatmahs.filter(k => k.id !== khatmahId);
      this.myCreatedKhatmahs = this.myCreatedKhatmahs.filter(k => k.id !== khatmahId);
      saveCreatedKhatmahsToStorage(this.myCreatedKhatmahs);
      
      // Remove creator token
      if (this.creatorTokens[khatmahId]) {
        delete this.creatorTokens[khatmahId];
        saveCreatorTokensToStorage(this.creatorTokens);
      }
      
      // Remove from participations if exists
      if (this.myParticipations[khatmahId]) {
        delete this.myParticipations[khatmahId];
        saveParticipantsToStorage(this.myParticipations);
      }
      
      return true;
    } catch (error) {
      console.error(`Error deleting khatmah ${khatmahId}:`, error);
      
      // Capture and display specific error messages from the API
      if (error.response && error.response.data && error.response.data.error) {
        this.error = error.response.data.error;
      } else {
        this.error = 'Failed to delete khatmah';
      }
      
      return false;
    } finally {
      this.loading = false;
    }
  },

  // Helper method to validate UUIDs
  isValidUUID(uuid) {
    // Regular expression for validating UUID
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    return typeof uuid === 'string' && uuidRegex.test(uuid);
  },

  async removeParticipant(khatmahId, participantId) {
    this.loading = true;
    this.error = null;
    try {
      // Validate UUIDs
      if (!this.isValidUUID(khatmahId) || !this.isValidUUID(participantId)) {
        this.error = 'Invalid khatmah or participant ID format';
        return null;
      }

      // Prepare request data with authentication
      const requestData = {
        participant_id: participantId
      };

      // Add authentication - prefer creator token if available
      if (this.creatorTokens[khatmahId]) {
        requestData.creator_token = this.creatorTokens[khatmahId];
      } else if (this.currentParticipant) {
        requestData.requester_participant_id = this.currentParticipant.id;
      } else {
        this.error = 'You are not authorized to remove participants';
        return null;
      }

      const response = await axios.post(
        `${API_URL}/khatmahs/${khatmahId}/remove_participant/`,
        requestData
      );

      // If the removed participant was in local storage, remove them
      if (this.myParticipations[khatmahId] && 
          this.myParticipations[khatmahId].id === participantId) {
        delete this.myParticipations[khatmahId];
        saveParticipantsToStorage(this.myParticipations);
      }

      // Update current khatmah data
      this.currentKhatmah = response.data;

      return response.data;
    } catch (error) {
      console.error('Error removing participant:', error);
      if (error.response?.data?.error) {
        this.error = error.response.data.error;
      } else {
        this.error = 'Failed to remove participant';
      }
      return null;
    } finally {
      this.loading = false;
    }
  }
}); 