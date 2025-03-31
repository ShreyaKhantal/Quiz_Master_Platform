<template>
  <div class="admin-dashboard">
    <!-- Dashboard Header -->
    <section class="dashboard-header">
      <div class="dashboard-welcome">
        <h1>Admin Dashboard</h1>
        <p>Manage your subjects, chapters, and quizzes all in one place</p>
      </div>
      <div class="dashboard-actions">
        <div class="search-bar">
          <i class="bi bi-search"></i>
          <input type="text" placeholder="Search users, subjects, or quizzes..." v-model="searchQuery"
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
          <span class="stat-count">{{ stats.subjects }}</span>
          <span class="stat-name">Subjects</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="bi bi-list-check"></i>
        </div>
        <div class="stat-details">
          <span class="stat-count">{{ stats.chapters }}</span>
          <span class="stat-name">Chapters</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="bi bi-question-circle"></i>
        </div>
        <div class="stat-details">
          <span class="stat-count">{{ stats.quizzes }}</span>
          <span class="stat-name">Quizzes</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">
          <i class="bi bi-people"></i>
        </div>
        <div class="stat-details">
          <span class="stat-count">{{ stats.users }}</span>
          <span class="stat-name">Users</span>
        </div>
      </div>
    </section>

    <!-- Main Dashboard Content -->
    <div class="dashboard-content">
      <!-- Sidebar Navigation -->
      <aside class="dashboard-sidebar">
        <ul class="sidebar-nav">
          <li :class="{ active: activeSection === 'subjects' }" @click="setActiveSection('subjects')">
            <i class="bi bi-book"></i>
            <span>Subjects</span>
          </li>
          <li :class="{ active: activeSection === 'quizzes' }" @click="setActiveSection('quizzes')">
            <i class="bi bi-question-circle"></i>
            <span>Quizzes</span>
          </li>
          <li :class="{ active: activeSection === 'users' }" @click="setActiveSection('users')">
            <i class="bi bi-people"></i>
            <span>Users</span>
          </li>
          <li :class="{ active: activeSection === 'analytics' }" @click="setActiveSection('analytics')">
            <i class="bi bi-bar-chart"></i>
            <span>Analytics</span>
          </li>
        </ul>
      </aside>

      <!-- Main Content Area -->
      <div class="main-content">
        <!-- Subjects Management View -->
        <div v-if="activeSection === 'subjects'" class="subjects-view">
          <div class="content-header">
            <h2>Subject Management</h2>
            <button class="action-button" @click="openSubjectModal()">
              <i class="bi bi-plus-circle"></i> New Subject
            </button>
          </div>

          <div class="subjects-container">
            <div v-if="subjects.length === 0" class="empty-state">
              <i class="bi bi-journal-x"></i>
              <p>No subjects found. Create your first subject to get started.</p>
            </div>

            <div v-else class="subject-cards">
              <div v-for="subject in filteredSubjects" :key="subject.id" class="subject-card">
                <div class="subject-card-header">
                  <h3>{{ subject.name }}</h3>
                  <div class="card-actions">
                    <button class="icon-button" @click="openSubjectModal(subject)">
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button class="icon-button delete" @click="confirmDeleteSubject(subject)">
                      <i class="bi bi-trash"></i>
                    </button>
                  </div>
                </div>
                <p class="subject-description">{{ subject.description }}</p>
                <div class="subject-stats">
                  <span>{{ getChapterCount(subject.id) }} Chapters</span>
                  <span>{{ getQuizCount(subject.id) }} Quizzes</span>
                </div>
                <div class="subject-actions">
                  <button class="secondary-button" @click="toggleChapters(subject.id)">
                    <i class="bi" :class="expandedSubject === subject.id ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
                    {{ expandedSubject === subject.id ? 'Hide Chapters' : 'View Chapters' }}
                  </button>
                  <button class="action-button" @click="openChapterModal(subject.id)">
                    <i class="bi bi-plus-circle"></i> Add Chapter
                  </button>
                </div>

                <!-- Chapters List (Expandable) -->
                <div v-if="expandedSubject === subject.id" class="chapters-list">
                  <div v-if="getChaptersBySubject(subject.id).length === 0" class="empty-state small">
                    <p>No chapters yet. Add your first chapter.</p>
                  </div>
                  <div v-else class="chapter-accordion">
                    <div v-for="chapter in getChaptersBySubject(subject.id)" :key="chapter.id" class="chapter-item">
                      <div class="chapter-header">
                        <div class="chapter-title">
                          <i class="bi" :class="expandedChapter === chapter.id ? 'bi-folder2-open' : 'bi-folder'"></i>
                          <h4>{{ chapter.name }}</h4>
                        </div>
                        <div class="chapter-actions">
                          <button class="icon-button" @click="openChapterModal(subject.id, chapter)">
                            <i class="bi bi-pencil"></i>
                          </button>
                          <button class="icon-button delete" @click="confirmDeleteChapter(chapter)">
                            <i class="bi bi-trash"></i>
                          </button>
                          <button class="icon-button" @click="toggleQuizzes(chapter.id)">
                            <i class="bi"
                              :class="expandedChapter === chapter.id ? 'bi-chevron-up' : 'bi-chevron-down'"></i>
                          </button>
                        </div>
                      </div>
                      <p class="chapter-description">{{ chapter.description }}</p>

                      <!-- Quizzes List (Expandable) -->
                      <div v-if="expandedChapter === chapter.id" class="quizzes-list">
                        <div class="quiz-list-header">
                          <h5>Quizzes</h5>
                          <button class="action-button small" @click="openQuizModal(chapter.id)">
                            <i class="bi bi-plus-circle"></i> Add Quiz
                          </button>
                        </div>
                        <div v-if="getQuizzesByChapter(chapter.id).length === 0" class="empty-state smaller">
                          <p>No quizzes yet. Add your first quiz.</p>
                        </div>
                        <div v-else class="quiz-items">
                          <div v-for="quiz in getQuizzesByChapter(chapter.id)" :key="quiz.id" class="quiz-item">
                            <div class="quiz-header">
                              <div class="quiz-title">
                                <i class="bi bi-question-diamond"></i>
                                <span>{{ quiz.title }}</span>
                              </div>
                              <div class="quiz-actions">
                                <button class="icon-button" @click="openQuizModal(chapter.id, quiz)">
                                  <i class="bi bi-pencil"></i>
                                </button>
                                <button class="icon-button" @click="openQuestionManager(quiz)">
                                  <i class="bi bi-list-check"></i>
                                </button>
                                <button class="icon-button delete" @click="confirmDeleteQuiz(quiz)">
                                  <i class="bi bi-trash"></i>
                                </button>
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
          </div>
        </div>

        <!-- Quiz Management View -->
        <div v-if="activeSection === 'quizzes'" class="quizzes-view">
          <div class="content-header">
            <h2>Quiz Management</h2>
            <div class="filter-actions">
              <div class="select-container">
                <select v-model="quizFilter">
                  <option value="all">All Quizzes</option>
                  <option value="active">Active Quizzes</option>
                  <option value="upcoming">Upcoming Quizzes</option>
                  <option value="past">Past Quizzes</option>
                </select>
              </div>
            </div>
          </div>

          <div class="quizzes-container">
            <div v-if="allQuizzes.length === 0" class="empty-state">
              <i class="bi bi-question-diamond"></i>
              <p>No quizzes found. Create a subject and chapter first, then add quizzes.</p>
            </div>

            <div v-else class="quiz-table-container">
              <table class="quiz-table">
                <thead>
                  <tr>
                    <th>Quiz Title</th>
                    <th>Subject</th>
                    <th>Chapter</th>
                    <th>Questions</th>
                    <th>Date & Time</th>
                    <th>Duration</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
                    <td>{{ quiz.title }}</td>
                    <td>{{ getSubjectForQuiz(quiz) }}</td>
                    <td>{{ getChapterForQuiz(quiz) }}</td>
                    <td>{{ quiz.questionCount || 0 }}</td>
                    <td>{{ quiz.date || 'Not set' }}</td>
                    <td>{{ quiz.duration || 'Not set' }}</td>
                    <td class="actions-cell">
                      <button class="icon-button" @click="openQuizScheduleModal(quiz)">
                        <i class="bi bi-calendar"></i>
                      </button>
                      <button class="icon-button" @click="openQuestionManager(quiz)">
                        <i class="bi bi-list-check"></i>
                      </button>
                      <button class="icon-button" @click="openQuizModal(quiz.chapter_id, quiz)">
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button class="icon-button delete" @click="confirmDeleteQuiz(quiz)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Analytics View -->
        <div v-if="activeSection === 'analytics'" class="analytics-view">
          <div class="content-header">
            <h2>Analytics Dashboard</h2>
          </div>

          <div class="analytics-dashboard">
            <div class="dashboard-header">
              <h1>Analytics Dashboard</h1>
            </div>

            <div class="analytics-container">
              <div class="graph-container">
                <h2>Quiz Participation by Subject</h2>
                <img v-if="subjectParticipationGraph" :src="`data:image/png;base64,${subjectParticipationGraph}`"
                  alt="Subject Participation Graph" class="graph-image" />
              </div>
              <div class="graph-container">
                <h2>Performance by Subject</h2>
                <img v-if="performanceGraph" :src="`data:image/png;base64,${performanceGraph}`" alt="Performance Graph"
                  class="graph-image" />
              </div>
              <div class="graph-container">
                <h2>User Growth</h2>
                <img v-if="userGrowthGraph" :src="`data:image/png;base64,${userGrowthGraph}`" alt="User Growth Graph"
                  class="graph-image" />
              </div>
            </div>
          </div>
        </div>

        <!-- Users View -->
        <!-- <div v-if="activeSection === 'users'" class="users-view">
          <div class="content-header">
            <h2>User Management</h2>
            <div class="search-bar">
              <i class="bi bi-search"></i>
              <input type="text" placeholder="Search users..." v-model="userSearchQuery" />
            </div>
          </div>

          <div class="users-container">
            <div class="users-table-placeholder">
              <div class="placeholder-message">
                <i class="bi bi-people"></i>
                <p>User management functionality would display here</p>
                <p class="placeholder-details">
                  Including registration data, quiz performance, and account management
                </p>

                <div class="quiz-table-container">                  
                <table class="quiz-table" >
                <thead>
                  <tr>
                    <th>Quiz Title</th>
                    <th>Subject</th>
                    <th>Chapter</th>
                    <th>Questions</th>
                    <th>Date & Time</th>
                    <th>Duration</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
                    <td>{{ quiz.title }}</td>
                    <td>{{ getSubjectForQuiz(quiz) }}</td>
                    <td>{{ getChapterForQuiz(quiz) }}</td>
                    <td>{{ quiz.questionCount || 0 }}</td>
                    <td>{{ quiz.date || 'Not set' }}</td>
                    <td>{{ quiz.duration || 'Not set' }}</td>
                    <td class="actions-cell">
                      <button class="icon-button" @click="openQuizScheduleModal(quiz)">
                        <i class="bi bi-calendar"></i>
                      </button>
                      <button class="icon-button" @click="openQuestionManager(quiz)">
                        <i class="bi bi-list-check"></i>
                      </button>
                      <button class="icon-button" @click="openQuizModal(quiz.chapter_id, quiz)">
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button class="icon-button delete" @click="confirmDeleteQuiz(quiz)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
                </div>
              </div>

              
            </div>
          </div>
        </div> -->
        <div v-if="activeSection === 'users'" class="users-view">
          <div class="content-header">
            <h2>User Management</h2>
            <div class="search-filter-container">
              <div class="search-bar">
                <i class="bi bi-search"></i>
                <input type="text" placeholder="Search users..." v-model="userSearchQuery" @input="filterUsers" />
              </div>
            </div>
          </div>

          <div class="quiz-table-container">
            <div v-if="filteredUsers.length === 0" class="empty-state">
              <i class="bi bi-people-fill"></i>
              <p>No users found matching your search or filter.</p>
            </div>
            <table v-else class="quiz-table">
              <thead>
                <tr>
                  <th>First Name</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.id">
                  <td>{{ user.first_name }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ user.email }}</td>
                  <td class="actions-cell">
                    <button class="icon-button details" @click="showUserDetails(user)" title="View User Details">
                      <i class="bi bi-info-circle"></i>
                    </button>
                    <!-- <button class="icon-button flag" @click="toggleUserFlag(user)"
                      :title="user.is_flagged ? 'Unblock User' : 'Block User'">
                      <i :class="user.is_flagged ? 'bi bi-unlock' : 'bi bi-lock'"></i>
                    </button> -->
                    <button class="icon-button export" @click="exportUserScores(user)" title="Export User Scores">
                      <i class="bi bi-download"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- User Details Modal -->
          <div v-if="selectedUser" class="modal user-details-modal">
            <div class="modal-content">
              <span class="close-button" @click="selectedUser = null">&times;</span>
              <h3>User Details</h3>
              <div class="user-details">
                <p><strong>Full Name:</strong> {{ selectedUser.full_name }}</p>
                <p><strong>Username:</strong> {{ selectedUser.username }}</p>
                <p><strong>Email:</strong> {{ selectedUser.email }}</p>
                <p><strong>Date of Birth:</strong> {{ selectedUser.dob || 'Not provided' }}</p>
                <p><strong>Qualification:</strong> {{ selectedUser.qualification || 'Not specified' }}</p>

                <h4>Recent Quiz Attempts</h4>
                <table v-if="selectedUser.quiz_attempts && selectedUser.quiz_attempts.length"
                  class="recent-attempts-table">
                  <thead>
                    <tr>
                      <th>Quiz Title</th>
                      <th>Score</th>
                      <th>Attempted At</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="attempt in selectedUser.quiz_attempts" :key="attempt.quiz_id">
                      <td>{{ attempt.quiz_title }}</td>
                      <td>{{ attempt.total_scored }}</td>
                      <td>{{ formatDateTime(attempt.attempt_time) }}</td>
                    </tr>
                  </tbody>
                </table>
                <p v-else>No recent quiz attempts</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <!-- Subject Modal -->
    <div class="modal-overlay" v-if="showSubjectModal" @click="closeSubjectModal"></div>
    <div class="modal" v-if="showSubjectModal">
      <div class="modal-header">
        <h3>{{ editingSubject ? 'Edit Subject' : 'New Subject' }}</h3>
        <button class="close-button" @click="closeSubjectModal">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="subject-name">Subject Name</label>
          <input type="text" id="subject-name" v-model="subjectForm.name" placeholder="Enter subject name" required />
        </div>
        <div class="form-group">
          <label for="subject-description">Description</label>
          <textarea id="subject-description" v-model="subjectForm.description" placeholder="Enter subject description"
            rows="4"></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="secondary-button" @click="closeSubjectModal">Cancel</button>
        <button class="action-button" @click="saveSubject">
          {{ editingSubject ? 'Update Subject' : 'Create Subject' }}
        </button>
      </div>
    </div>

    <!-- Chapter Modal -->
    <div class="modal-overlay" v-if="showChapterModal" @click="closeChapterModal"></div>
    <div class="modal" v-if="showChapterModal">
      <div class="modal-header">
        <h3>{{ editingChapter ? 'Edit Chapter' : 'New Chapter' }}</h3>
        <button class="close-button" @click="closeChapterModal">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="chapter-name">Chapter Name</label>
          <input type="text" id="chapter-name" v-model="chapterForm.name" placeholder="Enter chapter name" required />
        </div>
        <div class="form-group">
          <label for="chapter-description">Description</label>
          <textarea id="chapter-description" v-model="chapterForm.description" placeholder="Enter chapter description"
            rows="4"></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="secondary-button" @click="closeChapterModal">Cancel</button>
        <button class="action-button" @click="saveChapter">
          {{ editingChapter ? 'Update Chapter' : 'Create Chapter' }}
        </button>
      </div>
    </div>


    <div class="modal-overlay" v-if="showQuizModal" @click="closeQuizModal"></div>
    <div class="modal" v-if="showQuizModal">
      <div class="modal-header">
        <h3>{{ editingQuiz ? 'Edit Quiz' : 'New Quiz' }}</h3>
        <button class="close-button" @click="closeQuizModal">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>
      <div class="modal-body">
        <!-- Quiz Title -->
        <div class="form-group">
          <label for="quiz-title">Quiz Title</label>
          <input type="text" id="quiz-title" v-model="quizForm.title" placeholder="Enter quiz title" required />
        </div>

        <!-- Quiz Date -->
        <div class="form-group">
          <label for="quiz-date">Date</label>
          <input type="date" id="quiz-date" v-model="quizForm.date" required />
        </div>

        <!-- Quiz Time -->
        <div class="form-group">
          <label for="quiz-time">Time</label>
          <input type="time" id="quiz-time" v-model="quizForm.time" required />
        </div>

        <!-- Quiz Duration -->
        <div class="form-group">
          <label for="quiz-duration">Duration</label>
          <input type="number" id="quiz-duration" v-model="quizForm.duration" placeholder="Enter duration" min="1"
            required />
        </div>
      </div>

      <div class="modal-footer">
        <button class="secondary-button" @click="closeQuizModal">Cancel</button>
        <button class="action-button" @click="saveQuiz">
          {{ editingQuiz ? 'Update Quiz' : 'Create Quiz' }}
        </button>
      </div>
    </div>

    <!-- Quiz Schedule Modal -->
    <div class="modal-overlay" v-if="showQuizScheduleModal" @click="closeQuizScheduleModal"></div>
    <div class="modal" v-if="showQuizScheduleModal">
      <div class="modal-header">
        <h3>Schedule Quiz: {{ scheduleQuizForm.title }}</h3>
        <button class="close-button" @click="closeQuizScheduleModal">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="quiz-date">Quiz Date</label>
          <input type="date" id="quiz-date" v-model="scheduleQuizForm.date" min="2024-01-01" />
        </div>
        <div class="form-group">
          <label for="quiz-time">Quiz Time</label>
          <input type="time" id="quiz-time" v-model="scheduleQuizForm.time" />
        </div>
        <div class="form-group">
          <label for="quiz-duration">Duration (HH:MM)</label>
          <div class="duration-inputs">
            <input type="number" id="quiz-duration-hours" v-model="scheduleQuizForm.hours" min="0" max="23"
              placeholder="Hours" />
            :
            <input type="number" id="quiz-duration-minutes" v-model="scheduleQuizForm.minutes" min="0" max="59"
              placeholder="Minutes" />
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="secondary-button" @click="closeQuizScheduleModal">Cancel</button>
        <button class="action-button" @click="saveQuizSchedule">Save Schedule</button>
      </div>
    </div>

    <!-- Question Manager Modal -->
    <div class="modal-overlay large" v-if="showQuestionManager" @click="closeQuestionManager"></div>
    <div class="modal large" v-if="showQuestionManager" @click.stop>
      <div class="modal-header">
        <h3>Question Manager: {{ activeQuiz?.title }}</h3>
        <button class="close-button" @click="closeQuestionManager">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>
      <div class="modal-body question-manager">
        <div class="question-manager-sidebar">
          <div class="action-bar">
            <button class="action-button" @click="addNewQuestion">
              <i class="bi bi-plus-circle"></i> Add Question
            </button>
          </div>
          <div class="question-list">
            <div v-for="(question, index) in questions" :key="index" class="question-item"
              :class="{ active: activeQuestionIndex === index }" @click="setActiveQuestion(index)">
              <span class="question-number">Q{{ index + 1 }}</span>
              <span class="question-preview">{{ truncateText(question.text, 30) }}</span>
            </div>

            <div v-if="questions.length === 0" class="empty-question-list">
              <p>No questions yet</p>
              <p>Click "Add Question" to create your first question</p>
            </div>
          </div>
        </div>

        <div class="question-editor" v-if="activeQuestionIndex !== null">
          <div class="form-group">
            <label for="question-text">Question</label>
            <textarea id="question-text" v-model="questions[activeQuestionIndex].text" placeholder="Enter question text"
              rows="3"></textarea>
          </div>

          <div class="form-group">
            <label>Options</label>
            <div v-for="(option, optIndex) in questions[activeQuestionIndex].options" :key="optIndex"
              class="option-row">
              <div class="option-radio">
                <input type="radio" :id="`option-${optIndex}`" :name="`correct-answer-${activeQuestionIndex}`"
                  :checked="questions[activeQuestionIndex].correctOption === optIndex"
                  @change="setCorrectOption(optIndex)" />
                <label :for="`option-${optIndex}`">Correct</label>
              </div>
              <div class="option-input">
                <input type="text" v-model="questions[activeQuestionIndex].options[optIndex]"
                  :placeholder="`Option ${optIndex + 1}`" />
              </div>
              <button v-if="questions[activeQuestionIndex].options.length > 2" class="icon-button delete"
                @click="removeOption(optIndex)">
                <i class="bi bi-trash"></i>
              </button>
            </div>

            <button v-if="questions[activeQuestionIndex].options.length < 6" class="secondary-button small"
              @click="addOption">
              <i class="bi bi-plus-circle"></i> Add Option
            </button>
          </div>

          <div class="question-actions">
            <button class="secondary-button delete"
              @click="removeQuestion(questions[activeQuestionIndex].id, activeQuestionIndex)">
              <i class="bi bi-trash"></i> Delete Question
            </button>
            <button class="action-button" @click="saveQuestions">
              <i class="bi bi-save"></i> Save Questions
            </button>
          </div>
        </div>

        <div class="question-editor-placeholder" v-else>
          <div class="placeholder-content">
            <i class="bi bi-question-circle"></i>
            <p>Select a question from the list or add a new question</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div class="modal-overlay" v-if="showConfirmModal" @click="closeConfirmModal"></div>
    <div class="modal small" v-if="showConfirmModal">
      <div class="modal-header">
        <h3>{{ confirmData.title }}</h3>
        <button class="close-button" @click="closeConfirmModal">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>
      <div class="modal-body">
        <p>{{ confirmData.message }}</p>
      </div>
      <div class="modal-footer">
        <button class="secondary-button" @click="closeConfirmModal">Cancel</button>
        <button class="action-button delete" @click="confirmData.action">
          Confirm Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import 'vue-toast-notification/dist/theme-sugar.css';
