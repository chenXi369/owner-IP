<template>
  <div class="users-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
        </div>
      </template>
      
      <el-table :data="users" stripe v-loading="loading" style="width: 100%">
        <el-table-column type="index" width="60" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="phone" label="手机号" min-width="120" />
        <el-table-column prop="nickname" label="昵称" min-width="120" />
        <el-table-column prop="role" label="角色" width="110" align="center">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'info'">
              {{ row.role === 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="注册时间" min-width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template #default="{ row }">
            <el-button
              v-if="!['admin', 'superadmin'].includes(row.role)"
              type="primary"
              link
              size="small"
              @click="handleToggleRole(row)"
            >
              {{ row.role === 'admin' ? '降为用户' : '设为管理员' }}
            </el-button>
            <el-button
              type="warning"
              link
              size="small"
              @click="handleToggleStatus(row)"
              v-if="!['admin', 'superadmin'].includes(row.role)"
            >
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)" v-if="!['admin', 'superadmin'].includes(row.role)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, updateUser, deleteUser } from '../api/users'

const loading = ref(false)
const users = ref([])

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

const loadData = async () => {
  loading.value = true
  try {
    const data = await getUsers()
    users.value = data || []
  } catch (error) {
    console.error('加载失败:', error)
  } finally {
    loading.value = false
  }
}

const handleToggleRole = async (row) => {
  const newRole = row.role === 'admin' ? 'user' : 'admin'
  try {
    await updateUser(row.id, { role: newRole })
    row.role = newRole
    ElMessage.success('角色更新成功')
  } catch (error) {
    console.error('更新失败:', error)
  }
}

const handleToggleStatus = async (row) => {
  const newStatus = !row.is_active
  try {
    await updateUser(row.id, { is_active: newStatus })
    row.is_active = newStatus
    ElMessage.success(newStatus ? '账号已启用' : '账号已禁用')
  } catch (error) {
    console.error('更新失败:', error)
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该用户吗？', '提示', { type: 'warning' })
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
    // 取消删除
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
@use '../styles/variables.scss' as *;

.users-page {
  padding: 24px;
  min-height: 100vh;
  background: $bg-primary;

  :deep(.el-card) {
    background: $bg-card;
    border: 1px solid $border-color;
    border-radius: $border-radius-lg;
    box-shadow: $shadow;
    color: $text-primary;

    .el-card__header {
      border-bottom: 1px solid $border-color;
      padding: 18px 24px;
      background: transparent;
    }

    .el-card__body {
      padding: 24px;
      background: transparent;
    }
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 18px;
    font-weight: 600;
    color: $text-primary;

    span {
      letter-spacing: 0.5px;
    }
  }

  :deep(.el-button) {
    border-radius: $border-radius-sm;
    font-weight: 500;
    transition: all $transition-fast;

    &.el-button--primary {
      background: $primary;
      border-color: $primary;
      color: #fff;

      &:hover {
        background: $primary-light;
        border-color: $primary-light;
        transform: translateY(-1px);
        box-shadow: $shadow-glow;
      }
    }

    &.el-button--danger {
      background: $danger;
      border-color: $danger;
      color: #fff;

      &:hover {
        background: #f87171;
        border-color: #f87171;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
      }
    }

    &.el-button--warning {
      background: $warning;
      border-color: $warning;
      color: #fff;

      &:hover {
        background: #fbbf24;
        border-color: #fbbf24;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
      }
    }

    &.el-button--default {
      background: $bg-hover;
      border-color: $border-color;
      color: $text-primary;

      &:hover {
        background: #475569;
        border-color: #475569;
        color: #fff;
      }
    }

    &.is-link {
      background: transparent;
      border: none;
      padding: 4px 8px;

      &.el-button--primary {
        color: $primary-light;

        &:hover {
          color: $primary;
          background: rgba(99, 102, 241, 0.1);
          transform: none;
          box-shadow: none;
        }
      }

      &.el-button--danger {
        color: #f87171;

        &:hover {
          color: $danger;
          background: rgba(239, 68, 68, 0.1);
          transform: none;
          box-shadow: none;
        }
      }

      &.el-button--warning {
        color: #fbbf24;

        &:hover {
          color: $warning;
          background: rgba(245, 158, 11, 0.1);
          transform: none;
          box-shadow: none;
        }
      }
    }
  }

  :deep(.el-table) {
    background: transparent;
    color: $text-primary;

    &::before {
      display: none;
    }

    .el-table__header-wrapper {
      th.el-table__cell {
        background: $bg-secondary;
        color: $text-secondary;
        font-weight: 600;
        border-bottom: 1px solid $border-color;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 14px 12px;
      }
    }

    .el-table__body-wrapper {
      td.el-table__cell {
        background: transparent;
        color: $text-primary;
        border-bottom: 1px solid $border-color;
        padding: 14px 12px;
        font-size: 14px;
      }

      tr {
        background: transparent;
        transition: background $transition-fast;

        &:hover > td.el-table__cell {
          background: $bg-hover !important;
        }

        &.el-table__row--striped {
          td.el-table__cell {
            background: rgba(30, 41, 59, 0.5);
          }

          &:hover > td.el-table__cell {
            background: $bg-hover !important;
          }
        }
      }
    }

    .el-table__empty-block {
      background: transparent;
      color: $text-muted;
    }
  }

  :deep(.el-tag) {
    border-radius: $border-radius-sm;
    font-weight: 500;
    padding: 0 10px;
    height: 28px;
    line-height: 26px;
    border: 1px solid transparent;

    &.el-tag--success {
      background: rgba(16, 185, 129, 0.15);
      border-color: rgba(16, 185, 129, 0.3);
      color: #34d399;
    }

    &.el-tag--info {
      background: rgba(148, 163, 184, 0.15);
      border-color: rgba(148, 163, 184, 0.3);
      color: $text-secondary;
    }

    &.el-tag--danger {
      background: rgba(239, 68, 68, 0.15);
      border-color: rgba(239, 68, 68, 0.3);
      color: #f87171;
    }
  }
}
</style>
