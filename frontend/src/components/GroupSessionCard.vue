<template>
  <div class="session-card">
    <h4>{{ session.topic || "Doubt Clearing Session" }}</h4>
    <p><strong>Time:</strong> {{ session.time || "TBD" }}</p>
    <button @click="joinSession">Join</button>
  </div>
</template>

<script>
export default {
  props: {
    session: {
      type: Object,
      default: () => ({})
    }
  },
  methods: {
    joinSession() {
      alert('Redirecting to session (mock)...')
    }
  }
}
</script>

<style scoped>
.session-card {
  background: #eef;
  padding: 10px;
  margin: 10px 0;
  border-radius: 6px;
}
</style>
