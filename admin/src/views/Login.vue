<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-circle circle-1"></div>
      <div class="bg-circle circle-2"></div>
      <div class="bg-circle circle-3"></div>
      <div class="bg-grid"></div>
    </div>

    <!-- 左侧品牌区域 -->
    <div class="brand-section">
      <div class="brand-content">
        <div class="brand-logo">
          <el-icon size="48" color="#fff"><Document /></el-icon>
        </div>
        <h1 class="brand-title">简历管理系统</h1>
        <p class="brand-desc">智能化简历管理，高效便捷的数据维护</p>
        <div class="feature-list">
          <div class="feature-item">
            <el-icon size="18" color="#818cf8"><CircleCheck /></el-icon>
            <span>多维度数据概览</span>
          </div>
          <div class="feature-item">
            <el-icon size="18" color="#818cf8"><CircleCheck /></el-icon>
            <span>技能与项目管理</span>
          </div>
          <div class="feature-item">
            <el-icon size="18" color="#818cf8"><CircleCheck /></el-icon>
            <span>实时留言互动</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧登录表单 -->
    <div class="form-section">
      <div class="login-card-wrapper">
        <div class="login-card-glass">
          <h2 class="login-title">{{ isRegister ? '注册账号' : '欢迎回来' }}</h2>
          <p class="login-subtitle">{{ isRegister ? '创建您的新账号' : '请登录您的账号以继续' }}</p>

          <el-form :model="form" :rules="rules" ref="formRef" class="login-form">
            <el-form-item prop="username" v-if="isRegister">
              <el-input
                v-model="form.username"
                placeholder="用户名"
                :prefix-icon="User"
                size="large"
              />
            </el-form-item>
            <el-form-item prop="email" v-if="isRegister">
              <el-input
                v-model="form.email"
                placeholder="邮箱"
                :prefix-icon="Message"
                size="large"
              />
            </el-form-item>
            <el-form-item prop="phone" v-if="isRegister">
              <el-input
                v-model="form.phone"
                placeholder="手机号（选填）"
                :prefix-icon="Phone"
                size="large"
              />
            </el-form-item>
            <el-form-item prop="nickname" v-if="isRegister">
              <el-input
                v-model="form.nickname"
                placeholder="昵称（选填）"
                :prefix-icon="UserFilled"
                size="large"
              />
            </el-form-item>
            <el-form-item prop="username" v-if="!isRegister">
              <el-input
                v-model="form.username"
                placeholder="用户名或邮箱"
                :prefix-icon="User"
                size="large"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="密码"
                :prefix-icon="Lock"
                size="large"
                show-password
              />
            </el-form-item>
            <el-form-item prop="confirmPassword" v-if="isRegister">
              <el-input
                v-model="form.confirmPassword"
                type="password"
                placeholder="确认密码"
                :prefix-icon="Lock"
                size="large"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                size="large"
                class="submit-btn"
                :loading="loading"
                @click="handleSubmit"
              >
                {{ isRegister ? '注册' : '登录' }}
              </el-button>
            </el-form-item>
          </el-form>

          <div class="login-divider">
            <span>{{ isRegister ? '已有账号' : '还没有账号' }}</span>
          </div>

          <div class="login-toggle">
            <el-button type="primary" link @click="toggleMode">
              {{ isRegister ? '去登录' : '立即注册' }}
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部版权 -->
    <div class="login-footer">
      <span> 简历管理系统 v1.0.0</span>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message, Phone, UserFilled, Document, CircleCheck } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import { login, register } from '../api/auth'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const isRegister = ref(false)

const form = reactive({
  username: '',
  email: '',
  phone: '',
  nickname: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (isRegister.value && value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const toggleMode = () => {
  isRegister.value = !isRegister.value
  formRef.value?.resetFields()
}

const handleSubmit = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    if (isRegister.value) {
      await register({
        username: form.username,
        email: form.email,
        phone: form.phone,
        nickname: form.nickname,
        password: form.password
      })
      ElMessage.success('注册成功，请登录')
      isRegister.value = false
      form.password = ''
      form.confirmPassword = ''
    } else {
      const data = await login({
        username: form.username,
        password: form.password
      })
      userStore.setToken(data.token)
      userStore.setUserInfo(data.user)
      ElMessage.success('登录成功')
      router.push('/')
    }
  } catch (error) {
    console.error('操作失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
@use '../styles/variables.scss' as *;

.login-container {
  min-height: 100vh;
  display: flex;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.bg-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.circle-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, #6366f1 0%, transparent 70%);
  top: -200px;
  left: -100px;
  animation: float 8s ease-in-out infinite;
}

.circle-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #8b5cf6 0%, transparent 70%);
  bottom: -150px;
  right: -100px;
  animation: float 10s ease-in-out infinite reverse;
}

.circle-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #3b82f6 0%, transparent 70%);
  top: 50%;
  left: 30%;
  animation: float 12s ease-in-out infinite;
}

.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(99, 102, 241, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99, 102, 241, 0.05) 1px, transparent 1px);
  background-size: 60px 60px;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.05); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

/* 左侧品牌区域 */
.brand-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  position: relative;
  z-index: 1;
}

.brand-content {
  max-width: 480px;
}

.brand-logo {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 32px;
  box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
}

.brand-title {
  font-size: 42px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 16px;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #fff 0%, #c7d2fe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-desc {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 40px;
  line-height: 1.6;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  color: rgba(255, 255, 255, 0.8);
}

/* 右侧表单区域 */
.form-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
  position: relative;
  z-index: 1;
}

.login-card-wrapper {
  width: 100%;
  max-width: 440px;
}

.login-card-glass {
  background: rgba(30, 41, 59, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 40px;
  box-shadow:
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.05) inset;
}

.login-title {
  text-align: center;
  margin: 0 0 8px;
  font-size: 28px;
  font-weight: 700;
  color: #fff;
}

.login-subtitle {
  text-align: center;
  margin: 0 0 32px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
}

.login-form {
  :deep(.el-form-item) {
    margin-bottom: 20px;

    &:last-child {
      margin-bottom: 0;
      margin-top: 8px;
    }
  }

  :deep(.el-input__wrapper) {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: none;
    border-radius: 12px;
    padding: 4px 16px;
    transition: all 0.3s ease;

    &:hover {
      border-color: rgba(99, 102, 241, 0.4);
    }

    &.is-focus {
      border-color: #6366f1;
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
    }

    input {
      color: #fff;
      font-size: 15px;
      height: 44px;

      &::placeholder {
        color: rgba(255, 255, 255, 0.35);
      }
    }

    .el-input__icon {
      color: rgba(255, 255, 255, 0.4);
    }
  }
}

.submit-btn {
  width: 100%;
  height: 48px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
  }

  &:active {
    transform: translateY(0);
  }
}

.login-divider {
  display: flex;
  align-items: center;
  margin: 24px 0 16px;

  &::before,
  &::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255, 255, 255, 0.1);
  }

  span {
    padding: 0 16px;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.4);
  }
}

.login-toggle {
  text-align: center;

  :deep(.el-button.is-link) {
    font-size: 14px;
    color: #818cf8;
    font-weight: 500;

    &:hover {
      color: #a5b4fc;
    }
  }
}

/* 底部版权 */
.login-footer {
  position: absolute;
  bottom: 24px;
  left: 0;
  right: 0;
  text-align: center;
  z-index: 1;

  span {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
  }
}

/* 响应式 */
@media (max-width: 900px) {
  .brand-section {
    display: none;
  }

  .form-section {
    padding: 24px;
  }
}
</style>
