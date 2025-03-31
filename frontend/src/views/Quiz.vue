<template>
  <div class="quiz-container">
    <!-- Loading State -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Loading quiz...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-overlay">
      <div class="error-icon">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <p>{{ error }}</p>
    </div>

    <!-- Quiz Content -->
    <div v-else class="quiz-content">
      <!-- Quiz Header with Timer -->
      <div class="quiz-header">
        <h2 class="quiz-title">{{ quiz.title }}</h2>
        <div class="timer" :class="{'timer-urgent': timeRemaining <= 300}">
          <svg xmlns="http://www.w3.org/2000/svg" class="timer-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ formatTime(timeRemaining) }}</span>
        </div>
      </div>

      <!-- Questions Section -->
      <div v-if="currentQuestion" class="question-section">
        <div class="question-progress">
          <div class="progress-bar">
            <div 
              class="progress-indicator" 
              :style="{ width: `${(currentQuestionIndex + 1) / quiz.questions.length * 100}%` }"
            ></div>
          </div>
          <span class="progress-text">
            Question {{ currentQuestionIndex + 1 }} of {{ quiz.questions.length }}
          </span>
        </div>

        <div class="question-statement">
          {{ currentQuestion.question_statement }}
        </div>
        
        <div class="options-grid">
          <button 
            v-for="(option, index) in currentQuestion.options" 
            :key="index"
            @click="selectOption(index)"
            :class="{
              'option-btn': true, 
              'selected': selectedAnswer === index
            }"
          >
            <span class="option-letter">{{ String.fromCharCode(65 + index) }}.</span>
            {{ option }}
          </button>
        </div>

        <!-- Navigation Buttons -->
        <div class="navigation-buttons">
          <button 
            @click="previousQuestion" 
            :disabled="currentQuestionIndex === 0"
            class="nav-btn prev-btn"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Previous
          </button>
          <button 
            @click="nextQuestion" 
            :disabled="selectedAnswer === null"
            class="nav-btn next-btn"
          >
            Next
            <svg xmlns="http://www.w3.org/2000/svg" class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Quiz Summary / Submit Section -->
      <div v-if="quizCompleted" class="quiz-summary">
        <div class="summary-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
          </svg>
        </div>
        <h3>Quiz Completed!</h3>
        <p>Total Questions: {{ quiz.questions.length }}</p>
        <button @click="submitQuiz" class="submit-btn">Submit Quiz</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

// API token
const getToken = () => localStorage.getItem('accessToken');

// Headers with authorization
const authHeaders = computed(() => ({
  headers: { Authorization: `Bearer ${getToken()}` }
}));

const route = useRoute();
const router = useRouter();

const quiz = ref(null);
const loading = ref(true);
const error = ref(null);
const currentQuestionIndex = ref(0);
const selectedAnswer = ref(null);
const timeRemaining = ref(0);
const quizCompleted = ref(false);
const userAnswers = ref([]);
const quizScore = ref(null);
let timer = null;

const currentQuestion = computed(() => quiz.value?.questions[currentQuestionIndex.value] || null);

const fetchQuiz = async () => {
  try {
    const quizId = route.params.id;
    const response = await axios.get(`/user/quizzes/${quizId}`, authHeaders.value);
    quiz.value = response.data;
    initializeQuiz();
  } catch (err) {
    error.value = 'Failed to load quiz. Please try again.';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const initializeQuiz = () => {
  const [hours, minutes] = quiz.value.time_duration.split(':').map(Number);
  timeRemaining.value = (hours * 3600) + (minutes * 60);
  userAnswers.value = new Array(quiz.value.questions.length).fill(null);
  startTimer();
};

const startTimer = () => {
  timer = setInterval(() => {
    timeRemaining.value--;
    if (timeRemaining.value <= 0) {
      submitQuiz();
    }
  }, 1000);
};

const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
};

const selectOption = (index) => {
  selectedAnswer.value = index;
  userAnswers.value[currentQuestionIndex.value] = index;
};

const nextQuestion = () => {
  if (currentQuestionIndex.value < quiz.value.questions.length - 1) {
    currentQuestionIndex.value++;
    selectedAnswer.value = userAnswers.value[currentQuestionIndex.value];
  } else {
    quizCompleted.value = true;
  }
};

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--;
    selectedAnswer.value = userAnswers.value[currentQuestionIndex.value];
  }
};

const submitQuiz = async () => {
  clearInterval(timer);
  try {
    const response = await axios.post(
      `/user/quizzes/${quiz.value.id}/submit`,
      { answers: userAnswers.value },
      authHeaders.value
    );

    // Store the score in a reactive variable
    quizScore.value = response.data.score;

    // Optionally mark quiz as completed
    quizCompleted.value = true;
    router.push('/user_dashboard');
  } catch (err) {
    console.error('Quiz submission failed', err);
    error.value = 'Failed to submit quiz. Please try again.';
  }
};

onMounted(fetchQuiz);
onBeforeUnmount(() => {
  if (timer) {
    clearInterval(timer);
  }
});
</script>


<style scoped>
:root {
  --primary-color: #3498db;
  --secondary-color: #2ecc71;
  --background-color: #f4f6f7;
  --text-color: #2c3e50;
  --border-color: #e0e4e6;
}

.quiz-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid var(--border-color);
}

.quiz-title {
  font-size: 1.8rem;
  color: var(--text-color);
  font-weight: 700;
}

.timer {
  display: flex;
  align-items: center;
  font-weight: bold;
  color: var(--primary-color);
  background-color: #f0f4f8;
  padding: 10px 15px;
  border-radius: 8px;
}

.timer-urgent {
  color: #e74c3c;
  animation: pulse 1s infinite alternate;
}

.timer-icon {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

.question-section {
  background-color: var(--background-color);
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.question-progress {
  margin-bottom: 20px;
}

.progress-bar {
  height: 8px;
  background-color: #e0e4e6;
  border-radius: 4px;
  overflow: hidden;
}

.progress-indicator {
  height: 100%;
  background-color: var(--primary-color);
  transition: width 0.3s ease;
}

.progress-text {
  display: block;
  text-align: right;
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-top: 5px;
}

.question-statement {
  font-size: 1.2rem;
  color: var(--text-color);
  margin-bottom: 20px;
  line-height: 1.6;
}

.options-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.option-btn {
  display: flex;
  align-items: center;
  padding: 15px;
  border: 2px solid var(--border-color);
  background-color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.option-btn:hover {
  border-color: var(--primary-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.option-btn.selected {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.option-letter {
  margin-right: 10px;
  font-weight: bold;
  opacity: 0.7;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 25px;
}

.nav-btn {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  border: none;
  border-radius: 8px;
  background-color: var(--primary-color);
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.nav-btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.prev-btn {
  background-color: #ecf0f1;
  color: var(--text-color);
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.prev-btn svg {
  margin-right: 10px;
}

.next-btn svg {
  margin-left: 10px;
}

.quiz-summary {
  text-align: center;
  padding: 30px;
  background-color: var(--background-color);
  border-radius: 12px;
}

.summary-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 20px;
  color: var(--secondary-color);
}

.submit-btn {
  margin-top: 20px;
  padding: 12px 25px;
  background-color: var(--secondary-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #27ae60;
}

.loading-overlay, .error-overlay {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 300px;
  text-align: center;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.error-icon {
  width: 100px;
  height: 100px;
  color: #e74c3c;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  100% { transform: scale(1.05); }
}

@media (max-width: 600px) {
  .options-grid {
    grid-template-columns: 1fr;
  }

  .quiz-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .timer {
    margin-top: 10px;
    align-self: flex-start;
  }
}
</style>