import { useToast } from 'vue-toast-notification';

// State variables
const activeSection = ref('subjects');
const subjects = ref([]);
const chapters = ref([]);
const allQuizzes = ref([]);
const searchQuery = ref('');
const userSearchQuery = ref('');
const quizFilter = ref('all');


// Users
const users = ref([]);

// Expansion tracking
const expandedSubject = ref(null);
const expandedChapter = ref(null);

// Modal states
const showSubjectModal = ref(false);
const showChapterModal = ref(false);
const showQuizModal = ref(false);
const showQuestionManager = ref(false);
const showQuizScheduleModal = ref(false);
const showConfirmModal = ref(false);

// Form data
const subjectForm = ref({ name: '', description: '' });
const chapterForm = ref({ name: '', description: '', subject_id: null });
const quizForm = ref({ title: '', chapter_id: null });
const scheduleQuizForm = ref({
  id: null,
  title: '',
  date: '',
  time: '',
  hours: 1,
  minutes: 30
});
const editingSubject = ref(false);
const editingChapter = ref(false);
const editingQuiz = ref(false);
const activeQuiz = ref(null);

// Question editor
const questions = ref([]);
const activeQuestionIndex = ref(null);

// Confirmation data
const confirmData = ref({
  title: '',
  message: '',
  action: () => { }
});

