# ha-moorgen-home

Moorgen/摩根主机的 Home Assistant 本地自定义集成（custom integration）。

> 面向开发者的技术文档见：`docs/DEVELOPER_GUIDE.md`

---

## 项目定位

- **Domain**: `ha_moorgen_home`
- **Name**: `Moorgen Home`
- **IOT Class**: `local_polling`
- **Version**: `0.1.0`

该插件用于将 Moorgen 主机接入 Home Assistant，并把主机场景映射为 HA 的 `button` 实体；点击按钮即可触发场景。

---

## 安装

将本项目放置到 HA 的 `custom_components/ha_moorgen_home/` 目录中，目录结构示例：

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

然后重启 Home Assistant。

---

## 添加集成

在 Home Assistant 中：

1. 设置 → 设备与服务
2. 添加集成
3. 搜索 **Moorgen Home**
4. 填写：
   - `host`：摩根主机 IP（如 `192.168.1.246`）
   - `port`：端口（默认 `9000`）

---

## 使用方式

- 集成初始化后会创建多个按钮实体（每个场景一个按钮）。
- 在仪表盘或实体页点击按钮，即可触发对应场景。

---

## 日志配置

默认 HA 日志级别是 `warning`。如需查看本插件日志，可在 `configuration.yaml` 配置：

```yaml
logger:
  default: warning
  logs:
    custom_components.ha_moorgen_home: info
```

更详细可用 `debug`：

```yaml
logger:
  default: warning
  logs:
    custom_components.ha_moorgen_home: debug
```

---

## 单连接服务端说明（重要）

部分摩根服务端一次只允许一个 TCP 连接：

- 若其他客户端连入，HA 连接可能被服务端断开（日志常见 `Server closed the connection`）。
- 本插件已做适配：
  - 普通故障：由 coordinator（10 秒）按需触发重连
  - 服务端主动断连：进入 10 分钟冷却，避免立刻抢回连接

如需调整冷却时间，可修改 `core/socket_client.py` 中 `_kick_cooldown_seconds`。

---

## 更新插件

本地手动更新代码后，建议重启 HA Core 以确保新代码完全生效。

> 说明：仅重载集成（Reload）在部分代码变更场景下可能不完全可靠。

---

## 许可证

本项目采用 **MIT License**，详见仓库根目录的 `LICENSE` 文件。
