<template>
  <div id="app">
    <!-- HEADER / NAVBAR -->
    <header class="navbar">
      <div class="nav-left">
        <router-link to="/home">Home</router-link>
        <router-link to="/sessions">Sessions</router-link>
        <router-link to="/msg">Msg</router-link>
        <router-link to="/post">Post</router-link>
         
          
      </div>

      <div class="nav-right">
        <!-- Show if NOT logged in -->
        <router-link v-if="!isLoggedIn" to="/register">Register</router-link>
        <router-link v-if="!isLoggedIn" to="/login">Login</router-link>

        <!-- Show if logged in -->
        <router-link v-if="isLoggedIn" to="/profile">Profile</router-link>
        <button v-if="isLoggedIn" @click="logout">Logout</button>
      </div>
    </header>

    <!-- PAGE CONTENT -->
    <main class="main-content">
      <router-view />
    </main>

    <!-- FOOTER -->
    <footer class="footer">
      <p>&copy; 2025 UniConnect | Built for students, from the students.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: !!localStorage.getItem('token')
    }
  },
  watch: {
    $route() {
      this.isLoggedIn = !!localStorage.getItem('token');
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.isLoggedIn = false;
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar {
  display: flex;
  justify-content: space-between;
  padding: 15px 20px;
  background-color:rgb(70, 62, 73);
  border-bottom: 1px solid #ccc;
}

.nav-left a,
.nav-right a {
  margin-right: 15px;
  text-decoration: none;
  color: #ffffff;;
  font-weight: bold;
}

.nav-right button {
  background-color: transparent;
  border: none;
  color:rgb(227, 230, 234);
  cursor: pointer;
  font-size: 18px;
}

.main-content {
  flex: 1;
  padding: 20px;
}

.footer {
  background-color:rgb(70, 62, 73);
  border-top: 1px solid #ccc;
  padding: 15px 20px;
  text-align: center;
  font-size: 15px;
  color:#ffffff;
  font-weight: bold;
}
</style>
