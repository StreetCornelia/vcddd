# 模板：frontend/app-architecture.md

```text
目标路径：docs/vcddd/frontend/app-architecture.md
```

# 前端基础架构

## 技术栈

- 前端框架：
- 路由方案：
- 状态管理：
- 表单/输入管理：
- 组件库：
- 调用 server/API 的方式：

## 目录与职责

| 区域 | 职责 | 禁止 |
|------|------|------|
| pages | 页面组合、路由入口、页面级状态 | 业务判断、不变式保护 |
| components | 可复用 UI 组件 | 直接调用域命令 |
| providers/controllers/view-models | 连接页面状态、读模型、命令触发 | 维护业务状态机 |
| theme | 颜色、字体、间距、组件视觉规则 | 页面专属业务规则 |

## 调用边界

- 页面通过读模型获取展示数据
- 页面通过命令表达用户意图
- 命令是否允许执行、状态如何迁移，由 `server/{domain}/` 决定

## Google Design.md 依赖

前端页面进入设计转实现阶段时，必须调用本地 `google-design-md` skill。VCDDD 不复制其方法论，只把本文件、页面文件、域文档作为输入传给它。
