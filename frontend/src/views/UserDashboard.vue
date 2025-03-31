<template>
  <div class="user-dashboard">
    <!-- Dashboard Header -->
    <section class="dashboard-header">
      <div class="dashboard-welcome">
        <h1>Student Dashboard</h1>
        <p>Access your courses, track progress, and take quizzes all in one place</p>
      </div>
      <div class="dashboard-actions">
        <div class="search-bar">
          <i class="bi bi-search"></i>
          <input type="text" placeholder="Search subjects, quizzes, or materials..." v-model="searchQuery"
            @input="handleSearch" />
        </div>
      </div>
    </section>

    <!-- Dashboard Stats -->
    <section class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="bi bi-book"></i>
        </div>
        <div class="stat-details">
          <span class="stat-count">{{ stats ? stats.enrolledSubjects : 0 }}</span>
          <span class="stat-name">Subjects</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="bi bi-check-circle"></i>
        </div>
        <div class="stat-details">
          <span class="stat-count">{{ stats ? stats.completedQuizzes : 0 }}</span>
          <span class="stat-name">Completed Quizzes</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="bi bi-calendar-event"></i>
        </div>
        <div class="stat-details">
          <span class="stat-count">{{ stats ? stats.upcomingQuizzes : 0 }}</span>
          <span class="stat-name">Upcoming Quizzes</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="bi bi-trophy"></i>
        </div>
        <div class="stat-details">
          <span class="stat-count">{{ stats ? stats.averageScore : 0 }}%</span>
          <span class="stat-name">Average Score</span>
        </div>
      </div>
    </section>

    <!-- Main Dashboard Content -->
    <div class="dashboard-content">
      <!-- Sidebar Navigation -->
      <aside class="dashboard-sidebar">
        <div class="user-profile">
          <!-- <div class="profile-avatar">
            <img :src="user.avatarUrl || '/images/default-avatar.png'" alt="Profile" />
          </div> -->
          <div class="profile-details">
            <h3>{{ user.name }}</h3>
            <span>{{ user.email }}</span>
          </div>
        </div>
        <ul class="sidebar-nav">
          <li :class="{ active: activeSection === 'overview' }" @click="setActiveSection('overview')">
            <i class="bi bi-grid"></i>
            <span>Overview</span>
          </li>
          <li :class="{ active: activeSection === 'subjects' }" @click="setActiveSection('subjects')">
            <i class="bi bi-book"></i>
            <span>My Subjects</span>
          </li>
          <li :class="{ active: activeSection === 'quizzes' }" @click="setActiveSection('quizzes')">
            <i class="bi bi-question-circle"></i>
            <span>Quizzes</span>
          </li>
          <li :class="{ active: activeSection === 'progress' }" @click="setActiveSection('progress')">
            <i class="bi bi-graph-up"></i>
            <span>My Progress</span>
          </li>
          <li :class="{ active: activeSection === 'calendar' }" @click="setActiveSection('calendar')">
            <i class="bi bi-calendar3"></i>
            <span>Calendar</span>
          </li>
          <li :class="{ active: activeSection === 'settings' }" @click="setActiveSection('settings')">
            <i class="bi bi-gear"></i>
            <span>Settings</span>
          </li>
        </ul>
      </aside>

      <!-- Main Content Area -->
      <div class="main-content">
        <!-- Overview Section -->
        <div v-if="activeSection === 'overview'" class="overview-view">
          <div class="content-header">
            <h2>Dashboard Overview</h2>
          </div>
          
          <!-- Upcoming Quizzes -->
          <div class="content-section">
            <div class="section-header">
              <h3>Upcoming Quizzes</h3>
              <button class="action-button small" @click="setActiveSection('quizzes')">
                View All <i class="bi bi-arrow-right"></i>
              </button>
            </div>
            <div class="upcoming-quizzes">
              <div v-if="upcomingQuizzes.length === 0" class="empty-state">
                <i class="bi bi-calendar-x"></i>
                <p>No upcoming quizzes scheduled.</p>
              </div>
              <div v-else class="quiz-cards">
                <div v-for="quiz in upcomingQuizzes" :key="quiz.id" class="quiz-card">
                  <div class="quiz-card-header">
                    <h4>{{ quiz.title }}</h4>
                    <span :class="['quiz-status', getStatusClass(quiz)]">
                      {{ getStatusText(quiz) }}
                    </span>
                  </div>
                  <div class="quiz-info">
                    <div class="info-item">
                      <i class="bi bi-book"></i>
                      <span>{{ quiz.subject }}</span>
                    </div>
                    <div class="info-item">
                      <i class="bi bi-calendar-event"></i>
                      <span>{{ formatDate(quiz.date) }}</span>
                    </div>
                    <div class="info-item">
                      <i class="bi bi-clock"></i>
                      <span>{{ quiz.time }}</span>
                    </div>
                    <div class="info-item">
                      <i class="bi bi-hourglass-split"></i>
                      <span>{{ quiz.duration }} mins</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- My Subjects Section -->
        <div v-if="activeSection === 'subjects'" class="subjects-view">
          <div class="content-header">
            <h2>My Subjects</h2>
            
          </div>

          <div class="subjects-container">
            <div v-if="filteredSubjects.length === 0" class="empty-state">
              <i class="bi bi-journal-x"></i>
              <p>No subjects found. Enroll in subjects to get started.</p>
            </div>

            <div v-else class="subject-cards">
              <div v-for="subject in filteredSubjects" :key="subject.id" class="subject-card">
                <div class="subject-card-header">
                  <h3>{{ subject.name }}</h3>
                  <!-- <div class="completion-badge" :class="getCompletionClass(subject)">
                    {{ subject.completion }}% Complete
                  </div> -->
                </div>
                <p class="subject-description">{{ subject.description }}</p>
                <!-- <div class="progress-bar">
                  <div class="progress-fill" :style="`width: ${subject.completion}%`"></div>
                </div> -->
                <!-- <div class="subject-stats">
                  <div class="stat">
                    <i class="bi bi-list-check"></i>
                    <span>{{ subject.chaptersCompleted }}/{{ subject.totalChapters }} Chapters</span>
                  </div>
                  <div class="stat">
                    <i class="bi bi-clock-history"></i>
                    <span>{{ subject.hoursSpent }} Hours</span>
                  </div>
                </div> -->
                <div class="subject-actions">
                  <button class="secondary-button" @click="toggleChapters(subject.id)">
                    <i class="bi" :class="expandedSubject === subject.id ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
                    {{ expandedSubject === subject.id ? 'Hide Chapters' : 'View Chapters' }}
                  </button>
                  <!-- <button class="action-button" @click="continueSubject(subject)">
                    Continue Learning
                  </button> -->
                </div>

                <!-- Chapters List (Expandable) -->
                <div v-if="expandedSubject === subject.id" class="chapters-list">
                  <div v-if="getChaptersBySubject(subject.id).length === 0" class="empty-state small">
                    <p>No chapters available for this subject.</p>
                  </div>
                  <div v-else class="chapter-accordion">
                    <div v-for="chapter in getChaptersBySubject(subject.id)" :key="chapter.id" class="chapter-item">
                      <div class="chapter-header">
                        <div class="chapter-title">
                          <i class="bi" :class="chapter.completed ? 'bi-check-circle-fill' : 'bi-circle'"></i>
                          <h4>{{ chapter.name }}</h4>
                        </div>
                      </div>
                      <p class="chapter-description">{{ chapter.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quizzes Section -->
        <div v-if="activeSection === 'quizzes'" class="quizzes-view">
          <div class="content-header">
            <h2>My Quizzes</h2>
            <div class="filter-actions">
              <div class="select-container">
                <select v-model="quizFilter">
                  <option value="all">All Quizzes</option>
                  <option value="upcoming">Upcoming</option>
                  <option value="completed">Completed</option>
                  <option value="past-due">Past Due</option>
                </select>
              </div>
            </div>
          </div>

          <div class="quizzes-container">
            <div v-if="filteredQuizzes.length === 0" class="empty-state">
              <i class="bi bi-question-diamond"></i>
              <p>No quizzes found based on your current filter.</p>
            </div>

            <div v-else class="quiz-table-container">
              <table class="quiz-table">
                <thead>
                  <tr>
                    <th>Quiz</th>
                    <th>Subject</th>
                    <th>Date & Time</th>
                    <th>Status</th>
                    <th>Score</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
                    <td>{{ quiz.title }}</td>
                    <td>{{ quiz.subject }}</td>
                    <td>{{ formatDate(quiz.date) }} at {{ quiz.time }}</td>
                    <td>
                      <span :class="['status-badge', getStatusClass(quiz)]">
                        {{ getStatusText(quiz) }}
                      </span>
                    </td>
                    <td>{{ quiz.completed ? `${quiz.score}%` : 'N/A' }}</td>
                    <td class="actions-cell">
                      <button v-if="quiz.completed" class="secondary-button small">
                        Done
                      </button>
                      <button v-else class="action-button small" :disabled="!isQuizAvailable(quiz)"
                        @click="startQuiz(quiz)">
                        {{ isQuizAvailable(quiz) ? 'Start' : 'Not Available' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Progress Section -->
        <div v-if="activeSection === 'progress'" class="progress-view">
          <div class="content-header">
            <h2>My Progress</h2>
          </div>

          <div class="progress-container">
            <div class="progress-container">
              <div class="graph-container">
                <h2>Quiz Attempts per Subject</h2>
                <img v-if="quizAttemptsGraph" :src="`data:image/png;base64,${quizAttemptsGraph}`"
                  alt="Quiz Attempts Graph" class="graph-image" />
              </div>
              <div class="graph-container">
                <h2>Most Attempted Course</h2>
                <img v-if="mostAttemptedCourseGraph" :src="`data:image/png;base64,${mostAttemptedCourseGraph}`"
                  alt="Most Attempted Course Graph" class="graph-image" />
              </div>
              <div class="graph-container">
                <h2>Average Score per Subject</h2>
                <img v-if="averageScoreGraph" :src="`data:image/png;base64,${averageScoreGraph}`"
                  alt="Average Score Graph" class="graph-image" />
              </div>              
            </div>
            <div class="strength-weaknesses">
              <div class="strength-section">
                <h3>Strengths</h3>
                <ul class="analytics-list">
                  <li v-for="(strength, index) in strengths" :key="index">
                    <i class="bi bi-check-circle"></i>
                    <span>{{ strength }}</span>
                  </li>
                </ul>
              </div>
              <div class="weakness-section">
                <h3>Areas for Improvement</h3>
                <ul class="analytics-list">
                  <li v-for="(weakness, index) in weaknesses" :key="index">
                    <i class="bi bi-exclamation-circle"></i>
                    <span>{{ weakness }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Calendar Section -->
        <div v-if="activeSection === 'calendar'" class="calendar-view">
          <div class="content-header">
            <h2>Study Calendar</h2>
            <div class="calendar-navigation">
              <button class="icon-button" @click="previousMonth">
                <i class="bi bi-chevron-left"></i>
              </button>
              <span class="current-month">{{ currentMonthDisplay }}</span>
              <button class="icon-button" @click="nextMonth">
                <i class="bi bi-chevron-right"></i>
              </button>
            </div>
          </div>

          <div class="calendar-container">
            <div class="calendar-grid">
              <div class="calendar-header">
                <div class="weekday" v-for="day in weekdays" :key="day">{{ day }}</div>
              </div>
              <div class="calendar-days">
                <div v-for="(day, index) in calendarDays" :key="index" class="calendar-day" :class="{
                  'other-month': !day.currentMonth,
                  'today': day.isToday,
                  'has-events': day.events && day.events.length > 0
                }" @click="viewDayEvents(day)">
                  <span class="day-number">{{ day.number }}</span>
                  <div v-if="day.events && day.events.length > 0" class="day-events">
                    <div v-for="(event, i) in day.events.slice(0, 2)" :key="i" class="day-event-indicator"
                      :class="event.type">
                      {{ event.title }}
                    </div>
                    <div v-if="day.events.length > 2" class="more-events">
                      +{{ day.events.length - 2 }} more
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Settings Section -->
        <div v-if="activeSection === 'settings'" class="settings-view">
          <div class="content-header">
            <h2>Account Settings</h2>
          </div>

          <div class="settings-container">
            <div class="settings-tabs">
              <div class="settings-tab" :class="{ active: activeSettingsTab === 'profile' }"
                @click="activeSettingsTab = 'profile'">
                <i class="bi bi-person"></i>
                <span>Profile</span>
              </div>
              <!-- <div class="settings-tab" :class="{ active: activeSettingsTab === 'notifications' }"
                @click="activeSettingsTab = 'notifications'">
                <i class="bi bi-bell"></i>
                <span>Notifications</span>
              </div> -->
              <!-- <div class="settings-tab" :class="{ active: activeSettingsTab === 'preferences' }"
                @click="activeSettingsTab = 'preferences'">
                <i class="bi bi-sliders"></i>
                <span>Preferences</span>
              </div> -->
              <div class="settings-tab" :class="{ active: activeSettingsTab === 'security' }"
                @click="activeSettingsTab = 'security'">
                <i class="bi bi-shield-lock"></i>
                <span>Security</span>
              </div>
            </div>

            <div class="settings-content">
              <!-- Profile Settings -->
              <div v-if="activeSettingsTab === 'profile'" class="settings-panel">
                <h3>Profile Information</h3>
                <div class="profile-form">
                  <!-- <div class="profile-picture">
                    <img :src="user.avatarUrl || '/images/default-avatar.png'" alt="Profile" />
                    <button class="secondary-button small">Change Photo</button>
                  </div> -->
                  <div class="form-fields">
                    <div class="form-group">
                      <label for="fullname">Full Name</label>
                      <input type="text" id="fullname" v-model="user.name" placeholder="Enter your full name" />
                    </div>
                    <div class="form-group">
                      <label for="email">Email Address</label>
                      <input type="email" id="email" v-model="user.email" placeholder="Enter your email" />
                    </div>
                    <div class="form-actions">
                      <button class="action-button" @click="saveProfile">Save Changes</button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Notifications Settings -->
              <div v-if="activeSettingsTab === 'notifications'" class="settings-panel">
                <h3>Notification Preferences</h3>
                <div class="notification-settings">
                  <div class="notification-option" v-for="(option, index) in notificationOptions" :key="index">
                    <div class="option-details">
                      <h4>{{ option.title }}</h4>
                      <p>{{ option.description }}</p>
                    </div>
                    <div class="option-toggle">
                      <input type="checkbox" :id="`notification-${index}`" v-model="option.enabled" />
                      <label :for="`notification-${index}`" class="toggle-switch"></label>
                    </div>
                  </div>
                  <div class="form-actions">
                    <button class="action-button" @click="saveNotificationSettings">Save Preferences</button>
                  </div>
                </div>
              </div>

              <!-- Security Settings -->
              <div v-if="activeSettingsTab === 'security'" class="settings-panel">
                <h3>Security Settings</h3>
                <div class="security-settings">
                  <div class="security-section">
                    <h4>Change Password</h4>
                    <div class="form-group">
                      <label for="new-password">New Password</label>
                      <input type="password" id="new-password" v-model="security.newPassword"
                        placeholder="Enter new password" />
                    </div>
                    <div class="form-group">
                      <label for="confirm-password">Confirm New Password</label>
                      <input type="password" id="confirm-password" v-model="security.confirmPassword"
                        placeholder="Confirm new password" />
                    </div>
                    <div class="form-actions">
                      <button class="action-button" @click="changePassword">Update Password</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

// API token
const getToken = () => localStorage.getItem('accessToken');

// Headers with authorization
const authHeaders = computed(() => ({
  headers: { Authorization: `Bearer ${getToken()}` }
}));


// Authentication headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('accessToken');
  return {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  };
};


// Refs for Bootstrap modals
const subjectModalRef = ref(null);
const confirmModalRef = ref(null);



// Fetch subjects and open modal
const openSubjectsModal = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await axios.get("http://127.0.0.1:5000/user/subjects");
    availableSubjects.value = response.data;
  } catch (err) {
    error.value = "Failed to load subjects. Please try again.";
  } finally {
    loading.value = false;
    subjectModal.show();
  }
};

// Open confirmation modal

const fetchAvailableSubjects = async () => {
  loading.value = true;
  error.value = null;

  try {
    const response = await axios.get('/user/get-subjects', getAuthHeaders());
    availableSubjects.value = response.data;
  } catch (err) {
    console.error('Error fetching subjects:', err);
    error.value = err.response?.data?.message || 'Failed to load subjects...';
  } finally {
    loading.value = false;
  }
};



// User information (will be populated from API)
const user = ref({
  id: null,
  name: '',
  email: '',
  username: '',
  qualification: '',
  dob: null,
  phone: ''
});

// Dashboard statistics
const stats = ref({
  enrolledSubjects: 0,
  completedQuizzes: 0,
  upcomingQuizzes: 0,
  averageScore: 0
});

// Navigation and state management
const activeSection = ref('overview');
const activeSettingsTab = ref('profile');
const expandedSubject = ref(null);

// Filters
const searchQuery = ref('');
const subjectFilter = ref('all');
const quizFilter = ref('all');
const progressTimeframe = ref('month');

const subjectModal = ref(null);

// State management
const loading = ref(false);
const error = ref(null);
const availableSubjects = ref([]);
const showQuiz = ref(false)
// Calendar data
const currentDate = ref(new Date().toLocaleDateString('en-US', {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric'
}));
const currentMonth = ref(new Date());
const weekdays = ref(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']);
const currentMonthDisplay = ref(new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' }));
const calendarDays = ref([]);

// Data collections
const subjects = ref([]);
const chapters = ref([]);
const allQuizzes = ref([]);
const progressData = ref({
  scores: [],
  statistics: {
    total_quizzes: 0,
    average_score: 0,
    subject_performance: {}
  },
  strengths: [],
  weaknesses: []
});

// Settings
const notificationOptions = ref([
  {
    title: 'Quiz Reminders',
    description: 'Receive notifications before upcoming quizzes',
    enabled: true
  },
  {
    title: 'New Content Alerts',
    description: 'Be notified when new chapters or materials are added',
    enabled: true
  },
  {
    title: 'Performance Updates',
    description: 'Get updates about your quiz scores and progress',
    enabled: true
  },
  {
    title: 'System Announcements',
    description: 'Important announcements about the platform',
    enabled: true
  }
]);

const security = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});

// Computed properties
const filteredSubjects = computed(() => {
  if (subjectFilter.value === 'all') {
    return subjects.value;
  } else if (subjectFilter.value === 'active') {
    return subjects.value.filter(subject => subject.completion < 100);
  } else {
    return subjects.value.filter(subject => subject.completion === 100);
  }
});

const upcomingQuizzes = computed(() => {
  return allQuizzes.value.filter(quiz => !quiz.completed && new Date(quiz.date) >= new Date());
});

const completedQuizzes = computed(() => {
  return allQuizzes.value.filter(quiz => quiz.completed);
});

const filteredQuizzes = computed(() => {
  if (quizFilter.value === 'all') {
    return allQuizzes.value;
  } else if (quizFilter.value === 'upcoming') {
    return upcomingQuizzes.value;
  } else if (quizFilter.value === 'completed') {
    return completedQuizzes.value;
  } else if (quizFilter.value === 'past-due') {
    return allQuizzes.value.filter(quiz => !quiz.completed && new Date(quiz.date) < new Date());
  }
  return allQuizzes.value;
});

const strengths = computed(() => {
  return progressData.value.strengths || [];
});

const weaknesses = computed(() => {
  return progressData.value.weaknesses || [];
});

// Methods
// Navigation methods
const setActiveSection = (section) => {
  activeSection.value = section;
  loadUserProgress();
  // Load specific data when changing sections
  if (section === 'subjects') {
    loadSubjects();
  } else if (section === 'quizzes') {
    loadQuizzes();
  } else if (section === 'progress') {
    loadUserProgress();
  } else if (section === 'calendar') {
    generateCalendarDays();
  }
};

// Load user profile
const loadUserProfile = async () => {
  try {
    const response = await axios.get('/user/profile', authHeaders.value);
    user.value = response.data;
  } catch (error) {
    console.error('Error loading user profile:', error);
    if (error.response && error.response.status === 401) {
      // Handle unauthorized (token expired, etc)
      window.location.href = '/login';
    }
  }
};

// Subject methods
const loadSubjects = async () => {
  try {
    console.log("Fetching subjects...");

    console.log("Header:", authHeaders);  // Debugging log
    const response = await axios.get('/user/get-subjects', authHeaders.value);

    console.log("Response received:", response.data);  // Debugging log
    subjects.value = response.data;
    stats.value.enrolledSubjects = subjects.value.length;

    // Calculate completion stats
    const totalChapters = subjects.value.reduce((sum, subject) => sum + subject.total_chapters, 0);
    const completedChapters = subjects.value.reduce((sum, subject) => sum + subject.completed_chapters, 0);

    if (totalChapters > 0) {
      stats.value.overallCompletion = Math.round((completedChapters / totalChapters) * 100).toFixed(1);
    }
  } catch (error) {
    console.error("Error loading subjects:", error.response ? error.response.data : error.message);
    if (error.response && error.response.status === 401) {
      window.location.href = '/login';
    }
  }
};


const toggleChapters = (subjectId) => {
  if (expandedSubject.value === subjectId) {
    expandedSubject.value = null;
  } else {
    expandedSubject.value = subjectId;
    loadChaptersForSubject(subjectId);
  }
};

const loadChaptersForSubject = async (subjectId) => {
  try {
    const response = await axios.get(`/user/subject/${subjectId}/chapters`, authHeaders.value);
    chapters.value = response.data;
    console.log('load chapters: ', chapters.value[1].name);
  } catch (error) {
    console.error(`Error loading chapters for subject ${subjectId}:`, error);
  }
};

const getChaptersBySubject = (subjectId) => {
  console.log(chapters.value.filter(chapter => chapter.subject_id === subjectId));
  return chapters.value.filter(chapter => chapter.subject_id === subjectId);
};

const continueSubject = (subject) => {
  // Find the first incomplete chapter
  expandedSubject.value = subject.id;
  loadChaptersForSubject(subject.id).then(() => {
    const subjectChapters = getChaptersBySubject(subject.id);
    const nextChapter = subjectChapters.find(chapter => !chapter.completed);

    if (nextChapter) {
      viewChapter(nextChapter);
    } else {
      // All chapters are completed
      alert('All chapters in this subject are completed!');
    }
  });
};

const viewChapter = (chapter) => {
  // Navigate to chapter content page
  window.location.href = `/chapter/${chapter.id}`;
};

const getCompletionClass = (subject) => {
  if (subject.completion >= 75) {
    return 'high';
  } else if (subject.completion >= 50) {
    return 'medium';
  } else {
    return 'low';
  }
};

// Quiz methods
const loadQuizzes = async () => {
  try {
    const response = await axios.get('/user/quizzes', authHeaders.value);
    allQuizzes.value = response.data;
    
    // Update quiz-related stats more comprehensively
    const completed = completedQuizzes.value;
    const upcoming = upcomingQuizzes.value;
    
    stats.value.completedQuizzes = completed.length;
    stats.value.upcomingQuizzes = upcoming.length;

    // Improved average score calculation
    if (completed.length > 0) {
      const totalScore = completed.reduce((sum, quiz) => sum + (quiz.score || 0), 0);
      stats.value.averageScore = (totalScore / completed.length).toFixed(1);
    } else {
      stats.value.averageScore = '0.0';
    }
  } catch (error) {
    console.error('Error loading quizzes:', error);
    if (error.response && error.response.status === 401) {
      window.location.href = '/login';
    }
  }
};


const startQuiz = (quiz) => {
  window.location.href = `/quiz/${quiz.id}`;
  showQuiz.value = true;
};

const reviewQuiz = (quiz) => {
  window.location.href = `/quiz/${quiz.id}/review`;
};

const isQuizAvailable = (quiz) => {
  // Check if the quiz date and time has arrived
  const quizDateTime = new Date(`${quiz.date} ${quiz.time}`);
  return new Date() >= quizDateTime;
};

const getStatusText = (quiz) => {
  if (quiz.completed) {
    return 'Completed';
  }

  const quizDate = new Date(quiz.date);
  const today = new Date();

  if (quizDate < today) {
    return 'Past Due';
  } else if (quizDate.toDateString() === today.toDateString()) {
    return 'Today';
  } else {
    return 'Upcoming';
  }
};

const getStatusClass = (quiz) => {
  if (quiz.completed) {
    return 'completed';
  }

  const quizDate = new Date(quiz.date);
  const today = new Date();

  if (quizDate < today) {
    return 'past-due';
  } else if (quizDate.toDateString() === today.toDateString()) {
    return 'today';
  } else {
    return 'upcoming';
  }
};

// Progress tracking
const loadUserProgress = async () => {
  try {
    const response = await axios.get(`/user/progress?timeframe=${progressTimeframe.value}`, authHeaders.value);
    progressData.value = response.data;

    // Update overview stats
    if (progressData.value.statistics) {
      stats.value.averageScore = progressData.value.statistics.average_score.toFixed(1);
    }
  } catch (error) {
    console.error('Error loading user progress:', error);
    if (error.response && error.response.status === 401) {
      window.location.href = '/login';
    }
  }
};

watch(progressTimeframe, () => {
  loadUserProgress();
});

// Calendar functionality
const generateCalendarDays = () => {
  const year = currentMonth.value.getFullYear();
  const month = currentMonth.value.getMonth();

  // First day of the month
  const firstDay = new Date(year, month, 1);
  const firstDayOfWeek = firstDay.getDay();

  // Last day of the month
  const lastDay = new Date(year, month + 1, 0);
  const daysInMonth = lastDay.getDate();

  // Previous month days to display
  const prevMonthLastDay = new Date(year, month, 0).getDate();

  const days = [];

  // Add previous month days
  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    days.push({
      number: prevMonthLastDay - i,
      currentMonth: false,
      isToday: false,
      events: []
    });
  }

  // Add current month days
  const today = new Date();
  for (let i = 1; i <= daysInMonth; i++) {
    const isToday = today.getDate() === i &&
      today.getMonth() === month &&
      today.getFullYear() === year;

    days.push({
      number: i,
      currentMonth: true,
      isToday: isToday,
      events: getEventsForDay(new Date(year, month, i))
    });
  }

  // Add next month days
  const daysNeeded = 42 - days.length; // 6 rows of 7 days
  for (let i = 1; i <= daysNeeded; i++) {
    days.push({
      number: i,
      currentMonth: false,
      isToday: false,
      events: []
    });
  }

  calendarDays.value = days;
};

