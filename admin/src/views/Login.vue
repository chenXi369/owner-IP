<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2 class="login-title">{{ isRegister ? '注册账号' : '简历管理系统' }}</h2>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef">
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
            style="width: 100%"
            :loading="loading"
            @click="handleSubmit"
          >
            {{ isRegister ? '注册' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
      <div class="login-tips">
        <p v-if="!isRegister">
          还没有账号？
          <el-button type="primary" link @click="toggleMode">立即注册</el-button>
        </p>
        <p v-else>
          已有账号？
          <el-button type="primary" link @click="toggleMode">去登录</el-button>
        </p>
        <p v-if="!isRegister" style="margin-top: 8px; color: #909399; font-size: 12px">
          演示账号: admin / admin123
        </p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message, Phone, UserFilled } from '@element-plus/icons-vue'
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
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 420px;
  background: rgba(30, 41, 59, 0.95);
  border: 1px solid $border-color;
  border-radius: $border-radius-lg;
  box-shadow: $shadow-lg;
  color: $text-primary;

  :deep(.el-card__header) {
    border-bottom: 1px solid $border-color;
    padding: 20px 24px;
  }

  :deep(.el-card__body) {
    padding: 24px;
  }

  :deep(.el-input__wrapper) {
    background: $bg-primary;
    box-shadow: 0 0 0 1px $border-color inset;

    &.is-focus {
      box-shadow: 0 0 0 1px $primary inset;
    }

    input {
      color: $text-primary;

      &::placeholder {
        color: $text-muted;
      }
    }
  }
}

.login-title {
  text-align: center;
  margin: 0;
  font-size: 24px;
  color: $text-primary;
}

.login-tips {
  text-align: center;
  margin-top: 16px;
}

.login-tips p {
  margin: 0;
  color: $text-secondary;
  font-size: 14px;
}
</style>
