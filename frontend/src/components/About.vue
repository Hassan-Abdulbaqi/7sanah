<template>
  <div class="about-container">
    <h1 class="page-title">{{ $t('about.title') || 'About 7sanah' }}</h1>
    
    <div class="about-content">
      <div class="about-section dedication">
        <h2 class="section-title">{{ $t('about.dedication.title') || 'إهداء' }}</h2>
        <p class="section-text" :class="{ 'arabic-font': $i18n.locale === 'ar' }">
          {{ $t('about.dedication.text') }}
        </p>
        <p class="recite-fatiha" :class="{ 'arabic-font': $i18n.locale === 'ar' }">{{ $t('about.dedication.reciteFatiha') }}</p>
      </div>
      
      <div class="about-section">
        <h2 class="section-title">{{ $t('about.contact.title') || 'Contact' }}</h2>
        <p class="section-text" :class="{ 'arabic-font': $i18n.locale === 'ar' }">{{ $t('about.contact.description') || 'For suggestions, feedback, or questions, please reach out to us at:' }}</p>
        <p class="contact-email">contact@7sanah.com</p>
        <p class="contact">حسن عبد الباقي خلف</p>
      </div>
      
      <div class="about-section">
        <h2 class="section-title">{{ $t('about.version.title') || 'Version' }}</h2>
        <p class="section-text">7sanah v1.0.0</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
}

.page-title {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 2rem;
  text-align: center;
}

.about-content {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.about-section {
  margin-bottom: 2rem;
}

.about-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 1.5rem;
  color: var(--text-color);
  margin-bottom: 1rem;
  border-bottom: 2px solid var(--primary-light);
  padding-bottom: 0.5rem;
}

.section-text {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.dedication {
  padding: 1.5rem;
  background-color: var(--primary-bg);
  border-radius: 8px;
  margin-bottom: 2.5rem;
}

.arabic-font {
  font-family: var(--arabic-font);
  font-size: 1.2rem;
  line-height: 1.8;
}

.recite-fatiha {
  font-weight: 600;
  margin-top: 1.5rem;
  color: var(--primary-color);
}

.contact-email {
  font-weight: 600;
  color: var(--primary-color);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .about-content {
    padding: 1.5rem;
  }
  
  .page-title {
    font-size: 1.8rem;
  }
  
  .section-title {
    font-size: 1.3rem;
  }
  
  .arabic-font {
    font-size: 1.1rem;
  }
}
</style>