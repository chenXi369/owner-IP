<template>
  <div class="messages-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>留言列表</span>
          <el-button type="danger" size="small" @click="handleClear">清空已读</el-button>
        </div>
      </template>
      
      <el-table :data="messages" stripe v-loading="loading">
        <el-table-column type="index" width="60" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="message" label="内容" show-overflow-tooltip />
        <el-table-column prop="is_read" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_read ? 'info' : 'danger'">
              {{ row.is_read ? '已读' : '未读' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleRead(row)">标记已读</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMessages, deleteMessage, markMessageRead } from '../api/messages'

const loading = ref(false)
const messages = ref([])

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

const loadData = async () => {
  loading.value = true
  try {
    const data = await getMessages()
    messages.value = data || []
  } catch (error) {
    console.error('加载失败:', error)
  } finally {
    loading.value = false
  }
}

const handleRead = async (row) => {
  try {
    await markMessageRead(row.id)
    row.is_read = true
    ElMessage.success('已标记为已读')
  } catch (error) {
    console.error('操作失败:', error)
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该留言吗？', '提示', { type: 'warning' })
    await deleteMessage(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch {
    // 取消删除
  }
}

const handleClear = () => {
  messages.value = messages.value.filter(m => !m.is_read)
  ElMessage.success('已清空已读留言')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped lang="scss">
@use '../styles/variables.scss' as *;

.messages-page {
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
