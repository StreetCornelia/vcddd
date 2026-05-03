# 棕地项目初始化（Brownfield Init）

对已有代码但未使用 VCDDD 文档结构的项目，进行代码认知分析，生成**给大模型使用的架构知识库文档**。

## 核心目标

不改变原有代码结构。而是分析现有代码，将其业务含义、入口点、流程逻辑整理成文档，让大模型在后续工作中能理解项目全局，不需要重写已有功能。

**这些文档不是 VCDDD 域设计文档**，而是对现有代码的业务理解记录。大模型读这些文档来"认识"项目，而非设计项目。

---

## 触发方式

### 手动触发

用户通过以下指令手动调用：

- `启动棕地初始化` / `brownfield init`
- `分析项目结构` / `生成代码认知文档`
- `更新项目认知` / `重新扫描项目`

### 自动触发

编排者检测到以下条件时，自动提示用户：

```
项目目录有源代码，但 docs/vcddd/brownfield/ 目录不存在或内容可能过期
  → "检测到项目已有代码但缺少架构认知文档，是否运行棕地初始化？
     这将分析代码结构，生成供大模型参考的业务模块文档。"
```

---

## 棕地初始化的三步流程

```
Step 1: 项目级扫描
  技术栈 → 目录结构 → 入口点 → 配置文件
        │
        ▼
Step 2: 模块级分析
  每个模块：入口点 → 业务功能 → 核心逻辑 → 依赖关系
        │
        ▼
Step 3: 输出认知文档
  写入 docs/vcddd/brownfield/，供大模型后续参考
```

---

## Step 1: 项目级扫描

### 1.1 技术栈与配置

扫描配置文件，记录项目的基础技术信息：

```
语言         → package.json / pyproject.toml / go.mod / Cargo.toml
框架         → 路由框架、ORM、测试框架
数据库       → 连接配置、迁移工具
构建/运行    → build 命令、启动命令、环境变量
```

输出到 `docs/vcddd/brownfield/tech.md`。

### 1.2 目录结构总览

扫描顶层和二级目录，记录结构：

```
project/
├── src/或app/或server/
│   ├── controllers/    ← 入口层
│   ├── services/       ← 业务逻辑层
│   ├── models/         ← 数据模型层
│   └── middleware/     ← 中间件
├── config/
├── tests/
└── ...
```

对每一层记录：存放什么类型的代码、职责是什么。

输出到 `docs/vcddd/brownfield/structure.md`。

### 1.3 入口点清单

扫描路由定义、API 端点、CLI 命令、消息队列消费者等入口，建立完整入口清单：

```
API 端点：
  POST /api/orders          → orderController.create
  GET  /api/orders/:id      → orderController.getById
  POST /api/payments        → paymentController.process

后台任务：
  src/jobs/expireOrders.js  → 每分钟运行，超时未支付订单取消

消息消费者：
  src/consumers/paymentResult.js → 消费 payment.completed 事件
```

每个入口标注：HTTP 方法/触发方式、路径、对应代码位置、简要职责。

输出到 `docs/vcddd/brownfield/endpoints.md`。

---

## Step 2: 模块级分析

### 2.1 模块识别

根据代码实际组织方式（按目录或按功能聚类）识别模块：

```
识别依据：
  - 独立目录：src/orders/、src/payments/
  - 独立命名空间：Services.OrderService、Services.PaymentService
  - 功能聚类：所有与"订单"相关的文件聚集在一起
  
输出候选模块列表，向用户确认后进入后续分析。
```

### 2.2 对每个模块的分析

按以下模板分析每个模块：

```markdown
# 模块：{模块名}

## 位置
{代码目录路径，如 src/services/orderService.js}

## 业务职责
{用一两句话说明这个模块在业务中的角色}

## 入口点
{这个模块被调用的方式，列出每个入口：
  - 被哪个 API 端点/后台任务/消费者触发
  - 调用代码位置
  - 入参和出参的关键信息}

## 核心逻辑
{模块内的关键业务流程描述，不是代码逐行翻译，而是业务逻辑的归纳。
 例如："创建订单时先验证库存，然后扣减预占，最后发布订单创建事件"}
  - 关键的判断分支（if-else / switch）
  - 重要的数据处理步骤
  - 调用外部服务/模块的地方

## 关键数据结构
{这个模块操作的核心数据对象/模型，字段含义}

## 依赖关系
{依赖了哪些其他模块 → 标注依赖方向}
{被哪些其他模块依赖 → 标注依赖方向}

## 注意事项
{代码中不直观但重要的行为，如：
  - 幂等处理方式
  - 重试策略
  - 补偿/回滚机制
  - 超时处理}
```

每个模块输出一个文件到 `docs/vcddd/brownfield/modules/{module}.md`。

### 2.3 关键业务数据流

从入口点到多个模块的调用链，梳理完整业务数据流：

```markdown
## 业务流：下单支付

用户下单 (POST /api/orders)
  → orderController.create
    → OrderService.createOrder
      → 验证商品库存 (调用 InventoryService.checkStock)
      → 创建订单记录 (写入 orders 表)
      → 扣减库存预占 (调用 InventoryService.reserve)
      → 发布事件 order.created
  → 返回订单 ID

支付回调 (消费者 payment.completed)
  → PaymentResultConsumer.handle
    → OrderService.confirmPayment
      → 更新订单状态 (orders 表)
      → 发布事件 order.paymentConfirmed
  → ...
```

每个业务流标注：触发入口、经过的模块、关键状态变更、产生的事件/数据。

输出到 `docs/vcddd/brownfield/data-flows.md`。

---

## Step 3: 输出摘要

所有文档生成完成后，向用户呈现：

```
## 棕地初始化完成

### 文档位置
docs/vcddd/brownfield/
├── tech.md         ← 技术栈与配置
├── structure.md    ← 目录结构与职责
├── endpoints.md    ← 入口点清单
├── data-flows.md   ← 关键业务数据流
└── modules/
    ├── order.md      ← 订单模块
    ├── payment.md    ← 支付模块
    └── inventory.md  ← 库存模块

### 使用方式

大模型在接手此项目时，先读取 docs/vcddd/brownfield/ 下的文件，
即可理解项目整体架构、各模块业务职责和关键数据流，
无需从零遍历代码。

### 注意事项

- 本文档基于代码分析生成，reflects 代码实际行为而非业务意图
- 业务含义标注有推测成分，关键判断仍以代码为准
- 代码更新后需要重新运行棕地初始化以同步文档
```

---

## 关键规则

1. **不修改原有代码**：分析只读不写，不插入注释、不改写代码结构
2. **不产生 VCDDD 域文档**：不生成 boundary.md / business.md / implementation.md，这些是设计文档，不是认知文档
3. **不可靠推断需标注**：代码本身无法确认的业务意图，标注为 `[推测]`
4. **入口点必须精确**：入口点的代码位置必须精确到文件名和函数名，不做模糊描述
5. **业务逻辑归纳而非翻译**：不是逐行注释代码，而是归纳出业务层面的流程
