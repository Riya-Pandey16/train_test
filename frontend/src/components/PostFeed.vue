<template>
  <div class="post-feed">
    <h2>Recent Posts</h2>
    <div v-for="post in posts" :key="post.id" class="post-card">
      <h3>{{ post.title }}</h3>
      <p>{{ post.content }}</p>
      <small>By {{ post.author }} • {{ post.date }}</small>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PostFeed',
  data() {
    return {
      posts: [
        {
          id: 1,
          title: 'Welcome to the platform!',
          content: 'This is a sample post from the system.',
          author: 'Admin',
          date: '2025-05-10'
        },
        {
          id: 2,
          title: 'Study group for nanoelectronics?',
          content: 'Anyone up for a session this weekend?',
          author: 'Balkrishna',
          date: '2025-05-09'
        }
      ]
    }
  }
}
</script>

<style scoped>
.post-feed {
  padding: 1rem;
}
.post-card {
  border: 1px solid #ddd;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  background-color: #fff;
}
</style>
