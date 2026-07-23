---
name: send
description: Send a structured inter-session message via sessions_send — single source of truth for the call format, XML message wrapping, and field spec. Triggers: 发送消息, send message, sessions_send, 回传消息, 会话通信, 主动汇报.
---

# send — 会话消息发送

## Mission

作为 `sessions_send` 工具调用的唯一权威来源。定义调用签名、XML 消息包裹格式、STATUS/SUMMARY/EVIDENCE/NEXT 字段规格，以及 `sessionKey` 与 `from` 属性的角色区分。

## When to use

- 需要构造并执行 `sessions_send` 调用时
- 作为 callee 向 caller 回传一条结构化消息
- 接收方需要知道消息的精确字段格式和允许值

不要用于：决定何时发送消息（那是 `session-coordination`）、会话 spawn、会话列举/历史读取。

## 输入

| 参数 | 必需 | 类型 | 描述 |
|------|------|------|------|
| sessionKey | 是 | string | callee 自己的可路由 session key（标识发送方），不以 `:thread:<id>` 结尾 |
| message | 是 | string | 包裹在 `<message>` XML 标签内的结构化文本 |
| timeoutSeconds | 否 | integer | 0 = 非阻塞投递；正值 = 等待回复（默认 0） |

## 消息格式

### XML 包裹

`message` 字符串必须用 `<message>` XML 标签包裹，`from` 属性填 caller 的 session key：

```xml
<message from="<caller_session_key>">
STATUS: blocker | decision_needed | finding | milestone
SUMMARY: <一句话>
EVIDENCE: <必要证据或具体原因>
NEXT: <callee 将继续做什么，或 caller 需要做什么>
</message>
```

禁止纯文本或其他格式。`from` 属性必填。

### STATUS 允许值

| 值 | 含义 |
|----|------|
| blocker | 输入缺失、不可读或任务无法继续 |
| decision_needed | 需要接收方决策方案、范围或风险 |
| finding | 已验证且会改变后续工作方向的发现 |
| milestone | 关键阶段完成，可据此安排后续工作 |

### 字段要求

| 字段 | 要求 |
|------|------|
| SUMMARY | 一句话概括 |
| EVIDENCE | 可追溯、可验证的证据或具体原因 |
| NEXT | 可行动——callee 接下来做什么，或 caller 需要做什么 |

### 关键约束

- `sessionKey` = callee 自己的 session key。
- `<message from="...">` = caller 的 session key。
- 不向 `:thread:<id>` 结尾的 session key 发送。
- 不发送 secrets、无关私人上下文或未经验证的推测。

## 执行流程

1. 取得 callee 自己的可路由 session key（= `sessionKey` 参数）和 caller 的 session key（= `from` 属性值）。
2. 按 XML 格式构造 `message`：填充 STATUS、SUMMARY、EVIDENCE、NEXT。
3. 调用 `sessions_send(sessionKey, message, timeoutSeconds)`。
4. 若投递失败，继续完成可完成的工作，在最终 reply 中说明哪条回传未送达。

## 完成门禁

- `message` 使用 `<message>` XML 包裹，`from` 属性存在且正确。
- `sessionKey` = callee own key，`from` = caller key。
- STATUS 为四个允许值之一。
- SUMMARY / EVIDENCE / NEXT 均有内容。
