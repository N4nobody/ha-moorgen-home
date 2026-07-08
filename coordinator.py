import asyncio
import logging
from datetime import timedelta

import async_timeout
from homeassistant.helpers.update_coordinator import (DataUpdateCoordinator,
                                                      UpdateFailed)

from .parse import query_scene_details, activate_scene
from .socket_client import AsyncSocketClient

_LOGGER = logging.getLogger(__name__)


class FurnitureLightsCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config_entry):
        """初始化协调器"""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name="Furniture Lights Coordinator",
            update_interval=timedelta(seconds=10),  # 数据同步间隔
            always_update=True
        )

        self.client = AsyncSocketClient(config_entry.data.get(
            'host'), config_entry.data.get('port'))

    async def _async_setup(self):
        await self.client.start()

    async def activate_scene(self, scene_id):
        _LOGGER.info(
            f"activate scene {scene_id}")
        await self.client.send_command(activate_scene(scene_id))

    async def _async_update_data(self):
        """异步刷新设备总体状态"""
        try:
            await asyncio.sleep(3)
            await self.client.send_command(query_scene_details())
            await asyncio.sleep(10)
            _LOGGER.info(
                f"async update result is {self.client.data}")
            return self.client.data
        except Exception as ex:
            _LOGGER.info(f"async update failed {ex}")
            raise UpdateFailed(f"Error fetching lights data: {ex}")
