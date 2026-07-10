# <业务名称>

## 1. 业务说明

- 业务目标：
- 触发时机：
- 当前状态：已验证 / 部分验证 / 待验证

## 2. 协议映射

- 请求：`proto_type=?`, `link_code=?`
- 响应：`proto_type=?`, `link_code=?`
- 关键字段：
  - `Datareq_Type(15)=?`
  - `Operate_Type(16)=?`

## 3. 业务层 JSON 表达

### 3.1 请求 JSON

```json
{
  "action": "<业务动作>",
  "proto_type": 0,
  "link_code": 0
}
```

### 3.2 响应 JSON

```json
{
  "action": "<业务动作>",
  "proto_type": 0,
  "link_code": 0
}
```

## 4. 样本报文（hex）

### 4.1 请求

```text
<hex>
```

### 4.2 响应

```text
<hex>
```

> 可对超长响应做节选，但要保留关键字段所在片段。

## 5. Java 证据（内联代码段）

### 5.1 常量证据

来源：`<class>`

```java
<代码片段>
```

解释：
- 该片段证明了什么：

### 5.2 构包/解包证据

来源：`<class>#<method>`

```java
<代码片段>
```

解释：
- 该片段证明了什么：

## 6. 协议体字段说明

### 6.1 头部

- `msg_flag`
- `msg_len`
- `proto_name`
- `proto_num`
- `proto_type`
- `link_code`
- `serial_num`
- `data_len`

### 6.2 TLV 字段

| 字段 ID | 名称 | 长度 | 含义 | 证据 |
|---:|---|---|---|---|
|  |  |  |  |  |

## 7. 解析结论与边界

- 已确认：
- 未确认：
- 风险点：

## 8. 单测映射

- 测试文件：`tests/protocol/test_<业务名>.py`
- 测试规范：遵循 `docs/DEVELOPER_GUIDE.md` 第 `8.1` 节。
- 断言映射：
  - 结论 A -> `test_xxx` 中断言 ...
  - 结论 B -> `test_xxx` 中断言 ...
