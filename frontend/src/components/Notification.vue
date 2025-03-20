<template>
  <div class="notification-container" v-if="notifications.length > 0">
    <transition-group name="notification-fade">
      <div 
        v-for="notification in notifications" 
        :key="notification.id"
        :class="['notification', `notification-${notification.type}`]"
      >
        <span class="notification-message">{{ notification.message }}</span>
        <button class="notification-close" @click="removeNotification(notification.id)">×</button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';

const notifications = ref([]);
let nextId = 0;
const timeouts = {};

const showNotification = (message, type = 'info', timeout = 5000) => {
  const id = nextId++;
  notifications.value.push({ id, message, type });
  
  if (timeout > 0) {
    timeouts[id] = setTimeout(() => {
      removeNotification(id);
    }, timeout);
  }
  
  return id;
};

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id);
  if (index !== -1) {
    notifications.value.splice(index, 1);
    if (timeouts[id]) {
      clearTimeout(timeouts[id]);
      delete timeouts[id];
    }
  }
};

// Clear all timeouts when component is unmounted
onUnmounted(() => {
  Object.values(timeouts).forEach(timeout => clearTimeout(timeout));
});

// Expose methods
defineExpose({
  info: (message, timeout) => showNotification(message, 'info', timeout),
  success: (message, timeout) => showNotification(message, 'success', timeout),
  warning: (message, timeout) => showNotification(message, 'warning', timeout),
  error: (message, timeout) => showNotification(message, 'error', timeout),
  removeAll: () => {
    notifications.value = [];
    Object.values(timeouts).forEach(timeout => clearTimeout(timeout));
    Object.keys(timeouts).forEach(id => delete timeouts[id]);
  }
});
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 350px;
}

.notification {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  color: white;
  animation: slide-in 0.3s ease-out;
}

.notification-info {
  background-color: #3498db;
}

.notification-success {
  background-color: #07bc0c;
}

.notification-warning {
  background-color: #f1c40f;
  color: #333;
}

.notification-error {
  background-color: #e74c3c;
}

.notification-message {
  flex: 1;
  margin-right: 10px;
}

.notification-close {
  background: transparent;
  border: none;
  color: inherit;
  font-size: 18px;
  cursor: pointer;
  padding: 0 5px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Animations */
.notification-fade-enter-active {
  transition: all 0.3s ease-out;
}

.notification-fade-leave-active {
  transition: all 0.2s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}

.notification-fade-enter-from {
  transform: translateX(20px);
  opacity: 0;
}

.notification-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

@keyframes slide-in {
  from {
    transform: translateX(50px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* RTL support */
:global([dir="rtl"]) .notification-container {
  left: 20px;
  right: auto;
}

:global([dir="rtl"]) .notification-fade-enter-from,
:global([dir="rtl"]) .notification-fade-leave-to {
  transform: translateX(-20px);
}

:global([dir="rtl"]) @keyframes slide-in {
  from {
    transform: translateX(-50px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style> 