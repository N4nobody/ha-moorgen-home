# ha-moorgen-home

一个用于 **Home Assistant** 的本地自定义集成（custom integration），用于对接 Moorgen/摩根主机，通过 TCP Socket 协议读取场景信息并以按钮实体形式在 HA 中触发场景。

## 项目定位

- **集成域名（domain）**：`ha_moorgen_home`
- **连接方式**：局域网 TCP 直连
- **HA IOT Class**：`local_polling`
- **当前版本**：`0.1.0`

该项目核心目标是：
1. 建立与摩根主机的长连接；
2. 解析主机协议数据包并提取场景信息；
3. 在 HA 中自动生成场景按钮（`button` 实体）；
4. 点击按钮后向主机发送场景执行指令。

---

## 功能特性

- ✅ 支持通过 UI 配置 `host` / `port`
- ✅ 支持自动重连的异步 Socket 客户端
- ✅ 支持场景列表查询与解析
- ✅ 为每个场景创建一个 `button` 实体
- ✅ 支持按钮触发场景执行

---

## 代码结构

> 当前仓库文件就是 custom component 的核心代码文件。

- `manifest.json`：HA 集成元信息（domain、版本、config_flow 等）
- `__init__.py`：集成入口，初始化 coordinator 并转发到 button 平台
- `config_flow.py`：UI 配置流程（host / port）
- `button.py`：按钮实体定义与场景触发逻辑
- `const.py`：常量定义
- `core/coordinator.py`：数据协调器（定时拉取场景）
- `core/socket_client.py`：异步 TCP 客户端（连接、收包、发包、重连）
- `core/protocol/models.py`：协议字段映射与数据模型（`data_types`、`DataPacket` 等）
- `core/protocol/codec.py`：协议编解码与路由（构包/解包、`route`、场景/设备/房间解析）
- `core/protocol/commands.py`：业务命令构造（查询场景、触发场景等）

---

## 工作流程（简化）

1. 用户在 HA 中添加集成，填写主机地址和端口。
2. `FurnitureLightsCoordinator` 启动，内部 `AsyncSocketClient` 建立 TCP 连接。
3. 协调器周期性发送 `query_scene_details()`。
4. Socket 收到数据后，`parse_protocol_packet()` 解包，`route()` 分发并更新 `data['scenes']`。
5. `button` 平台根据场景列表创建按钮实体。
6. 用户点击按钮后，调用 `activate_scene(scene_id)` 下发执行命令。

---

## 安装方式（Home Assistant）

### 1) 放置代码

将本项目放置到 HA 的 `custom_components/ha_moorgen_home/` 目录下，确保目录结构类似：

```text
custom_components/
  ha_moorgen_home/
    __init__.py
    manifest.json
    config_flow.py
    button.py
    const.py
    core/
      coordinator.py
      socket_client.py
      protocol/
        commands.py
        codec.py
        models.py
```

### 2) 重启 Home Assistant

重启后在“设置 -> 设备与服务 -> 添加集成”中搜索 **Moorgen Home**。

### 3) 配置参数

- `host`：摩根主机 IP（默认示例 `192.168.1.246`）
- `port`：主机端口（默认 `9000`）

配置完成后将自动创建场景按钮实体。

---

## 使用说明

- 在 HA 的实体列表中可看到多个按钮实体（每个场景一个）。
- 点击对应按钮即可触发摩根场景。
- 如果主机短时离线，客户端会自动每 2 秒重连。

---

## 开发说明

### 本地开发环境

建议使用 Python 3.13+。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

> 说明：本项目是 Home Assistant custom integration，运行时依赖由 `manifest.json` 中的 `requirements` 管理；
> `requirements-dev.txt` 主要用于本地开发与测试工具安装。

### 代码质量检查（Ruff）

```bash
ruff check .
ruff check . --fix
ruff format .
```

- `ruff check .`：静态检查
- `ruff check . --fix`：自动修复可修复问题
- `ruff format .`：统一代码格式

Ruff 配置文件：`.ruff.toml`

### 测试（Pytest）

```bash
pytest -q
```

当前仓库尚未提供完整测试用例，可按需在 `tests/` 目录补充。

### 协议处理

协议代码按职责拆分后：

- `core/protocol/models.py` 包含：
  - 大量字段 ID 与名称映射（`data_types`）
  - 协议数据模型（`DataField` / `DataPacket` / `RoomInfo` / `SceneInfo`）
- `core/protocol/codec.py` 包含：
  - 通用协议解析 `parse_protocol_packet()`
  - 通用协议构包 `build_protocol_packet()`
  - 业务路由 `route()` 与各类数据解析函数
- `core/protocol/commands.py` 包含：
  - `query_room_info()`
  - `query_user_info()`
  - `query_device_details()`
  - `query_scene_details()`
  - `activate_scene(scene_name)`

### 调试日志

代码中已包含较多 `_LOGGER.info`，可在 HA `logger` 中开启该组件 debug/info 日志以排查连接和协议问题。

---

## 当前实现备注

- 场景实体在 `button` 平台初始化时创建，后续场景增减不会自动重建实体。
- 协议字段映射与解析依赖具体主机返回格式，不同网关/固件可能需要适配。

---

## 许可证

本项目采用 **MIT License**，详见仓库根目录的 `LICENSE` 文件。