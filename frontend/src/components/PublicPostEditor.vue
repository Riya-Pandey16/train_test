<template>
  <div class="post-editor">
    <textarea v-model="content" placeholder="Share your thoughts, notes, or videos..."></textarea>
    <button @click="submitPost">Post Publicly</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'PublicPostEditor',
  data() {
    return { content: '' }
  },
  methods: {
    async submitPost() {
      if (!this.content.trim()) return
      await axios.post('/api/public_posts', { content: this.content })
      this.content = ''
      this.$emit('post-submitted')
    }
  }
}
</script>

<style scoped>
textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
}
button {
  margin-top: 5px;
}
</style>
