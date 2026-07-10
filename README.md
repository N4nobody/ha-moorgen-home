# ha-moorgen-home

Moorgen/摩根主机的 Home Assistant 本地自定义集成（custom integration）。

> 面向开发者的技术文档与规范见：`docs/DEVELOPER_GUIDE.md`  
> AI/自动化协作约束见：`agent.md`

---

## 项目定位

- **Domain**: `ha_moorgen_home`
- **Name**: `Moorgen Home`
- **IOT Class**: `local_polling`
- **Version**: `0.1.0`

该插件用于将 Moorgen 主机接入 Home Assistant，目前已支持：

- 主机场景映射为 HA 的 `button` 实体（点击触发场景）
- 普通灯设备映射为 HA 的 `light` 实体（开/关）
- 调光灯设备映射为 HA 的 `light` 实体（亮度 0~100%，在 HA 中按 0~255 显示）

---

## 安装

将仓库中的 `custom_components/ha_moorgen_home/` 目录复制到 HA 配置目录下：

```text
/config/
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

- 集成初始化后会创建：
  - 多个按钮实体（每个场景一个按钮）
  - 多个灯实体（已识别为 light 类型的摩根设备）
- 在仪表盘或实体页：
  - 点击按钮触发对应场景
  - 对灯实体执行开/关控制

---

## 日志配置

建议本插件日志级别使用 `info`（仅输出 `info`/`warning`）。可在 `configuration.yaml` 配置：

```yaml
logger:
  default: warning
  logs:
    custom_components.ha_moorgen_home: info
```

---

## 状态同步策略

- 兜底轮询：coordinator 默认每 10 秒刷新（`update_interval=10s`）。
- 首次刷新：会等待场景/设备数据更新完成，保证首次实体构建尽量完整。
- 操作后加速刷新：每次场景执行或灯开关操作后，会在 `1s/2s/4s` 触发额外刷新。
- 刷新合并与限流：多次操作触发的刷新会合并，且手动触发刷新最小间隔不小于 `1s`。
- 当前未接入设备推送直驱实体状态（`proto_type=5/link=12`），状态以主动拉取为准。

---

## 单连接服务端说明（重要）

部分摩根服务端一次只允许一个 TCP 连接：

- 若其他客户端连入，HA 连接可能被服务端断开（日志常见 `Server closed the connection`）。
- 本插件已做适配：
  - 普通故障：由 coordinator（10 秒）按需触发重连
  - 服务端主动断连：进入 10 分钟冷却，避免立刻抢回连接

如需调整冷却时间，可修改 `custom_components/ha_moorgen_home/core/socket_client.py` 中 `_kick_cooldown_seconds`。

---

## 更新插件

本地手动更新代码后，建议重启 HA Core 以确保新代码完全生效。

> 说明：仅重载集成（Reload）在部分代码变更场景下可能不完全可靠。

---

## 许可证

本项目采用 **MIT License**，详见仓库根目录的 `LICENSE` 文件。