const getEventsForDay = (date) => {
  // Filter quizzes for this day
  return allQuizzes.value.filter(quiz => {
    const quizDate = new Date(quiz.date);
    return quizDate.getDate() === date.getDate() &&
      quizDate.getMonth() === date.getMonth() &&
      quizDate.getFullYear() === date.getFullYear();
  }).map(quiz => ({
    title: quiz.title,
    type: quiz.completed ? 'completed' : 'quiz',
    time: quiz.time,
    quizId: quiz.id
  }));
};

const viewDayEvents = (day) => {
  if (day.events && day.events.length > 0) {
    // Show events for this day in a modal or detail view
    alert(`Events for ${day.number}: ${day.events.map(e => e.title).join(', ')}`);
  }
};

const previousMonth = () => {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() - 1, 1);
  currentMonthDisplay.value = currentMonth.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  generateCalendarDays();
};

const nextMonth = () => {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1, 1);
  currentMonthDisplay.value = currentMonth.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  generateCalendarDays();
};

// Settings methods
const saveProfile = async () => {
  try {
    await axios.put('/user/profile', {
      name: user.value.name,
      email: user.value.email,
      phone: user.value.phone
    }, authHeaders.value);

    alert('Profile updated successfully!');
  } catch (error) {
    console.error('Error updating profile:', error);
    alert('Failed to update profile. Please try again.');
  }
};

