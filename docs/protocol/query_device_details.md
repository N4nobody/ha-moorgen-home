# 查询设备详情（query device details）

## 1. 业务说明

- 业务目标：查询设备列表详情（设备标识、名称、状态、所属房间等字段）。
- 触发时机：初始化数据拉取阶段。
- 当前状态：**已验证（高）**（pcap + APK 常量/构包双证据）。

## 2. 协议映射

- 请求：`proto_type=3`, `link_code=7`
- 响应：`proto_type=3`, `link_code=8`
- 关键字段：
  - `Datareq_Type(15)=1` -> 请求设备详情
  - `Datareq_Type(15)=4` -> 设备详情响应

## 3. 抓包样本

### 3.1 请求（抓包原样）

```text
231600646f6f7961736863700103070c0005000f0001000123
```

解读：`type=15,len=1,value=0x01`（`DATA_REQ_DEVICE`）

### 3.2 响应（抓包原样，TCP 重组后）

- 响应完整帧长度：`5499 bytes`
- 帧头（prefix）：

```text
237815646f6f796173686370010308000067150f00010004...
```

- 帧尾（suffix）：

```text
...0a000400011b0100940001000123
```

说明：设备详情响应体较大，需按 TCP payload 时序重组后再按 SHCP 帧长度解析。

## 4. APK 证据（Java）

来源：`com/moorgen/shcp/libs/internal/constants/MsgConst.java` / `.../msg/MainAction.java`

```java
public static final int DATATYPE_Datareq_Type = 15;
public static final int DATATYPE_DeviceCount = 17;
public static final int DATA_REQ_DEVICE = 1;
public static final int DATA_RSP_DEVICE = 4;
```

```java
public byte[] get_Byte_Data_Req(int i2) {
    DataFieldBean dataFieldBean = new DataFieldBean();
    dataFieldBean.setDataType(15);
    dataFieldBean.setDataLength(1);
    dataFieldBean.setDataValue(new byte[]{(byte) i2});
    return this.msgAction.reqDataPack(this.dataFieldList);
}
```

## 5. 响应字段特征（从抓包实证）

- `type=15,value=4`：设备详情响应类型
- `type=17,value=47`：设备数量
- 设备项中可见字段（部分）：
  - `type=4`：`Device_Mac`
  - `type=6`：`Device_Name`
  - `type=48`：`RoomDesc`
  - 其他设备能力/状态字段

样本中可解析到设备名示例：`床头射灯`、`玄关面板`、`客厅地暖`。

## 6. 单测映射

测试文件：`tests/protocol/test_query_device_details.py`

1. **请求对齐（静态资产）**
   - 在单测中直接固化请求 JSON 与请求 HEX：
     - `231600646f6f7961736863700103070c0005000f0001000123`
   - 断言 `JSON -> HEX` 与抓包样本一致。
   - 并断言 `query_device_details()`（serial=0）固定构包。

2. **响应解析（静态资产）**
   - 在单测中直接固化响应 HEX 与响应 JSON（不读取 pcap）。
   - 断言：
     - `datareq_type == 4`
     - `device_count == 47`
     - `request_data_over == 1`
     - 路由到 `devices`
     - 设备名称列表与预期 JSON 完全一致。
