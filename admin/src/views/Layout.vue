<template>
  <div class="layout-wrapper">
    <!-- 侧边栏 -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">
            <el-icon size="24"><Document /></el-icon>
          </div>
          <span v-show="!isCollapsed" class="logo-text">星辰简历</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in visibleMenuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: $route.path === item.path }"
        >
          <el-icon size="18">
            <component :is="item.icon" />
          </el-icon>
          <span v-show="!isCollapsed" class="nav-text">{{ item.title }}</span>
          <div v-show="!isCollapsed" class="nav-indicator"></div>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button class="collapse-btn" @click="isCollapsed = !isCollapsed">
          <el-icon><Fold v-if="!isCollapsed" /><Expand v-else /></el-icon>
        </button>
        <div class="version" v-show="!isCollapsed">v1.0.0</div>
      </div>
    </aside>
    
    <!-- 主内容区 -->
    <main class="main-area">
      <header class="top-header">
        <div class="breadcrumb">
          <el-icon size="16" color="#64748b"><HomeFilled /></el-icon>
          <span class="breadcrumb-sep">/</span>
          <span class="breadcrumb-current">{{ $route.meta?.title || '管理后台' }}</span>
        </div>
        <div class="header-actions">
          <div class="action-btn" title="通知">
            <el-icon size="18"><Bell /></el-icon>
            <span class="badge" v-if="unreadCount > 0">{{ unreadCount }}</span>
          </div>
          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-profile">
              <div class="avatar">
                <el-icon size="20"><User /></el-icon>
              </div>
              <div class="user-info" v-if="!isMobile">
                <div class="user-name">{{ userStore.userInfo?.nickname || userStore.userInfo?.username || '用户' }}</div>
                <div class="user-role">
                  <el-tag v-if="userStore.isSuperAdmin" size="small" type="danger" effect="dark">超级管理员</el-tag>
                  <el-tag v-else-if="userStore.isAdmin" size="small" type="warning" effect="dark">管理员</el-tag>
                  <el-tag v-else size="small" type="info">普通用户</el-tag>
                </div>
              </div>
              <el-icon class="dropdown-arrow"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon> 个人中心
                </el-dropdown-item>
                <el-dropdown-item command="password">
                  <el-icon><Lock /></el-icon> 修改密码
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon> 退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>
      
      <div class="content-wrapper">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>

    <!-- 修改密码对话框 -->
    <el-dialog v-model="passwordDialogVisible" title="修改密码" width="420px" destroy-on-close>
      <el-form :model="passwordForm" label-width="90px" :rules="passwordRules" ref="passwordFormRef">
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="passwordForm.old_password" type="password" show-password placeholder="请输入旧密码" />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="passwordForm.new_password" type="password" show-password placeholder="请输入新密码" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input v-model="passwordForm.confirm_password" type="password" show-password placeholder="请再次输入新密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleChangePassword">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Document, User, ArrowDown, Fold, Expand, HomeFilled, Bell, Lock, SwitchButton } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import { logout as logoutApi } from '../api/auth'
import { changePassword } from '../api/auth'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapsed = ref(false)
const isMobile = ref(window.innerWidth < 768)
const unreadCount = ref(0)

const menuItems = computed(() => {
  const layoutRoute = router.getRoutes().find(r => r.name === 'Layout')
  return layoutRoute?.children?.map(child => ({
    path: '/' + child.path,
    title: child.meta?.title || child.name,
    icon: child.meta?.icon || 'Document',
    adminOnly: child.meta?.adminOnly || false,
    userOnly: child.meta?.userOnly || false
  })) || []
})

const visibleMenuItems = computed(() => {
  return menuItems.value.filter(item => {
    if (item.adminOnly) return userStore.isAdmin
    if (item.userOnly) return !userStore.isAdmin
    return true
  })
})