// Stats
const stats = ref({
  subjects: 0,
  chapters: 0,
  quizzes: 0,
  users: 0 // Placeholder
});

// API token
const getToken = () => localStorage.getItem('accessToken');

// Headers with authorization
const authHeaders = computed(() => ({
  headers: { Authorization: `Bearer ${getToken()}` }
}));

// Load initial data
onMounted(async () => {
  await fetchUsers();
  await fetchSubjects();
  await fetchGraphs();
});

// Fetch all subjects
const fetchSubjects = async () => {
  try {
    const response = await axios.get('/admin/get-subjects', authHeaders.value);
    subjects.value = response.data;

    // For each subject, fetch its chapters
    for (const subject of subjects.value) {
      await fetchChapters(subject.id);
    }

    updateStats();
  } catch (error) {
    console.error('Error fetching subjects:', error);
  }
};

// Fetch chapters for a specific subject
const fetchChapters = async (subjectId) => {
  try {
    const response = await axios.get(`/admin/get-chapters/${subjectId}`, authHeaders.value);
    const subjectChapters = response.data;
    // Add chapters to the main chapters array
    chapters.value = [...chapters.value.filter(c => c.subject_id !== subjectId), ...subjectChapters];
    // For each chapter, fetch its quizzes
    for (const chapter of subjectChapters) {
      await fetchQuizzes(chapter.id);
    }
  } catch (error) {
    console.error(`Error fetching chapters for subject ${subjectId}:`, error);
  }
};

