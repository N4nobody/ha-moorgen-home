# 控制设备调光（panel dimming）

样本：`resources/moorgen_20260709_181646.pcap`  
操作：将 **主卧床头右** 从 `off` 逐步拉到 `100%`，再逐步拉回 `off`

## 1. 业务结论

这是 **设备控制**（非场景）：

- 请求：`proto_type=4`, `link_code=9`
- 回推：`proto_type=5`, `link_code=12`
- 心跳：`proto_type=6`, `link_code=13/14`

请求关键 TLV：
- `Operate_Type(16)=1`
- `Device_Mac(4)=0x1500ffffffff00ff`（十进制 `18374967954648268821`）
- `Device_Cmd(9)="random-light-dimming"`
- `Device_CmdData(10)=1字节亮度值`（0~100）

回推关键 TLV：
- `Device_Name(6)="主卧床头右"`
- `Device_State(11)`：`1=开`，`0=关`
- `PANEL_STATE(151)`：2字节，样本中恒为 `0xFFxx`，低字节 `xx` 与请求亮度一致

---

## 2. 关键时间线（请求/回推）

| 请求帧 | 时间(s) | 请求亮度(type=10) | 回推帧 | 回推时间(s) | 回推 state(11) | 回推 151 低字节 | 往返延迟(s) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4  | 0.461242 | 30  | 6  | 0.684000  | 1 | 30  | 0.223 |
| 8  | 1.969147 | 67  | 10 | 2.254516  | 1 | 67  | 0.285 |
| 14 | 4.938160 | 83  | 16 | 5.227579  | 1 | 83  | 0.289 |
| 18 | 6.644147 | 100 | 20 | 6.915316  | 1 | 100 | 0.271 |
| 22 | 9.033936 | 71  | 24 | 9.368057  | 1 | 71  | 0.334 |
| 26 | 10.770415| 8   | 28 | 11.134889 | 1 | 8   | 0.364 |
| 30 | 12.950973| 0   | 32 | 13.309835 | 0 | 0   | 0.359 |

补充：帧 12（亮度=67）为重复请求，未观察到独立回推（疑似网关合并/节流）。

---

## 3. 报文样本（用于固化测试资产）

> 按 `agent.md` 约定：测试运行时不读 pcap；以下 HEX/JSON 可直接固化进 `tests/protocol/`。

### 3.1 `100%` 请求/回推

#### 请求 HEX（帧18）

```text
233f00646f6f79617368637001040980012e001000010001040008001500ffffffff00ff0900140072616e646f6d2d6c696768742d64696d6d696e670a0001006423
```

#### 请求 JSON（业务）

```json
{
  "action": "control_device_dimming",
  "proto_type": 4,
  "link_code": 9,
  "serial_num": 384,
  "operate_type": 1,
  "device_mac": 18374967954648268821,
  "device_cmd": "random-light-dimming",
  "device_cmd_data": 100
}
```

#### 回推 HEX（帧20）

```text
232101646f6f79617368637001050c000010011b000100031100010001040008001500ffffffff00ff600001000198000100409c00010000720001000086000100085f00010000a700010002010201000205001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b000100010a009c00010504303730300500030201000002050430383030050003020100000301f000ffffffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d726576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d657865009700020064ff23
```

#### 回推 JSON（业务）

```json
{
  "action": "control_device_dimming_push",
  "proto_type": 5,
  "link_code": 12,
  "serial_num": 0,
  "update_proc": 3,
  "device_count": 1,
  "device": {
    "device_mac": 18374967954648268821,
    "device_is_online": 1,
    "device_version": 64,
    "device_forbid_by_lock": 0,
    "device_virtual_flag": 0,
    "dev_channel_sum": 8,
    "device_channel": 0,
    "device_icon": 2,
    "entity_hidden": 2,
    "device_desc_hex": "646f6f79617230313030723135338030",
    "device_name": "主卧床头右",
    "device_state": 1,
    "device_cmd_data_hex": "010504303730300500030201000002050430383030050003020100000301f000ffffffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d726576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d65786500",
    "panel_state_raw": 65380,
    "brightness": 100
  }
}
```

### 3.2 `off(0%)` 请求/回推

#### 请求 HEX（帧30）

```text
233f00646f6f79617368637001040986012e001000010001040008001500ffffffff00ff0900140072616e646f6d2d6c696768742d64696d6d696e670a0001000023
```

#### 请求 JSON（业务）

```json
{
  "action": "control_device_dimming",
  "proto_type": 4,
  "link_code": 9,
  "serial_num": 390,
  "operate_type": 1,
  "device_mac": 18374967954648268821,
  "device_cmd": "random-light-dimming",
  "device_cmd_data": 0
}
```

#### 回推 HEX（帧32）

```text
232101646f6f79617368637001050c000010011b000100031100010001040008001500ffffffff00ff600001000198000100409c00010000720001000086000100085f00010000a700010002010201000205001000646f6f7961723031303072313533803006000f00e4b8bbe58da7e5ba8ae5a4b4e58fb30b000100000a009c00010504303730300500030201000002050430383030050003020100000301f000ffffffff00ff01550004010200ffffffff02ff116c696768742d726576657273652d657865000505043036303005000302010000060504306330300500030201000007010100ffffffff07ff116c696768742d726576657273652d6578650008010100ffffffff05ff116c696768742d726576657273652d657865009700020000ff23
```

#### 回推 JSON（业务）

```json
{
  "action": "control_device_dimming_push",
  "proto_type": 5,
  "link_code": 12,
  "serial_num": 0,
  "update_proc": 3,
  "device_count": 1,
  "device": {
    "device_mac": 18374967954648268821,
    "device_name": "主卧床头右",
    "device_state": 0,
    "panel_state_raw": 65280,
    "brightness": 0
  }
}
```

---

## 4. 测试建议（按 `agent.md`）

建议新增：`tests/protocol/test_control_device_dimming.py`

建议覆盖 4 类断言：

1. `JSON -> HEX`（请求编码）
   - 100% 与 0% 的请求构包分别等于帧18/30 的 HEX。
2. `HEX -> JSON`（请求反解）
   - `type=9` 原始字节解码得到 `random-light-dimming`。
   - `type=10` 取 1 字节整数亮度。
3. `HEX -> JSON`（回推反解）
   - `Device_Name(6)=主卧床头右`
   - `Device_State(11)` 在亮度 0 时变为 0，否则为 1
   - `PANEL_STATE(151) & 0xFF == brightness`
4. 命令函数固定包断言
   - 若后续在 `commands.py` 新增 `control_device_dimming(device_mac, level)`，
     断言默认 serial=0 的固定构包。

---

## 5. 风险与待确认

- `type=10`（回推中的长字节块）语义尚未完全拆解，当前作为原始十六进制保留。
- `type=151` 高字节在样本中恒为 `0xFF`，建议后续补更多设备样本确认其含义。
