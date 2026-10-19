<script setup lang="ts">
/**
 * PageShell — 统一页面外壳
 *
 * Props:
 *   logo      字符串或 emoji，默认 ""
 *   title     主标题，默认 ""
 *   subtitle  副标题，默认 ""
 *   accent    强调色，'primary' | 'warning' | 'success' | 'danger' | 'info'，默认 'primary'
 *   width     内容区最大宽度，默认 '1180px'
 *
 * Slots:
 *   #nav     顶部导航（移动端折叠为菜单）
 *   default  主体内容
 *
 * 移动端（<768px）：
 *   - 顶栏折叠为「logo + 汉堡菜单」
 *   - 导航项变为下拉抽屉，点击项关闭
 *   - 内容区满宽，字号自适应
 */
import { computed, ref } from 'vue'

const props = withDefaults(
  defineProps<{
    logo?: string
    title?: string
    subtitle?: string
    accent?: 'primary' | 'warning' | 'success' | 'danger' | 'info'
    width?: string
  }>(),
  {
    logo: '',
    title: '',
    subtitle: '',
    accent: 'primary',
    width: '1180px',
  },
)

const accentClass = computed(() => `accent-${props.accent}`)
const menuOpen = ref(false)
</script>

<template>
  <div class="shell" :class="accentClass">
    <header class="shell-header">
      <div class="shell-header-inner">
        <div class="shell-brand">
          <span v-if="logo" class="shell-logo">{{ logo }}</span>
          <div v-if="title || subtitle" class="shell-titles">
            <h1 v-if="title" class="shell-title">{{ title }}</h1>
            <span v-if="subtitle" class="shell-subtitle">{{ subtitle }}</span>
          </div>
        </div>

        <!-- 桌面端导航 -->
        <nav class="shell-nav hide-mobile">
          <slot name="nav" />
        </nav>

        <!-- 移动端汉堡菜单 -->
        <button
          v-if="$slots.nav"
          class="shell-burger hide-desktop"
          type="button"
          aria-label="菜单"
          :aria-expanded="menuOpen"
          @click="menuOpen = !menuOpen"
        >
          <span class="burger-line" :class="{ open: menuOpen }"></span>
          <span class="burger-line" :class="{ open: menuOpen }"></span>
          <span class="burger-line" :class="{ open: menuOpen }"></span>
        </button>
      </div>

      <!-- 移动端下拉导航 -->
      <nav
        v-if="$slots.nav && menuOpen"
        class="shell-nav-mobile hide-desktop"
        @click="menuOpen = false"
      >
        <slot name="nav" />
      </nav>
    </header>

    <main class="shell-main">
      <div class="shell-content" :style="{ maxWidth: width }">
        <slot />
      </div>
    </main>
  </div>
</template>

<style scoped>
.shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg);
}

.shell-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.shell-header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--gap-m);
  height: var(--header-h);
  padding: 0 24px;
  max-width: 1280px;
  margin: 0 auto;
}

.shell-brand {
  display: flex;
  align-items: center;
  gap: var(--gap-s);
  min-width: 0;
}

.shell-logo {
  font-size: 26px;
  line-height: 1;
  flex-shrink: 0;
}

.shell-titles {
  display: flex;
  align-items: baseline;
  gap: 10px;
  min-width: 0;
}

.shell-title {
  margin: 0;
  font-size: 19px;
  font-weight: 600;
  color: var(--text);
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.shell-subtitle {
  font-size: 13px;
  color: var(--text-3);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.shell-nav {
  display: flex;
  align-items: center;
  gap: var(--gap-m);
}

.shell-nav a {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  color: var(--text-2);
  text-decoration: none;
  transition: all 0.2s;
}

.shell-nav a:hover {
  color: var(--accent);
  background: var(--accent-bg);
}

.shell-nav a.router-link-active,
.shell-nav a.router-link-exact-active {
  color: var(--accent);
  background: var(--accent-bg);
  font-weight: 500;
}

/* 汉堡菜单 */
.shell-burger {
  display: inline-flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  width: 44px;
  height: 44px;
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: var(--radius-sm);
}

.shell-burger:hover {
  background: var(--surface-2);
}

.burger-line {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--text);
  border-radius: 2px;
  transition: all 0.25s ease;
}

.burger-line:nth-child(1).open {
  transform: translateY(6px) rotate(45deg);
}
.burger-line:nth-child(2).open {
  opacity: 0;
}
.burger-line:nth-child(3).open {
  transform: translateY(-6px) rotate(-45deg);
}

/* 移动端下拉导航 */
.shell-nav-mobile {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 16px 12px;
  background: var(--surface);
  border-top: 1px solid var(--border);
}

.shell-nav-mobile a {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  min-height: 44px;
  border-radius: var(--radius-sm);
  font-size: 15px;
  color: var(--text-2);
  text-decoration: none;
}

.shell-nav-mobile a:hover {
  background: var(--accent-bg);
  color: var(--accent);
}

.shell-nav-mobile a.router-link-active,
.shell-nav-mobile a.router-link-exact-active {
  color: var(--accent);
  background: var(--accent-bg);
  font-weight: 500;
}

.shell-main {
  flex: 1;
  padding: var(--gap-l) 16px calc(var(--gap-l) + env(safe-area-inset-bottom));
}

.shell-content {
  margin: 0 auto;
  width: 100%;
}

/* 强调色族 */
.accent-primary {
  --accent: var(--accent-primary);
  --accent-bg: var(--accent-primary-bg);
}
.accent-warning {
  --accent: var(--accent-warning);
  --accent-bg: var(--accent-warning-bg);
}
.accent-success {
  --accent: var(--accent-success);
  --accent-bg: var(--accent-success-bg);
}
.accent-danger {
  --accent: var(--accent-danger);
  --accent-bg: var(--accent-danger-bg);
}
.accent-info {
  --accent: var(--accent-info);
  --accent-bg: var(--accent-info-bg);
}

/* 移动端 */
@media (max-width: 768px) {
  .shell-header-inner {
    padding: 0 14px;
  }

  .shell-title {
    font-size: 17px;
  }

  .shell-subtitle {
    display: none;
  }

  .shell-main {
    padding: var(--gap-m) 12px calc(var(--gap-m) + env(safe-area-inset-bottom));
  }
}

@media (max-width: 480px) {
  .shell-header-inner {
    height: 56px;
  }

  .shell-logo {
    font-size: 22px;
  }

  .shell-title {
    font-size: 16px;
  }
}
</style>