// Optional: Function to fetch detailed user information
const fetchUserDetails = async (userId) => {
  try {
    const response = await axios.get(`/admin/user/${userId}/details`, {
      headers: authHeaders.value
    });

    // Update the specific user's details in the users array
    const userIndex = users.value.findIndex(u => u.id === userId);
    if (userIndex !== -1) {
      users.value[userIndex] = {
        ...users.value[userIndex],
        ...response.data
      };
    }
  } catch (error) {
    console.error(`Error fetching details for user ${userId}:`, error);
  }
};

// Fetch quizzes for a specific chapter
const fetchQuizzes = async (chapterId) => {
  try {
    const response = await axios.get(`/admin/get-quizzes/${chapterId}`, authHeaders.value);
    const chapterQuizzes = response.data;

    // Add quizzes to the main quizzes array
    allQuizzes.value = [...allQuizzes.value.filter(q => q.chapter_id !== chapterId), ...chapterQuizzes];
  } catch (error) {
    console.error(`Error fetching quizzes for chapter ${chapterId}:`, error);
  }
};

// Update stats counters
const updateStats = () => {
  stats.value = {
    subjects: subjects.value.length,
    chapters: chapters.value.length,
    quizzes: allQuizzes.value.length,
    users: users.value.length, // Placeholder, would come from API
  };
};

// Filter subjects based on search query
const filteredSubjects = computed(() => {
  if (!searchQuery.value) return subjects.value;

  const query = searchQuery.value.toLowerCase();
  return subjects.value.filter(subject =>
    subject.name.toLowerCase().includes(query) ||
    subject.description.toLowerCase().includes(query)
  );
});

// Filter quizzes based on selected filter and search query
const filteredQuizzes = computed(() => {
  let filtered = allQuizzes.value;

  // Apply filter type
  if (quizFilter.value !== 'all') {
    const today = new Date();

    if (quizFilter.value === 'active') {
      filtered = filtered.filter(quiz => {
        if (!quiz.date) return false;
        const quizDate = new Date(quiz.date);
        return quizDate.getTime() === today.getTime();
      });
    } else if (quizFilter.value === 'upcoming') {
      filtered = filtered.filter(quiz => {
        if (!quiz.date) return false;
        const quizDate = new Date(quiz.date);
        return quizDate > today;
      });
    } else if (quizFilter.value === 'past') {
      filtered = filtered.filter(quiz => {
        if (!quiz.date) return false;
        const quizDate = new Date(quiz.date);
        return quizDate < today;
      });
    }
  }

  // Apply search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(quiz =>
      quiz.title.toLowerCase().includes(query)
    );
  }

  return filtered;
});

// Helper functions for getting related data
const getChapterCount = (subjectId) => {
  return chapters.value.filter(chapter => chapter.subject_id === subjectId).length;
};

