<template>
  <div class="user-profile">
    <h3>{{ user.name }}</h3>
    <p><strong>Branch:</strong> {{ user.branch }}</p>
    <p><strong>Year:</strong> {{ user.year }}</p>
    <p><strong>Skills:</strong> {{ user.skills }}</p>
    <button @click="messageUser">Message</button>
    <button @click="addToGroup">Add to Group</button>
  </div>
</template>

<script>
export default {
  props: ['user'],
  methods: {
    messageUser() {
      this.$router.push({ name: 'Messages', query: { to: this.user.id } })
    },
    addToGroup() {
      alert(`Added ${this.user.name} to your group (mock action)`)
    }
  }
}
</script>

<style scoped>
.user-profile {
  border: 1px solid #ccc;
  padding: 12px;
  border-radius: 6px;
  background-color: #f9f9f9;
}
</style>
