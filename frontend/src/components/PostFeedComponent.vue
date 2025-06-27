<template>
  <div>
    <form @submit.prevent="submitPost">
      <textarea v-model="content" placeholder="Share your thoughts..."></textarea>
      <button>Post</button>
    </form>
    <div v-for="post in posts" :key="post.id">
      <p><strong>{{ post.author }}</strong>:</p>
      <p>{{ post.content }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { content: '', posts: [] }
  },
  methods: {
    async fetchPosts() {
      const res = await axios.get('http://localhost:5000/posts', {
        headers: { Authorization: `Bearer ${localStorage.token}` }
      })
      this.posts = res.data
    },
    async submitPost() {
      await axios.post('http://localhost:5000/posts', { content: this.content }, {
        headers: { Authorization: `Bearer ${localStorage.token}` }
      })
      this.content = ''
      this.fetchPosts()
    }
  },
  mounted() {
    this.fetchPosts()
  }
}
</script>
