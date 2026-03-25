# 个人IP简历网站 - Three.js 3D视觉效果

一个具有高度视觉吸引力的个人IP简历网站，使用Nuxt.js + Three.js构建，展示丰富的3D视觉效果和交互体验。

## 技术栈

- **框架**: Nuxt.js 3.x
- **构建工具**: Vite
- **编程语言**: JavaScript (ES6+)
- **3D渲染**: Three.js
- **动画库**: GSAP
- **样式**: SCSS

## 项目结构

```
threejs简历/
├── assets/
│   └── styles/
│       ├── main.scss          # 全局样式
│       └── variables.scss     # 样式变量和混入
├── components/
│   ├── layout/
│   │   ├── Navigation.vue     # 导航组件
│   │   └── Footer.vue         # 页脚组件
│   └── three/
│       ├── StarfieldBackground.vue  # 星空背景场景
│       ├── SkillsGeometry.vue       # 技能几何体展示
│       ├── ParticleAvatar.vue       # 粒子人像
│       └── ParticleCursor.vue       # 鼠标粒子特效
├── composables/
│   ├── useThreeJS.js          # Three.js组合式函数
│   └── useAnimation.js        # 动画相关组合式函数
├── pages/
│   └── index.vue              # 主页面
├── app.vue                    # 应用入口
├── nuxt.config.js             # Nuxt配置
└── package.json               # 项目依赖

```

## 3D场景组件

### 1. 星空背景 (StarfieldBackground)
- 5000颗星星组成的星空场景
- 星云粒子效果
- 鼠标跟随视差效果
- 平滑旋转动画

### 2. 技能几何体 (SkillsGeometry)
- 6种不同几何体展示技能
- 动态旋转和浮动效果
- 悬停高亮交互
- 技能等级可视化

### 3. 粒子人像 (ParticleAvatar)
- 8000个粒子组成的人像轮廓
- 鼠标交互粒子波动
- 呼吸式动画效果
- 渐变色彩变化

### 4. 鼠标粒子特效 (ParticleCursor)
- 鼠标移动轨迹粒子
- 点击爆发效果
- 多彩粒子颜色
- 自动消失动画

## 页面模块

1. **首页英雄区**: 粒子人像 + 打字机效果
2. **关于我**: 个人介绍 + 统计数据
3. **技能展示**: 3D几何体 + 技能进度条
4. **项目作品**: 项目卡片展示
5. **工作经历**: 时间线布局
6. **教育背景**: 教育信息卡片
7. **联系方式**: 联系表单 + 信息

## 响应式设计

- 桌面端: 1280px+
- 平板端: 768px - 1279px
- 移动端: < 768px

## 性能优化

- Three.js场景按需渲染
- 粒子数量动态调整
- 组件懒加载
- 图片懒加载
- CSS动画硬件加速

## 开发命令

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 生成静态站点
npm run generate

# 预览生产版本
npm run preview
```

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## 自定义内容

请修改 `pages/index.vue` 中的以下内容:
- 个人信息 (姓名、职位、描述)
- 技能列表
- 项目作品
- 工作经历
- 教育背景
- 联系方式

## 许可证

MIT License
