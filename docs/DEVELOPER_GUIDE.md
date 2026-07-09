# 开发文档（DEVELOPER GUIDE）

本文档面向插件开发者，包含架构说明、关键实现与调试建议。

---

## 1. 架构概览

核心链路：

1. `config_flow.py` 接收 host/port 配置
2. `__init__.py` 初始化 coordinator 并加载 `button` 平台
3. `core/coordinator.py` 周期刷新数据（10s）
4. `core/socket_client.py` 维护 TCP 连接、收发包
5. `core/protocol/*` 负责协议模型、编解码、命令构造
6. `button.py` 将场景映射为按钮实体并触发执行

---

## 2. 代码结构

- `__init__.py`：集成入口与卸载
- `config_flow.py`：UI 配置流程
- `button.py`：ButtonEntity 实现
- `const.py`：全局常量（`DOMAIN`、`COORDINATOR`）
- `core/coordinator.py`：DataUpdateCoordinator 逻辑
- `core/socket_client.py`：连接生命周期、重连策略、收发包
- `core/protocol/models.py`：协议字段映射与 dataclass 模型
- `core/protocol/codec.py`：协议构包/解包、路由与解析
- `core/protocol/commands.py`：业务命令封装

---

## 3. 重连策略设计（单连接服务端适配）

针对“服务端只允许单连接”的场景：

- 普通连接异常：不在 socket 层快速死循环重连；等待下次 coordinator 刷新触发按需连接。
- 服务端主动断开（`ServerDisconnectedError`）：进入冷却期（默认 600 秒）。

目的：避免调试期间 HA 频繁抢占连接。

---

## 4. 生命周期与热更新相关

- 已实现 `async_unload_entry` → `coordinator.async_shutdown()` → `client.stop()`，可正确释放后台连接任务。
- 但 Python 模块级热更新不保证 100% 安全；代码更新后建议重启 HA Core。

---

## 5. 协议层拆分说明

- `models.py`：`data_types`、`get_type_by_id`、`DataPacket` 等
- `codec.py`：`parse_protocol_packet`、`build_protocol_packet`、`route`、`parse_*_info`
- `commands.py`：`query_scene_details`、`activate_scene` 等命令构造

---

## 6. 本地开发

建议 Python 3.13+。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

代码检查：

```bash
ruff check .
ruff check . --fix
ruff format .
```

测试：

```bash
pytest -q
```

---

## 7. 当前已知限制

- `button` 实体在平台初始化时创建，场景动态增减不会自动重建实体。
- 协议字段映射依赖网关返回格式，不同固件可能需要适配。

---

## 8. 建议后续优化

- 增加 config flow 连通性校验与唯一 ID
- 增加 options flow（轮询间隔/冷却时间可配置）
- 增加 diagnostics 与测试用例