const getQuizCount = (subjectId) => {
  const subjectChapterIds = chapters.value
    .filter(chapter => chapter.subject_id === subjectId)
    .map(chapter => chapter.id);

  return allQuizzes.value.filter(quiz => subjectChapterIds.includes(quiz.chapter_id)).length;
};

const getChaptersBySubject = (subjectId) => {
  return chapters.value.filter(chapter => chapter.subject_id === subjectId);
};

const getQuizzesByChapter = (chapterId) => {
  return allQuizzes.value.filter(quiz => quiz.chapter_id === chapterId);
};

const getSubjectForQuiz = (quiz) => {
  const chapter = chapters.value.find(chapter => chapter.id === quiz.chapter_id);
  if (!chapter) return 'Unknown';

  const subject = subjects.value.find(subject => subject.id === chapter.subject_id);
  return subject ? subject.name : 'Unknown';
};

const getChapterForQuiz = (quiz) => {
  const chapter = chapters.value.find(chapter => chapter.id === quiz.chapter_id);
  return chapter ? chapter.name : 'Unknown';
};

const setActiveSection = (section) => {
  activeSection.value = section;
};

const openSubjectModal = (subject = null) => {
  if (subject) {
    subjectForm.value = { ...subject };
    editingSubject.value = true;
  } else {
    subjectForm.value = { name: '', description: '' };
    editingSubject.value = false;
  }

  showSubjectModal.value = true;
};

const closeSubjectModal = () => {
  showSubjectModal.value = false;
};


// Toast notification
const toast = useToast()

const userRoleFilter = ref('all')
const selectedUser = ref(null)
const filteredUsers = ref([])

// Fetch users from backend
const fetchUsers = async () => {
  try {
    const response = await axios.get('/admin/get-users', authHeaders.value);
    users.value = response.data.map(user => ({
      ...user,
      is_flagged: user.is_active === false // Map backend is_active to is_flagged
    }));
    filterUsers();
  } catch (error) {
    console.error('Error fetching users:', error);
    toast.error('Failed to fetch users');
  }
}

// Filter users based on search query and role
const filterUsers = () => {
  filteredUsers.value = users.value.filter(user => {
    const matchesSearch = !userSearchQuery.value ||
      user.username.toLowerCase().includes(userSearchQuery.value.toLowerCase()) ||
      user.email.toLowerCase().includes(userSearchQuery.value.toLowerCase()) ||
      user.full_name.toLowerCase().includes(userSearchQuery.value.toLowerCase());

    const matchesRoleFilter =
      userRoleFilter.value === 'all' ||
      (userRoleFilter.value === 'flagged' && user.is_flagged) ||
      user.role === userRoleFilter.value;

    return matchesSearch && matchesRoleFilter;
  });
}

// Show user details in a modal
const showUserDetails = async (user) => {
  try {
    const response = await axios.get(`/admin/user/${user.id}/details`, authHeaders.value);
    selectedUser.value = response.data;
  } catch (error) {
    console.error('Error fetching user details:', error);
    toast.error('Failed to fetch user details');
  }
}

// Toggle user flag (block/unblock)
const toggleUserFlag = async (user) => {
  try {
    await axios.put(`/admin/user/${user.id}/flag`, {
      is_flagged: !user.is_flagged
    }, {
      headers: authHeaders.value
    });

    // Update local state
    user.is_flagged = !user.is_flagged;

    toast.success(`User ${user.is_flagged ? 'blocked' : 'unblocked'} successfully`);
  } catch (error) {
    console.error('Error flagging user:', error);
    toast.error('Failed to update user status');
  }
}

// Export user scores to CSV
const exportUserScores = async (user) => {
  try {
    const response = await axios.get(`/admin/user/${user.id}/scores/export`, authHeaders.value);

    // Create a download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${user.username}_scores.csv`);
    document.body.appendChild(link);
    link.click();

    toast.success('Scores exported successfully');
  } catch (error) {
    console.error('Error exporting user scores:', error);
    toast.error('Failed to export scores');
  }
}

// Helper method to format datetime
const formatDateTime = (dateTime) => {
  return new Date(dateTime).toLocaleString();
}

// Fetch users when component is mounted
onMounted(() => {
  fetchUsers();
})

// Expose methods and computed properties if needed
defineExpose({
  fetchUsers,
  showUserDetails,
  toggleUserFlag,
  exportUserScores,
  formatDateTime
})

const saveSubject = async () => {
  try {
    if (editingSubject.value) {
      // Update existing subject
      await axios.put(
        `/admin/update-subject/${subjectForm.value.id}`,
        subjectForm.value,
        authHeaders.value
      );

      // Update local data
      const index = subjects.value.findIndex(s => s.id === subjectForm.value.id);
      if (index !== -1) {
        subjects.value[index] = { ...subjectForm.value };
      }
    } else {
      // Create new subject
      const response = await axios.post(
        '/admin/create-subject',
        subjectForm.value,
        authHeaders.value
      );

      // Add to local data
      subjects.value.push(response.data);
    }

    updateStats();
    closeSubjectModal();
    fetchSubjects()
  } catch (error) {
    console.error('Error saving subject:', error);
  }
};

const confirmDeleteSubject = (subject) => {
  confirmData.value = {
    title: 'Delete Subject',
    message: `Are you sure you want to delete the subject "${subject.name}"? This will also delete all related chapters and quizzes.`,
    action: () => deleteSubject(subject.id)
  };

  showConfirmModal.value = true;
};

const deleteSubject = async (subjectId) => {
  try {
    await axios.delete(
      `/admin/delete-subject/${subjectId}`,
      authHeaders.value
    );

    // Remove subject and related chapters/quizzes from local data
    subjects.value = subjects.value.filter(subject => subject.id !== subjectId);

    const subjectChapterIds = chapters.value
      .filter(chapter => chapter.subject_id === subjectId)
      .map(chapter => chapter.id);

    chapters.value = chapters.value.filter(chapter => chapter.subject_id !== subjectId);
    allQuizzes.value = allQuizzes.value.filter(quiz => !subjectChapterIds.includes(quiz.chapter_id));

    updateStats();
    closeConfirmModal();
  } catch (error) {
    console.error(`Error deleting subject ${subjectId}:`, error);
  }
};

// Chapter functions
const toggleChapters = (subjectId) => {
  expandedSubject.value = expandedSubject.value === subjectId ? null : subjectId;
};

const openChapterModal = (subjectId, chapter = null) => {
  if (chapter) {
    chapterForm.value = { ...chapter };
    editingChapter.value = true;
  } else {
    chapterForm.value = { name: '', description: '', subject_id: subjectId };
    editingChapter.value = false;
  }

  showChapterModal.value = true;
};

const closeChapterModal = () => {
  showChapterModal.value = false;
};

