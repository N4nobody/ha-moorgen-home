# Agent Working Notes

本文件仅保留 AI/自动化协作的执行约束。

## 协议测试执行约束

1. 协议测试规范以 `docs/DEVELOPER_GUIDE.md` 第 `9.1` 节为准。
2. 禁止在测试执行路径中读取/解析 pcap。
3. 协议样本资产放在 `tests/protocol/fixtures/`，测试文件通过 import 使用。
4. 新增协议测试时，遵循命名规则：`test_<biz>_<phase>_<expected>`。

## 日志约束

1. 插件日志仅使用 `info` 与 `warning` 两个级别。
2. 默认日志输出按 `info` 级别编写（无需新增 `debug` 级别日志）。
3. 新增/修改日志时，优先使用参数化日志格式（`_LOGGER.info("... %s", value)`），避免 f-string 直接拼接。
