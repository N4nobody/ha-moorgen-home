import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN


class FurnitureLightsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Basic UI config flow."""

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=f"{user_input['host']}:{user_input['port']}", data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("host", default="192.168.1.246"): str,
                    vol.Required("port", default=9000): vol.All(int, vol.Range(min=1, max=65535)),
                }
            ),
        )
