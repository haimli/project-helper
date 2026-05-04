import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/project/:id',
      name: 'project',
      component: () => import('../views/ProjectView.vue'),
      props: true,
    },
    {
      path: '/chat/:projectId',
      name: 'chat',
      component: () => import('../views/ChatView.vue'),
      props: true,
    },
  ],
})

export default router
