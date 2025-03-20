import { reactive } from 'vue';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';
const STORAGE_KEY = 'quran_khatmah_participants';
const CREATED_KHATMAHS_KEY = 'quran_khatmah_created';

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

export const store = reactive({
  khatmahs: [],
  currentKhatmah: null,
  currentParticipant: null,
  myParticipations: loadParticipantsFromStorage(),
  myCreatedKhatmahs: loadCreatedKhatmahsFromStorage(),
  loading: false,
  error: null,
  pagination: {
    count: 0,
    next: null,
    previous: null,
    currentPage: 1
  },

  async fetchKhatmahs(page = 1, pageSize = 9) {
    this.loading = true;
    this.error = null;
    try {
      const response = await axios.get(`${API_URL}/khatmahs/`, {
        params: {
          page,
          page_size: pageSize
        }
      });
      
      // Update pagination information
      this.pagination = {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        currentPage: page
      };
      
      // Filter out private khatmahs from the list view
      this.khatmahs = response.data.results.filter(khatmah => !khatmah.is_private);
    } catch (error) {
      console.error('Error fetching khatmahs:', error);
      this.error = 'Failed to load khatmahs';
    } finally {
      this.loading = false;
    }
  },

  async createKhatmah(khatmahData) {
    this.loading = true;
    this.error = null;
    try {
      const response = await axios.post(`${API_URL}/khatmahs/`, khatmahData);
      
      // Only add to the list if it's not private
      if (!response.data.is_private) {
        this.khatmahs.push(response.data);
      }
      
      // Save to created khatmahs
      this.myCreatedKhatmahs.push({
        id: response.data.id,
        name: response.data.name,
        created_at: response.data.created_at,
        is_private: response.data.is_private
      });
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
          is_private: response.data.is_private
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
      this.error = 'Failed to update khatmah';
      return null;
    } finally {
      this.loading = false;
    }
  },

  async fetchKhatmah(id) {
    console.log(`store.fetchKhatmah called with id: ${id}`);
    this.loading = true;
    this.error = null;
    try {
      console.log(`Making API request to ${API_URL}/khatmahs/${id}/`);
      const response = await axios.get(`${API_URL}/khatmahs/${id}/`);
      console.log('API response received:', response.status);
      this.currentKhatmah = response.data;
      
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
      console.error(`Error fetching khatmah ${id}:`, error);
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
      const response = await axios.post(`${API_URL}/khatmahs/${khatmahId}/join/`, { name });
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
      this.error = 'Failed to join khatmah';
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
      
      const response = await axios.post(`${API_URL}/assignments/`, {
        khatmah: khatmahId,
        participant: this.currentParticipant.id,
        juz_number: juzNumber
      });
      
      // Refresh khatmah data
      await this.fetchKhatmah(khatmahId);
      
      return response.data;
    } catch (error) {
      console.error('Error assigning juz:', error);
      this.error = error.response?.data?.error || 'Failed to assign juz';
      return null;
    } finally {
      this.loading = false;
    }
  },

  async toggleJuzComplete(assignmentId, khatmahId) {
    this.loading = true;
    this.error = null;
    try {
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
    return this.myCreatedKhatmahs.some(k => k.id === khatmahId);
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
      await axios.delete(`${API_URL}/khatmahs/${khatmahId}/`);
      
      // Remove from lists
      this.khatmahs = this.khatmahs.filter(k => k.id !== khatmahId);
      this.myCreatedKhatmahs = this.myCreatedKhatmahs.filter(k => k.id !== khatmahId);
      saveCreatedKhatmahsToStorage(this.myCreatedKhatmahs);
      
      // Remove from participations if exists
      if (this.myParticipations[khatmahId]) {
        delete this.myParticipations[khatmahId];
        saveParticipantsToStorage(this.myParticipations);
      }
      
      return true;
    } catch (error) {
      console.error(`Error deleting khatmah ${khatmahId}:`, error);
      this.error = 'Failed to delete khatmah';
      return false;
    } finally {
      this.loading = false;
    }
  }
}); 