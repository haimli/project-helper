<script setup lang="ts">
defineProps<{
  tree: string
}>()
</script>

<template>
  <div class="directory-tree">
    <pre class="tree-content">{{ tree }}</pre>
  </div>
</template>

<style scoped lang="scss">
.directory-tree {
  background: var(--bg-code);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 16px;
  overflow-x: auto;
  max-height: 400px;
  overflow-y: auto;
}

.tree-content {
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin: 0;
  white-space: pre;
}
</style>
