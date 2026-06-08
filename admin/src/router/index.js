import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('../views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: '数据概览', icon: 'Odometer' }
      },
      {
        path: 'resume',
        name: 'Resume',
        component: () => import('../views/Resume.vue'),
        meta: { title: '简历管理', icon: 'Document' }
      },
      {
        path: 'skills',
        name: 'Skills',
        component: () => import('../views/Skills.vue'),
        meta: { title: '技能管理', icon: 'Star' }
      },
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('../views/Projects.vue'),
        meta: { title: '项目管理', icon: 'Folder' }
      },
      {
        path: 'experiences',
        name: 'Experiences',
        component: () => import('../views/Experiences.vue'),
        meta: { title: '工作经历', icon: 'OfficeBuilding' }
      },
      {
        path: 'educations',
        name: 'Educations',
        component: () => import('../views/Educations.vue'),
        meta: { title: '教育背景', icon: 'School' }
      },
      {
        path: 'contacts',
        name: 'Contacts',
        component: () => import('../views/Contacts.vue'),
        meta: { title: '联系方式', icon: 'Phone' }
      },
      {
        path: 'messages',
        name: 'Messages',
        component: () => import('../views/Messages.vue'),
        meta: { title: '留言管理', icon: 'Message' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/Users.vue'),
        meta: { title: '用户管理', icon: 'UserFilled', adminOnly: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (!to.meta.public && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && userStore.isLoggedIn) {
    next('/')
  } else if (to.meta.adminOnly && !userStore.isAdmin) {
    next('/')
  } else {
    next()
  }
})

export default router
