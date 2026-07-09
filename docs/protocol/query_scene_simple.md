# 查询场景简表（query scene simple）

## 1. 业务说明

- 业务目标：查询场景列表（场景 ID、名称、图标）。
- 触发时机：客户端初始化后拉取基础数据。
- 当前状态：**已验证（高）**。

## 2. 协议映射

- 请求：`proto_type=3`, `link_code=7`
- 响应：`proto_type=3`, `link_code=8`
- 关键字段：
  - `Datareq_Type(15)=17` -> 请求场景简表
  - `Datareq_Type(15)=18` -> 场景简表响应

## 3. 业务层 JSON 表达

### 3.1 请求 JSON（业务输入）

```json
{
  "action": "query_scene_simple",
  "proto_type": 3,
  "link_code": 7,
  "serial_num": 0,
  "datareq_type": 17
}
```

### 3.2 响应 JSON（业务输出）

```json
{
  "action": "query_scene_simple",
  "proto_type": 3,
  "link_code": 8,
  "serial_num": 0,
  "datareq_type": 18,
  "scene_count": 1,
  "request_data_over": 1,
  "scenes": [
    {
      "id": "0100",
      "name": "回家模式",
      "icon": 49
    }
  ]
}
```

> 说明：抓包真实响应通常包含多条 scene；这里的 JSON 示例使用单条 scene 便于阅读和单测 round-trip。

## 4. 样本报文（hex）

### 4.1 请求（抓包样本）

```text
231600646f6f7961736863700103070e0005000f0001001123
```

解读：
- `23` 开始，末尾 `23` 结束
- `proto_name=dooyashcp`
- `proto_type=03`, `link_code=07`
- TLV: `0f 00 01 00 11` -> `type=15`, `len=1`, `value=17`

### 4.2 响应（抓包样本）

```text
231a02646f6f796173686370010308000009020f00010012120002000e00020004003031303001000c00e59b9ee5aeb6e6a8a1e5bc8f5e00010031110002000200020004003032303001000c00e7a6bbe5aeb6e6a8a1e5bc8f5e00010031110002000c00020004003033303001000c00e4bc9ae5aea2e6a8a1e5bc8f5e00010031110002000500020004003034303001000c00e4bc91e997b2e6a8a1e5bc8f5e00010031110002000500020004003035303001000c00e5b0b1e9a490e6a8a1e5bc8f5e00010031110002000400020004003036303001000c00e4b8bbe58da7e585a8e5bc805e00010031110002000700020004003037303001000c00e4b8bbe58da7e585a8e585b35e00010031110002000700020004003038303001000f00e4b8bbe58da7e4bc91e997b2e58fb35e00010031110002000700020004003062303001000f00e4b8bbe58da7e4bc91e997b2e5b7a65e00010031110002000700020004003063303001000c00e99885e8afbbe6a8a1e5bc8f5e00010037110002000600300005007230353030020004003039303001000c00e5aea2e58e85e5bc80e781af5e00010037110002000100020004003061303001000c00e5aea2e58e85e585b3e781af5e00010037110002000300020004003064303001000c00e9a490e58e85e5bc80e781af5e00010037110002000100020004003065303001000c00e9a490e58e85e585b3e781af5e00010037110002000100940001000123
```

解读（关键）：
- `proto_type=03`, `link_code=08`
- 首个 TLV: `type=15,value=18`（响应类型）
- 每个场景项包含：
  - `type=2`：scene id
  - `type=1`：scene name
  - `type=94`：scene icon
- 末尾 `type=148,value=1`：`REQUEST_DATA_OVER`

## 5. Java 证据（内联代码段）

### 5.1 协议名与类型常量

来源：`ConstantsInner.java` / `MsgConst.java`

```java
public static final String PROTOCOL_NAME_IS = "dooyashcp";
public static final int DATATYPE_Datareq_Type = 15;
public static final int DATA_REQ_SCENE_SIMPLE_INFO = 17;
public static final int DATA_RSP_SCENE_SIMPLE_INFO = 18;
public static final int DATATYPE_REQUEST_DATA_OVER = 148;
```

说明：定义了本业务中关键协议名和字段常量。

### 5.2 查询请求构造证据

来源：`MainAction#get_Byte_Data_Req`

```java
DataFieldBean dataFieldBean = new DataFieldBean();
dataFieldBean.setDataType(15);
dataFieldBean.setDataLength(1);
dataFieldBean.setDataValue(new byte[]{(byte) i2});
return this.msgAction.reqDataPack(this.dataFieldList);
```

说明：请求通过 `type=15` 携带业务编号（此处为 17）。

### 5.3 帧结构证据

来源：`LocalMsgExecute#doMessage` / `splitMessage`

```java
bArr3[0] = protocolBean.getMsgFlag();     // 0x23
... protoName(9), protoNum, protoType, linkCode, serial, dataLen ...
bArr3[length] = protocolBean.getMsgFlag(); // 末尾 0x23
```

说明：确认帧起止字节、头部顺序和 TLV 解包方式与当前 Python 实现一致。

## 6. 协议体字段说明

### 6.1 头部

- `msg_flag=0x23`
- `msg_len`：小端 2 字节
- `proto_name=dooyashcp`
- `proto_num=1`
- `proto_type`：3（Data）
- `link_code`：7 请求 / 8 响应
- `serial_num`：请求序号
- `data_len`：TLV 总长度

### 6.2 TLV 字段（本业务）

| 字段 ID | 名称 | 含义 |
|---:|---|---|
| 15 | Datareq_Type | 17=请求场景简表，18=场景简表响应 |
| 18 | SceneCount | 场景总数（可选） |
| 2 | Scene_Desc（作为场景 ID） | 场景标识 |
| 1 | Scene_Name | 场景名称 |
| 94 | Scene_Icon | 场景图标 |
| 148 | REQUEST_DATA_OVER | 分段/列表结束标记 |

## 7. 解析结论与边界

- 已确认：请求 17 -> 响应 18；响应包含场景 ID/名称/图标及结束标记。
- 未确认：`type=2` 在所有固件下是否恒为同一编码格式。
- 边界：本结论针对“场景简表查询”，不包含场景执行链路。

## 8. 单测映射

测试文件：`tests/protocol/test_query_scene_simple.py`

当前测试全部基于**抓包原样 hex**（不使用人工构造响应包）：

1. **JSON -> HEX（请求）**
   - 使用业务请求 JSON（`serial_num=14`）编码
   - 断言输出 hex 与抓包请求完全一致：
     - `231600646f6f7961736863700103070e0005000f0001001123`

2. **HEX -> JSON（响应）**
   - 使用抓包原样响应 hex 解码为业务 JSON
   - 断言 `proto_type/link_code/datareq_type/request_data_over/scenes` 等关键字段
   - 断言结果包含场景名 `回家模式`
