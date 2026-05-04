<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <router-link to="/" class="logo">
        <span class="logo-icon">⬡</span>
        <span class="logo-text">Project Helper</span>
      </router-link>
      <nav class="nav-links">
        <router-link to="/">首页</router-link>
      </nav>
    </header>
    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped lang="scss">
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 60px;
  background: var(--bg-header);
  border-bottom: 1px solid var(--border-color);
  backdrop-filter: blur(12px);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: var(--text-primary);

  .logo-icon {
    font-size: 24px;
    color: var(--accent-primary);
  }

  .logo-text {
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
}

.nav-links {
  display: flex;
  gap: 20px;

  a {
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 14px;
    transition: color 0.2s;

    &:hover,
    &.router-link-active {
      color: var(--accent-primary);
    }
  }
}

.app-main {
  flex: 1;
  padding: 24px;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}
</style>
