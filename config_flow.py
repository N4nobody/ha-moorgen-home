import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN


class FurnitureLightsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """简单的UI配置流程"""

    async def async_step_user(self, user_input=None):
        # 1. 定义表单schema（host和port必须）
        data_schema = vol.Schema({
            vol.Required("host", default="192.168.1.246"): str,
            vol.Required("port", default=9000): vol.All(int, vol.Range(min=1, max=65535)),
        })

        # 2. 若用户已提交，则创建entry；否则显示表单
        if user_input is not None:
            # 这里可以做参数检测、连通性校验等
            return self.async_create_entry(
                title=f"{user_input['host']}:{user_input['port']}",
                data=user_input
            )
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema
        )
