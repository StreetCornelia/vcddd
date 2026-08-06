# 提交规范

## 提交流程

- 提交目标分支固定为 `develop/2.x`。
- 使用 `just commit "<message>"` 创建提交，不要直接调用 `git commit`。
- 如果当前不在 `develop/2.x`，提交命令会暂存当前改动、切换到目标分支、恢复改动，然后在目标分支上提交。
- 提交命令会执行 `git add --all`，因此执行前必须确认工作区中没有不应提交的改动。
- `message` 是必填参数，不能为空或只包含空白字符。
- 提交只写入本地 Git 仓库，不会自动执行 `git push`。

## Commit message 格式

使用 `<type>: <summary>` 格式，`summary` 简洁描述本次改动，建议使用祈使语气。常用的 `type` 包括：

- `feat`：新增功能
- `fix`：修复问题
- `docs`：文档或说明变更
- `refactor`：重构，不改变外部行为
- `test`：测试相关变更
- `chore`：工具、配置或其他维护性变更

示例：

```bash
just commit "docs: update submission guidelines"
```

## 推送规范

- 使用 `just push` 执行推送流程，不要手动跳过分支同步步骤。
- 推送前必须保证工作区干净，且本地提交已经完成。
- `just push` 会先推送 `develop/2.x`，再切换到 `main` 合并 `develop/2.x` 并推送 `main`，完成后回到 `develop/2.x`。
- 推送或合并任一步骤失败时，应先处理失败原因，不要强行继续后续操作。
