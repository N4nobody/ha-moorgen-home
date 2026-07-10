# ha-moorgen-home

这是一个用于 Home Assistant 的 Moorgen（摩根全屋智能）本地自定义集成。

Moorgen 是全屋智能品牌，提供智能主机、照明与场景控制等能力。官网：<https://www.moorgen.com/>

面向开发者的技术文档见：`docs/DEVELOPER_GUIDE.md`  
AI/自动化协作约束见：`agent.md`

## 支持能力

当前版本仅支持基础能力，主要是：

- 场景控制（映射为 HA `button` 实体）
- 开关/灯光面板相关控制（映射为 HA `light` 实体）
  - 普通灯：开/关
  - 调光灯：亮度 0~100%（HA 中显示为 0~255）

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

## 添加集成

在 Home Assistant 中：

1. 设置 → 设备与服务
2. 添加集成
3. 搜索 **Moorgen Home**
4. 填写：
   - `host`：摩根主机 IP（如 `192.168.1.246`）
   - `port`：端口（默认 `9000`）

## 使用方式

- 初始化后会创建：
  - 多个按钮实体（每个场景一个按钮）
  - 多个灯实体（已识别为 light 类型的摩根设备）
- 在仪表盘或实体页：
  - 点击按钮触发对应场景
  - 对灯实体执行开/关或亮度控制（调光灯）

## 使用界面截图

以下为当前接入与使用页面截图：

### 添加与配置

![添加与配置 1](docs/images/usage/001.png)
![添加与配置 2](docs/images/usage/002.png)

### 实体与控制

![实体与控制 1](docs/images/usage/003.png)
![实体与控制 2](docs/images/usage/004.png)

### 页面展示

![页面展示 1](docs/images/usage/005.png)
![页面展示 2](docs/images/usage/006.png)

## 日志配置

建议本插件日志级别使用 `info`。可在 `configuration.yaml` 配置：

```yaml
logger:
  default: warning
  logs:
    custom_components.ha_moorgen_home: info
```

## 更新插件

本地手动更新代码后，建议重启 HA Core 以确保新代码完全生效。

## 许可证

本项目采用 **MIT License**，详见仓库根目录的 `LICENSE` 文件。