const saveChapter = async () => {
  try {
    if (editingChapter.value) {
      // Update existing chapter
      await axios.put(
        `/admin/update-chapter/${chapterForm.value.id}`,
        chapterForm.value,
        authHeaders.value
      );

      // Update local data
      const index = chapters.value.findIndex(c => c.id === chapterForm.value.id);
      if (index !== -1) {
        chapters.value[index] = { ...chapterForm.value };
      }
    } else {
      // Create new chapter
      const response = await axios.post(
        '/admin/create-chapter',
        chapterForm.value,
        authHeaders.value
      );

      // Add to local data
      chapters.value.push(response.data);
    }

    updateStats();
    closeChapterModal();
    fetchSubjects();
  } catch (error) {
    console.error('Error saving chapter:', error);
  }
};

const confirmDeleteChapter = (chapter) => {
  confirmData.value = {
    title: 'Delete Chapter',
    message: `Are you sure you want to delete the chapter "${chapter.name}"? This will also delete all related quizzes.`,
    action: () => deleteChapter(chapter.id)
  };

  showConfirmModal.value = true;
};

const deleteChapter = async (chapterId) => {
  try {
    await axios.delete(
      `/admin/delete-chapter/${chapterId}`,
      authHeaders.value
    );

    // Remove chapter and related quizzes from local data
    chapters.value = chapters.value.filter(chapter => chapter.id !== chapterId);
    allQuizzes.value = allQuizzes.value.filter(quiz => quiz.chapter_id !== chapterId);

    updateStats();
    closeConfirmModal();
  } catch (error) {
    console.error(`Error deleting chapter ${chapterId}:`, error);
  }
};

// Quiz functions
const toggleQuizzes = (chapterId) => {
  expandedChapter.value = expandedChapter.value === chapterId ? null : chapterId;
};

const openQuizModal = (chapterId, quiz = null) => {
  if (quiz) {
    quizForm.value = { ...quiz };
    editingQuiz.value = true;
  } else {
    quizForm.value = { title: '', chapter_id: chapterId };
    editingQuiz.value = false;
  }

  showQuizModal.value = true;
};

const closeQuizModal = () => {
  showQuizModal.value = false;
};

const saveQuiz = async () => {
  try {
    if (editingQuiz.value) {
      // Update existing quiz
      await axios.put(
        `/admin/update-quiz/${quizForm.value.id}`,
        quizForm.value,
        authHeaders.value
      );

      // Update local data
      const index = allQuizzes.value.findIndex(q => q.id === quizForm.value.id);
      if (index !== -1) {
        allQuizzes.value[index] = { ...allQuizzes.value[index], ...quizForm.value };
      }
    } else {
      // Create new quiz
      const response = await axios.post(
        '/admin/create-quiz',
        quizForm.value,
        authHeaders.value
      );
      console.log(response.data)
      // Add to local data
      allQuizzes.value.push(response.data);
    }

    updateStats();
    fetchSubjects();
    fetchQuizzes();
    closeQuizModal();
  } catch (error) {
    console.error('Error saving quiz:', error);
  }
};

const confirmDeleteQuiz = (quiz) => {
  confirmData.value = {
    title: 'Delete Quiz',
    message: `Are you sure you want to delete the quiz "${quiz.title}"?`,
    action: () => deleteQuiz(quiz.id)
  };

  showConfirmModal.value = true;
};

const deleteQuiz = async (quizId) => {
  try {
    await axios.delete(
      `/admin/delete-quiz/${quizId}`,
      authHeaders.value
    );

    // Remove quiz from local data
    allQuizzes.value = allQuizzes.value.filter(quiz => quiz.id !== quizId);

    updateStats();
    closeConfirmModal();
  } catch (error) {
    console.error(`Error deleting quiz ${quizId}:`, error);
  }
};

// Quiz Schedule functions
const openQuizScheduleModal = (quiz) => {
  const quizDate = quiz.date ? new Date(quiz.date) : new Date();

  scheduleQuizForm.value = {
    id: quiz.id,
    title: quiz.title,
    date: quizDate.toISOString().split('T')[0],
    time: quiz.time || '09:00',
    hours: quiz.duration ? Math.floor(quiz.duration / 60) : 1,
    minutes: quiz.duration ? quiz.duration % 60 : 30
  };

  showQuizScheduleModal.value = true;
};

const closeQuizScheduleModal = () => {
  showQuizScheduleModal.value = false;
};

const saveQuizSchedule = async () => {
  try {
    // Format the data for API
    const formData = {
      id: scheduleQuizForm.value.id,
      date: scheduleQuizForm.value.date,
      time: scheduleQuizForm.value.time,
      duration: (parseInt(scheduleQuizForm.value.hours) * 60) + parseInt(scheduleQuizForm.value.minutes)
    };

    // Send to API
    await axios.put(
      `/admin/schedule-quiz/${formData.id}`,
      formData,
      authHeaders.value
    );

    // Update local data
    const index = allQuizzes.value.findIndex(q => q.id === formData.id);
    if (index !== -1) {
      allQuizzes.value[index] = {
        ...allQuizzes.value[index],
        date: formData.date,
        time: formData.time,
        duration: formData.duration
      };
    }

    closeQuizScheduleModal();
  } catch (error) {
    console.error('Error scheduling quiz:', error);
  }
};

// Question Manager functions
const openQuestionManager = async (quiz) => {
  activeQuiz.value = quiz;
  activeQuestionIndex.value = null;

  try {
    // Fetch questions for this quiz
    const response = await axios.get(
      `/admin/get-questions/${quiz.id}`,
      authHeaders.value
    );

    questions.value = response.data.map(q => ({
      ...q,
      options: q.options || ['', ''],
      correctOption: q.correctOption || 0
    }));

    showQuestionManager.value = true;
  } catch (error) {
    console.error(`Error fetching questions for quiz ${quiz.id}:`, error);
    // Initialize with empty questions array if fetch fails
    questions.value = [];
    showQuestionManager.value = true;
  }
};

const closeQuestionManager = () => {
  showQuestionManager.value = false;
  activeQuiz.value = null;
  questions.value = [];
  activeQuestionIndex.value = null;
};

const setActiveQuestion = (index) => {
  activeQuestionIndex.value = index;
};

const addNewQuestion = () => {
  questions.value.push({
    text: '',
    options: ['', ''],
    correctOption: 0,
    quiz_id: activeQuiz.value.id
  });

  // Set the new question as active
  activeQuestionIndex.value = questions.value.length - 1;
};

const addOption = () => {
  if (activeQuestionIndex.value !== null) {
    questions.value[activeQuestionIndex.value].options.push('');
  }
};

const removeOption = (optionIndex) => {
  if (activeQuestionIndex.value !== null) {
    const question = questions.value[activeQuestionIndex.value];

    // Update correctOption if we're removing the currently selected correct option
    if (question.correctOption === optionIndex) {
      question.correctOption = 0;
    } else if (question.correctOption > optionIndex) {
      // Decrement correctOption if it's after the removed option
      question.correctOption--;
    }

    question.options.splice(optionIndex, 1);
  }
};