// const saveNotificationSettings = async () => {
//   try {
//     await axios.put('/user/notifications', {
//       notifications: notificationOptions.value.map(option => ({
//         type: option.title,
//         enabled: option.enabled
//       }))
//     }, authHeaders.value);

//     alert('Notification preferences saved!');
//   } catch (error) {
//     console.error('Error saving notification preferences:', error);
//     alert('Failed to save notification preferences. Please try again.');
//   }
// };

const changePassword = async () => {
  // Validate passwords
  if (security.value.newPassword !== security.value.confirmPassword) {
    alert('New passwords do not match!');
    return;
  }

  try {
    await axios.put('/user/change-password', {
      currentPassword: security.value.currentPassword,
      newPassword: security.value.newPassword
    }, authHeaders.value);

    alert('Password changed successfully!');
    security.value.currentPassword = '';
    security.value.newPassword = '';
    security.value.confirmPassword = '';
  } catch (error) {
    console.error('Error changing password:', error);
    if (error.response && error.response.status === 400) {
      alert('Current password is incorrect. Please try again.');
    } else {
      alert('Failed to change password. Please try again.');
    }
  }
};

// Quiz attempt functionality
const submitQuiz = async (quizId, answers) => {
  const totalScored = calculateScore(answers);

  try {
    await axios.post(`/user/attempt-quiz/${quizId}`, {
      total_scored: totalScored
    }, authHeaders.value);

    alert('Quiz submitted successfully!');
    window.location.href = `/quiz/${quizId}/results`;
  } catch (error) {
    console.error('Error submitting quiz:', error);
    if (error.response && error.response.status === 400) {
      alert('You have already attempted this quiz.');
    } else {
      alert('Failed to submit quiz. Please try again.');
    }
  }
};

