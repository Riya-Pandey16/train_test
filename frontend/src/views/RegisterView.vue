<template>
  <div class="register-container">
    <h2>Join UniConnect</h2>
    <form @submit.prevent="register" class="register-form">
      <input v-model="username" placeholder="Username" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />

      <select v-model="branch" required>
        <option value="" disabled>Select Branch</option>
        <option>CSE</option>
        <option>ECE</option>
        <option>ME</option>
        <option>CE</option>
        <option>EE</option>
        <option>IT</option>
        <option>other</option>
      </select>

      <select v-model="year" required>
        <option value="" disabled>Select Your Level</option>
        <option>1st Year</option>
        <option>2nd Year</option>
        <option>3rd Year</option>
        <option>4th Year</option>
        <option>other</option>
        <option>Professor</option>
        <option>Director</option>
        
      </select>

      <label class="checkbox-label">
        <input type="checkbox" v-model="isAdmin" />
        Register as Admin (Admins can manage users and posts)
      </label>

      <button type="submit" class="register-button">Register</button>
      <p v-if="message" class="message">{{ message }}</p>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      branch: '',
      year: '',
      isAdmin: false,
      message: ''
    };
  },
  methods: {
    async register() {
      if (!this.username || !this.email || !this.password || !this.branch || !this.year) {
        this.message = 'Please fill in all fields.';
        return;
      }

      try {
        const response = await fetch('/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
            branch: this.branch,
            year: this.year,
            is_admin: this.isAdmin
          })
        });

        const data = await response.json();

        if (!response.ok) {
          this.message = data.error || 'Registration failed.';
        } else {
          this.message = 'Registration successful! Redirecting to login...';
          setTimeout(() => this.$router.push('/login'), 2000);
        }
      } catch (err) {
        console.error(err);
        this.message = 'Something went wrong. Try again later.';
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  max-width: 450px;
  margin: 60px auto;
  padding: 2rem;
  background: rgb(206, 206, 231);
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

input,
select {
  padding: 10px;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  color: #444;
}

.register-button {
  padding: 12px;
  background-color: #0077cc;
  color: white;
  border: none;
  font-weight: bold;
  border-radius: 8px;
  transition: background 0.3s;
  cursor: pointer;
}

.register-button:hover {
  background-color: #005fa3;
}

.message {
  margin-top: 10px;
  font-size: 0.95rem;
  color: green;
}
</style>