const setCorrectOption = (optionIndex) => {
  if (activeQuestionIndex.value !== null) {
    questions.value[activeQuestionIndex.value].correctOption = optionIndex;
  }
};

const removeQuestion = async (questionId, index) => {
  try {
    await axios.delete(
      `/admin/delete-question/${questionId}`,
      authHeaders.value
    );

    // Remove question from the local state
    questions.value.splice(index, 1);

    // Adjust active question index
    if (questions.value.length === 0) {
      activeQuestionIndex.value = null;
    } else if (activeQuestionIndex.value >= questions.value.length) {
      activeQuestionIndex.value = questions.value.length - 1;
    }

    console.log("Question deleted successfully!");
  } catch (error) {
    console.error("Error deleting question:", error);
  }
};

const saveQuestions = async () => {
  try {
    // Format questions for API
    const questionData = questions.value.map(q => ({
      id: q.id,
      text: q.text,
      options: q.options,
      correct_option: q.correctOption,  // Ensure correct field name for backend
      quiz_id: activeQuiz.value.id
    }));

    // Send to API
    await axios.post(
      `/admin/save-questions/${activeQuiz.value.id}`,
      questionData,
      authHeaders.value
    );

    // Update quiz question count in local data
    const index = allQuizzes.value.findIndex(q => q.id === activeQuiz.value.id);
    if (index !== -1) {
      allQuizzes.value[index].questionCount = questions.value.length;
    }
    closeQuestionManager();
    console.log("Questions saved successfully");
  } catch (error) {
    console.error("Error saving questions:", error);
  }
};


const truncateText = (text, maxLength) => {
  if (!text) return '';
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

// Confirmation modal
const closeConfirmModal = () => {
  showConfirmModal.value = false;
};

// Search handling
const handleSearch = () => {
  // This is just a placeholder for any additional search logic
  // Filtering is handled by computed properties
};

const subjectParticipationGraph = ref('')
const userGrowthGraph = ref('')
const performanceGraph = ref('')

// Fetch graph data
const fetchGraphs = async () => {
  try {
    // Fetch subject participation graph
    const subjectResponse = await axios.get('/admin/subject-participation-graph', authHeaders.value)
    subjectParticipationGraph.value = subjectResponse.data.graph

    // Fetch user growth graph
    const userGrowthResponse = await axios.get('/admin/user-growth-graph', authHeaders.value)
    userGrowthGraph.value = userGrowthResponse.data.graph

    // Fetch performance graph
    const performanceResponse = await axios.get('/admin/performance-graph', authHeaders.value)
    performanceGraph.value = performanceResponse.data.graph
  } catch (error) {
    console.error('Error fetching analytics graphs:', error)
  }
}


</script>

<style>
/* Base Styles */
:root {
  --primary-color: #4a6cf7;
  --primary-hover: #3a5ce4;
  --danger-color: #e53e3e;
  --danger-hover: #c53030;
  --success-color: #48bb78;
  --warning-color: #f6ad55;
  --text-color: #2d3748;
  --text-light: #4a5568;
  --text-lighter: #718096;
  --bg-color: #f9fafb;
  --bg-light: #f1f5f9;
  --border-color: #e2e8f0;
  --card-bg: #ffffff;
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --border-radius: 8px;
  --transition: all 0.3s ease;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  line-height: 1.5;
  margin: 0;
  padding: 0;
}

/* Admin Dashboard Layout */
.admin-dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.dashboard-header {
  background-color: var(--card-bg);
  border-bottom: 1px solid var(--border-color);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.dashboard-welcome h1 {
  font-size: 1.5rem;
  margin: 0;
  color: var(--text-color);
}

.dashboard-welcome p {
  color: var(--text-lighter);
  margin: 0.25rem 0 0;
}

.dashboard-actions {
  display: flex;
  align-items: center;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: var(--bg-light);
  border-radius: 6px;
  padding: 0.5rem 1rem;
  width: 300px;
}

.search-bar i {
  color: var(--text-lighter);
  margin-right: 0.5rem;
}

.search-bar input {
  border: none;
  background: transparent;
  width: 100%;
  outline: none;
  color: var(--text-color);
}

/* Dashboard Stats */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem 2rem;
  background-color: var(--bg-light);
}

.stat-card {
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 1.25rem;
  display: flex;
  align-items: center;
  box-shadow: var(--shadow);
  transition: var(--transition);
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  background-color: rgba(74, 108, 247, 0.1);
  color: var(--primary-color);
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
}

.stat-icon i {
  font-size: 1.5rem;
}

.stat-details {
  display: flex;
  flex-direction: column;
}

.stat-count {
  font-size: 1.5rem;
  font-weight: 600;
}

.stat-name {
  color: var(--text-lighter);
  font-size: 0.875rem;
}

/* Dashboard Content */
.dashboard-content {
  display: flex;
  flex: 1;
  margin: 0 2rem 2rem;
}

.dashboard-sidebar {
  width: 240px;
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  margin-right: 1.5rem;
  margin-top: 1.5rem;
}

.sidebar-nav {
  list-style: none;
  padding: 1rem 0;
  margin: 0;
}

.sidebar-nav li {
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  color: var(--text-light);
  cursor: pointer;
  transition: var(--transition);
}

.sidebar-nav li:hover {
  background-color: var(--bg-light);
  color: var(--primary-color);
}

.sidebar-nav li.active {
  background-color: rgba(74, 108, 247, 0.1);
  color: var(--primary-color);
  font-weight: 500;
  position: relative;
}

.sidebar-nav li.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: var(--primary-color);
}

