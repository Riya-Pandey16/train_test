<template>
  <div class="landing-container">
    <div class="landing-content">
      <h1>Welcome to <span class="highlight">UniConnect</span></h1>
      <p class="subtitle">Where every university student finds their community</p>
      <router-link to="/home">
        <button class="cta-button">Get Started</button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.landing-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #A9A9A9,#778899);
  color: #fff;
  text-align: center;
  padding: 20px;
}

.landing-content {
  max-width: 800px;
  animation: fadeIn 1.2s ease-out;
}

h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  font-weight: 700;
  line-height: 1.2;
}

.highlight {
  color: #3238d1;
}

.subtitle {
  font-size: 1.3rem;
  margin-bottom: 40px;
  font-weight: 400;
  opacity: 0.9;
}

.cta-button {
  background-color: #ffe066;
  color: #003049;
  padding: 14px 32px;
  border: none;
  border-radius: 30px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-weight: 600;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.cta-button:hover {
  background-color: #ffdd00;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
