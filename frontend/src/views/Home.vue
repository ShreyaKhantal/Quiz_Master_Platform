<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Quiz Master</h1>
        <p class="hero-subtitle">Elevate your knowledge with our interactive quizzes</p>
        <div class="hero-buttons">
          <router-link to="/register" class="btn btn-get-started">Get Started</router-link>
          <router-link to="/login" class="btn btn-login">Login</router-link>
        </div>
      </div>
    </div>

    <div class="features-section">
      <h2 class="section-title">Why Choose Quiz Master?</h2>
      
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <i class="bi bi-book"></i>
          </div>
          <h3>Multiple Subjects</h3>
          <p>Explore quizzes across various subjects and topics to expand your knowledge</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <i class="bi bi-graph-up"></i>
          </div>
          <h3>Track Progress</h3>
          <p>Monitor your improvement with detailed performance analytics</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <i class="bi bi-stopwatch"></i>
          </div>
          <h3>Timed Challenges</h3>
          <p>Test yourself under time pressure to improve speed and accuracy</p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <i class="bi bi-trophy"></i>
          </div>
          <h3>Achievements</h3>
          <p>Earn badges and certificates as you master different subjects</p>
        </div>
      </div>
    </div>

    <div class="cta-section">
      <h2>Ready to Test Your Knowledge?</h2>
      <p>Join thousands of students improving their skills through our platform</p>
      <router-link to="/register" class="btn btn-cta">Create Account</router-link>
    </div>
  </div>
</template>

<script setup>
// Home component logic can go here
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.hero-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 500px;
  padding: 40px 0;
}

.hero-content {
  flex: 1;
  padding-right: 40px;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--primary-color);
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 32px;
  color: var(--text-secondary);
  font-weight: 300;
}

.hero-buttons {
  display: flex;
  gap: 16px;
}

.btn {
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-get-started {
  background-color: var(--primary-color);
  color: white;
}

.btn-get-started:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-login {
  background-color: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
}

.btn-login:hover {
  background-color: rgba(var(--primary-rgb), 0.05);
  transform: translateY(-2px);
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-image img {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.features-section {
  padding: 80px 0;
}

.section-title {
  text-align: center;
  margin-bottom: 50px;
  font-size: 2.2rem;
  color: var(--primary-color);
  position: relative;
}

.section-title:after {
  content: '';
  position: absolute;
  width: 80px;
  height: 4px;
  background-color: var(--accent-color);
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 2px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 30px;
}

.feature-card {
  background-color: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background-color: rgba(var(--primary-rgb), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.feature-icon i {
  font-size: 28px;
  color: var(--primary-color);
}

.feature-card h3 {
  font-size: 1.4rem;
  margin-bottom: 15px;
  color: var(--text-primary);
}

.feature-card p {
  color: var(--text-secondary);
  line-height: 1.6;
}

.cta-section {
  background-color: var(--primary-color);
  color: white;
  text-align: center;
  padding: 60px 30px;
  border-radius: 12px;
  margin: 40px 0 80px;
}

.cta-section h2 {
  font-size: 2rem;
  margin-bottom: 16px;
}

.cta-section p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  opacity: 0.9;
}

.btn-cta {
  background-color: white;
  color: var(--primary-color);
  padding: 14px 32px;
  font-size: 1.1rem;
}

.btn-cta:hover {
  background-color: var(--accent-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

@media (max-width: 768px) {
  .hero-section {
    flex-direction: column;
    text-align: center;
  }
  
  .hero-content {
    padding-right: 0;
    margin-bottom: 40px;
  }
  
  .hero-buttons {
    justify-content: center;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>