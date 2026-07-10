# Agent Working Notes

本文件仅保留 AI/自动化协作的执行约束。

## 协议测试执行约束

1. 协议测试规范以 `docs/DEVELOPER_GUIDE.md` 第 `8.1` 节为准。
2. 禁止在测试执行路径中读取/解析 pcap。
3. 协议样本资产放在 `tests/protocol/fixtures/`，测试文件通过 import 使用。
4. 新增协议测试时，遵循命名规则：`test_<biz>_<phase>_<expected>`。
