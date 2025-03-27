<!-- Map Selector Modal -->
<div v-if="showMapSelector" class="map-modal">
  <div class="map-modal-content">
    <div class="modal-header">
      <h2>{{ $t('prayerTimes.selectLocation') }}</h2>
      <button class="close-btn" @click="showMapSelector = false">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" width="20" height="20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
    <div class="modal-body">
      <MapSelector @location-selected="handleLocationSelected" />
    </div>
  </div>
</div>

<style scoped>
.map-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
  overflow-y: auto;
}

.map-modal-content {
  background-color: var(--card-bg);
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  position: relative;
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: var(--card-bg);
  border-radius: 12px 12px 0 0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-color);
}

.modal-body {
  padding: 1.5rem;
  background-color: var(--card-bg);
  border-radius: 0 0 12px 12px;
}

.close-btn {
  background: transparent;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: var(--text-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: var(--bg-secondary);
  color: var(--text-secondary);
}
</style> 