const calculateScore = (answers) => {
  // This would be implemented based on your scoring logic
  // For now, we'll just return a mock score
  return Math.floor(Math.random() * 40) + 60; // Random score between 60-100
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

// Load initial data on component mount
onMounted(() => {
  loadUserProfile();
  loadSubjects();
  loadQuizzes();
  loadUserProgress();
  generateCalendarDays();
  fetchAvailableSubjects();
  fetchGraphs();
});

const quizAttemptsGraph = ref('')
const averageScoreGraph = ref('')
const mostAttemptedCourseGraph = ref('')

// Fetch graph data
const fetchGraphs = async () => {
  try {
    // Fetch subject participation graph
    const subjectResponse = await axios.get('/user/quiz-attempts-per-subject', authHeaders.value)
    quizAttemptsGraph.value = subjectResponse.data.graph

    // Fetch user growth graph
    const userGrowthResponse = await axios.get('/user/average-score-per-subject', authHeaders.value)
    averageScoreGraph.value = userGrowthResponse.data.graph

    // Fetch performance graph
    const performanceResponse = await axios.get('/user/most-attempted-course', authHeaders.value)
    mostAttemptedCourseGraph.value = performanceResponse.data.graph
  } catch (error) {
    console.error('Error fetching analytics graphs:', error)
  }
}

</script>

<style>
/* Main Variables */
:root {
  --primary-color: #4361ee;
  --primary-light: #e9efff;
  --secondary-color: #3f37c9;
  --success-color: #2ecc71;
  --warning-color: #f39c12;
  --danger-color: #e74c3c;
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-light: #888888;
  --border-color: #e0e0e0;
  --background-light: #f8f9fa;
  --background-white: #ffffff;
  --shadow-light: 0 2px 10px rgba(0, 0, 0, 0.05);
  --shadow-medium: 0 5px 15px rgba(0, 0, 0, 0.1);
  --border-radius: 8px;
  --sidebar-width: 260px;
}

/* Reset & Base Styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', sans-serif;
  color: var(--text-primary);
  background-color: var(--background-light);
  line-height: 1.5;
  font-size: 14px;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

/* Main Container */
.user-dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Dashboard Header */
.dashboard-header {
  background-color: var(--background-white);
  padding: 20px 30px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.dashboard-welcome h1 {
  font-size: 1.8rem;
  margin-bottom: 5px;
  color: var(--text-primary);
}

.dashboard-welcome p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.dashboard-actions {
  display: flex;
  align-items: center;
}

.search-bar {
  position: relative;
  width: 300px;
}

.search-bar i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
}

.search-bar input {
  width: 100%;
  padding: 10px 15px 10px 35px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.search-bar input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
}

/* Dashboard Stats */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  padding: 20px 30px;
  background-color: var(--background-white);
  border-bottom: 1px solid var(--border-color);
}

