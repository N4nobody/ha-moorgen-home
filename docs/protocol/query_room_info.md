# 查询房间信息（query room info）

## 1. 业务说明

- 业务目标：查询房间列表（房间 ID、名称、图片/图标）。
- 触发时机：客户端初始化阶段拉取基础数据。
- 当前状态：**已验证（高）**（抓包 + APK 常量/构包代码）。

## 2. 协议映射

- 请求：`proto_type=3`, `link_code=7`
- 响应：`proto_type=3`, `link_code=8`
- 关键字段：
  - `Datareq_Type(15)=11` -> 请求房间信息
  - `Datareq_Type(15)=12` -> 房间信息响应

## 3. 业务层 JSON 表达

### 3.1 请求 JSON（业务输入）

```json
{
  "action": "query_room_info",
  "proto_type": 3,
  "link_code": 7,
  "serial_num": 8,
  "datareq_type": 11
}
```

### 3.2 响应 JSON（业务输出）

```json
{
  "action": "query_room_info",
  "proto_type": 3,
  "link_code": 8,
  "serial_num": 0,
  "datareq_type": 12,
  "room_count": 7,
  "request_data_over": 1,
  "rooms": [
    {"id": "r0100", "name": "公共区域", "image": 0},
    {"id": "r0200", "name": "空调", "image": 49}
  ]
}
```

## 4. 样本报文（hex）

### 4.1 请求（抓包样本）

```text
231600646f6f796173686370010307080005000f0001000b23
```

解读：
- `type=15,len=1,value=0x0b(11)` -> `DATA_REQ_ROOM`

### 4.2 响应（抓包样本）

```text
23d100646f6f7961736863700103080000c0000f0001000c35000200070030000500723031303036000c00e585ace585b1e58cbae59f9f3700000030000500723032303036000600e7a9bae8b083370001003130000500723033303036000600e696b0e9a38e370001003130000500723034303036000600e59cb0e69a96370001003130000500723035303036000600e4b8bbe58da7370001003130000500723036303036000900e5aea2e9a490e58e85370001003130000500723037303036000600e5a487e794a83700010031940001000123
```

解读（关键）：
- `type=15,value=12`：房间信息响应
- `type=53,value=7`：房间数量
- 每个房间项包含：
  - `type=48`：RoomDesc（房间 ID）
  - `type=54`：RoomName（房间名）
  - `type=55`：RoomImage（房间图片）
- 末尾 `type=148,value=1`：`REQUEST_DATA_OVER`

## 5. APK 证据（Java）

来源：`com/moorgen/shcp/libs/internal/constants/MsgConst.java` / `.../msg/MainAction.java`

```java
public static final int DATATYPE_Datareq_Type = 15;
public static final int DATA_REQ_ROOM = 11;
public static final int DATA_RSP_ROOM = 12;
public static final int DATATYPE_RoomCount = 53;
public static final int DATATYPE_RoomDesc = 48;
public static final int DATATYPE_RoomName = 54;
public static final int DATATYPE_RoomImage = 55;
public static final int DATATYPE_REQUEST_DATA_OVER = 148;
```

```java
public byte[] get_Byte_Data_Req(int i2) {
    DataFieldBean dataFieldBean = new DataFieldBean();
    dataFieldBean.setDataType(15);
    dataFieldBean.setDataLength(1);
    dataFieldBean.setDataValue(new byte[]{(byte) i2});
    ...
}
```

## 6. 协议体字段说明（本业务）

| 字段 ID | 名称 | 含义 |
|---:|---|---|
| 15 | Datareq_Type | 11=请求房间信息，12=房间信息响应 |
| 53 | RoomCount | 房间总数 |
| 48 | RoomDesc | 房间标识（如 `r0100`） |
| 54 | RoomName | 房间名称 |
| 55 | RoomImage | 房间图片/图标 |
| 148 | REQUEST_DATA_OVER | 列表结束标记 |

## 7. 单测映射

测试文件：`tests/protocol/test_query_room_info.py`

1. **JSON -> HEX（请求）**
   - 使用抓包请求 JSON 编码，断言与抓包 hex 完全一致。
2. **HEX -> JSON（响应）**
   - 使用抓包响应 hex 解码，断言 `datareq_type/room_count/request_data_over/rooms`。
3. **命令构包对齐**
   - 断言 `query_room_info()` 在 `serial=0` 下输出固定请求包。
