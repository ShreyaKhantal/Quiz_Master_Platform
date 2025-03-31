<template>
  <div class="app">
    <header class="app-header">
      <nav class="navbar">
        <div class="navbar-brand">
          <router-link to="/" class="logo">
            <i class="bi bi-puzzle"></i>
            <span>Quiz Master</span>
          </router-link>
        </div>
        
        <div class="navbar-menu">
          <!-- <div class="navbar-start">
            <router-link v-if="!isLoggedIn" to="/" class="nav-link">Home</router-link>
            <router-link v-if="!isLoggedIn" to="/leaderboard" class="nav-link">Leaderboard</router-link>
            <router-link v-if="!isLoggedIn" to="/about" class="nav-link">About</router-link>
          </div> -->
          
          <div class="navbar-end">
            <router-link v-if="!isLoggedIn" to="/login" class="nav-link">Log In</router-link>
            <router-link v-if="!isLoggedIn" to="/register" class="nav-link sign-up">Sign Up</router-link>
            <div v-else class="user-dropdown">
              <button class="dropdown-trigger" @click="toggleDropdown">
                <div class="user-avatar">
                  <span>{{ userInitials }}</span>
                </div>
                <span class="username">{{ username }}</span>
                <i class="bi bi-chevron-down"></i>
              </button>
              
              <div class="dropdown-menu" v-show="dropdownOpen">
                <div class="dropdown-divider"></div>
                <button @click="handleLogout" class="dropdown-item logout">
                  <i class="bi bi-box-arrow-right"></i> Log Out
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <button class="mobile-menu-toggle" @click="toggleMobileMenu">
          <i class="bi" :class="mobileMenuOpen ? 'bi-x-lg' : 'bi-list'"></i>
        </button>
        
        <div class="mobile-menu" v-show="mobileMenuOpen">
          <router-link to="/" class="mobile-nav-link" @click="closeMobileMenu">Home</router-link>
          <router-link to="/quizzes" class="mobile-nav-link" @click="closeMobileMenu">Quizzes</router-link>
          <router-link to="/leaderboard" class="mobile-nav-link" @click="closeMobileMenu">Leaderboard</router-link>
          <router-link to="/about" class="mobile-nav-link" @click="closeMobileMenu">About</router-link>
          <div class="mobile-divider"></div>
          <div v-if="!isLoggedIn">
            <router-link to="/login" class="mobile-nav-link" @click="closeMobileMenu">Log In</router-link>
            <router-link to="/register" class="mobile-nav-link" @click="closeMobileMenu">Sign Up</router-link>
          </div>
          <div v-else>
            <router-link to="/dashboard" class="mobile-nav-link" @click="closeMobileMenu">Dashboard</router-link>
            <router-link to="/profile" class="mobile-nav-link" @click="closeMobileMenu">Profile</router-link>
            <router-link to="/settings" class="mobile-nav-link" @click="closeMobileMenu">Settings</router-link>
            <button @click="handleLogout" class="mobile-nav-link logout">Log Out</button>
          </div>
        </div>
      </nav>
    </header>
    
    <main class="app-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <footer class="app-footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3 class="footer-title">Quiz Master</h3>
          <p class="footer-description">
            Expand your knowledge with interactive quizzes across various subjects.
          </p>
          <div class="social-links">
            <a href="#" class="social-link"><i class="bi bi-facebook"></i></a>
            <a href="#" class="social-link"><i class="bi bi-twitter"></i></a>
            <a href="#" class="social-link"><i class="bi bi-instagram"></i></a>
            <a href="#" class="social-link"><i class="bi bi-linkedin"></i></a>
          </div>
        </div>
        
        <div class="footer-section">
          <h3 class="footer-title">Links</h3>
          <ul class="footer-links">
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/quizzes">Quizzes</router-link></li>
            <li><router-link to="/leaderboard">Leaderboard</router-link></li>
            <li><router-link to="/about">About Us</router-link></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h3 class="footer-title">Contact</h3>
          <ul class="footer-contact">
            <li><i class="bi bi-envelope"></i> khantalshreya@gmail.com </li>
            <li><i class="bi bi-telephone"></i> +91 9876543210</li>
            <li><i class="bi bi-geo-alt"></i> IIT MADRAS</li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h3 class="footer-title">Subscribe</h3>
          <p>Get notified about new quizzes and updates</p>
          <div class="subscribe-form">
            <input type="email" placeholder="Your email address" />
            <button><i class="bi bi-arrow-right"></i></button>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; 2025 Quiz Master. All rights reserved.</p>
        <div class="footer-bottom-links">
          <a href="#">Privacy Policy</a>
          <a href="#">Terms of Service</a>
          <a href="#">Cookie Policy</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const isLoggedIn = ref(false);