.stat-card {
  background-color: var(--background-white);
  border-radius: var(--border-radius);
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: var(--shadow-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-medium);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: var(--primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.stat-icon i {
  color: var(--primary-color);
  font-size: 1.4rem;
}

.stat-details {
  display: flex;
  flex-direction: column;
}

.stat-count {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-name {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

/* Dashboard Content Layout */
.dashboard-content {
  display: flex;
  flex: 1;
}

/* Sidebar */
.dashboard-sidebar {
  width: var(--sidebar-width);
  background-color: var(--background-white);
  border-right: 1px solid var(--border-color);
  padding: 20px 0;
  height: calc(100vh - 170px);
  position: sticky;
  top: 170px;
  overflow-y: auto;
}

.user-profile {
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-avatar {
  width: 50px;
  height: 50px;
  overflow: hidden;
  border-radius: 50%;
  margin-right: 15px;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-details h3 {
  font-size: 1rem;
  margin-bottom: 2px;
}

.profile-details span {
  font-size: 0.8rem;
  color: var(--text-secondary);
  display: block;
}

.sidebar-nav {
  list-style: none;
}

.sidebar-nav li {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  margin-bottom: 5px;
}

.sidebar-nav li:hover {
  background-color: var(--primary-light);
  color: var(--primary-color);
}

.sidebar-nav li.active {
  background-color: var(--primary-light);
  color: var(--primary-color);
  border-left-color: var(--primary-color);
  font-weight: 500;
}

.sidebar-nav i {
  margin-right: 12px;
  font-size: 1.1rem;
  width: 20px;
  text-align: center;
}

/* Main Content Area */
.main-content {
  flex: 1;
  padding: 20px 30px;
  overflow-y: auto;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.content-header h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
}

.date-display {
  display: flex;
  align-items: center;
  color: var(--text-secondary);
  font-size: 0.85rem;
}

.date-display i {
  margin-right: 5px;
}

/* Content Sections */
.content-section {
  background-color: var(--background-white);
  border-radius: var(--border-radius);
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-light);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h3 {
  font-size: 1.1rem;
  color: var(--text-primary);
}

/* Button Styles */
.action-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius);
  padding: 10px 18px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  font-weight: 500;
}

.action-button i {
  margin-left: 8px;
}

.action-button:hover {
  background-color: var(--secondary-color);
  transform: translateY(-2px);
}

.action-button:disabled {
  background-color: var(--text-light);
  cursor: not-allowed;
  transform: none;
}

.action-button.small {
  padding: 6px 12px;
  font-size: 0.8rem;
}

.secondary-button {
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 9px 16px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
}

.secondary-button i {
  margin-right: 8px;
}

.secondary-button:hover {
  background-color: var(--background-light);
  border-color: var(--text-light);
}

.secondary-button.small {
  padding: 5px 10px;
  font-size: 0.8rem;
}

.icon-button {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all 0.3s ease;
}

.icon-button:hover {
  background-color: var(--background-light);
}

/* Quiz Cards */
.quiz-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.quiz-card {
  background-color: var(--background-white);
  border-radius: var(--border-radius);
  padding: 20px;
  box-shadow: var(--shadow-light);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.quiz-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-medium);
}

.quiz-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.quiz-card-header h4 {
  font-size: 1.1rem;
  color: var(--text-primary);
}

.quiz-status {
  font-size: 0.75rem;
  padding: 3px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.quiz-status.upcoming {
  background-color: #fff8e1;
  color: #f39c12;
}

.quiz-status.available {
  background-color: #e3f2fd;
  color: #2196f3;
}

.quiz-status.completed {
  background-color: #e8f5e9;
  color: #4caf50;
}

.quiz-status.past-due {
  background-color: #ffebee;
  color: #f44336;
}

.quiz-info {
  margin-bottom: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.info-item i {
  margin-right: 10px;
  width: 16px;
  color: var(--text-light);
}

.quiz-actions {
  display: flex;
  justify-content: flex-end;
}

/* Subject Cards */
.subject-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.subject-card {
  background-color: var(--background-white);
  border-radius: var(--border-radius);
  padding: 20px;
  box-shadow: var(--shadow-light);
  border: 1px solid var(--border-color);
}

.subject-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.completion-badge {
  font-size: 0.75rem;
  padding: 3px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.completion-badge.low {
  background-color: #ffebee;
  color: #f44336;
}

.completion-badge.medium {
  background-color: #fff8e1;
  color: #f39c12;
}

.completion-badge.high {
  background-color: #e8f5e9;
  color: #4caf50;
}

.subject-description {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 15px;
  line-height: 1.5;
}

.progress-bar {
  height: 8px;
  background-color: var(--background-light);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress-fill {
  height: 100%;
  background-color: var(--primary-color);
  border-radius: 4px;
}

.subject-stats {
  display: flex;
  margin-bottom: 20px;
}

.subject-stats .stat {
  display: flex;
  align-items: center;
  margin-right: 20px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.subject-stats .stat i {
  margin-right: 8px;
  color: var(--text-light);
}

.subject-actions {
  display: flex;
  justify-content: space-between;
}

/* Chapters List */
.chapters-list {
  margin-top: 15px;
  border-top: 1px solid var(--border-color);
  padding-top: 15px;
}

.chapter-item {
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}

.chapter-item:last-child {
  border-bottom: none;
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.chapter-title {
  display: flex;
  align-items: center;
}

.chapter-title i {
  margin-right: 10px;
  color: var(--text-light);
}

.chapter-title i.bi-check-circle-fill {
  color: var(--success-color);
}

.chapter-title h4 {
  font-size: 0.95rem;
  font-weight: 500;
}

.chapter-description {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-left: 26px;
}

/* Quiz Table */
.quiz-table-container {
  overflow-x: auto;
}

.quiz-table {
  width: 100%;
  border-collapse: collapse;
}

.quiz-table th,
.quiz-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.quiz-table th {
  font-weight: 600;
  color: var(--text-primary);
  background-color: var(--background-light);
}

.quiz-table tr:last-child td {
  border-bottom: none;
}

.quiz-table tr:hover {
  background-color: var(--background-light);
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.upcoming {
  background-color: #fff8e1;
  color: #f39c12;
}

.status-badge.available {
  background-color: #e3f2fd;
  color: #2196f3;
}

.status-badge.completed {
  background-color: #e8f5e9;
  color: #4caf50;
}

.status-badge.past-due {
  background-color: #ffebee;
  color: #f44336;
}

.actions-cell {
  text-align: right;
}

/* Charts and Analytics */
.chart-container {
  background-color: var(--background-white);
  border-radius: var(--border-radius);
  padding: 20px;
  box-shadow: var(--shadow-light);
  margin-bottom: 20px;
}

.chart-container.large {
  height: 300px;
}

.chart-header {
  margin-bottom: 15px;
}

.chart-header h3 {
  font-size: 1.1rem;
  color: var(--text-primary);
}

.chart-placeholder {
  height: 100%;
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--background-light);
  border-radius: var(--border-radius);
}

.chart-message {
  text-align: center;
  color: var(--text-secondary);
}

.chart-message i {
  font-size: 2rem;
  margin-bottom: 10px;
  color: var(--text-light);
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.strength-weaknesses {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.strength-section,
.weakness-section {
  background-color: var(--background-white);
  border-radius: var(--border-radius);
  padding: 20px;
  box-shadow: var(--shadow-light);
}

.analytics-list {
  list-style: none;
  margin-top: 15px;
}

.analytics-list li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.analytics-list li i {
  margin-right: 10px;
  margin-top: 3px;
}

.analytics-list li i.bi-check-circle {
  color: var(--success-color);
}

.analytics-list li i.bi-exclamation-circle {
  color: var(--warning-color);
}

/* Calendar */
.calendar-navigation {
  display: flex;
  align-items: center;
}

.current-month {
  margin: 0 15px;
  font-size: 1rem;
  font-weight: 500;
}

.calendar-grid {
  background-color: var(--background-white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-light);
  overflow: hidden;
}

.calendar-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background-color: var(--primary-light);
}

.weekday {
  text-align: center;
  padding: 12px;
  font-weight: 500;
  color: var(--primary-color);
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}

.calendar-day {
  height: 110px;
  border: 1px solid var(--border-color);
  padding: 8px;
  overflow: hidden;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.calendar-day:hover {
  background-color: var(--background-light);
}

.calendar-day.other-month {
  opacity: 0.5;
}

.calendar-day.today {
  background-color: var(--primary-light);
}

.day-number {
  display: block;
  text-align: right;
  margin-bottom: 5px;
  font-weight: 500;
}

.day-events {
  font-size: 0.75rem;
}

.day-event-indicator {
  margin-bottom: 3px;
  padding: 2px 5px;
  border-radius: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.day-event-indicator.quiz {
  background-color: #e3f2fd;
  color: #2196f3;
}

.day-event-indicator.deadline {
  background-color: #ffebee;
  color: #f44336;
}

.day-event-indicator.lecture {
  background-color: #e8f5e9;
  color: #4caf50;
}

.more-events {
  font-size: 0.7rem;
  color: var(--text-light);
  text-align: center;
}

/* Settings */
.settings-container {
  display: flex;
  background-color: var(--background-white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-light);
  overflow: hidden;
}

.settings-tabs {
  width: 220px;
  border-right: 1px solid var(--border-color);
  padding: 20px 0;
}

.settings-tab {
  padding: 12px 20px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.settings-tab i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
}

.settings-tab:hover {
  background-color: var(--background-light);
}

.settings-tab.active {
  background-color: var(--primary-light);
  color: var(--primary-color);
  font-weight: 500;
}

.settings-content {
  flex: 1;
  padding: 20px;
}

.settings-panel h3 {
  margin-bottom: 20px;
  font-size: 1.1rem;
}

.profile-form {
  display: flex;
  gap: 30px;
}

.profile-picture {
  width: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-picture img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 15px;
}

.form-fields {
  flex: 1;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
}

/* Notification Options */
.notification-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid var(--border-color);
}

.notification-option:last-child {
  border-bottom: none;
}

.option-details h4 {
  font-size: 0.95rem;
  margin-bottom: 5px;
}

.option-details p {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
  background-color: var(--border-color);
  border-radius: 12px;
  transition: all 0.3s;
  cursor: pointer;
}

.toggle-switch::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: white;
  top: 2px;
  left: 2px;
  transition: all 0.3s;
}

input[type="checkbox"] {
  display: none;
}

input[type="checkbox"]:checked+.toggle-switch {
  background-color: var(--primary-color);
}

input[type="checkbox"]:checked+.toggle-switch::after {
  left: 22px;
}

/* Empty States */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: var(--text-light);
  text-align: center;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 15px;
}

.empty-state.small {
  padding: 20px 0;
}

.empty-state.small i {
  font-size: 2rem;
}

/* Filter Styles */
.filter-actions {
  display: flex;
  align-items: center;
}

.select-container {
  position: relative;
}

.select-container select {
  padding: 8px 30px 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  appearance: none;
  background-color: white;
  cursor: pointer;
  font-size: 0.9rem;
}

.select-container::after {
  content: '\f282';
  font-family: 'Bootstrap Icons';
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

/* Responsive Styles */
@media (max-width: 1024px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .dashboard-content {
    flex-direction: column;
  }

  .dashboard-sidebar {
    width: 100%;
    height: auto;
    position: relative;
    top: 0;
    border-right: none;
    border-bottom: 1px solid var(--border-color);
  }

  .sidebar-nav {
    display: flex;
    overflow-x: auto;
  }

  .sidebar-nav li {
    border-left: none;
    border-bottom: 3px solid transparent;
  }

  .sidebar-nav li.active {
    border-left-color: transparent;
    border-bottom-color: var(--primary-color);
  }

  .user-profile {
    display: none;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats-cards {
    grid-template-columns: 1fr;
  }

  .search-bar {
    width: 100%;
  }

  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .subject-cards,
  .quiz-cards {
    grid-template-columns: 1fr;
  }

  .profile-form {
    flex-direction: column;
  }

  .settings-container {
    flex-direction: column;
  }

  .settings-tabs {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--border-color);
    padding: 0;
    display: flex;
    overflow-x: auto;
  }

  .settings-tab {
    padding: 15px;
    flex-shrink: 0;
  }
}
</style>