import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .protocol.commands import (
    activate_scene,
    control_device,
    query_device_details,
    query_scene_details,
)
from .refresh_scheduler import RefreshScheduler
from .socket_client import AsyncSocketClient

_LOGGER = logging.getLogger(__name__)


class MoorgenDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config_entry):
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name="Moorgen Data Coordinator",
            update_interval=timedelta(seconds=10),
            always_update=True,
        )

        self._refresh_scheduler = RefreshScheduler(
            hass,
            trigger_refresh=self.async_refresh,
            delay_seconds=1.0,
            min_interval_seconds=1.0,
        )
        self.client = AsyncSocketClient(
            config_entry.data.get("host"),
            config_entry.data.get("port"),
            on_server_push=self._refresh_scheduler.schedule_on_server_push,
        )
        self._first_refresh_completed = False

    async def _async_setup(self):
        await self.client.start()

    async def async_shutdown(self):
        await self._refresh_scheduler.async_shutdown()
        await self.client.stop()

    async def activate_scene(self, scene_id):
        _LOGGER.info("activate scene %s", scene_id)
        await self.client.wait_until_connected(timeout=5)
        await self.client.send_command(activate_scene(scene_id))
        self._refresh_scheduler.schedule_post_operation()

    async def turn_device_on(self, device_mac: int):
        _LOGGER.info("turn on device %s", device_mac)
        await self.client.wait_until_connected(timeout=5)
        await self.client.send_command(control_device(device_mac, "light-on"))
        self._refresh_scheduler.schedule_post_operation()

    async def turn_device_off(self, device_mac: int):
        _LOGGER.info("turn off device %s", device_mac)
        await self.client.wait_until_connected(timeout=5)
        await self.client.send_command(control_device(device_mac, "light-off"))
        self._refresh_scheduler.schedule_post_operation()

    async def _async_update_data(self):
        """Refresh data from the host asynchronously."""
        try:
            await self.client.wait_until_connected(timeout=5)

            previous_scene_version = self.client.scene_version
            previous_device_version = self.client.device_version

            await self.client.send_command(query_scene_details())
            await self.client.send_command(query_device_details())

            if not self._first_refresh_completed:
                await self.client.wait_for_scene_update(previous_scene_version, timeout=5)
                await self.client.wait_for_device_update(previous_device_version, timeout=5)
                self._first_refresh_completed = True

            _LOGGER.info(
                "async update result: scenes=%s, rooms=%s, devices=%s",
                len(self.client.data.get("scenes", [])),
                len(self.client.data.get("rooms", [])),
                len(self.client.data.get("devices", [])),
            )
            return self.client.data
        except TimeoutError as ex:
            _LOGGER.warning("data refresh timeout, reconnect socket: %r", ex)
            await self.client.stop()
            await self.client.start()
            return self.client.data
        except ConnectionError as ex:
            _LOGGER.info("skip refresh while disconnected: %s", ex)
            return self.client.data
        except Exception as ex:
            _LOGGER.warning("async update failed: %r", ex)
            raise UpdateFailed(f"Error fetching lights data: {ex!r}") from ex
