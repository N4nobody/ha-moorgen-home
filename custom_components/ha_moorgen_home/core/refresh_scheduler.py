import asyncio
from collections.abc import Awaitable, Callable

from homeassistant.core import HomeAssistant


class RefreshScheduler:
    """Collect refresh requests and trigger merged, throttled coordinator refreshes."""

    def __init__(
        self,
        hass: HomeAssistant,
        trigger_refresh: Callable[[], Awaitable[None]],
        delay_seconds: float = 1.0,
        min_interval_seconds: float = 1.0,
    ):
        self._hass = hass
        self._trigger_refresh = trigger_refresh
        self._delay_seconds = delay_seconds
        self._min_interval_seconds = min_interval_seconds

        self._scheduled_refresh: asyncio.TimerHandle | None = None
        self._refresh_lock = asyncio.Lock()
        self._last_refresh_ts = 0.0
        self._stopped = False

    def schedule_post_operation(self):
        """Schedule one delayed refresh after manual operation."""
        self._schedule_delayed_refresh()

    def schedule_on_server_push(self):
        """Schedule one delayed refresh after server push packet."""
        self._schedule_delayed_refresh()

    def _schedule_delayed_refresh(self):
        if self._stopped:
            return

        if self._scheduled_refresh and not self._scheduled_refresh.cancelled():
            # Merge requests in the same second window.
            return

        loop = asyncio.get_running_loop()
        self._scheduled_refresh = loop.call_later(
            self._delay_seconds,
            self._trigger_scheduled_refresh,
        )

    def _trigger_scheduled_refresh(self):
        self._scheduled_refresh = None
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
        if self._scheduled_refresh:
            self._scheduled_refresh.cancel()
            self._scheduled_refresh = None