.sidebar-nav li i {
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

.main-content {
  flex: 1;
  margin-top: 1.5rem;
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  overflow: hidden;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.content-header h2 {
  margin: 0;
  font-size: 1.25rem;
}

/* Button Styles */
.action-button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: center;
}

.action-button:hover {
  background-color: var(--primary-hover);
}

.action-button i {
  margin-right: 0.5rem;
}

.action-button.small {
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
}

.action-button.delete {
  background-color: var(--danger-color);
}

.action-button.delete:hover {
  background-color: var(--danger-hover);
}

.secondary-button {
  background-color: transparent;
  color: var(--text-light);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: center;
}

.secondary-button:hover {
  background-color: var(--bg-light);
  border-color: var(--text-lighter);
}

.secondary-button i {
  margin-right: 0.5rem;
}

.secondary-button.small {
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
}

.secondary-button.delete {
  color: var(--danger-color);
  border-color: var(--danger-color);
}

.secondary-button.delete:hover {
  background-color: rgba(229, 62, 62, 0.1);
}

.icon-button {
  background-color: transparent;
  color: var(--text-light);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
}

.icon-button:hover {
  background-color: var(--bg-light);
  color: var(--primary-color);
}

.icon-button.delete {
  color: var(--danger-color);
}

.icon-button.delete:hover {
  background-color: rgba(229, 62, 62, 0.1);
}

/* Filter and Selection Styles */
.filter-actions {
  display: flex;
  align-items: center;
}

.select-container {
  position: relative;
  margin-left: 0.5rem;
}

.select-container select {
  appearance: none;
  background-color: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 0.5rem 2rem 0.5rem 1rem;
  font-size: 0.875rem;
  color: var(--text-color);
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='%234a5568' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: calc(100% - 8px) center;
}

/* Subject Management Styles */
.subjects-container {
  margin-top: 1rem;
}

.empty-state {
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
  padding: 2rem;
  text-align: center;
  color: var(--text-lighter);
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state.small {
  padding: 1rem;
}

.empty-state.smaller {
  padding: 0.75rem;
  font-size: 0.875rem;
}

.subject-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.subject-card {
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 1.25rem;
  box-shadow: var(--shadow);
  transition: var(--transition);
}

.subject-card:hover {
  box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.subject-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.subject-card-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.subject-description {
  color: var(--text-light);
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.subject-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.75rem;
  color: var(--text-lighter);
}

.subject-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

/* Chapters Styles */
.chapters-list {
  margin-top: 1rem;
  border-top: 1px solid var(--border-color);
  padding-top: 1rem;
}

.chapter-accordion {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.chapter-item {
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
  padding: 0.75rem;
}

.chapter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chapter-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chapter-title h4 {
  margin: 0;
  font-size: 1rem;
}

.chapter-actions {
  display: flex;
  gap: 0.25rem;
}

.chapter-description {
  color: var(--text-light);
  font-size: 0.8125rem;
  margin: 0.5rem 0;
}

/* Quizzes Styles */
.quizzes-list {
  margin-top: 0.75rem;
  border-top: 1px dashed var(--border-color);
  padding-top: 0.75rem;
  margin-left: 0.5rem;
}

.quiz-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.quiz-list-header h5 {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-light);
}

.quiz-items {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.quiz-item {
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border-color);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quiz-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8125rem;
}

.quiz-actions {
  display: flex;
  gap: 0.25rem;
}

/* Quiz Table Styles */
.quiz-table-container {
  overflow-x: auto;
}

.quiz-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
}

.quiz-table th,
.quiz-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.quiz-table th {
  background-color: var(--bg-light);
  font-weight: 500;
  color: var(--text-light);
  font-size: 0.875rem;
}

.quiz-table tr:hover {
  background-color: var(--bg-light);
}

.quiz-table tr:last-child td {
  border-bottom: none;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

/* Analytics Styles */
.analytics-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.chart-container {
  background-color: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  overflow: hidden;
}

.chart-container.large {
  height: 300px;
}

.chart-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.chart-header h3 {
  margin: 0;
  font-size: 1rem;
  color: var(--text-color);
}

.chart-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  background-color: var(--bg-light);
}

.chart-message {
  text-align: center;
  color: var(--text-lighter);
}

.chart-message i {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

/* User Management Styles */
.users-container {
  margin-top: 1rem;
}

.users-table-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
}

.placeholder-message {
  text-align: center;
  color: var(--text-lighter);
  padding: 2rem;
}

.placeholder-message i {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.placeholder-details {
  font-size: 0.875rem;
  opacity: 0.7;
  margin-top: 0.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background-color: var(--card-bg);
  border-radius: var(--border-radius);
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 5px 10px -5px rgba(0, 0, 0, 0.05);
  z-index: 101;
  /* These are the key properties you need to ensure centering */
  margin: 0 auto;
  position: relative;
}

.modal-overlay.large {
  background-color: rgba(0, 0, 0, 0.7);
}

.modal.large {
  width: 800px;
}

.modal.small {
  width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.close-button {
  background: transparent;
  border: none;
  color: var(--text-lighter);
  cursor: pointer;
  font-size: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  transition: var(--transition);
}

.close-button:hover {
  background-color: var(--bg-light);
  color: var(--text-color);
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

/* Form Styles */
.form-group {
  margin-bottom: 1.25rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  color: var(--text-color);
}

.form-group input[type="text"],
.form-group input[type="date"],
.form-group input[type="time"],
.form-group input[type="number"],
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 0.875rem;
  color: var(--text-color);
  background-color: var(--card-bg);
  transition: var(--transition);
}

.form-group input[type="text"]:focus,
.form-group input[type="date"]:focus,
.form-group input[type="time"]:focus,
.form-group input[type="number"]:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 2px rgba(74, 108, 247, 0.2);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.duration-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.duration-inputs input {
  width: 80px;
}

/* Question Manager Styles */
.question-manager {
  display: flex;
  gap: 1.5rem;
  max-height: 500px;
  overflow: hidden;
}

.question-manager-sidebar {
  width: 240px;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border-color);
  padding-right: 1rem;
}

.action-bar {
  margin-bottom: 1rem;
}

.question-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.question-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  transition: var(--transition);
  gap: 0.75rem;
}

.question-item:hover {
  background-color: var(--bg-light);
}

.question-item.active {
  background-color: var(--primary-color);
  color: white;
}

.question-number {
  font-weight: 600;
  font-size: 0.75rem;
  width: 24px;
}

.question-preview {
  font-size: 0.875rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.empty-question-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 2rem 0;
  color: var(--text-lighter);
  text-align: center;
  font-size: 0.875rem;
}

.question-editor {
  flex: 1;
  overflow-y: auto;
  padding-left: 1rem;
}

.question-editor-placeholder {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-light);
  border-radius: var(--border-radius);
}

.placeholder-content {
  text-align: center;
  color: var(--text-lighter);
}

.placeholder-content i {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.option-row {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
  gap: 0.75rem;
}

.option-radio {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 80px;
}

.option-input {
  flex: 1;
}

.question-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

/* Responsive Adjustments */
@media (max-width: 1024px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .charts-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-content {
    flex-direction: column;
    margin: 0 1rem 1rem;
  }

  .dashboard-sidebar {
    width: 100%;
    margin-right: 0;
    margin-bottom: 1rem;
  }

  .stats-cards {
    padding: 1rem;
  }

  .sidebar-nav {
    display: flex;
    overflow-x: auto;
    padding: 0.5rem;
  }

  .sidebar-nav li {
    padding: 0.5rem 1rem;
    white-space: nowrap;
  }

  .sidebar-nav li.active::before {
    width: 100%;
    height: 4px;
    top: auto;
    bottom: 0;
    left: 0;
    right: 0;
  }

  .question-manager {
    flex-direction: column;
    max-height: none;
  }

  .question-manager-sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--border-color);
    padding-right: 0;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
  }

  .question-list {
    max-height: 200px;
  }

  .question-editor {
    padding-left: 0;
  }
}




@media (max-width: 576px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
  }

  .search-bar {
    width: 100%;
  }

  .content-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .stats-cards {
    grid-template-columns: 1fr;
  }

  .subject-cards {
    grid-template-columns: 1fr;
  }

  .duration-inputs {
    flex-direction: column;
    align-items: flex-start;
  }

  .duration-inputs input {
    width: 100%;
  }
}

.analytics-dashboard {
  padding: 20px;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 30px;
}

.analytics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.graph-container {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.graph-image {
  max-width: 100%;
  height: auto;
  object-fit: contain;
}

</style>