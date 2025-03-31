<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h1>Create Account</h1>
        <p>Join our community of learners today</p>
      </div>
      
      <div class="alert alert-danger" v-if="errorMessage">
        <i class="bi bi-exclamation-triangle-fill"></i> {{ errorMessage }}
      </div>
      
      <div class="alert alert-success" v-if="successMessage">
        <i class="bi bi-check-circle-fill"></i> {{ successMessage }}
      </div>
      
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-row">
          <div class="form-group">
            <label for="username">Username</label>
            <div class="input-with-icon">
              <i class="bi bi-person"></i>
              <input 
                type="text" 
                id="username" 
                v-model="username" 
                placeholder="Choose a username" 
                required
                style="text-indent: 35px;"
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="email">Email Address</label>
            <div class="input-with-icon">
              <i class="bi bi-envelope"></i>
              <input 
                type="email" 
                id="email" 
                v-model="email" 
                placeholder="Enter your email" 
                required
              />
            </div>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="password">Password</label>
            <div class="input-with-icon">
              <i class="bi bi-lock"></i>
              <input 
                type="password" 
                id="password" 
                v-model="password" 
                placeholder="Create a password" 
                required
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="full_name">Full Name</label>
            <div class="input-with-icon">
              <i class="bi bi-person-badge"></i>
              <input 
                type="text" 
                id="full_name" 
                v-model="fullName" 
                placeholder="Enter your full name" 
                required
                style="text-indent: 35px;"
              />
            </div>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="qualification">Qualification</label>
            <div class="select-wrapper">
              <select 
                id="qualification" 
                v-model="qualification"
                required
              >
                <option value="" disabled selected>Select qualification</option>
                <option value="High School">High School</option>
                <option value="Bachelors">Bachelor's Degree</option>
                <option value="Masters">Master's Degree</option>
                <option value="PhD">PhD</option>
                <option value="Other">Other</option>
              </select>
              <i class="bi bi-chevron-down"></i>
            </div>
          </div>
          
          <div class="form-group">
            <label for="dob">Date of Birth</label>
            <div class="input-with-icon">
              <i class="bi bi-calendar"></i>
              <input 
                type="date" 
                id="dob" 
                v-model="dob"
                required
                style="text-indent: 15px;"
              />
            </div>
          </div>
        </div>
        
        <div class="terms-checkbox">
          <input type="checkbox" id="terms" v-model="termsAccepted" required />
          <label for="terms">
            I agree to the <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>
          </label>
        </div>
        
        <button 
          type="submit" 
          class="register-button"
          :disabled="isLoading || !termsAccepted"
        >
          <span v-if="isLoading" class="spinner"></span>
          <span v-else>Create Account</span>
        </button>
      </form>
      
      <div class="register-footer">
        <p>Already have an account? <router-link to="/login">Log in</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const fullName = ref('');
const qualification = ref('');
const dob = ref('');
const termsAccepted = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const handleRegister = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';
    successMessage.value = '';
    
    const response = await fetch('http://127.0.0.1:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
        full_name: fullName.value,
        qualification: qualification.value,
        dob: dob.value
      }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.message || 'Registration failed');
    }
    
    successMessage.value = 'Registration successful! Redirecting to login...';
    
    // Clear form inputs
    username.value = '';
    email.value = '';
    password.value = '';
    fullName.value = '';
    qualification.value = '';
    dob.value = '';
    termsAccepted.value = false;
    
    // Redirect to login after successful registration
    setTimeout(() => {
      router.push('/login');
    }, 2000);
    
  } catch (error) {
    errorMessage.value = error.message;
    console.error('Registration error:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}

.register-card {
  width: 100%;
  max-width: 800px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 40px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h1 {
  color: var(--primary-color);
  font-size: 2rem;
  margin-bottom: 10px;
}

.register-header p {
  color: var(--text-secondary);
  font-size: 1rem;
}

.alert {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.alert-danger {
  background-color: #fee2e2;
  color: #b91c1c;
  border-left: 4px solid #ef4444;
}

.alert-success {
  background-color: #dcfce7;
  color: #166534;
  border-left: 4px solid #22c55e;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
}

.form-group {
  flex: 1;
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-primary);
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center; /* Ensures proper vertical alignment */
}
.input-with-icon {
  position: relative;
  display: flex;
  align-items: center; /* Ensures consistent vertical alignment */
}

.input-with-icon i {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  font-size: 1.2rem; /* Ensures uniform icon size */
  pointer-events: none; /* Prevents click interference */
}

.input-with-icon input {
  width: 100%;
  padding: 14px 16px 14px 45px; /* Left padding increased for icon space */
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background-color: white;
  box-sizing: border-box;
  appearance: none;
  height: 45px; /* Ensures uniform height */
}

.input-with-icon input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.2);
  outline: none;
}

/* Apply same styles to all input types */
.input-with-icon input[type="text"],
.input-with-icon input[type="email"],
.input-with-icon input[type="password"] {
  line-height: normal;
}

.select-wrapper {
  position: relative;
}

.select-wrapper select {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  appearance: none;
  background-color: white;
}

.select-wrapper select:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.2);
  outline: none;
}

.select-wrapper i {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
}

.password-toggle {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
}

.terms-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 24px;
}

.terms-checkbox input[type="checkbox"] {
  margin-top: 3px;
}

.terms-checkbox label {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.5;
}

.terms-checkbox a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 500;
}

.terms-checkbox a:hover {
  text-decoration: underline;
}

.register-button {
  width: 100%;
  padding: 16px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.register-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.register-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.register-footer {
  margin-top: 24px;
  text-align: center;
  color: var(--text-secondary);
}

.register-footer a {
  color: var(--primary-color);
  font-weight: 600;
  text-decoration: none;
}

.register-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .register-card {
    padding: 30px 20px;
  }
}
</style>