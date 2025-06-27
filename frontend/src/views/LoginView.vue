<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <input v-model="email" placeholder="email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    async login() {
      try {
        const response = await fetch('/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });

        const data = await response.json();

        if (!response.ok) {
          this.errorMessage = data.error || 'Login failed';
          return;
        }

        localStorage.setItem('token', data.access_token);
        localStorage.setItem('is_admin', data.is_admin);

        this.$router.push(data.is_admin ? '/admin' : '/home');

      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = 'An error occurred while logging in.';
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
