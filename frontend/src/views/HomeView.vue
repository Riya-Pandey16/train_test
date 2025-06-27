<template>
  <div class="home-view">
    <section class="hero">
      <h1>Welcome to UniConnect</h1>
      <p>A student social platform to share knowledge, connect with peers, and grow together.</p>
    </section>

    <section class="features">
      <router-link to="/post" class="feature-card">
        <h2>📌 Share Posts</h2>
        <p>Post ideas, videos, notes, and academic resources. See what others are sharing!</p>
      </router-link>

      <router-link to="/msg" class="feature-card">
        <h2>💬 Message Friends</h2>
        <p>Chat directly with students from any year or branch and clear doubts together.</p>
      </router-link>

      <router-link to="/sessions" class="feature-card">
        <h2>📚 Join Sessions</h2>
        <p>Attend or host group sessions and collaborative study events.</p>
      </router-link>

      

      <router-link to="/profile" class="feature-card">
        <h2>🙋 Your Profile</h2>
        <p>Showcase your branch, year, skills, and connect with others academically.</p>
      </router-link>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home-view {
  padding: 30px;
  font-family: 'Segoe UI', sans-serif;
   background: #f0f8ff;
}

.hero {
  text-align: center;
  margin-bottom: 0px;
  background: #f0f8ff;;
}

.hero h1 {
  font-size: 36px;
  color: #0000FF;
 
}

.hero p {
  font-size: 18px;
  color: #D2691E;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  background:#f0f8ff;;
  
}

.feature-card {
  background: #ffffff;
  border: 1px solid #ddd;
  padding: 20px;
  text-decoration: none;
  color: inherit;
  border-radius: 10px;
  transition: 0.3s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
  background: #dfdedb;
  transform: translateY(-2px);
}

.feature-card h2 {
  margin: 0 0 10px;
  font-size: 20px;
}

.feature-card p {
  color: #666;
  font-size: 15px;
  
}
</style>