const username = ref('');
const role = ref('');
const dropdownOpen = ref(false);
const mobileMenuOpen = ref(false);

// Compute user initials for avatar
const userInitials = computed(() => {
  if (!username.value) return '';
  return username.value
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2);
});

// Function to fetch user info from backend
const fetchUserInfo = async () => {
  const token = localStorage.getItem('accessToken');
  if (!token) return;

  try {
    const response = await axios.get('http://127.0.0.1:5000/user-info', {
      headers: { Authorization: `Bearer ${token}` },
    });

    username.value = response.data.username; // Update username
    role.value = response.data.role; // Update roll
    isLoggedIn.value = true; // Mark user as logged in
  } catch (error) {
    console.error('Error fetching user info:', error);
    isLoggedIn.value = false; // Handle invalid session
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }
};

// Function to update login state
const updateAuthStatus = () => {
  const token = localStorage.getItem('accessToken');
  isLoggedIn.value = !!token;

  if (isLoggedIn.value) {
    fetchUserInfo(); // Fetch username from API
  } else {
    username.value = '';
  }
};

// Handle outside clicks to close the dropdown
const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.user-dropdown');
  if (dropdown && !dropdown.contains(event.target)) {
    dropdownOpen.value = false;
  }
};

// Check if user is logged in when component mounts
onMounted(() => {
  updateAuthStatus(); // Initial check

  // Listen for login/logout changes
  window.addEventListener('storage', updateAuthStatus);

  // Close dropdown when clicking outside
  document.addEventListener('click', handleClickOutside);
});

// Cleanup event listeners when component unmounts
onBeforeUnmount(() => {
  window.removeEventListener('storage', updateAuthStatus);
  document.removeEventListener('click', handleClickOutside);
});

// Toggle user dropdown
const toggleDropdown = (event) => {
  event.stopPropagation();
  dropdownOpen.value = !dropdownOpen.value;
};

// Toggle mobile menu
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
  document.body.style.overflow = mobileMenuOpen.value ? 'hidden' : '';
};

// Close mobile menu
const closeMobileMenu = () => {
  mobileMenuOpen.value = false;
  document.body.style.overflow = '';
};

// Handle logout
const handleLogout = () => {
  // Clear local storage
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');

  // Reset state
  isLoggedIn.value = false;
  username.value = '';
  role.value = '';
  dropdownOpen.value = false;

  // Notify other tabs (optional)
  window.dispatchEvent(new Event('storage'));

  // Redirect to home page
  router.push('/');
};
</script>


<style>
/* CSS Variables */
:root {
  --primary-color: #4f46e5;
  --primary-rgb: 79, 70, 229;
  --primary-dark: #4338ca;
  --accent-color: #f97316;
  --accent-rgb: 249, 115, 22;
  --text-primary: #1f2937;
  --text-secondary: #4b5563;
  --bg-color: #f9fafb;
  --card-bg: #ffffff;
  --border-color: #e5e7eb;
  --success-color: #10b981;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
  --info-color: #3b82f6;
}

/* Global Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-primary);
  line-height: 1.6;
}

a {
  text-decoration: none;
  color: inherit;
}

ul {
  list-style: none;
}

/* App Container */
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Header Styles */
.app-header {
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.logo i {
  margin-right: 0.5rem;
  font-size: 1.75rem;
}

.navbar-menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex: 1;
  margin-left: 2rem;
}

