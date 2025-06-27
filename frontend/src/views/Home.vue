<template>
  <div class="home-layout">
    <Sidebar />
    <div class="center"><PostFeed /></div>
    <div class="right">
      <h3>Group Sessions</h3>
      <GroupSessionCard v-for="n in 2" :key="n" />
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar.vue'
import PostFeed from '@/components/PostFeed.vue'
import GroupSessionCard from '@/components/GroupSessionCard.vue'
export default { components: { Sidebar, PostFeed, GroupSessionCard } }
</script>

<style scoped>
.home-layout {
  display: flex;
  gap: 20px;
}
.center {
  flex: 2;
}
.right {
  flex: 1;
  background: #f4f4f4;
  padding: 10px;
}
</style>
