import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import AdminDashboard from '@/views/AdminDashboard.vue';
import UserDashboard from '@/views/UserDashboard.vue';
import Quiz from '@/views/Quiz.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/admin_dashboard', component: AdminDashboard },
  { path: '/user_dashboard', component: UserDashboard },
  {
    path: '/quiz/:id',
    name: 'QuizAttempt',
    component: Quiz,
    meta: { requiresAuth: true } // Add authentication guard if needed
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