.navbar-start, .navbar-end {
  display: flex;
  align-items: center;
}

.navbar-end {
  margin-left: auto;
}

.nav-link {
  margin: 0 1rem;
  padding: 0.5rem 0;
  color: var(--text-secondary);
  font-weight: 500;
  transition: color 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: var(--primary-color);
}

.nav-link.router-link-active {
  color: var(--primary-color);
}

.nav-link.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--primary-color);
  border-radius: 2px;
}

.nav-link.sign-up {
  background-color: var(--primary-color);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.nav-link.sign-up:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* User Dropdown */
.user-dropdown {
  position: relative;
}

.dropdown-trigger {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.dropdown-trigger:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: 0.5rem;
}

.username {
  margin-right: 0.5rem;
  font-weight: 500;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 200px;
  z-index: 10;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  color: var(--text-secondary);
  transition: background-color 0.3s ease;
}

.dropdown-item i {
  margin-right: 0.75rem;
  font-size: 1.1rem;
}

.dropdown-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.dropdown-item.logout {
  color: var(--danger-color);
}

.dropdown-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 0.5rem 0;
}

/* Mobile Menu */
.mobile-menu-toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  color: var(--text-primary);
}

.mobile-menu {
  display: none;
  position: fixed;
  top: 76px;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: white;
  padding: 1rem;
  z-index: 99;
  overflow-y: auto;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

.mobile-nav-link {
  display: block;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
}

.mobile-nav-link.router-link-active {
  color: var(--primary-color);
}

.mobile-nav-link.logout {
  color: var(--danger-color);
  text-align: left;
  width: 100%;
  background: none;
  border: none;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
}

.mobile-divider {
  height: 1px;
  background-color: var(--border-color);
  margin: 1rem 0;
}

/* Main Content */
.app-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

/* Page Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Footer Styles */
.app-footer {
  background-color: #1f2937;
  color: white;
  padding: 3rem 2rem 1.5rem;
  margin-top: 3rem;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-title {
  font-size: 1.25rem;
  margin-bottom: 1.25rem;
  position: relative;
}

.footer-title::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -8px;
  width: 40px;
  height: 3px;
  background-color: var(--accent-color);
  border-radius: 2px;
}

.footer-description {
  color: #d1d5db;
  margin-bottom: 1.25rem;
  line-height: 1.6;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  transition: all 0.3s ease;
}

.social-link:hover {
  background-color: var(--primary-color);
  transform: translateY(-3px);
}

.footer-links li {
  margin-bottom: 0.75rem;
}

.footer-links a {
  color: #d1d5db;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: white;
  text-decoration: underline;
}

.footer-contact li {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  color: #d1d5db;
}

.footer-contact i {
  margin-right: 0.75rem;
  color: var(--accent-color);
}

.subscribe-form {
  display: flex;
  margin-top: 1rem;
}

.subscribe-form input {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 6px 0 0 6px;
  border: none;
  outline: none;
}

.subscribe-form button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 0 1rem;
  border-radius: 0 6px 6px 0;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.subscribe-form button:hover {
  background-color: var(--primary-dark);
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #9ca3af;
  font-size: 0.875rem;
}

.footer-bottom-links {
  display: flex;
  gap: 1.5rem;
}

.footer-bottom-links a {
  color: #9ca3af;
  transition: color 0.3s ease;
}

.footer-bottom-links a:hover {
  color: white;
}

/* Responsive Styles */
@media (max-width: 992px) {
  .navbar-menu {
    display: none;
  }

  .mobile-menu-toggle {
    display: block;
  }

  .mobile-menu {
    display: block;
  }
}

@media (max-width: 768px) {
  .navbar {
    padding: 1rem;
  }

  .footer-content {
    grid-template-columns: 1fr;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .footer-bottom-links {
    justify-content: center;
  }
}
</style>