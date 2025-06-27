<template>
  <nav class="navbar">
    <div class="left">
      <router-link to="/home">Home</router-link>
      <router-link to="/sessions">Sessions</router-link>
      <router-link to="/messages">Messages</router-link>
      <router-link to="/groups">Groups</router-link>
      <router-link to="/posts">Posts</router-link>
       <router-link v-if="isAdmin" to="/admin">Admin</router-link> <!-- 👈 Admin link -->
    </div>
    <div class="right">
      <router-link v-if="!isLoggedIn" to="/register">Register</router-link>
      <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
      <router-link v-if="isLoggedIn" to="/profile">Profile</router-link>
      <button v-if="isLoggedIn" @click="logout">Logout</button>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      isLoggedIn: false,
      isAdmin: false
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.isLoggedIn = false
      this.$router.push('/login')
    }
  },
  mounted() {
    this.isLoggedIn = !!localStorage.getItem('token')
  },
  watch: {
    // Optional: reactively update when route changes (like after login/register)
    '$route'() {
      this.isLoggedIn = !!localStorage.getItem('token')
    }
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  padding: 12px 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
}
.left, .right {
  display: flex;
  gap: 15px;
  align-items: center;
}
button {
  background: none;
  border: none;
  cursor: pointer;
  color: #007bff;
}
button:hover {
  text-decoration: underline;
}
</style>
