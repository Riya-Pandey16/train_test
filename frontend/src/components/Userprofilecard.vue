<template>
  <div class="profile-card">
    <h2>{{ user.name }}</h2>
    <p>Branch: {{ user.branch }}</p>
    <p>Year: {{ user.year }}</p>
    <p>Skills: {{ user.skills.join(', ') }}</p>
  </div>
</template>

<script>
export default {
  name: 'UserProfileCard',
  props: ['user']
}
</script>

<style scoped>
.profile-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
}
</style>
