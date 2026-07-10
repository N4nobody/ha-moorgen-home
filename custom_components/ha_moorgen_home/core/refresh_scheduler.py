import asyncio
from collections.abc import Awaitable, Callable

from homeassistant.core import HomeAssistant


class RefreshScheduler:
    """Collect refresh requests and trigger merged, throttled coordinator refreshes."""

    def __init__(
        self,
        hass: HomeAssistant,
        trigger_refresh: Callable[[], Awaitable[None]],
        delays: tuple[int, ...] = (1, 2, 4),
        min_interval_seconds: float = 1.0,
    ):
        self._hass = hass
        self._trigger_refresh = trigger_refresh
        self._delays = delays
        self._min_interval_seconds = min_interval_seconds

        self._scheduled_refreshes: dict[int, asyncio.TimerHandle] = {}
        self._refresh_lock = asyncio.Lock()
        self._last_refresh_ts = 0.0
        self._stopped = False

    def schedule_post_operation(self):
        if self._stopped:
            return

        loop = asyncio.get_running_loop()
        for delay in self._delays:
            existing = self._scheduled_refreshes.get(delay)
            if existing and not existing.cancelled():
                continue

            self._scheduled_refreshes[delay] = loop.call_later(
                delay, self._trigger_scheduled_refresh, delay
            )

    def _trigger_scheduled_refresh(self, delay: int):
        self._scheduled_refreshes.pop(delay, None)
        if self._stopped:
            return
        self._hass.async_create_task(self._async_trigger_refresh_throttled())

    async def _async_trigger_refresh_throttled(self):
        if self._stopped:
            return

        async with self._refresh_lock:
            if self._stopped:
                return

            now = asyncio.get_running_loop().time()
            wait_seconds = self._min_interval_seconds - (now - self._last_refresh_ts)
            if wait_seconds > 0:
                await asyncio.sleep(wait_seconds)

            self._last_refresh_ts = asyncio.get_running_loop().time()
            await self._trigger_refresh()

    async def async_shutdown(self):
        self._stopped = True
        for handle in self._scheduled_refreshes.values():
            handle.cancel()
        self._scheduled_refreshes.clear()
