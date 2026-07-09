import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .protocol.commands import activate_scene, query_scene_details
from .socket_client import AsyncSocketClient

_LOGGER = logging.getLogger(__name__)


class FurnitureLightsCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config_entry):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name="Furniture Lights Coordinator",
            update_interval=timedelta(seconds=10),
            always_update=True,
        )

        self.client = AsyncSocketClient(
            config_entry.data.get("host"), config_entry.data.get("port")
        )

    async def _async_setup(self):
        await self.client.start()

    async def async_shutdown(self):
        await self.client.stop()

    async def activate_scene(self, scene_id):
        _LOGGER.info("activate scene %s", scene_id)
        await self.client.wait_until_connected(timeout=5)
        await self.client.send_command(activate_scene(scene_id))

    async def _async_update_data(self):
        """Refresh data from the host asynchronously."""
        try:
            await self.client.wait_until_connected(timeout=5)
            previous_version = self.client.scene_version
            await self.client.send_command(query_scene_details())
            await self.client.wait_for_scene_update(previous_version, timeout=5)
            _LOGGER.info("async update result is %s", self.client.data)
            return self.client.data
        except ConnectionError as ex:
            _LOGGER.debug("skip refresh while disconnected: %s", ex)
            return self.client.data
        except Exception as ex:
            _LOGGER.warning("async update failed: %r", ex)
            raise UpdateFailed(f"Error fetching lights data: {ex!r}") from ex
