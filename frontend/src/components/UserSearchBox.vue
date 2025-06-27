<template>
  <div class="user-search">
    <input v-model="query" @input="searchUsers" placeholder="Search users by name or email..." />
    <ul v-if="results.length">
      <li v-for="user in results" :key="user.id" @click="$emit('select-user', user)">
        {{ user.name }} ({{ user.email }})
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UserSearchBox',
  data() {
    return {
      query: '',
      results: []
    }
  },
  methods: {
    async searchUsers() {
      if (this.query.length < 2) return
      const res = await axios.get(`/api/search_users?q=${this.query}`)
      this.results = res.data
    }
  }
}
</script>

<style scoped>
.user-search input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}
ul {
  background: white;
  list-style: none;
  padding: 0;
}
li {
  padding: 6px;
  cursor: pointer;
}
li:hover {
  background: #eee;
}
</style>
