# Agent Working Notes

## 协议单测编写约定（用户新增要求）

从现在开始，协议测试（`tests/protocol/`）统一按以下方式编写：

1. **禁止在单测里直接读取/解析 pcap 文件**
   - 单测不依赖 `*.pcap`。
   - 不在测试里做 TCP 重组、抓包扫描等逻辑。

2. **测试资产（asset）直接固化在测试文件中**
   - 必须在测试中直接定义并使用：
     - 请求 JSON
     - 请求 HEX
     - 响应 HEX
     - 响应 JSON
   - 响应 JSON 要尽量完整展示解析结果：
     - 不只写名称列表，要包含可解析出的全部 key/value（例如 `devices` 的完整字典列表）。
     - 若字段名未知，使用 `unknown_<id>` 形式保留原始字段。
3. **测试结构参考现有标准样式**
   - 参考：
     - `tests/protocol/test_query_scene_simple.py`
     - `tests/protocol/test_query_room_info.py`
   - 推荐包含：
     - `JSON -> HEX`（请求编码对齐）
     - `HEX -> JSON`（请求反解）
     - `HEX -> JSON`（响应反解并断言业务 JSON）
     - 命令函数固定包断言（如 `query_xxx().hex()`）

4. **抓包仅作为离线取样来源，不进入测试执行路径**
   - 需要新样本时，可以离线从 pcap 提取后粘贴为常量。
   - 但运行测试时不能再依赖 pcap 文件存在。