const handleResize = () => {
  isMobile.value = window.innerWidth < 768
  if (window.innerWidth < 768) {
    isCollapsed.value = true
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  handleResize()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      try { await logoutApi() } catch {}
      userStore.logout()
      router.push('/login')
    } catch {
      // 用户取消，不做任何操作
    }
  } else if (command === 'password') {
    passwordDialogVisible.value = true
  } else if (command === 'profile') {
    router.push('/profile')
  }
}

// 修改密码
const passwordDialogVisible = ref(false)
const passwordFormRef = ref(null)
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const passwordRules = {
  old_password: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const handleChangePassword = async () => {
  const valid = await passwordFormRef.value?.validate().catch(() => false)
  if (!valid) return

  try {
    await changePassword({
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    })
    ElMessage.success('密码修改成功，请重新登录')
    passwordDialogVisible.value = false
    userStore.logout()
    router.push('/login')
  } catch (error) {
    console.error('修改密码失败:', error)
  }
}
</script>

<style scoped lang="scss">
@use '../styles/variables.scss' as *;

.layout-wrapper {
  display: flex;
  height: 100vh;
  background: $bg-primary;
}

// 侧边栏
.sidebar {
  width: 240px;
  background: $bg-secondary;
  border-right: 1px solid $border-color;
  display: flex;
  flex-direction: column;
  transition: width $transition;
  flex-shrink: 0;
  position: relative;
  z-index: 100;

  &.collapsed {
    width: 64px;

    .logo-icon {
      margin-right: 0;
    }
  }
}

.sidebar-header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid $border-color;
}

.logo {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  overflow: hidden;

  .logo-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, $primary, $primary-dark);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    flex-shrink: 0;
  }

  .logo-text {
    font-size: 18px;
    font-weight: 700;
    color: $text-primary;
    white-space: nowrap;
    letter-spacing: -0.5px;
  }
}

.sidebar-nav {
  flex: 1;
  padding: 12px 10px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: $border-radius-sm;
  color: $text-secondary;
  text-decoration: none;
  margin-bottom: 4px;
  transition: all $transition-fast;
  position: relative;
  overflow: hidden;

  .nav-text {
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
  }

  .nav-indicator {
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 0;
    background: $primary;
    border-radius: 0 3px 3px 0;
    transition: height $transition;
  }

  &:hover {
    background: rgba(99, 102, 241, 0.08);
    color: $primary-light;
  }

  &.active {
    background: rgba(99, 102, 241, 0.12);
    color: $primary-light;

    .nav-indicator {
      height: 24px;
    }
  }
}

.sidebar-footer {
  padding: 12px 16px;
  border-top: 1px solid $border-color;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;

  .collapse-btn {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: $text-muted;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all $transition-fast;

    &:hover {
      background: $bg-hover;
      color: $text-primary;
    }
  }

  .version {
    font-size: 11px;
    color: $text-muted;
    text-align: center;
  }
}

// 主内容区
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}

.top-header {
  height: 64px;
  background: $bg-secondary;
  border-bottom: 1px solid $border-color;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  flex-shrink: 0;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;

  .breadcrumb-sep {
    color: $text-muted;
  }

  .breadcrumb-current {
    color: $text-primary;
    font-weight: 600;
  }
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: $text-secondary;
  cursor: pointer;
  transition: all $transition-fast;
  position: relative;

  &:hover {
    background: $bg-hover;
    color: $text-primary;
  }

  .badge {
    position: absolute;
    top: 4px;
    right: 4px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: $danger;
    color: white;
    font-size: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: all $transition-fast;

  &:hover {
    background: $bg-hover;
  }

  .avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, $primary, $primary-dark);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }

  .user-info {
    display: flex;
    flex-direction: column;
    gap: 2px;

    .user-name {
      font-size: 13px;
      font-weight: 600;
      color: $text-primary;
    }

    .user-role {
      :deep(.el-tag) {
        border: none;
        padding: 0 6px;
        height: 18px;
        font-size: 10px;
      }
    }
  }

  .dropdown-arrow {
    color: $text-muted;
    font-size: 12px;
  }
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

// 移动端适配
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    transform: translateX(-100%);

    &.collapsed {
      transform: translateX(0);
    }
  }
}
</style>
